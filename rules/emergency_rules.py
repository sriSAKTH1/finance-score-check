from context.financial_context import FinancialContext
from tools.cashflow import calculate_total_expenses


context = FinancialContext()


def calculate_emergency_coverage_months(
    user_id: str
) -> float:

    assets = context.get_assets(user_id)

    monthly_expenses = calculate_total_expenses(user_id)

    if monthly_expenses == 0:
        return 0.0

    emergency_savings = assets.bank_savings

    return emergency_savings / monthly_expenses


def check_emergency_fund(user_id: str) -> dict:

    monthly_expenses = calculate_total_expenses(user_id)

    assets = context.get_assets(user_id)

    emergency_savings = assets.bank_savings

    coverage_months = calculate_emergency_coverage_months(
        user_id
    )

    findings = []

    if coverage_months < 3:
        status = "attention"
        finding = (
            "Emergency savings cover less than "
            "three months of expenses."
        )

    else:
        status = "informational"
        finding = (
            "Emergency savings cover at least "
            "three months of expenses."
        )

    findings.append({
        "rule": "emergency_fund_coverage",
        "status": status,
        "finding": finding,
        "value": coverage_months,
        "reason": (
            "Coverage is calculated using bank savings "
            "divided by monthly expenses."
        )
    })

    return {
        "emergency_savings": emergency_savings,
        "monthly_expenses": monthly_expenses,
        "coverage_months": coverage_months,
        "findings": findings
    }