from tools.cashflow import (
    calculate_total_income,
    calculate_total_expenses,
    calculate_monthly_cashflow,
    calculate_savings_rate,
)

from audit.audit_logger import log_rule_event


def check_cashflow(
    user_id: str,
    session_id: str | None = None,
) -> dict:
    """
    Evaluate cash-flow rules and record rule evaluation events.
    """

    if session_id is None:
        session_id = f"cashflow-{user_id}"

    income = calculate_total_income(user_id)

    expenses = calculate_total_expenses(user_id)

    cashflow = calculate_monthly_cashflow(user_id)

    savings_rate = calculate_savings_rate(user_id)

    findings = []

    # ------------------------------------------------
    # Monthly cashflow rule
    # ------------------------------------------------

    if cashflow < 0:

        finding = {
            "rule": "negative_cashflow",
            "status": "critical",
            "finding": "Monthly expenses exceed monthly income.",
            "value": cashflow,
            "reason": (
                "The calculated monthly cash flow is negative."
            ),
        }

    elif cashflow == 0:

        finding = {
            "rule": "zero_cashflow",
            "status": "attention",
            "finding": "There is no monthly surplus.",
            "value": cashflow,
            "reason": (
                "Income is equal to expenses."
            ),
        }

    else:

        finding = {
            "rule": "positive_cashflow",
            "status": "healthy",
            "finding": "Monthly income exceeds monthly expenses.",
            "value": cashflow,
            "reason": (
                "The calculated monthly cash flow is positive."
            ),
        }

    findings.append(finding)

    log_rule_event(
        user_id=user_id,
        session_id=session_id,
        rule_name=finding["rule"],
        result=finding["status"],
        data={
            "value": finding["value"],
        },
    )

    # ------------------------------------------------
    # Savings rate rule
    # ------------------------------------------------

    if savings_rate < 10:

        finding = {
            "rule": "low_savings_rate",
            "status": "attention",
            "finding": "Savings rate is relatively low.",
            "value": savings_rate,
            "reason": (
                "The calculated savings rate is below 10%."
            ),
        }

        findings.append(finding)

        log_rule_event(
            user_id=user_id,
            session_id=session_id,
            rule_name=finding["rule"],
            result=finding["status"],
            data={
                "value": finding["value"],
            },
        )

    return {
        "income": income,
        "expenses": expenses,
        "cashflow": cashflow,
        "savings_rate": savings_rate,
        "findings": findings,
    }