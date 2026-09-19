from context.financial_context import FinancialContext

from agents.supervisor import classify_intent
from agents.loan_parser import extract_loan_details

from agents.goal_agent import analyze_goal
from agents.cashflow_agent import analyze_cashflow
from agents.investment_agent import analyze_investment
from agents.protection_agent import analyze_protection
from agents.retirement_agent import analyze_retirement
from agents.tax_agent import analyze_tax
from agents.financial_health_agent import analyze_financial_health

from agents.scenario_agent import (
    analyze_investment_scenario,
    analyze_loan_scenario,
    analyze_goal_scenario,
    analyze_retirement_scenario,
)

from graph.financial_health_nodes import (
    collect_financial_health_data,
    financial_health_analysis_node,
)

from graph.state import FinancialState


context = FinancialContext()


# ============================================================
# LOAD FINANCIAL CONTEXT
# ============================================================

def load_financial_context(state):

    user_id = state["user_id"]

    user = context.get_user(user_id)

    return {
        "financial_context": user.model_dump()
    }


# ============================================================
# SUPERVISOR
# ============================================================

def supervisor_node(state):

    user_message = state["user_message"]

    last_intent = state.get("last_intent")

    message = user_message.lower()

    # ========================================================
    # EXPLICIT SCENARIO DETECTION
    # ========================================================
    #
    # This must happen before normal intent classification.
    #
    # Examples:
    #
    # "What if I invest 10000?"
    # "What if I take a loan of 50000?"
    # "What if I retire at 50?"
    #
    # All of these are SCENARIO questions.
    #

    scenario_phrases = [
        "what if",
        "what happens if",
        "if i",
        "instead",
        "increase",
        "decrease",
        "raise",
        "lower",
        "change",
    ]

    if any(
        phrase in message
        for phrase in scenario_phrases
    ):

        return {
            "intent": "SCENARIO"
        }

    # ========================================================
    # FOLLOW-UP SCENARIO
    # ========================================================

    follow_up_words = [
        "it",
        "that",
        "this",
        "more",
        "less",
    ]

    is_follow_up = any(
        word in message
        for word in follow_up_words
    )

    if (
        is_follow_up
        and last_intent == "SCENARIO"
    ):

        return {
            "intent": "SCENARIO"
        }

    # ========================================================
    # NORMAL SUPERVISOR
    # ========================================================

    intent = classify_intent(
        user_message
    )

    return {
        "intent": intent
    }


# ============================================================
# LOAN EXTRACTION
# ============================================================

def extract_loan_node(state):

    user_message = state["user_message"]

    loan_request = extract_loan_details(
        user_message
    )

    missing_information = []

    if loan_request.loan_amount is None:
        missing_information.append("loan amount")

    if loan_request.interest_rate is None:
        missing_information.append("interest rate")

    if loan_request.tenure_months is None:
        missing_information.append("loan tenure")

    if missing_information:

        missing_text = ", ".join(
            missing_information
        )

        response = (
            "I need the following information "
            "before I can calculate the loan impact: "
            f"{missing_text}."
        )

        return {
            "loan_request": loan_request.model_dump(),
            "missing_information": missing_information,
            "final_response": response,
        }

    return {
        "loan_request": loan_request.model_dump(),
        "missing_information": [],
    }


# ============================================================
# GOAL ANALYSIS
# ============================================================

def goal_analysis_node(state):

    user_id = state["user_id"]

    user_message = state["user_message"]

    goal = state[
        "financial_context"
    ]["goals"][0]

    result = analyze_goal(

        user_id=user_id,

        user_message=user_message,

        goal_name=goal["name"],

        current_corpus=
            goal["current_corpus"],

        target_amount=
            goal["target_amount"],

        years=
            goal["years"],

        monthly_contribution=
            goal["monthly_contribution"],
    )

    return {
        "analysis":
            result["analysis"],

        "final_response":
            result["response"],
    }


# ============================================================
# CASHFLOW ANALYSIS
# ============================================================

def cashflow_analysis_node(state):

    user_id = state["user_id"]

    user_message = state["user_message"]

    result = analyze_cashflow(

        user_id=user_id,

        user_message=user_message,
    )

    return {
        "analysis":
            result["analysis"],

        "final_response":
            result["response"],
    }


