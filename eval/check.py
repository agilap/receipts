"""Validate data/eval/labeled_claims.jsonl before running metrics.

Usage: python -m eval.check
Checks: valid JSON per line, required fields, known labels, repo names that
exist in the evidence corpus, no duplicate claims, and per-label counts.
"""

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABELS = ("true", "stretched", "fabricated")


def main():
    chunks = json.loads((ROOT / "data" / "evidence" / "chunks.json").read_text())
    repos = {c["repo"] for c in chunks}

    path = ROOT / "data" / "eval" / "labeled_claims.jsonl"
    errors, rows, seen = [], [], set()
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"line {n}: bad JSON ({e})")
            continue
        for field in ("claim", "repo", "label"):
            if not row.get(field, "").strip():
                errors.append(f"line {n}: empty {field!r}")
        if row.get("label") and row["label"] not in LABELS:
            errors.append(f"line {n}: unknown label {row['label']!r}")
        if row.get("repo") and row["repo"] not in repos:
            errors.append(f"line {n}: repo {row['repo']!r} not in evidence "
                          f"corpus {sorted(repos)}")
        if row.get("claim"):
            if row["claim"] in seen:
                errors.append(f"line {n}: duplicate claim")
            seen.add(row["claim"])
        rows.append(row)

    counts = Counter(r.get("label") for r in rows)
    print(f"{len(rows)} rows; labels: {dict(counts)}")
    if errors:
        print("\n".join(errors))
        sys.exit(f"{len(errors)} problem(s) found")
    print("format OK")


if __name__ == "__main__":
    main()
