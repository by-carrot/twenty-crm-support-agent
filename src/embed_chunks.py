"""
Reads data/chunks.json, embeds each chunk with all-MiniLM-L6-v2, and saves:
  - data/chunk_vectors.npy  — float32 matrix, one row per chunk
  - data/chunk_index.json   — list of chunk metadata, position i matches row i
"""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path(__file__).parent.parent / "data" / "chunks.json"
VECTORS_OUT = Path(__file__).parent.parent / "data" / "chunk_vectors.npy"
INDEX_OUT = Path(__file__).parent.parent / "data" / "chunk_index.json"
MODEL_NAME = "all-MiniLM-L6-v2"


def main() -> None:
    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    print(f"Loaded {len(chunks)} chunks.")

    model = SentenceTransformer(MODEL_NAME)
    texts = [c["text"] for c in chunks]

    print(f"Embedding with {MODEL_NAME}...")
    vectors = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    np.save(VECTORS_OUT, vectors)

    index = [
        {"text": c["text"], "source": c["source"], "heading": c["heading"]}
        for c in chunks
    ]
    INDEX_OUT.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Saved {vectors.shape[0]} vectors (dim={vectors.shape[1]}) -> {VECTORS_OUT}")
    print(f"Saved index -> {INDEX_OUT}")


if __name__ == "__main__":
    main()
