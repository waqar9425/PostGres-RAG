import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

CHUNKS_PATH = "data/chunks/chunks.json"
OUTPUT_DIR = "embeddings"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FAISS_INDEX_PATH = os.path.join(OUTPUT_DIR, "faiss.index")
METADATA_PATH = os.path.join(OUTPUT_DIR, "metadata.json")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("[INFO] Loading chunks...")
    chunks = load_chunks()

    texts = [chunk["text"] for chunk in chunks]
    #metadata = [chunk["metadata"] | {"chunk_id": chunk["chunk_id"]} for chunk in chunks]
    metadata = [
    {
        "chunk_id": chunk["chunk_id"],
        "text": chunk["text"],
        **chunk["metadata"]
    }
    for chunk in chunks
]


    print(f"[INFO] Total chunks: {len(texts)}")

    print("[INFO] Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("[INFO] Generating embeddings...")
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True  # IMPORTANT for cosine similarity
    )

    dim = embeddings.shape[1]
    print(f"[INFO] Embedding dimension: {dim}")

    print("[INFO] Creating FAISS index...")
    index = faiss.IndexFlatIP(dim)  # Inner Product = cosine (since normalized)
    index.add(embeddings)

    print(f"[OK] Total vectors indexed: {index.ntotal}")

    print("[INFO] Saving FAISS index...")
    faiss.write_index(index, FAISS_INDEX_PATH)

    print("[INFO] Saving metadata...")
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("[DONE] Embedding + indexing complete")


if __name__ == "__main__":
    main()
