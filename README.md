PostgreSQL 16 Documentation Q&A (RAG App)

A lightweight Retrieval-Augmented Generation (RAG) application that answers questions over official PostgreSQL 16 documentation using semantic search and an LLM.
It retrieves relevant documentation chunks, generates grounded answers, supports conversational memory, and cites sources.

Features:

    Semantic search over PostgreSQL 16 docs

    RAG-based question answering

    Chat-style interface with conversation memory

    Sources cited per answer

    Handles irrelevant questions gracefully

    Evaluation via Recall@k and answer similarity


Architecture:

    PostgreSQL Docs (HTML)
            ↓
    HTML Parsing & Cleaning
            ↓
    Chunking (overlap)
            ↓
    Embedding Model
            ↓
    Vector Store (FAISS)
            ↓
    Top-k Retrieval
            ↓
    Prompt Construction
            ↓
    LLM
            ↓
    Answer + Citations
            ↓
    Streamlit UI


Project Structure:

rag_postgres/
│
├── data/
│   ├── raw_docs/          # Parsed PostgreSQL HTML docs
│   ├── chunks.json        # Chunked documents
│   └── qa_dataset.json    # Evaluation Q&A set
│
├── embeddings/
│   ├── faiss.index        # FAISS vector index
│   └── metadata.json      # Chunk metadata
│
├── ingest_docs.py         # Fetch & parse docs
├── chunk_docs.py          # Chunking with overlap
├── embed_chunks.py        # Embedding + FAISS indexing
├── retriever.py           # Top-k semantic retrieval
├── prompt.py              # Prompt construction (with memory)
├── generate.py            # LLM wrapper
├── app.py                 # Streamlit UI
├── eval.py                # Evaluation metrics
├── requirements.txt
└── README.md


Chunking Strategy:

    Chunk size: 500 characters

    Overlap: 100 characters

    Metadata: document name, section, source URL

    This ensures high recall while keeping context manageable.


Retrieval & Embeddings:

    Vector store: FAISS

    Embedding model: sentence-transformers/all-MiniLM-L6-v2

    Similarity: Cosine similarity

    Top-k retrieval: Configurable via UI slider

Prompt & LLM:

    Strict system prompt ensures:

    Answer only from retrieved context

    Use chat history for follow-up questions

    Respond with "The answer is not found..." if unsupported

    Memory of last 3 conversation turns is maintained

Handling Irrelevant Queries:

    If retrieval returns no chunks, assistant replies gracefully:
    "This question is outside the scope of PostgreSQL documentation."


Evaluation:

    Dataset: 10–20 curated Q&A pairs from PostgreSQL docs

    Metrics:

    Recall@k: Checks if the correct document is retrieved

    Answer similarity: Cosine similarity of embeddings between generated and reference answers

Start the app:

    streamlit run app.py

    Installation and Setup:

    # Create environment
    conda create -n open_source_rag python=3.10
    conda activate open_source_rag

    # Install dependencies
    pip install -r requirements.txt

    # Run ingestion and embedding
    python ingest_docs.py
    python chunk_docs.py
    python embed_chunks.py

    # Launch the app
    streamlit run app.py


Limitations:

    Lightweight embedding model (not domain-tuned)

    No reranker; may fail on very subtle queries

    HTML parsing is heuristic-based

    LLM hallucination possible if retrieval fails

    Designed for demonstration, not production-scale deployment

    Retriver evaluation only considering source doc for now. This should be chunk at chunk level. So we check if chunk was from right document but we are checking withing that document whether the chunks we relevant. chunk level ground truth creation will take time hence going with source doc level evaluation for now.