# ============================================================
# INVESTMENT ANALYSIS
# ============================================================

def investment_analysis_node(state):

    user_id = state["user_id"]

    user_message = state["user_message"]

    result = analyze_investment(

        user_id=user_id,

        user_message=user_message,

        current_investment=250000,

        monthly_investment=10000,

        years=10,

        assumed_return=10,

        risk_category="Moderate",
    )

    return {
        "analysis":
            result["analysis"],

        "final_response":
            result["response"],
    }


# ============================================================
# PROTECTION / INSURANCE
# ============================================================

def protection_analysis_node(state):

    user_id = state["user_id"]

    user_message = state["user_message"]

    result = analyze_protection(

        user_id=user_id,

        user_message=user_message,

        required_life_cover=3_000_000,

        existing_life_cover=1_000_000,

        health_cover=500_000,

        dependents=2,

        annual_income=80_000 * 12,
    )

    return {
        "analysis":
            result["analysis"],

        "final_response":
            result["response"],
    }


# ============================================================
# RETIREMENT ANALYSIS
# ============================================================

def retirement_analysis_node(state):

    user_id = state["user_id"]

    user_message = state["user_message"]

    result = analyze_retirement(

        user_id=user_id,

        user_message=user_message,

        current_age=28,

        retirement_age=55,

        current_monthly_expense=45_000,

        inflation_rate=6,

        years_in_retirement=25,

        current_corpus=500_000,

        expected_return=10,
    )

    return {
        "analysis":
            result["analysis"],

        "final_response":
            result["response"],
    }


# ============================================================
# TAX ANALYSIS
# ============================================================

def tax_analysis_node(state):

    user_id = state["user_id"]

    user_message = state["user_message"]

    result = analyze_tax(

        user_id=user_id,

        user_message=user_message,

        gross_income=1_200_000,

        deductions=150_000,

        tax_rate=20,

        deduction_amount=150_000,

        pre_tax_return=10,
    )

    return {
        "analysis":
            result["analysis"],

        "final_response":
            result["response"],
    }


# ============================================================
# FINANCIAL HEALTH ANALYSIS
# ============================================================

def financial_health_analysis_node(state):
    user_id = state["user_id"]

    context = state.get("financial_context", {})

    cashflow_result = state.get("cashflow_analysis", {})
    debt_result = state.get("debt_analysis", {})
    emergency_result = state.get("emergency_analysis", {})
    investment_result = state.get("investment_analysis", {})
    goal_result = state.get("goal_analysis", {})
    insurance_result = state.get("protection_analysis", {})
    retirement_result = state.get("retirement_analysis", {})
    tax_result = state.get("tax_analysis", {})

    result = analyze_financial_health(
        financial_context=context,
        cashflow_result=cashflow_result,
        debt_result=debt_result,
        emergency_result=emergency_result,
        investment_result=investment_result,
        goal_result=goal_result,
        insurance_result=insurance_result,
        retirement_result=retirement_result,
        tax_result=tax_result,
    )

    return {
        "financial_health": result,
        "analysis": result,
        "final_response": result.get(
            "overall_status",
            "Financial health analysis completed."
        ),
    }


# ============================================================
# SCENARIO ANALYSIS
# ============================================================

