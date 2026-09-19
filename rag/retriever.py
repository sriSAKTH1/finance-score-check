from rag.vectorstore import load_vectorstore
from audit.audit_logger import log_rag_event


def retrieve(
    query: str,
    k: int = 4,
    user_id: str = "system",
    session_id: str = "system"
) -> list[dict]:

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    output = []

    for document in results:
        output.append({
            "text": document.page_content,
            "metadata": document.metadata
        })

    # Extract source information for audit
    sources = []

    for document in results:
        metadata = document.metadata or {}

        sources.append({
            "source": metadata.get("source"),
            "page": metadata.get("page"),
        })

    # Audit RAG retrieval
    log_rag_event(
        user_id=user_id,
        session_id=session_id,
        query=query,
        sources=sources
    )

    return output