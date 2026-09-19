from typing import Any


def validate_non_negative(
    value: float,
    field_name: str,
) -> dict[str, Any]:

    if value < 0:
        return {
            "valid": False,
            "field": field_name,
            "error": f"{field_name} cannot be negative.",
        }

    return {
        "valid": True,
        "field": field_name,
    }


def validate_positive(
    value: float,
    field_name: str,
) -> dict[str, Any]:

    if value <= 0:
        return {
            "valid": False,
            "field": field_name,
            "error": f"{field_name} must be greater than zero.",
        }

    return {
        "valid": True,
        "field": field_name,
    }


def validate_percentage(
    value: float,
    field_name: str,
    maximum: float | None = None,
) -> dict[str, Any]:

    if value < 0:
        return {
            "valid": False,
            "field": field_name,
            "error": f"{field_name} cannot be negative.",
        }

    if maximum is not None and value > maximum:
        return {
            "valid": False,
            "field": field_name,
            "error": (
                f"{field_name} exceeds the configured "
                f"maximum of {maximum}%."
            ),
        }

    return {
        "valid": True,
        "field": field_name,
    }


def validate_age(
    age: int,
    field_name: str = "Age",
) -> dict[str, Any]:

    if age <= 0:
        return {
            "valid": False,
            "field": field_name,
            "error": f"{field_name} must be greater than zero.",
        }

    if age > 120:
        return {
            "valid": False,
            "field": field_name,
            "error": f"{field_name} is outside the supported range.",
        }

    return {
        "valid": True,
        "field": field_name,
    }


def validate_years(
    years: int,
    field_name: str = "Years",
) -> dict[str, Any]:

    if years <= 0:
        return {
            "valid": False,
            "field": field_name,
            "error": f"{field_name} must be greater than zero.",
        }

    return {
        "valid": True,
        "field": field_name,
    }


def validate_financial_inputs(
    inputs: dict[str, Any],
) -> dict[str, Any]:

    errors = []

    non_negative_fields = [
        "monthly_investment",
        "current_investment",
        "monthly_expense",
        "loan_amount",
        "current_corpus",
    ]

    for field in non_negative_fields:

        value = inputs.get(field)

        if value is None:
            continue

        result = validate_non_negative(
            float(value),
            field.replace("_", " ").title(),
        )

        if not result["valid"]:
            errors.append(result["error"])

    percentage_fields = [
        "annual_return",
        "interest_rate",
        "inflation_rate",
    ]

    for field in percentage_fields:

        value = inputs.get(field)

        if value is None:
            continue

        result = validate_percentage(
            float(value),
            field.replace("_", " ").title(),
        )

        if not result["valid"]:
            errors.append(result["error"])

    for field in ["years", "tenure_months", "retirement_age"]:

        value = inputs.get(field)

        if value is None:
            continue

        result = validate_positive(
            float(value),
            field.replace("_", " ").title(),
        )

        if not result["valid"]:
            errors.append(result["error"])

    if errors:

        return {
            "valid": False,
            "errors": errors,
        }

    return {
        "valid": True,
        "errors": [],
    }