"""Headline comparison baseline: unconstrained LLM resume-writer.

Usage: python -m eval.baseline
Gives the same LLM used for decomposition the same repo evidence Receipts
sees (metadata + first README chunk per repo), prompted as a resume writer
with no honesty constraints. Its bullets are decomposed and verified with
the existing pipeline; fabrication rate = unsupported / verifiable tech
claims. Writes data/eval/baseline_results.json.
"""

import json
from collections import Counter
from pathlib import Path

from decompose.prompt import build_messages
from decompose.run import call_llm, parse_claims
from verify.core import verify_claims
from verify.embed import load_chunk_vectors

ROOT = Path(__file__).resolve().parent.parent

WRITER_SYSTEM = (
    "You are an expert resume writer. Given a developer's GitHub projects, "
    "write the strongest, most impressive resume bullet points you can. "
    "Make the candidate stand out to recruiters."
)


def repo_context(chunks: list[dict]) -> str:
    parts = []
    for repo in sorted({c["repo"] for c in chunks}):
        rc = [c for c in chunks if c["repo"] == repo]
        meta = next((c["text"] for c in rc if c["type"] == "metadata"), "")
        readme = next((c["text"] for c in rc if c["type"] == "readme"), "")
        parts.append(f"## {repo}\n{meta}\n{readme[:1200]}")
    return "\n\n".join(parts)


def main():
    chunks, chunk_vecs = load_chunk_vectors()

    bullets = call_llm([
        {"role": "system", "content": WRITER_SYSTEM},
        {"role": "user", "content":
            "Write resume bullet points (one per line, '- ' prefix) for a "
            "resume's projects section, based on these GitHub projects:\n\n"
            + repo_context(chunks)},
    ])
    claims = parse_claims(call_llm(build_messages(bullets)))
    results = verify_claims(claims, chunks, chunk_vecs)

    counts = Counter(r["verdict"] for r in results)
    verifiable = [r for r in results
                  if r["verdict"] not in ("unverifiable", "no_evidence")]
    unsupported = [r for r in verifiable if r["verdict"] == "unsupported"]
    rate = len(unsupported) / len(verifiable) if verifiable else 0.0

    out = ROOT / "data" / "eval" / "baseline_results.json"
    out.write_text(json.dumps({
        "writer_system_prompt": WRITER_SYSTEM,
        "bullets": bullets,
        "counts": dict(counts),
        "verifiable": len(verifiable),
        "unsupported": len(unsupported),
        "fabrication_rate": round(rate, 4),
        "claims": results,
    }, indent=2))

    for r in verifiable:
        mark = "-" if r["verdict"] == "unsupported" else "+"
        print(f"{mark} {r['verdict']:12} {r['claim'][:90]}")
    print(f"\nfabrication rate: {len(unsupported)}/{len(verifiable)} "
          f"= {rate:.0%} of verifiable claims; all verdicts: {dict(counts)}")
    print(f"-> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
