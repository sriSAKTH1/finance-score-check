import os
import json
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from schemas.scenario import ScenarioInput

from scenarios.scenario_engine import (
    run_investment_scenario,
    run_loan_scenario,
    run_goal_scenario,
    run_retirement_scenario,
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

SCENARIO_TEST_MODE = (
    os.getenv("SCENARIO_TEST_MODE", "false").lower() == "true"
)


# ============================================================
# GEMINI
# ============================================================

model = None

if not SCENARIO_TEST_MODE:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Add it to .env or enable SCENARIO_TEST_MODE=true."
        )

    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
    )


# ============================================================
# HELPERS
# ============================================================
def extract_number(message: str):
    """
    Extract a monetary amount only.

    Examples:
        50000
        50,000
        ₹50000
        ₹50,000
        1 lakh
        1.5 lakh

    IMPORTANT:
    Do not treat:
        10%
        12%
        36 months
        10 years
    as money.
    """

    message_lower = message.lower()

    # --------------------------------------------------------
    # 1. Lakh / Lac
    # --------------------------------------------------------

    lakh_match = re.search(
        r"(?:₹\s*)?(\d+(?:\.\d+)?)\s*(?:lakh|lac)\b",
        message_lower,
    )

    if lakh_match:
        return float(lakh_match.group(1)) * 100000

    # --------------------------------------------------------
    # 2. Explicit ₹ amount
    # --------------------------------------------------------

    rupee_match = re.search(
        r"₹\s*(\d[\d,]*)",
        message,
    )

    if rupee_match:
        return float(
            rupee_match.group(1).replace(",", "")
        )

    # --------------------------------------------------------
    # 3. Explicit rupees / Rs
    # --------------------------------------------------------

    rupees_match = re.search(
        r"(\d[\d,]*)\s*(?:rupees?|rs\.?)\b",
        message_lower,
    )

    if rupees_match:
        return float(
            rupees_match.group(1).replace(",", "")
        )

    # --------------------------------------------------------
    # 4. Number after financial amount keywords
    # --------------------------------------------------------

    amount_match = re.search(
        r"(?:invest|investment|loan|borrow|"
        r"amount|contribution|contribute|sip|"
        r"corpus|deposit)"
        r".{0,30}?"
        r"(\d[\d,]*)",
        message_lower,
    )

    if amount_match:
        return float(
            amount_match.group(1).replace(",", "")
        )

    # --------------------------------------------------------
    # 5. Nothing found
    # --------------------------------------------------------

    return None


def extract_percentage(message: str):
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*%",
        message,
    )

    if match:
        return float(match.group(1))

    return None


def extract_months(message: str):
    match = re.search(
        r"(\d+)\s*(?:months?|month)\b",
        message.lower(),
    )

    if match:
        return int(match.group(1))

    return None


def extract_years(message: str):
    match = re.search(
        r"(\d+)\s*(?:years?|year)\b",
        message.lower(),
    )

    if match:
        return int(match.group(1))

    return None

def get_previous_assumption(previous_scenario, key):
    """
    Read an assumption from the previous scenario.
    """

    if not previous_scenario:
        return None

    scenario = previous_scenario.get("scenario", {})

    assumptions = scenario.get("assumptions", {})

    return assumptions.get(key)


# ============================================================
# SCENARIO PARSER
# ============================================================

