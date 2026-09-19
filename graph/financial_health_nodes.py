from tools.cashflow import (
    calculate_total_income,
    calculate_total_expenses,
    calculate_monthly_cashflow,
    calculate_savings_rate,
    calculate_net_worth,
)

from tools.debt import (
    calculate_existing_emi,
    calculate_debt_burden,
)

from rules.emergency_rules import (
    calculate_emergency_coverage_months,
    check_emergency_fund,
)

from rules.investment_rules import (
    check_risk_profile,
    check_investment_horizon,
    check_investment_concentration,
    check_goal_alignment,
)

from rules.insurance_rules import evaluate_insurance
from rules.retirement_rules import evaluate_retirement
from rules.tax_rules import evaluate_tax

from context.financial_context import FinancialContext

from agents.financial_health_agent import (
    analyze_financial_health,
    build_financial_health_response,
)


def collect_financial_health_data(state):

    user_id = state["user_id"]

    context = FinancialContext()

    # --------------------------------------------------
    # FINANCIAL CONTEXT
    # --------------------------------------------------

    user = context.get_user(user_id)
    assets = context.get_assets(user_id)
    goals = context.get_goals(user_id)
    insurance = context.get_insurance(user_id)
    risk_profile = context.get_risk_profile(user_id)
    income = context.get_income(user_id)
    expenses = context.get_expenses(user_id)
    liabilities = context.get_liabilities(user_id)

    # --------------------------------------------------
    # CASH FLOW
    # --------------------------------------------------

    monthly_income = calculate_total_income(user_id)
    monthly_expenses = calculate_total_expenses(user_id)
    monthly_cashflow = calculate_monthly_cashflow(user_id)
    savings_rate = calculate_savings_rate(user_id)
    net_worth = calculate_net_worth(user_id)

    # --------------------------------------------------
    # DEBT
    # --------------------------------------------------

    existing_emi = calculate_existing_emi(user_id)
    debt_burden = calculate_debt_burden(user_id)

    # --------------------------------------------------
    # EMERGENCY FUND
    # --------------------------------------------------

    emergency_coverage = calculate_emergency_coverage_months(
        user_id
    )

    emergency_result = check_emergency_fund(
        user_id
    )

    # --------------------------------------------------
    # INVESTMENTS
    # --------------------------------------------------

    total_investments = 0.0
    largest_investment = 0.0

    if assets is not None:

        investment_values = [
            float(getattr(assets, "mutual_funds", 0) or 0),
            float(getattr(assets, "gold", 0) or 0),
        ]

        investment_values = [
            value
            for value in investment_values
            if value > 0
        ]

        if investment_values:
            total_investments = sum(investment_values)
            largest_investment = max(investment_values)

    risk_category = "Moderate"

    if isinstance(risk_profile, dict):
        risk_category = risk_profile.get(
            "category",
            "Moderate"
        )

    investment_results = {
        "risk_profile": check_risk_profile(
            risk_category
        ),
    }

    # --------------------------------------------------
    # INVESTMENT HORIZON / GOAL HORIZON
    # --------------------------------------------------

    goal_horizon = 0

    if isinstance(goals, list) and goals:

        horizons = []

        for goal in goals:

            if isinstance(goal, dict):

                years = goal.get("years")

                if isinstance(years, (int, float)):
                    horizons.append(int(years))

        if horizons:
            goal_horizon = min(horizons)

    if goal_horizon > 0:

        investment_results[
            "investment_horizon"
        ] = check_investment_horizon(
            goal_horizon
        )

        investment_results[
            "goal_alignment"
        ] = check_goal_alignment(
            goal_horizon,
            goal_horizon
        )

    investment_results[
        "investment_concentration"
    ] = check_investment_concentration(
        total_investments,
        largest_investment
    )

    # --------------------------------------------------
    # INSURANCE
    # --------------------------------------------------

    existing_life_cover = 0.0
    health_cover = 0.0
    dependents = 0

    if insurance is not None:

        existing_life_cover = float(
            getattr(
                insurance,
                "life_cover",
                0
            ) or 0
        )

        health_cover = float(
            getattr(
                insurance,
                "health_cover",
                0
            ) or 0
        )

    if user is not None:

        profile = getattr(
            user,
            "profile",
            None
        )

        if profile is not None:
            dependents = int(
                getattr(
                    profile,
                    "dependents",
                    0
                ) or 0
            )

    # Existing project doesn't expose a required-cover
    # calculation here, so use existing life cover as the
    # required-cover input until that calculation exists.
    required_life_cover = existing_life_cover

    insurance_result = evaluate_insurance(
        required_life_cover=required_life_cover,
        existing_life_cover=existing_life_cover,
        health_cover=health_cover,
        dependents=dependents,
    )

    # --------------------------------------------------
    # RETIREMENT
    # --------------------------------------------------

    retirement_result = {}

    # Existing retirement rule requires calculated
    # corpus values. We only call it when those values
    # are available from the financial context.
    if isinstance(user, dict):

        profile = user.get(
            "profile",
            {}
        )

        current_age = profile.get(
            "age"
        )

        if isinstance(current_age, (int, float)):

            retirement_age = 60

            years_to_retirement = (
                retirement_age - int(current_age)
            )

            if years_to_retirement > 0:

                retirement_result = {
                    "status": "INFO",
                    "message": (
                        "Retirement inputs available; "
                        "detailed corpus evaluation "
                        "requires retirement assumptions."
                    )
                }

    # --------------------------------------------------
    # TAX
    # --------------------------------------------------

    tax_result = {
        "status": "INFO",
        "message": (
            "Tax assessment requires taxable income, "
            "deductions, tax rate and estimated tax."
        )
    }

    # --------------------------------------------------
    # RETURN COMPLETE DATA
    # --------------------------------------------------

    return {
        "financial_health_data": {

            "cashflow": {
                "monthly_income": monthly_income,
                "monthly_expenses": monthly_expenses,
                "monthly_cashflow": monthly_cashflow,
                "savings_rate": savings_rate,
                "net_worth": net_worth,
            },

            "debt": {
                "existing_emi": existing_emi,
                "debt_burden": debt_burden,
            },

            "emergency_fund": {
                "coverage_months": emergency_coverage,
                "result": emergency_result,
            },

            "investments": investment_results,

            "insurance": insurance_result,

            "retirement": retirement_result,

            "tax": tax_result,

            "assets": assets,

            "goals": goals,

            "risk_profile": risk_profile,

            "income": income,

            "expenses": expenses,

            "liabilities": liabilities,
        }
    }


def financial_health_analysis_node(state):

    financial_health_data = state.get(
        "financial_health_data",
        {}
    )

    financial_context = state.get(
        "financial_context",
        {}
    )

    result = analyze_financial_health(
        financial_context=financial_context,
        financial_health_data=financial_health_data,
    )

    response = build_financial_health_response(
        result
    )

    return {
        "financial_health": result,
        "analysis": result,
        "final_response": response,
    }