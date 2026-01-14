def build_prompt(
    context_chunks,
    question,
    chat_history=None,
    max_turns=3
):
    """
    chat_history: list of dicts [{"role": "user"/"assistant", "content": "..."}]
    max_turns: number of (user, assistant) pairs to keep
    """

    # -----------------------
    # Context
    # -----------------------
    context_text = ""
    for i, chunk in enumerate(context_chunks, 1):
        context_text += (
            f"[Source {i}: {chunk['metadata']['doc_name']}]\n"
            f"{chunk['text']}\n\n"
        )

    # -----------------------
    # Memory (last N turns)
    # -----------------------
    history_text = ""
    if chat_history:
        max_messages = max_turns * 2
        for turn in chat_history[-max_messages:]:
            history_text += (
                f"{turn['role'].capitalize()}: {turn['content']}\n"
            )

    # -----------------------
    # System prompt
    # -----------------------
    system_prompt = """
You are an expert PostgreSQL documentation assistant.

Rules:
- Answer ONLY using the provided documentation context.
- Use chat history only to resolve references like "this", "that", or "it".
- If the answer is not present in the context, say:
  "The answer is not found in the provided PostgreSQL documentation."
- Do NOT use external knowledge.
- Cite sources using document names in square brackets.
""".strip()

    # -----------------------
    # User prompt
    # -----------------------
    user_prompt = f"""
Conversation so far:
{history_text}

Context:
{context_text}

Question:
{question}

Answer:
""".strip()

    return system_prompt, user_prompt
