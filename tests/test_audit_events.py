from audit.audit_logger import (
    log_tool_event,
    log_rule_event,
    log_rag_event,
)


def test_log_tool_event():
    event = log_tool_event(
        user_id="demo_user_001",
        session_id="session_001",
        tool_name="calculate_emi",
        success=True,
    )

    assert event["event_type"] == "TOOL_EXECUTED"
    assert event["data"]["tool"] == "calculate_emi"
    assert event["data"]["success"] is True


def test_log_rule_event():
    event = log_rule_event(
        user_id="demo_user_001",
        session_id="session_001",
        rule_name="debt_burden",
        result="attention",
    )

    assert event["event_type"] == "RULE_EVALUATED"
    assert event["data"]["rule"] == "debt_burden"
    assert event["data"]["result"] == "attention"


def test_log_rag_event():
    event = log_rag_event(
        user_id="demo_user_001",
        session_id="session_001",
        query="How should debt be managed?",
        sources=["NISM-Series-X-A"],
    )

    assert event["event_type"] == "RAG_RETRIEVED"
    assert event["data"]["query"] == "How should debt be managed?"
    assert event["data"]["sources"] == ["NISM-Series-X-A"]