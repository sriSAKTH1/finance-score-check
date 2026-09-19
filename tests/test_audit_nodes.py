from graph.audit_nodes import (
    audit_request_node,
    audit_intent_node,
    audit_context_node,
    audit_agent_node,
    audit_response_node,
)


def base_state():

    return {
        "user_id": "demo_user_001",
        "session_id": "audit-node-test",
        "user_message": "Can I take a loan?",
        "intent": "LOAN",
        "financial_context": {
            "income": {},
            "expenses": {},
            "liabilities": {},
        },
        "scenario_type": "loan",
        "final_response": "Loan analysis completed.",
    }


def test_audit_request_node():

    result = audit_request_node(
        base_state()
    )

    assert result == {}


def test_audit_intent_node():

    result = audit_intent_node(
        base_state()
    )

    assert result == {}


def test_audit_context_node():

    result = audit_context_node(
        base_state()
    )

    assert result == {}


def test_audit_agent_node():

    result = audit_agent_node(
        base_state()
    )

    assert result == {}


def test_audit_response_node():

    result = audit_response_node(
        base_state()
    )

    assert result == {}