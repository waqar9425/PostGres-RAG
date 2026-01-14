import json
from retriever import retrieve_chunks

QA_PATH = "data/qa/qa.json"

def recall_at_k(k=5):
    with open(QA_PATH, "r", encoding="utf-8") as f:
        qa_set = json.load(f)

    hits = 0

    for qa in qa_set:
        results = retrieve_chunks(qa["question"], top_k=k)
        retrieved_docs = {r["metadata"]["doc_name"] for r in results}

        if qa["source_doc"] in retrieved_docs:
            hits += 1

    recall = hits / len(qa_set)
    print(f"Recall@{k}: {recall:.2f}")


if __name__ == "__main__":
    recall_at_k(k=5)
