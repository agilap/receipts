"""Run the full verification pipeline: claims + evidence -> report.

Usage: python -m verify.run [claims_path]
Writes data/report/report.json and prints a per-claim summary.
"""

import json
import sys
from collections import Counter
from pathlib import Path

from verify.core import verify_claims
from verify.embed import load_chunk_vectors

ROOT = Path(__file__).resolve().parent.parent


def main():
    claims_path = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "data" / "claims" / "claims.json"
    claims = json.loads(claims_path.read_text())
    chunks, chunk_vecs = load_chunk_vectors()

    results = verify_claims(claims, chunks, chunk_vecs)

    out = ROOT / "data" / "report" / "report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2))

    counts = Counter(r["verdict"] for r in results)
    for r in results:
        mark = {"supported": "+", "partial": "~", "unsupported": "-",
                "no_evidence": "0", "unverifiable": "?"}[r["verdict"]]
        best = r["evidence"][0] if r["evidence"] else None
        src = f"  [{best['repo']} e={best['entailment']}]" if best else ""
        print(f"{mark} {r['verdict']:12} {r['claim'][:90]}{src}")
    verifiable = sum(v for k, v in counts.items()
                     if k not in ("unverifiable", "no_evidence"))
    print(f"\n{counts['supported']}/{verifiable} verifiable claims supported; "
          f"{dict(counts)} -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