def extract_scenario(
    user_message: str,
    scenario_type: str,
    previous_scenario: dict | None = None,
):

    message = user_message.lower().strip()


    # ========================================================
    # TEST MODE
    # ========================================================
    is_test = (
        SCENARIO_TEST_MODE
        or os.getenv("SCENARIO_TEST_MODE", "false").lower() == "true"
        or os.getenv("FINAI_TEST_MODE") == "1"
    )

    if SCENARIO_TEST_MODE:
    if is_test:

        # ====================================================
        # INVESTMENT
        # ====================================================

        if scenario_type == "investment":

            monthly_investment = extract_number(message)

            annual_return = extract_percentage(message)

            years = extract_years(message)

            if monthly_investment is None:
                monthly_investment = get_previous_assumption(
                    previous_scenario,
                    "monthly_investment"
                )

            if annual_return is None:
                annual_return = get_previous_assumption(
                    previous_scenario,
                    "annual_return"
                )

            if years is None:
                years = get_previous_assumption(
                    previous_scenario,
                    "years"
                )

            if monthly_investment is None:
                monthly_investment = 10000

            if annual_return is None:
                annual_return = 10

            if years is None:
                years = 10

            return {
                "name": "Investment Scenario",
                "monthly_investment": monthly_investment,
                "current_investment": None,
                "annual_return": annual_return,
                "years": years,
            }


        # ====================================================
        # GOAL
        # ====================================================

        if scenario_type == "goal":

            monthly_investment = extract_number(message)

            if monthly_investment is None:
                monthly_investment = get_previous_assumption(
                    previous_scenario,
                    "monthly_investment",
                )

            if monthly_investment is None:
                monthly_investment = 10000

            return {
                "name": "Goal Contribution Scenario",
                "monthly_investment": monthly_investment,
                "current_investment": None,
                "annual_return": None,
                "years": None,
            }


        # ====================================================
        # LOAN
        # ====================================================

        if scenario_type == "loan":

            # --------------------------------------------------------
            # Extract only the parameters relevant to this message
            # --------------------------------------------------------

            loan_amount = extract_number(message)

            interest_rate = extract_percentage(message)

            tenure_months = extract_months(message)

            # --------------------------------------------------------
            # Preserve previous values
            # --------------------------------------------------------

            if loan_amount is None:
                loan_amount = get_previous_assumption(
                    previous_scenario,
                    "loan_amount",
                )

            if interest_rate is None:
                interest_rate = get_previous_assumption(
                    previous_scenario,
                    "interest_rate",
                )

            if tenure_months is None:
                tenure_months = get_previous_assumption(
                    previous_scenario,
                    "tenure_months",
                )

            # --------------------------------------------------------
            # Demo defaults
            # --------------------------------------------------------

            if loan_amount is None:
                loan_amount = 50000

            if interest_rate is None:
                interest_rate = 12

            if tenure_months is None:
                tenure_months = 24

            return {
                "name": "New Loan",
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "tenure_months": tenure_months,
            }


        # ====================================================
        # RETIREMENT
        # ====================================================

        if scenario_type == "retirement":

            retirement_age = extract_age(message)

            annual_return = extract_percentage(message)

            # --------------------------------------------
            # Previous scenario
            # --------------------------------------------

            if retirement_age is None:
                retirement_age = get_previous_assumption(
                    previous_scenario,
                    "retirement_age"
                )

            if annual_return is None:
                annual_return = get_previous_assumption(
                    previous_scenario,
                    "annual_return"
                )

            # --------------------------------------------
            # Defaults
            # --------------------------------------------

            if retirement_age is None:
                retirement_age = 55

            if annual_return is None:
                annual_return = 10

            return {
                "name": "Alternative Retirement Age",
                "retirement_age": retirement_age,
                "annual_return": annual_return,
            }


        return {}


    # ========================================================
    # NORMAL GEMINI MODE
    # ========================================================

    prompt = f"""
You are a financial scenario parameter extractor.

Scenario type:
{scenario_type}

Current user message:
{user_message}

Previous scenario:
{previous_scenario}

Rules:

1. Extract values explicitly provided by the user.
2. If the user says "it", "this", "that", "change it", "increase it",
   or similar, use the previous scenario.
3. Do not invent values.
4. Do not calculate.
5. Return ONLY valid JSON.

For investment:
{{
    "name": "Investment Scenario",
    "monthly_investment": null,
    "current_investment": null,
    "annual_return": null,
    "years": null
}}

For goal:
{{
    "name": "Goal Contribution Scenario",
    "monthly_investment": null,
    "current_investment": null,
    "annual_return": null,
    "years": null
}}

For loan:
{{
    "name": "New Loan",
    "loan_amount": null,
    "interest_rate": null,
    "tenure_months": null
}}

For retirement:
{{
    "name": "Alternative Retirement Age",
    "retirement_age": null,
    "annual_return": null
}}
"""

    response = model.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        content = "".join(str(item) for item in content)
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
        content = " ".join(parts)

    return json.loads(content)
    text = str(content).strip()

    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        text = json_match.group(1).strip()
    else:
        brace_match = re.search(r"\{.*\}", text, re.DOTALL)
        if brace_match:
            text = brace_match.group(0).strip()
        else:
            text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


