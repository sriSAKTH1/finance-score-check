from schemas.scenario import (
    ScenarioInput,
    ScenarioResult,
    ScenarioComparison,
)

from tools.investment import (
    calculate_total_investment_value,
)

from tools.debt import (
    calculate_emi,
    calculate_post_loan_cashflow,
)

from tools.goals import (
    future_value_with_monthly_contribution,
    required_future_value,
)

from tools.retirement import (
    calculate_future_expense,
    calculate_retirement_corpus,
    calculate_future_value,
)

from scenarios.comparator import compare_scenarios


# ============================================================
# INVESTMENT SCENARIO
# ============================================================

def run_investment_scenario(
    current_investment: float,
    monthly_investment: float,
    annual_return: float,
    years: int,
    scenario: ScenarioInput,
):
    """
    Compare the current investment plan
    against an alternative scenario.
    """

    scenario_monthly_investment = (
        scenario.monthly_investment
        if scenario.monthly_investment is not None
        else monthly_investment
    )

    scenario_current_investment = (
        scenario.current_investment
        if scenario.current_investment is not None
        else current_investment
    )

    scenario_return = (
        scenario.annual_return
        if scenario.annual_return is not None
        else annual_return
    )

    scenario_years = (
        scenario.years
        if scenario.years is not None
        else years
    )

    # -----------------------------
    # BASELINE
    # -----------------------------

    baseline_value = calculate_total_investment_value(
        current_amount=current_investment,
        monthly_investment=monthly_investment,
        annual_return=annual_return,
        years=years,
    )

    baseline_contributions = (
        current_investment
        + monthly_investment * years * 12
    )

    baseline = ScenarioResult(
        scenario_name="Baseline",
        metrics={
            "projected_value": baseline_value,
            "total_contributions": baseline_contributions,
        },
        assumptions={
            "annual_return": annual_return,
            "years": years,
        },
    )

    # -----------------------------
    # SCENARIO
    # -----------------------------

    scenario_value = calculate_total_investment_value(
        current_amount=scenario_current_investment,
        monthly_investment=scenario_monthly_investment,
        annual_return=scenario_return,
        years=scenario_years,
    )

    scenario_contributions = (
        scenario_current_investment
        + scenario_monthly_investment
        * scenario_years
        * 12
    )

    alternative = ScenarioResult(
        scenario_name=scenario.name,
        metrics={
            "projected_value": scenario_value,
            "total_contributions": scenario_contributions,
        },
        assumptions={
            "annual_return": scenario_return,
            "years": scenario_years,
        },
    )

    return compare_scenarios(
        baseline=baseline,
        scenario=alternative,
    )


# ============================================================
# LOAN SCENARIO
# ============================================================

def run_loan_scenario(
    user_id: str,
    loan_amount: float,
    interest_rate: float,
    tenure_months: int,
    current_monthly_cashflow: float,
    scenario_name: str = "New Loan",
):
    """
    Compare current monthly cash flow with
    monthly cash flow after taking a new loan.
    """

    # -----------------------------
    # LOAN EMI
    # -----------------------------

    new_emi = calculate_emi(
        principal=loan_amount,
        annual_rate=interest_rate,
        tenure_months=tenure_months,
    )

    # -----------------------------
    # BASELINE
    # -----------------------------

    baseline = ScenarioResult(
        scenario_name="Current Situation",
        metrics={
            "monthly_cashflow": current_monthly_cashflow,
            "new_loan_emi": 0.0,
        },
        assumptions={},
    )

    # -----------------------------
    # SCENARIO
    # -----------------------------

    post_loan_cashflow = calculate_post_loan_cashflow(
        user_id=user_id,
        new_loan_emi=new_emi,
    )

    scenario = ScenarioResult(
        scenario_name=scenario_name,
        metrics={
            "monthly_cashflow": post_loan_cashflow,
            "new_loan_emi": new_emi,
        },
        assumptions={
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
        },
    )

    # -----------------------------
    # COMPARISON
    # -----------------------------

    return compare_scenarios(
        baseline=baseline,
        scenario=scenario,
    )


# ============================================================
# GOAL SCENARIO
# ============================================================

