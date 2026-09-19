from audit.audit_logger import (
    log_audit_event,
    log_tool_event,
    log_rule_event,
    log_rag_event,
)

from audit.metrics import (
    get_total_requests,
    get_intent_counts,
    get_agent_counts,
    get_tool_success_rate,
    get_rule_results,
    get_rag_usage,
    get_error_count,
)


def setup_audit_data():
    log_audit_event(
        user_id="demo_user_001",
        session_id="metrics_001",
        event_type="REQUEST_RECEIVED",
    )

    log_audit_event(
        user_id="demo_user_001",
        session_id="metrics_001",
        event_type="INTENT_DETECTED",
        data={"intent": "DEBT"},
    )

    log_audit_event(
        user_id="demo_user_001",
        session_id="metrics_001",
        event_type="INTENT_DETECTED",
        data={"intent": "INVESTMENT"},
    )

    log_audit_event(
        user_id="demo_user_001",
        session_id="metrics_001",
        event_type="AGENT_SELECTED",
        data={"intent": "DEBT"},
    )

    log_tool_event(
        user_id="demo_user_001",
        session_id="metrics_001",
        tool_name="calculate_emi",
        success=True,
    )

    log_tool_event(
        user_id="demo_user_001",
        session_id="metrics_001",
        tool_name="calculate_debt_burden",
        success=False,
    )

    log_rule_event(
        user_id="demo_user_001",
        session_id="metrics_001",
        rule_name="debt_burden",
        result="attention",
    )

    log_rag_event(
        user_id="demo_user_001",
        session_id="metrics_001",
        query="debt management",
        sources=["NISM-Series-X-A"],
    )

    log_audit_event(
        user_id="demo_user_001",
        session_id="metrics_001",
        event_type="ERROR",
        data={"errors": ["Test error"]},
    )


def test_total_requests():

    setup_audit_data()

    assert get_total_requests() >= 1


def test_intent_counts():

    setup_audit_data()

    counts = get_intent_counts()

    assert counts["DEBT"] >= 1
    assert counts["INVESTMENT"] >= 1


def test_agent_counts():

    setup_audit_data()

    counts = get_agent_counts()

    assert counts["DEBT"] >= 1


def test_tool_success_rate():

    setup_audit_data()

    rate = get_tool_success_rate()

    assert 0 <= rate <= 100


def test_rule_results():

    setup_audit_data()

    results = get_rule_results()

    assert results["attention"] >= 1


def test_rag_usage():

    setup_audit_data()

    assert get_rag_usage() >= 1


def test_error_count():

    setup_audit_data()

    assert get_error_count() >= 1