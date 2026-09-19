from typing import Any


REQUIRED_FIELDS = {
    "loan": [
        "income",
        "expenses",
        "liabilities",
    ],
    "investment": [
        "income",
        "expenses",
        "risk_profile",
    ],
    "goal": [
        "income",
        "expenses",
        "goals",
    ],
    "retirement": [
        "income",
        "expenses",
        "risk_profile",
    ],
    "financial_health": [
        "income",
        "expenses",
        "assets",
        "liabilities",
    ],
}


def check_missing_fields(
    financial_context: dict[str, Any],
    required_fields: list[str],
) -> list[str]:
    """
    Return required financial fields that are missing.
    """

    missing = []

    for field in required_fields:
        value = financial_context.get(field)

        if value is None:
            missing.append(field)

        elif isinstance(value, (dict, list)) and len(value) == 0:
            missing.append(field)

    return missing


def validate_required_data(
    scenario_type: str,
    financial_context: dict[str, Any],
) -> dict[str, Any]:
    """
    Check whether enough financial information exists
    for the requested analysis.
    """

    required_fields = REQUIRED_FIELDS.get(
        scenario_type,
        [],
    )

    missing = check_missing_fields(
        financial_context,
        required_fields,
    )

    return {
        "valid": len(missing) == 0,
        "missing": missing,
        "required": required_fields,
    }


def build_missing_data_message(
    missing_fields: list[str],
) -> str:
    """
    Build a clear user-facing message.
    """

    if not missing_fields:
        return ""

    readable = ", ".join(
        field.replace("_", " ")
        for field in missing_fields
    )

    return (
        "I need some additional financial information "
        f"before I can complete this analysis: {readable}."
    )


def apply_missing_data_guardrail(
    scenario_type: str,
    financial_context: dict[str, Any],
) -> dict[str, Any]:
    """
    Apply the missing-data safety check.
    """

    result = validate_required_data(
        scenario_type,
        financial_context,
    )

    if result["valid"]:
        return {
            "allowed": True,
            "missing": [],
            "message": None,
        }

    return {
        "allowed": False,
        "missing": result["missing"],
        "message": build_missing_data_message(
            result["missing"]
        ),
    }