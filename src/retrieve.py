"""
Retrieval: embed a query and return the top-k most similar chunks by cosine
similarity against the precomputed chunk vectors.

Usage as a script:
    python src/retrieve.py "how do I create a custom field?"
"""

import json
import sys
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = Path(__file__).parent.parent / "data"
VECTORS_FILE = DATA_DIR / "chunk_vectors.npy"
INDEX_FILE = DATA_DIR / "chunk_index.json"
MODEL_NAME = "all-MiniLM-L6-v2"

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def retrieve(query: str, k: int = 5) -> list[dict]:
    """
    Return the top-k chunks most relevant to query, each with keys:
    text, source, heading, score (cosine similarity, higher = more relevant).
    """
    model = _get_model()
    vectors = np.load(VECTORS_FILE)
    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))

    query_vec = model.encode([query], convert_to_numpy=True)
    scores = cosine_similarity(query_vec, vectors)[0]

    top_indices = scores.argsort()[::-1][:k]
    return [
        {
            "text": index[i]["text"],
            "source": index[i]["source"],
            "heading": index[i]["heading"],
            "score": float(scores[i]),
        }
        for i in top_indices
    ]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    query = " ".join(sys.argv[1:]) or "How do I create a custom field?"
    results = retrieve(query, k=3)
    for r in results:
        print(f"\n[{r['score']:.3f}] {r['source']} / {r['heading']}")
        print(r["text"][:400])
