from guardrails.missing_data_guardrail import (
    check_missing_fields,
    validate_required_data,
    build_missing_data_message,
    apply_missing_data_guardrail,
)


def test_no_missing_fields():

    context = {
        "income": {"monthly_salary": 75000},
        "expenses": {"rent": 15000},
        "liabilities": {
            "home_loan": {
                "outstanding": 1200000
            }
        },
    }

    result = check_missing_fields(
        context,
        ["income", "expenses", "liabilities"],
    )

    assert result == []


def test_missing_income():

    context = {
        "expenses": {"rent": 15000},
        "liabilities": {},
    }

    result = check_missing_fields(
        context,
        ["income", "expenses", "liabilities"],
    )

    assert "income" in result
    assert "liabilities" in result


def test_loan_required_data():

    context = {
        "income": {"monthly_salary": 75000},
        "expenses": {"rent": 15000},
        "liabilities": {
            "home_loan": {
                "emi": 15000
            }
        },
    }

    result = validate_required_data(
        "loan",
        context,
    )

    assert result["valid"] is True
    assert result["missing"] == []


def test_investment_missing_risk_profile():

    context = {
        "income": {"monthly_salary": 75000},
        "expenses": {"rent": 15000},
    }

    result = validate_required_data(
        "investment",
        context,
    )

    assert result["valid"] is False
    assert "risk_profile" in result["missing"]


def test_missing_data_message():

    message = build_missing_data_message(
        ["income", "risk_profile"]
    )

    assert "income" in message
    assert "risk profile" in message


def test_guardrail_allows_complete_data():

    context = {
        "income": {"monthly_salary": 75000},
        "expenses": {"rent": 15000},
        "risk_profile": {"category": "Moderate"},
    }

    result = apply_missing_data_guardrail(
        "investment",
        context,
    )

    assert result["allowed"] is True
    assert result["missing"] == []


def test_guardrail_blocks_incomplete_data():

    context = {
        "income": {"monthly_salary": 75000},
    }

    result = apply_missing_data_guardrail(
        "investment",
        context,
    )

    assert result["allowed"] is False
    assert "expenses" in result["missing"]
    assert "risk_profile" in result["missing"]
    assert result["message"] is not None