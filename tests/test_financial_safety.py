from guardrails.input_guardrails import validate_financial_inputs
from guardrails.assumption_guardrails import evaluate_assumptions
from guardrails.advice_guardrails import guard_advice
from guardrails.nism_grounding_guardrail import (
    validate_nism_evidence,
)
from guardrails.missing_data_guardrail import (
    apply_missing_data_guardrail,
)
from guardrails.output_safety_guardrail import (
    sanitize_output,
)


def test_negative_investment_blocked():

    result = validate_financial_inputs(
        {
            "monthly_investment": -5000,
        }
    )

    assert result["valid"] is False


def test_zero_years_blocked():

    result = validate_financial_inputs(
        {
            "years": 0,
        }
    )

    assert result["valid"] is False


def test_unrealistic_return_warning():

    result = evaluate_assumptions(
        {
            "annual_return": 100,
        }
    )

    assert result["valid"] is True
    assert len(result["warnings"]) > 0


def test_high_interest_warning():

    result = evaluate_assumptions(
        {
            "interest_rate": 50,
        }
    )

    assert result["valid"] is True
    assert len(result["warnings"]) > 0


def test_missing_investment_context():

    context = {
        "income": {
            "monthly_salary": 75000
        },
        "expenses": {
            "rent": 15000
        },
    }

    result = apply_missing_data_guardrail(
        "investment",
        context,
    )

    assert result["allowed"] is False
    assert "risk_profile" in result["missing"]


def test_safe_financial_advice():

    context = {
        "risk_profile": {
            "category": "Moderate"
        },
        "goals": [
            {
                "name": "Child Education"
            }
        ],
        "income": {
            "monthly_salary": 75000
        },
        "expenses": {
            "rent": 15000
        },
    }

    result = guard_advice(
        (
            "The projected value is based on the "
            "assumed return. Actual returns can vary."
        ),
        context,
    )

    assert result["unsafe_phrases"] == []


def test_unsafe_financial_advice():

    context = {
        "risk_profile": {
            "category": "Moderate"
        },
        "goals": [
            {
                "name": "Child Education"
            }
        ],
        "income": {
            "monthly_salary": 75000
        },
        "expenses": {
            "rent": 15000
        },
    }

    result = guard_advice(
        "This investment gives guaranteed returns.",
        context,
    )

    assert result["safe"] is False


def test_missing_nism_evidence():

    result = validate_nism_evidence([])

    assert result["grounded"] is False
    assert result["warning"] is not None


def test_valid_nism_evidence():

    rag_results = [
        {
            "text": "Borrowing uses future income.",
            "metadata": {
                "source": "NISM-Series-X-A",
                "page": 71,
            },
        }
    ]

    result = validate_nism_evidence(
        rag_results
    )

    assert result["grounded"] is True


def test_unsafe_final_output_blocked():

    result = sanitize_output(
        (
            "You must invest all your savings "
            "because this investment has "
            "guaranteed returns."
        )
    )

    assert result["allowed"] is False
    assert result["response"] is None


def test_safe_final_output_allowed():

    result = sanitize_output(
        (
            "The projected corpus is based on "
            "the assumptions provided. Actual "
            "returns may vary."
        )
    )

    assert result["allowed"] is True
    assert result["response"] is not None