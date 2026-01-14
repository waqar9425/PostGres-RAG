import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

FAISS_INDEX_PATH = "embeddings/faiss.index"
METADATA_PATH = "embeddings/metadata.json"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# -----------------------
# Load resources ONCE
# -----------------------

print("[INFO] Loading FAISS index...")
faiss_index = faiss.read_index(FAISS_INDEX_PATH)

print("[INFO] Loading metadata...")
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

print("[INFO] Loading embedding model...")
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


# -----------------------
# Retrieval function
# -----------------------

def retrieve_chunks(
    query: str,
    top_k: int = 5,
    similarity_threshold: float = 0.25
):
    """
    Retrieve top-k relevant chunks for a query.
    Returns a list of dicts with text, score, and metadata.
    """

    # Embed query
    query_embedding = embedding_model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).reshape(1, -1)

    # Search FAISS
    scores, indices = faiss_index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        if score < similarity_threshold:
            continue

        chunk_meta = metadata[idx]

        results.append({
            "score": float(score),
            "text": chunk_meta["text"],
            "metadata": {
                "doc_name": chunk_meta["doc_name"],
                "section_title": chunk_meta["section_title"],
                "url": chunk_meta["url"]
            }
        })

    return results
