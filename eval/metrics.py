"""Run the eval set through the verification core and report metrics.

Usage: python -m eval.metrics
Reads data/eval/labeled_claims.jsonl; writes data/eval/results.json and
prints per-verdict precision/recall plus the confusion matrix as markdown.
"""

import json
from collections import Counter
from pathlib import Path

from verify.core import verify_tech_claim
from verify.embed import embed_texts, load_chunk_vectors

ROOT = Path(__file__).resolve().parent.parent

EXPECTED = {"true": "supported", "stretched": "partial",
            "fabricated": "unsupported"}
VERDICTS = ("supported", "partial", "unsupported")


def main():
    rows = [json.loads(l) for l in
            (ROOT / "data" / "eval" / "labeled_claims.jsonl")
            .read_text().splitlines() if l.strip()]
    chunks, chunk_vecs = load_chunk_vectors()
    claim_vecs = embed_texts([r["claim"] for r in rows])

    for row, vec in zip(rows, claim_vecs):
        idx = [i for i, c in enumerate(chunks) if c["repo"] == row["repo"]]
        verdict, evidence, method = verify_tech_claim(
            row["claim"], vec, [chunks[i] for i in idx], chunk_vecs[idx])
        row["verdict"] = verdict
        row["method"] = method
        row["expected"] = EXPECTED[row["label"]]
        row["best_entailment"] = max(
            (e.get("entailment", 0.0) for e in evidence), default=0.0)

    (ROOT / "data" / "eval" / "results.json").write_text(
        json.dumps(rows, indent=2))

    # Confusion matrix: label rows x verdict columns.
    conf = Counter((r["label"], r["verdict"]) for r in rows)
    print("| label \\ verdict | " + " | ".join(VERDICTS) + " |")
    print("|---|" + "---|" * len(VERDICTS))
    for label in ("true", "stretched", "fabricated"):
        cells = [str(conf.get((label, v), 0)) for v in VERDICTS]
        print(f"| {label} | " + " | ".join(cells) + " |")

    print()
    for v in VERDICTS:
        tp = sum(1 for r in rows if r["verdict"] == v and r["expected"] == v)
        fp = sum(1 for r in rows if r["verdict"] == v and r["expected"] != v)
        fn = sum(1 for r in rows if r["verdict"] != v and r["expected"] == v)
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        print(f"{v:12} precision={prec:.2f} recall={rec:.2f}")

    acc = sum(1 for r in rows if r["verdict"] == r["expected"]) / len(rows)
    fab_caught = sum(1 for r in rows if r["label"] == "fabricated"
                     and r["verdict"] == "unsupported")
    print(f"\naccuracy={acc:.2f}  fabrications flagged: {fab_caught}/20")


if __name__ == "__main__":
    main()
