from tools.debt import (
    calculate_existing_emi,
    calculate_debt_burden,
)

from audit.audit_logger import log_rule_event


def check_debt(
    user_id: str,
    session_id: str | None = None,
) -> dict:
    """
    Evaluate debt rules and record rule evaluation events.
    """

    if session_id is None:
        session_id = f"debt-{user_id}"

    existing_emi = calculate_existing_emi(user_id)

    debt_burden = calculate_debt_burden(user_id)

    findings = []

    # ------------------------------------------------
    # Existing debt burden rule
    # ------------------------------------------------

    if debt_burden >= 50:

        status = "critical"

        finding = (
            "Existing EMI burden is high relative to income."
        )

    elif debt_burden >= 40:

        status = "attention"

        finding = (
            "Existing EMI burden requires careful assessment."
        )

    else:

        status = "informational"

        finding = (
            "Existing EMI burden is below the configured "
            "attention threshold."
        )

    rule_finding = {
        "rule": "existing_debt_burden",
        "status": status,
        "finding": finding,
        "value": debt_burden,
        "reason": (
            "Debt burden is calculated as existing EMI "
            "divided by monthly income."
        ),
    }

    findings.append(rule_finding)

    log_rule_event(
        user_id=user_id,
        session_id=session_id,
        rule_name=rule_finding["rule"],
        result=rule_finding["status"],
        data={
            "value": rule_finding["value"],
        },
    )

    return {
        "existing_emi": existing_emi,
        "debt_burden": debt_burden,
        "findings": findings,
    }