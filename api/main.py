"""Receipts API: verify resume claims against the fetched GitHub evidence.

Run: uvicorn api.main:app --port 8000
The evidence corpus (data/evidence/chunks.json) is loaded at startup;
fetching evidence stays an offline step (ingest/fetch_github.py).
"""

import json
import sqlite3
import time
from collections import Counter
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from decompose.run import call_llm, parse_claims
from decompose.prompt import build_messages
from verify.core import verify_claims
from verify.embed import load_chunk_vectors

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "receipts.db"

app = FastAPI(title="Receipts")
_corpus = {}


@app.on_event("startup")
def startup():
    _corpus["chunks"], _corpus["vecs"] = load_chunk_vectors()
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at REAL NOT NULL,
        resume_chars INTEGER NOT NULL,
        report_json TEXT NOT NULL)""")
    con.commit()
    con.close()


class VerifyRequest(BaseModel):
    resume_text: str


def summarize(results: list[dict]) -> dict:
    counts = Counter(r["verdict"] for r in results)
    verifiable = sum(v for k, v in counts.items()
                     if k not in ("unverifiable", "no_evidence"))
    return {"counts": dict(counts), "verifiable": verifiable,
            "supported": counts.get("supported", 0),
            "headline": f"{counts.get('supported', 0)}/{verifiable} "
                        "verifiable claims supported"}


@app.post("/api/verify")
def verify(req: VerifyRequest):
    text = req.resume_text.strip()
    if len(text) < 100:
        raise HTTPException(400, "resume text too short to decompose")
    if len(text) > 30000:
        raise HTTPException(400, "resume text too long")

    claims = parse_claims(call_llm(build_messages(text)))
    results = verify_claims(claims, _corpus["chunks"], _corpus["vecs"])
    report = {"summary": summarize(results), "claims": results}

    con = sqlite3.connect(DB)
    con.execute("INSERT INTO runs (created_at, resume_chars, report_json) "
                "VALUES (?, ?, ?)",
                (time.time(), len(text), json.dumps(report)))
    con.commit()
    con.close()
    return report


@app.get("/api/runs/latest")
def latest_run():
    con = sqlite3.connect(DB)
    row = con.execute("SELECT report_json FROM runs "
                      "ORDER BY id DESC LIMIT 1").fetchone()
    con.close()
    if row is None:
        raise HTTPException(404, "no runs yet")
    return json.loads(row[0])


@app.get("/api/health")
def health():
    return {"ok": True, "chunks": len(_corpus.get("chunks", []))}
