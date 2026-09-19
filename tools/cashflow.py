from context.financial_context import FinancialContext


context = FinancialContext()


def calculate_total_income(user_id: str) -> float:
    income = context.get_income(user_id)

    return (
        income.monthly_salary
        + income.other_income
    )


def calculate_total_expenses(user_id: str) -> float:
    expenses = context.get_expenses(user_id)

    return (
        expenses.rent
        + expenses.food
        + expenses.transport
        + expenses.utilities
        + expenses.education
        + expenses.other
    )


def calculate_monthly_cashflow(user_id: str) -> float:
    income = calculate_total_income(user_id)
    expenses = calculate_total_expenses(user_id)

    return income - expenses


def calculate_savings_rate(user_id: str) -> float:
    income = calculate_total_income(user_id)
    savings = calculate_monthly_cashflow(user_id)

    if income == 0:
        return 0.0

    return (savings / income) * 100


def calculate_net_worth(user_id: str) -> float:
    assets = context.get_assets(user_id)
    liabilities = context.get_liabilities(user_id)

    total_assets = (
        assets.bank_savings
        + assets.mutual_funds
        + assets.gold
    )

    total_liabilities = 0

    if liabilities.home_loan:
        total_liabilities += liabilities.home_loan.outstanding

    return total_assets - total_liabilities