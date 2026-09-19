from graph.workflow import graph


def test_final_agent_loan_flow():

    state = {
        "user_id": "demo_user_001",
        "session_id": "final-agent-test",
        "user_message": "Can I take a loan of 50000?",
        "conversation_history": [],
    }

    result = graph.invoke(state)

    assert result is not None

    assert "intent" in result

    assert result["intent"].upper() in [
        "LOAN",
        "DEBT",
        "DEBT_ANALYSIS",
    ]

    assert "final_response" in result

    assert result["final_response"]


def test_final_agent_cashflow_flow():

    state = {
        "user_id": "demo_user_001",
        "session_id": "final-cashflow-test",
        "user_message": "How is my monthly cash flow?",
        "conversation_history": [],
    }

    result = graph.invoke(state)

    assert result is not None
    assert "final_response" in result
    assert result["final_response"]