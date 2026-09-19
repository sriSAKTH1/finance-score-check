from graph.final_guardrail_node import final_guardrail_node


def test_final_response_with_nism_evidence():

    state = {
        "financial_context": {
            "income": {
                "monthly_salary": 75000
            },
            "expenses": {
                "monthly_expense": 45000
            },
            "risk_profile": {
                "category": "Moderate"
            },
            "goals": []
        },
        "final_response": (
            "Your financial plan should consider "
            "your income, expenses and financial goals."
        ),
        "rag_results": [
            {
                "text": (
                    "Financial planning involves assessing "
                    "the current financial situation and "
                    "identifying current and future needs."
                ),
                "metadata": {
                    "source": "NISM-Series-X-A",
                    "page": 25
                }
            }
        ]
    }

    result = final_guardrail_node(state)

    assert result["final_response"]

    assert "NISM" in result["final_response"]