def check_risk_profile(risk_category: str):
    """
    Check whether an investment approach should consider
    the user's recorded risk profile.
    """

    if not risk_category:
        return {
            "rule": "risk_profile",
            "status": "attention",
            "message": "Risk profile is not available.",
        }

    return {
        "rule": "risk_profile",
        "status": "informational",
        "message": f"Recorded risk profile: {risk_category}.",
    }


def check_investment_horizon(years: int):
    """
    Classify the investment time horizon.
    These are FinSource application rules, not NISM thresholds.
    """

    if years <= 0:
        return {
            "rule": "investment_horizon",
            "status": "critical",
            "message": "Investment horizon must be greater than zero.",
        }

    if years < 3:
        status = "short_term"
    elif years <= 7:
        status = "medium_term"
    else:
        status = "long_term"

    return {
        "rule": "investment_horizon",
        "status": "informational",
        "message": f"Investment horizon classified as {status}.",
    }


def check_investment_concentration(
    total_investments: float,
    largest_investment: float,
):
    """
    Detect possible concentration in one investment.

    This is a configurable FinSource rule and is not a universal
    regulatory threshold.
    """

    if total_investments <= 0:
        return {
            "rule": "investment_concentration",
            "status": "attention",
            "message": "No investment value is available.",
        }

    concentration = (
        largest_investment / total_investments
    ) * 100

    return {
        "rule": "investment_concentration",
        "status": "informational",
        "concentration_percent": round(concentration, 2),
        "message": (
            f"Largest investment represents "
            f"{concentration:.2f}% of total investments."
        ),
    }


def check_goal_alignment(
    investment_horizon: int,
    goal_horizon: int,
):
    """
    Compare investment horizon with financial goal horizon.
    """

    if investment_horizon < goal_horizon:
        return {
            "rule": "goal_alignment",
            "status": "attention",
            "message": (
                "Investment horizon is shorter than the "
                "financial goal horizon."
            ),
        }

    return {
        "rule": "goal_alignment",
        "status": "informational",
        "message": "Investment horizon covers the goal horizon.",
    }