"""Run claim decomposition on a resume file.

Usage: python -m decompose.run [resume_path]

Reads OPENAI_API_KEY from the environment or a .env file in the repo root.
Writes data/claims/claims.json.
"""

import json
import os
import sys
from pathlib import Path

import requests

from decompose.prompt import build_messages
from decompose.taxonomy import CLAIM_TYPES

ROOT = Path(__file__).resolve().parent.parent
MODEL = os.environ.get("RECEIPTS_LLM_MODEL", "gpt-4o-mini")


def load_api_key() -> str:
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("OPENAI_API_KEY not found in environment or .env")


def call_llm(messages: list[dict]) -> str:
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {load_api_key()}"},
        json={"model": MODEL, "messages": messages, "temperature": 0},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def parse_claims(text: str) -> list[dict]:
    """Parse and validate the model output; raises ValueError if malformed."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    claims = json.loads(text)
    if not isinstance(claims, list) or not claims:
        raise ValueError("expected a non-empty JSON array")
    for c in claims:
        if not all(isinstance(c.get(k), str) and c[k].strip()
                   for k in ("claim", "type", "source_bullet")):
            raise ValueError(f"bad claim object: {c}")
        if c["type"] not in CLAIM_TYPES:
            raise ValueError(f"unknown type {c['type']!r} in: {c}")
    return claims


def main():
    resume_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "resume.txt"
    resume = resume_path.read_text()

    messages = build_messages(resume)
    text = call_llm(messages)
    try:
        claims = parse_claims(text)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"malformed output ({e}); retrying once...", file=sys.stderr)
        messages.append({"role": "assistant", "content": text})
        messages.append({"role": "user", "content":
                         f"Your output was invalid ({e}). Output only the "
                         "corrected JSON array, nothing else."})
        claims = parse_claims(call_llm(messages))

    out = ROOT / "data" / "claims" / "claims.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(claims, indent=2))

    counts = {t: sum(1 for c in claims if c["type"] == t) for t in CLAIM_TYPES}
    print(f"{len(claims)} claims -> {out.relative_to(ROOT)}  {counts}")


if __name__ == "__main__":
    main()
