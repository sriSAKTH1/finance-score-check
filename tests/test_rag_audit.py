from rag.retriever import retrieve
from audit.audit_reader import get_session_events


def test_rag_creates_audit_event():

    session_id = "rag-audit-test"
    user_id = "demo_user_001"

    results = retrieve(
        "What is financial planning?",
        k=2,
        user_id=user_id,
        session_id=session_id,
    )

    assert isinstance(results, list)

    events = get_session_events(session_id)

    rag_events = [
        event
        for event in events
        if event.get("event_type") == "RAG_RETRIEVED"
    ]

    assert len(rag_events) >= 1

    event = rag_events[-1]

    assert event["data"]["query"] == "What is financial planning?"

    assert "sources" in event["data"]