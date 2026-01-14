import streamlit as st

from retriever import retrieve_chunks
from prompt import build_prompt
from generate import generate_answer

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="PostgreSQL Docs QA",
    page_icon="🐘",
    layout="wide"
)

st.title("🐘 PostgreSQL 16 Documentation Q&A")
st.caption("RAG-based question answering over official PostgreSQL documentation")

# -----------------------
# Sidebar controls
# -----------------------
with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Top-k retrieved chunks", 3, 10, 5)
    st.markdown("---")
    st.markdown(
        """
        **Notes**
        - Answers are grounded in PostgreSQL 16 docs
        - Follow-up questions are supported
        """
    )

# -----------------------
# Session state
# -----------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------
# Display chat history
# -----------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------
# Chat input
# -----------------------
user_question = st.chat_input("Ask a question about PostgreSQL SQL commands...")

if user_question:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_question
    })

    # -----------------------
    # Retrieval
    # -----------------------
    retrieved_chunks = retrieve_chunks(user_question, top_k=top_k)

    if not retrieved_chunks:
        assistant_answer = "This question is outside the scope of PostgreSQL documentation."
        sources = []
    else:
        # Build prompt with last 3 conversations
        system_prompt, user_prompt = build_prompt(
            retrieved_chunks,
            user_question,
            chat_history=st.session_state.chat_history
        )

        # LLM call
        assistant_answer = generate_answer(system_prompt, user_prompt)

        # Collect sources
        sources = {
            chunk["metadata"]["doc_name"]
            for chunk in retrieved_chunks
        }

    # -----------------------
    # Display assistant response
    # -----------------------
    with st.chat_message("assistant"):
        st.markdown(assistant_answer)

        if sources:
            with st.expander("Sources"):
                for src in sorted(sources):
                    st.markdown(f"- `{src}`")

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_answer
    })
