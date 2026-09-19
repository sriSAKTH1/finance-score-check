from rules.cashflow_rules import check_cashflow
from rules.debt_rules import check_debt
from rules.emergency_rules import check_emergency_fund


def analyze_financial_rules(user_id: str) -> dict:

    cashflow = check_cashflow(user_id)

    debt = check_debt(user_id)

    emergency = check_emergency_fund(user_id)

    return {
        "cashflow": cashflow,
        "debt": debt,
        "emergency_fund": emergency
    }