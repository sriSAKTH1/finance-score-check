from graph.workflow import graph
from audit.audit_reader import get_session_events


def test_complete_agent_audit_trail():

    user_id = "demo_user_001"
    session_id = "final-audit-test"

    state = {
        "user_id": user_id,
        "session_id": session_id,
        "user_message": (
            "Can I take a loan of 50000 at 12% interest "
            "for 24 months?"
        ),
        "conversation_history": [],
    }

    result = graph.invoke(state)

    assert result is not None
    assert result.get("final_response")

    events = get_session_events(session_id)

    assert events

    event_types = [
        event.get("event_type")
        for event in events
    ]

    # Request
    assert "REQUEST_RECEIVED" in event_types

    # Intent
    assert "INTENT_DETECTED" in event_types

    # Agent
    assert "AGENT_SELECTED" in event_types

    # Tool
    assert "TOOL_EXECUTED" in event_types

    # Rule
    assert "RULE_EVALUATED" in event_types

    # RAG
    assert "RAG_RETRIEVED" in event_types

    # Response
    assert "RESPONSE_GENERATED" in event_types
    assert "RESPONSE_AUDITED" in event_types