"""Embed evidence chunks with bge-m3, cached to disk.

Usage: python -m verify.embed  (re-embeds only when chunks.json changes)
"""

import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CHUNKS = ROOT / "data" / "evidence" / "chunks.json"
VECS = ROOT / "data" / "evidence" / "chunks.npy"
STAMP = ROOT / "data" / "evidence" / "chunks.sha"

MODEL_NAME = "BAAI/bge-m3"
_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    return get_model().encode(texts, normalize_embeddings=True,
                              show_progress_bar=len(texts) > 10)


def load_chunk_vectors() -> tuple[list[dict], np.ndarray]:
    """Return (chunks, vectors), re-embedding if chunks.json changed."""
    raw = CHUNKS.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    chunks = json.loads(raw)
    if VECS.exists() and STAMP.exists() and STAMP.read_text() == sha:
        return chunks, np.load(VECS)
    vecs = embed_texts([c["text"] for c in chunks])
    np.save(VECS, vecs)
    STAMP.write_text(sha)
    return chunks, vecs


if __name__ == "__main__":
    chunks, vecs = load_chunk_vectors()
    print(f"{len(chunks)} chunks embedded, shape {vecs.shape}")
