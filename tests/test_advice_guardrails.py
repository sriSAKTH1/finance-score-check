from guardrails.advice_guardrails import (
    find_unsafe_phrases,
    validate_advice_context,
    guard_advice,
)


def test_safe_explanation():
    text = (
        "Based on the assumed return, the projected value "
        "may increase. Actual returns can vary."
    )

    result = find_unsafe_phrases(text)

    assert result == []


def test_guaranteed_return():
    text = "This investment gives guaranteed returns."

    result = find_unsafe_phrases(text)

    assert "guaranteed returns" in result


def test_risk_free():
    text = "This is a completely risk-free investment."

    result = find_unsafe_phrases(text)

    assert "risk-free" in result


def test_imperative_advice():
    text = "You should buy this investment immediately."

    result = find_unsafe_phrases(text)

    assert "you should buy" in result


def test_complete_context():
    context = {
        "risk_profile": {"category": "Moderate"},
        "goals": [{"name": "Education"}],
        "income": {"monthly_salary": 75000},
        "expenses": {"rent": 15000},
    }

    result = validate_advice_context(context)

    assert result["valid"] is True
    assert result["missing"] == []


def test_missing_context():
    context = {
        "income": {"monthly_salary": 75000},
        "expenses": {"rent": 15000},
    }

    result = validate_advice_context(context)

    assert result["valid"] is False
    assert "risk profile" in result["missing"]


def test_guard_advice():
    text = "This investment has guaranteed returns."

    context = {
        "risk_profile": {"category": "Moderate"},
        "goals": [{"name": "Education"}],
        "income": {"monthly_salary": 75000},
        "expenses": {"rent": 15000},
    }

    result = guard_advice(text, context)

    assert result["safe"] is False
    assert len(result["warnings"]) > 0