def scenario_analysis_node(state: FinancialState):
    """
    Analyze a user's What-If scenario.

    Explicit scenario keywords always take priority.
    Previous scenario type is used only for genuine follow-up
    messages such as "increase it to 15000".
    """

    user_message = state["user_message"]
    message = user_message.lower()
    previous_scenario = state.get("last_scenario")

    previous_type = None

    if previous_scenario:
        previous_type = previous_scenario.get("type")

    if any(
        word in message
        for word in ["loan", "borrow", "emi", "debt"]
    ):
        scenario_type = "loan"

    elif any(
        word in message
        for word in [
            "invest",
            "investment",
            "sip",
            "mutual fund",
            "mutual funds",
            "return",
            "annual return",
        ]
    ):
        scenario_type = "investment"

    elif any(
        word in message
        for word in ["retirement", "retire", "pension"]
    ):
        scenario_type = "retirement"

    elif any(
        word in message
        for word in ["goal", "education", "corpus", "target"]
    ):
        scenario_type = "goal"

    else:
        follow_up_phrases = [
            "increase it",
            "decrease it",
            "reduce it",
            "raise it",
            "lower it",
            "change it",
            "instead",
            "make it",
            "set it",
            "increase",
            "decrease",
            "reduce",
            "raise",
            "lower",
            "change",
        ]

        pronoun_follow_up = ["it", "that", "this"]

        is_follow_up = (
            any(
                phrase in message
                for phrase in follow_up_phrases
            )
            or any(
                word in message.split()
                for word in pronoun_follow_up
            )
        )

        if is_follow_up and previous_type:
            scenario_type = previous_type
        else:
            scenario_type = None

    if scenario_type is None:
        return {
            "scenario_type": None,
            "final_response": (
                "I couldn't determine which financial scenario "
                "you want to evaluate. Please specify whether "
                "you mean a loan, investment, goal, or retirement scenario."
            ),
        }

    try:
        if scenario_type == "loan":
            result = analyze_loan_scenario(
                user_message,
                previous_scenario=previous_scenario,
            )

        elif scenario_type == "goal":
            result = analyze_goal_scenario(
                user_message,
                previous_scenario=previous_scenario,
            )

        elif scenario_type == "retirement":
            result = analyze_retirement_scenario(
                user_message,
                previous_scenario=previous_scenario,
            )

        else:
            result = analyze_investment_scenario(
                user_message,
                previous_scenario=previous_scenario,
            )

        if hasattr(result, "model_dump"):
            result = result.model_dump()

        if isinstance(result, dict):
            result["type"] = scenario_type

        # ========================================================
        # BUILD USER RESPONSE
        # ========================================================

        response = None

        if isinstance(result, dict):

            if result.get("response"):
                response = result["response"]

            elif result.get("error"):
                response = result["error"]

            else:
                baseline = result.get("baseline", {})
                scenario = result.get("scenario", {})
                differences = result.get("differences", {})

                baseline_metrics = baseline.get("metrics", {})
                scenario_metrics = scenario.get("metrics", {})
                scenario_assumptions = scenario.get("assumptions", {})

                response_lines = [
                    f"### WHAT-IF SCENARIO: {scenario.get('scenario_name', 'Scenario')}",
                    "",
                    "### BASELINE",
                ]

                for key, value in baseline_metrics.items():
                    response_lines.append(
                        f"- {key.replace('_', ' ').title()}: ₹{value:,.2f}"
                        if isinstance(value, (int, float))
                        else f"- {key.replace('_', ' ').title()}: {value}"
                    )

                response_lines.extend([
                    "",
                    "### SCENARIO",
                ])

                for key, value in scenario_metrics.items():
                    response_lines.append(
                        f"- {key.replace('_', ' ').title()}: ₹{value:,.2f}"
                        if isinstance(value, (int, float))
                        else f"- {key.replace('_', ' ').title()}: {value}"
                    )

                if scenario_assumptions:
                    response_lines.extend([
                        "",
                        "### ASSUMPTIONS",
                    ])

                    for key, value in scenario_assumptions.items():
                        response_lines.append(
                            f"- {key.replace('_', ' ').title()}: {value}"
                        )

                if differences:
                    response_lines.extend([
                        "",
                        "### DIFFERENCE",
                    ])

                    for key, value in differences.items():
                        response_lines.append(
                            f"- {key.replace('_', ' ').title()}: "
                            f"{value:+,.2f}"
                        )

                annual_return = scenario_assumptions.get("annual_return")

                if annual_return is not None and annual_return >= 30:
                    response_lines.extend([
                        "",
                        "### IMPORTANT",
                        (
                            f"The scenario uses an assumed annual return of "
                            f"{annual_return}%. This is a hypothetical assumption "
                            "for the calculation and should not be treated as a "
                            "guaranteed or expected return."
                        ),
                    ])

                response = "\n".join(response_lines)

        return {
            "scenario_type": scenario_type,
            "scenario_results": [result],
            "analysis": result,
            "final_response": response,
        }

    except Exception as e:
        return {
            "scenario_type": scenario_type,
            "scenario_results": [],
            "errors": [
                "Scenario analysis error: "
                f"{str(e)}"
            ],
        }