# ============================================================
# INVESTMENT SCENARIO
# ============================================================

def analyze_investment_scenario(
    user_message: str,
    previous_scenario: dict | None = None,
):

    scenario_data = extract_scenario(
        user_message=user_message,
        scenario_type="investment",
        previous_scenario=previous_scenario,
    )

    scenario = ScenarioInput(
        name=scenario_data["name"],
        monthly_investment=scenario_data.get("monthly_investment"),
        current_investment=scenario_data.get("current_investment"),
        annual_return=scenario_data.get("annual_return"),
        years=scenario_data.get("years"),
    )

    return run_investment_scenario(
        current_investment=250_000,
        monthly_investment=10_000,
        annual_return=10,
        years=10,
        scenario=scenario,
    )


# ============================================================
# LOAN SCENARIO
# ============================================================

def analyze_loan_scenario(
    user_message: str,
    previous_scenario: dict | None = None,
):

    scenario_data = extract_scenario(
        user_message=user_message,
        scenario_type="loan",
        previous_scenario=previous_scenario,
    )

    loan_amount = scenario_data.get("loan_amount")
    interest_rate = scenario_data.get("interest_rate")
    tenure_months = scenario_data.get("tenure_months")

    if loan_amount is None:
        return {
            "error": "Loan amount is required."
        }

    if interest_rate is None:
        return {
            "error": "Interest rate is required."
        }

    if tenure_months is None:
        return {
            "error": "Loan tenure is required."
        }

    return run_loan_scenario(
        user_id="demo_user_001",
        loan_amount=loan_amount,
        interest_rate=interest_rate,
        tenure_months=tenure_months,
        current_monthly_cashflow=35_000,
        scenario_name=scenario_data["name"],
    )


# ============================================================
# GOAL SCENARIO
# ============================================================

def analyze_goal_scenario(
    user_message: str,
    previous_scenario: dict | None = None,
):

    scenario_data = extract_scenario(
        user_message=user_message,
        scenario_type="goal",
        previous_scenario=previous_scenario,
    )

    scenario = ScenarioInput(
        name=scenario_data["name"],
        monthly_investment=scenario_data.get("monthly_investment"),
        current_investment=scenario_data.get("current_investment"),
        annual_return=scenario_data.get("annual_return"),
        years=scenario_data.get("years"),
    )

    return run_goal_scenario(
        current_corpus=400_000,
        monthly_contribution=5_000,
        target_amount=2_000_000,
        annual_return=10,
        inflation_rate=6,
        years=12,
        scenario=scenario,
    )


# ============================================================
# RETIREMENT SCENARIO
# ============================================================

def analyze_retirement_scenario(
    user_message: str,
    previous_scenario: dict | None = None,
):

    scenario_data = extract_scenario(
        user_message=user_message,
        scenario_type="retirement",
        previous_scenario=previous_scenario,
    )

    retirement_age = scenario_data.get("retirement_age")

    annual_return = scenario_data.get(
        "annual_return",
        10,
    )

    if retirement_age is None:
        return {
            "error": "Retirement age is required."
        }

    return run_retirement_scenario(
        current_age=28,
        retirement_age=55,
        current_monthly_expense=45_000,
        inflation_rate=6,
        years_in_retirement=25,
        current_corpus=500_000,
        annual_return=annual_return,
        scenario=ScenarioInput(
            name=scenario_data["name"],
            retirement_age=retirement_age,
            annual_return=annual_return,
        ),
    )
    