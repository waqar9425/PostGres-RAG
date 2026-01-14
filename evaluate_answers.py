import json
import numpy as np
from sentence_transformers import SentenceTransformer
from qa_pipeline import answer_question

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
QA_PATH = "data/qa/qa.json"


def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def evaluate():
    with open(QA_PATH, "r", encoding="utf-8") as f:
        qa_set = json.load(f)

    scores = []

    for qa in qa_set:
        generated = answer_question(qa["question"])
        emb_gen = model.encode(generated)
        emb_ref = model.encode(qa["answer"])

        score = cosine(emb_gen, emb_ref)
        scores.append(score)

    print(f"Average answer similarity: {sum(scores)/len(scores):.2f}")


if __name__ == "__main__":
    evaluate()
