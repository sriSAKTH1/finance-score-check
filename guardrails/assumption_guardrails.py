from typing import Any


def check_return_assumption(
    annual_return: float,
) -> dict[str, Any]:

    warnings = []

    if annual_return > 30:
        warnings.append(
            "The assumed annual return is unusually high. "
            "This should be treated as a hypothetical scenario, "
            "not a guaranteed or expected return."
        )

    elif annual_return > 15:
        warnings.append(
            "The assumed annual return is relatively high. "
            "Actual investment returns can vary."
        )

    return {
        "valid": True,
        "warnings": warnings,
    }


def check_interest_rate(
    interest_rate: float,
) -> dict[str, Any]:

    warnings = []

    if interest_rate > 30:
        warnings.append(
            "The assumed interest rate is very high. "
            "Verify the actual loan terms before making a decision."
        )

    elif interest_rate > 20:
        warnings.append(
            "The assumed interest rate is high. "
            "Check the lender's actual rate and total borrowing cost."
        )

    return {
        "valid": True,
        "warnings": warnings,
    }


def check_inflation_assumption(
    inflation_rate: float,
) -> dict[str, Any]:

    warnings = []

    if inflation_rate > 15:
        warnings.append(
            "The assumed inflation rate is unusually high. "
            "Review the assumption used for this scenario."
        )

    return {
        "valid": True,
        "warnings": warnings,
    }


def evaluate_assumptions(
    assumptions: dict[str, Any],
) -> dict[str, Any]:

    warnings = []

    annual_return = assumptions.get("annual_return")

    if annual_return is not None:
        result = check_return_assumption(
            float(annual_return)
        )
        warnings.extend(result["warnings"])

    interest_rate = assumptions.get("interest_rate")

    if interest_rate is not None:
        result = check_interest_rate(
            float(interest_rate)
        )
        warnings.extend(result["warnings"])

    inflation_rate = assumptions.get("inflation_rate")

    if inflation_rate is not None:
        result = check_inflation_assumption(
            float(inflation_rate)
        )
        warnings.extend(result["warnings"])

    return {
        "valid": True,
        "warnings": warnings,
    }