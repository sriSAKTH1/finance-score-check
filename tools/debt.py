from context.financial_context import FinancialContext
from tools.cashflow import (
    calculate_total_income,
    calculate_total_expenses,
)


context = FinancialContext()


def calculate_emi(
    principal: float,
    annual_rate: float,
    tenure_months: int,
) -> float:
    """
    Calculate monthly EMI using reducing-balance method.
    """

    if principal <= 0:
        raise ValueError("Principal must be greater than 0")

    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative")

    if tenure_months <= 0:
        raise ValueError("Tenure must be greater than 0")

    monthly_rate = annual_rate / 12 / 100

    # Zero-interest case
    if monthly_rate == 0:
        return principal / tenure_months

    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** tenure_months
        / ((1 + monthly_rate) ** tenure_months - 1)
    )

    return emi


def calculate_total_repayment(
    principal: float,
    annual_rate: float,
    tenure_months: int,
) -> float:

    emi = calculate_emi(
        principal,
        annual_rate,
        tenure_months,
    )

    return emi * tenure_months


def calculate_total_interest(
    principal: float,
    annual_rate: float,
    tenure_months: int,
) -> float:

    total_repayment = calculate_total_repayment(
        principal,
        annual_rate,
        tenure_months,
    )

    return total_repayment - principal


def calculate_existing_emi(user_id: str) -> float:

    liabilities = context.get_liabilities(user_id)

    total_emi = 0.0

    if liabilities.home_loan:
        total_emi += liabilities.home_loan.emi

    return total_emi


def calculate_debt_burden(user_id: str) -> float:

    income = calculate_total_income(user_id)

    if income == 0:
        return 0.0

    existing_emi = calculate_existing_emi(user_id)

    return (existing_emi / income) * 100


def calculate_post_loan_cashflow(
    user_id: str,
    new_loan_emi: float,
) -> float:

    current_cashflow = (
        calculate_total_income(user_id)
        - calculate_total_expenses(user_id)
    )

    return current_cashflow - new_loan_emi