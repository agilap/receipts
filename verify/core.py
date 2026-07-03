"""Verification core: retrieval + NLI + verdict logic.

Verdicts:
- supported: some evidence chunk entails the claim (p >= SUPPORTED_T)
- partial: weaker entailment signal (best p >= PARTIAL_T)
- unsupported: the claim's repo evidence exists and does not back the claim
- no_evidence: the claim's project has no repo in the evidence corpus
- unverifiable: quantitative/soft claims code evidence cannot decide
"""

import re

import numpy as np

from verify.embed import embed_texts
from verify.mapping import load_aliases, resolve_repo

NLI_MODEL = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
TOP_K = 5
SUPPORTED_T = 0.75
PARTIAL_T = 0.40

# Package names that are also common English words; never claim a
# deterministic match on these (e.g. "handles requests" != uses `requests`).
DEP_MATCH_STOPWORDS = {"requests", "black", "click", "rich", "arrow"}

# Scale/extent modifiers whose removal yields the claim's "core". If the core
# is entailed but the full claim is not, the extent is the unsupported part
# -> verdict "partial". Order matters: multi-word phrases first.
EXTENT_PATTERNS = [
    r"\bin real[- ]time\b", r"\breal[- ]time\b",
    r"\bat scale\b", r"\bacross (?:all )?(?:devices|platforms)\b",
    r"\b(?:hundreds|thousands|millions|dozens) of\b",
    r"\ball major\b", r"\ball\b", r"\bany\b", r"\bevery\b", r"\bfull\b",
    r"\benterprise(?:-grade)?\b", r"\bproduction(?:-grade|-ready)?\b",
    r"\bcloud[- ]hosted\b", r"\bconcurrent\b", r"\bdirectly\b",
    r"\bseamlessly\b", r"\bautomatically\b", r"\bend[- ]to[- ]end\b",
]


def claim_variants(claim_text: str) -> list[str]:
    """Weakened hypotheses for the partial check.

    Extent stripping removes scale modifiers ("monitors hundreds of production
    models in real time" -> "monitors models"); conjunction splitting scores
    each conjunct of "X and Y" alone. A variant is only returned if it still
    reads as a sentence and actually differs from the original.
    """
    variants = []
    core = claim_text
    for pat in EXTENT_PATTERNS:
        core = re.sub(pat, "", core, flags=re.I)
    core = re.sub(r"\s{2,}", " ", core).strip(" ,")
    core = re.sub(r"\s+(?:in|with|for|on|at|to|of|and|or)$", "", core,
                  flags=re.I)
    if core.lower() != claim_text.lower() and len(core.split()) >= 3:
        variants.append(core)

    for base in [claim_text] + variants[:1]:
        if re.search(r"\band\b", base, flags=re.I):
            keep_first = re.sub(r",?\s+and\s+\S+(?:\s+\S+)?\s*$", "", base,
                                flags=re.I)
            keep_last = re.sub(r"\S+(?:\s+\S+)?,?\s+and\s+", "", base,
                               count=1, flags=re.I)
            for v in (keep_first, keep_last):
                v = v.strip(" ,")
                if v.lower() != base.lower() and len(v.split()) >= 3:
                    variants.append(v)

    seen, out = set(), []
    for v in variants:
        if v.lower() not in seen:
            seen.add(v.lower())
            out.append(v)
    return out

_nli = None


def _norm(token: str) -> str:
    return re.sub(r"[^a-z0-9]", "", token.lower())


def dependency_match(claim_text: str, repo_chunks: list[dict]) -> tuple[list[str], dict | None]:
    """Deterministic check: does the claim name a package the repo declares?

    Matches claim words against manifest package names (and their dash/dot
    parts, so "Whisper" matches openai-whisper). Returns (matched packages,
    the dependency chunk) or ([], None).
    """
    words = {_norm(w) for w in re.findall(r"[A-Za-z0-9_.-]+", claim_text)}
    words.discard("")
    for c in repo_chunks:
        if c["type"] != "dependencies":
            continue
        matched = []
        for pkg in c.get("packages", []):
            if pkg.lower() in DEP_MATCH_STOPWORDS:
                continue
            parts = {_norm(pkg)} | {_norm(p) for p in re.split(r"[-_.]", pkg)}
            parts -= {_norm(s) for s in DEP_MATCH_STOPWORDS} | {""}
            if words & parts:
                matched.append(pkg)
        if matched:
            return matched, c
    return [], None


def get_nli():
    global _nli
    if _nli is None:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        tok = AutoTokenizer.from_pretrained(NLI_MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL)
        model.eval()
        _nli = (tok, model, torch)
    return _nli


