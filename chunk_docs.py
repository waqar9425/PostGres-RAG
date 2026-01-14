import os
import json
from pathlib import Path
from tqdm import tqdm

RAW_DOCS_DIR = Path("data/raw_docs")
OUTPUT_DIR = Path("data/chunks")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE_TOKENS = 500
OVERLAP_TOKENS = 100
CHARS_PER_TOKEN = 4  # safe approximation


def chunk_text(text, chunk_size_tokens, overlap_tokens):
    chunk_size_chars = chunk_size_tokens * CHARS_PER_TOKEN
    overlap_chars = overlap_tokens * CHARS_PER_TOKEN

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size_chars
        chunk = text[start:end]
        chunks.append(chunk.strip())

        if end >= text_length:
            break

        start = end - overlap_chars

    return chunks


def process_document(doc_path):
    with open(doc_path, "r", encoding="utf-8") as f:
        doc = json.load(f)

    doc_name = doc["doc_name"]
    url = doc["url"]

    all_chunks = []
    chunk_counter = 0

    for section in doc["sections"]:
        section_title = section["title"]
        section_text = section["text"].strip()

        if not section_text:
            continue

        text_chunks = chunk_text(
            section_text,
            CHUNK_SIZE_TOKENS,
            OVERLAP_TOKENS
        )

        for chunk in text_chunks:
            all_chunks.append({
                "chunk_id": chunk_counter,
                "text": chunk,
                "metadata": {
                    "doc_name": doc_name,
                    "section_title": section_title,
                    "url": url
                }
            })
            chunk_counter += 1

    return all_chunks


def main():
    all_documents_chunks = []

    for doc_file in tqdm(list(RAW_DOCS_DIR.glob("*.json"))):
        print(f"Chunking {doc_file.name}")
        chunks = process_document(doc_file)
        all_documents_chunks.extend(chunks)

    output_path = OUTPUT_DIR / "chunks.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_documents_chunks, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Total chunks created: {len(all_documents_chunks)}")
    print(f"[OK] Saved to {output_path}")


if __name__ == "__main__":
    main()
