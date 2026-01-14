POSTGRES_KEYWORDS = [
    "select", "insert", "update", "delete", "table", "index",
    "transaction", "commit", "rollback", "vacuum", "explain",
    "analyze", "postgres", "sql"
]

def is_potentially_relevant(question: str) -> bool:
    q = question.lower()
    return True
    #return any(keyword in q for keyword in POSTGRES_KEYWORDS)