def entailment_probs(pairs: list[tuple[str, str]]) -> list[dict]:
    """NLI over (premise, hypothesis) pairs -> per-pair label probabilities."""
    tok, model, torch = get_nli()
    enc = tok([p for p, _ in pairs], [h for _, h in pairs],
              truncation=True, padding=True, max_length=512,
              return_tensors="pt")
    with torch.no_grad():
        probs = torch.softmax(model(**enc).logits, dim=-1)
    labels = [model.config.id2label[i].lower() for i in range(probs.shape[1])]
    return [dict(zip(labels, row.tolist())) for row in probs]


def retrieve(claim_vec: np.ndarray, chunk_vecs: np.ndarray,
             chunks: list[dict], k: int = TOP_K) -> list[tuple[dict, float]]:
    sims = chunk_vecs @ claim_vec
    order = np.argsort(-sims)[:k]
    return [(chunks[i], float(sims[i])) for i in order]


def verdict_from_entailment(best_entail: float) -> str:
    if best_entail >= SUPPORTED_T:
        return "supported"
    if best_entail >= PARTIAL_T:
        return "partial"
    return "unsupported"


def verify_tech_claim(claim_text: str, claim_vec: np.ndarray,
                      repo_chunks: list[dict],
                      repo_vecs: np.ndarray) -> tuple[str, list[dict], str]:
    """Verify one tech claim against one repo's evidence.

    Returns (verdict, evidence entries, method). Deterministic manifest
    matches win over NLI: if the claim names a declared package, the claim's
    tech is provably present regardless of how the NLI reads the phrasing.
    """
    hits = retrieve(claim_vec, repo_vecs, repo_chunks,
                    k=min(TOP_K, len(repo_chunks)))
    probs = entailment_probs([(c["text"], claim_text) for c, _ in hits])
    scored = sorted(
        (
            {
                "chunk_id": c["id"], "repo": c["repo"], "type": c["type"],
                "url": c["url"], "retrieval_score": round(sim, 4),
                "entailment": round(p.get("entailment", 0.0), 4),
                "contradiction": round(p.get("contradiction", 0.0), 4),
                "excerpt": c["text"][:200],
            }
            for (c, sim), p in zip(hits, probs)
        ),
        key=lambda e: -e["entailment"],
    )
    verdict = verdict_from_entailment(scored[0]["entailment"])

    if verdict != "supported":
        matched, dep_chunk = dependency_match(claim_text, repo_chunks)
        if matched:
            dep_ev = {
                "chunk_id": dep_chunk["id"], "repo": dep_chunk["repo"],
                "type": "dependencies", "url": dep_chunk["url"],
                "matched_packages": matched,
                "excerpt": dep_chunk["text"][:200],
            }
            return "supported", [dep_ev] + scored[:2], "dependency_match"

    if verdict == "unsupported":
        variants = claim_variants(claim_text)
        if variants:
            top_chunks = [c for c, _ in hits[:3]]
            pairs = [(c["text"], v) for v in variants for c in top_chunks]
            vprobs = entailment_probs(pairs)
            best_v, best_p = None, 0.0
            for (v, p) in zip((v for v in variants for _ in top_chunks),
                              (p.get("entailment", 0.0) for p in vprobs)):
                if p > best_p:
                    best_v, best_p = v, p
            if best_p >= SUPPORTED_T:
                scored[0]["core_variant"] = best_v
                scored[0]["core_entailment"] = round(best_p, 4)
                return "partial", scored[:3], "nli_core"

    return verdict, scored[:3], "nli"


def verify_claims(claims: list[dict], chunks: list[dict],
                  chunk_vecs: np.ndarray) -> list[dict]:
    """Attach verdict + evidence to every claim. Mutates nothing; returns new."""
    results = []
    aliases = load_aliases()
    repo_names = sorted({c["repo"] for c in chunks})
    tech = [c for c in claims if c["type"] == "tech"]
    tech_vecs = embed_texts([c["claim"] for c in tech]) if tech else None

    ti = 0
    for claim in claims:
        entry = dict(claim)
        if claim["type"] != "tech":
            entry["verdict"] = "unverifiable"
            entry["evidence"] = []
            entry["note"] = ("quantitative claims need business/metrics "
                            "evidence, not code" if claim["type"] == "quantitative"
                            else "soft skills cannot be shown by code evidence")
            results.append(entry)
            continue

        claim_vec = tech_vecs[ti]
        ti += 1

        repo = resolve_repo(claim["claim"], repo_names, aliases)
        if repo is None:
            entry["verdict"] = "no_evidence"
            entry["evidence"] = []
            entry["note"] = ("no repository for this project in the evidence "
                             "corpus; nothing to check the claim against")
            results.append(entry)
            continue

        # Scope retrieval to the claim's own repo to avoid cross-repo noise.
        idx = [i for i, c in enumerate(chunks) if c["repo"] == repo]
        verdict, evidence, method = verify_tech_claim(
            claim["claim"], claim_vec, [chunks[i] for i in idx],
            chunk_vecs[idx])
        entry["verdict"] = verdict
        entry["evidence"] = evidence
        entry["method"] = method
        results.append(entry)
    return results
