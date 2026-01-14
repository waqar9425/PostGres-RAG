from guards import is_potentially_relevant

def answer_question(question, chat_history=None):
    if not is_potentially_relevant(question):
        return "This question is outside the scope of PostgreSQL documentation."

    retrieved = retrieve_chunks(question)

    if not retrieved:
        return "This question is outside the scope of PostgreSQL documentation."

    system_prompt, user_prompt = build_prompt(
        retrieved, question, chat_history
    )

    return generate_answer(system_prompt, user_prompt)