def run_goal_scenario(
    current_corpus: float,
    monthly_contribution: float,
    target_amount: float,
    annual_return: float,
    inflation_rate: float,
    years: int,
    scenario: ScenarioInput,
):
    """
    Compare a baseline financial goal plan
    with an alternative scenario.
    """

    scenario_corpus = (
        scenario.current_investment
        if scenario.current_investment is not None
        else current_corpus
    )

    scenario_monthly = (
        scenario.monthly_investment
        if scenario.monthly_investment is not None
        else monthly_contribution
    )

    scenario_return = (
        scenario.annual_return
        if scenario.annual_return is not None
        else annual_return
    )

    scenario_years = (
        scenario.years
        if scenario.years is not None
        else years
    )

    # -----------------------------
    # INFLATION-ADJUSTED TARGET
    # -----------------------------

    future_target = required_future_value(
        current_goal_amount=target_amount,
        inflation_rate=inflation_rate,
        years=years,
    )

    # -----------------------------
    # BASELINE
    # -----------------------------

    baseline_projected = future_value_with_monthly_contribution(
        current_corpus=current_corpus,
        monthly_contribution=monthly_contribution,
        annual_return=annual_return,
        years=years,
    )

    baseline_gap = future_target - baseline_projected

    baseline = ScenarioResult(
        scenario_name="Current Goal Plan",
        metrics={
            "projected_corpus": baseline_projected,
            "target_amount": future_target,
            "goal_gap": baseline_gap,
        },
        assumptions={
            "annual_return": annual_return,
            "inflation_rate": inflation_rate,
            "years": years,
        },
    )

    # -----------------------------
    # ALTERNATIVE SCENARIO
    # -----------------------------

    scenario_projected = future_value_with_monthly_contribution(
        current_corpus=scenario_corpus,
        monthly_contribution=scenario_monthly,
        annual_return=scenario_return,
        years=scenario_years,
    )

    scenario_gap = future_target - scenario_projected

    alternative = ScenarioResult(
        scenario_name=scenario.name,
        metrics={
            "projected_corpus": scenario_projected,
            "target_amount": future_target,
            "goal_gap": scenario_gap,
        },
        assumptions={
            "annual_return": scenario_return,
            "inflation_rate": inflation_rate,
            "years": scenario_years,
        },
    )

    return compare_scenarios(
        baseline=baseline,
        scenario=alternative,
    )


# ============================================================
# RETIREMENT SCENARIO
# ============================================================

def run_retirement_scenario(
    current_age: int,
    retirement_age: int,
    current_monthly_expense: float,
    inflation_rate: float,
    years_in_retirement: int,
    current_corpus: float,
    annual_return: float,
    scenario: ScenarioInput,
):
    """
    Compare the baseline retirement plan
    with an alternative retirement scenario.
    """

    # -----------------------------
    # BASELINE
    # -----------------------------

    baseline_years = retirement_age - current_age

    baseline_future_expense = calculate_future_expense(
        current_monthly_expense=current_monthly_expense,
        inflation_rate=inflation_rate,
        years=baseline_years,
    )

    baseline_required_corpus = calculate_retirement_corpus(
        future_monthly_expense=baseline_future_expense,
        years_in_retirement=years_in_retirement,
        annual_return=annual_return,
    )

    baseline_projected_corpus = calculate_future_value(
        current_amount=current_corpus,
        annual_return=annual_return,
        years=baseline_years,
    )

    baseline_gap = (
        baseline_required_corpus
        - baseline_projected_corpus
    )

    baseline = ScenarioResult(
        scenario_name="Current Retirement Plan",
        metrics={
            "years_to_retirement": baseline_years,
            "future_monthly_expense": baseline_future_expense,
            "required_corpus": baseline_required_corpus,
            "projected_corpus": baseline_projected_corpus,
            "retirement_gap": baseline_gap,
        },
        assumptions={
            "annual_return": annual_return,
            "inflation_rate": inflation_rate,
        },
    )

    # -----------------------------
    # ALTERNATIVE SCENARIO
    # -----------------------------

    scenario_retirement_age = (
        scenario.retirement_age
        if scenario.retirement_age is not None
        else retirement_age
    )

    scenario_years = (
        scenario_retirement_age - current_age
    )

    scenario_return = (
        scenario.annual_return
        if scenario.annual_return is not None
        else annual_return
    )

    scenario_future_expense = calculate_future_expense(
        current_monthly_expense=current_monthly_expense,
        inflation_rate=inflation_rate,
        years=scenario_years,
    )

    scenario_required_corpus = calculate_retirement_corpus(
        future_monthly_expense=scenario_future_expense,
        years_in_retirement=years_in_retirement,
        annual_return=scenario_return,
    )

    scenario_projected_corpus = calculate_future_value(
        current_amount=current_corpus,
        annual_return=scenario_return,
        years=scenario_years,
    )

    scenario_gap = (
        scenario_required_corpus
        - scenario_projected_corpus
    )

    alternative = ScenarioResult(
        scenario_name=scenario.name,
        metrics={
            "years_to_retirement": scenario_years,
            "future_monthly_expense": scenario_future_expense,
            "required_corpus": scenario_required_corpus,
            "projected_corpus": scenario_projected_corpus,
            "retirement_gap": scenario_gap,
        },
        assumptions={
            "annual_return": scenario_return,
            "inflation_rate": inflation_rate,
        },
    )

    # -----------------------------
    # COMPARISON
    # -----------------------------

    return compare_scenarios(
        baseline=baseline,
        scenario=alternative,
    )