from audit.audit_reader import get_session_events
from audit.metrics import (
    get_total_requests,
    get_intent_counts,
    get_agent_counts,
    get_tool_success_rate,
    get_rule_results,
    get_rag_usage,
)


def test_end_to_end_audit_events():

    session_id = "audit-e2e-test"

    events = get_session_events(session_id)

    assert isinstance(events, list)


def test_audit_metrics():

    assert get_total_requests() >= 0
    assert isinstance(get_intent_counts(), dict)
    assert isinstance(get_agent_counts(), dict)

    rate = get_tool_success_rate()

    assert 0 <= rate <= 100

    assert isinstance(get_rule_results(), dict)

    assert get_rag_usage() >= 0