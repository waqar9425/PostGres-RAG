from retriever import retrieve_chunks
from prompt import build_prompt
from generate import generate_answer


def answer_question(question, chat_history=None):
    retrieved = retrieve_chunks(question)

    if not retrieved:
        return "This question is outside the scope of PostgreSQL documentation."

    system_prompt, user_prompt = build_prompt(
        retrieved, question, chat_history
    )

    return generate_answer(system_prompt, user_prompt)
