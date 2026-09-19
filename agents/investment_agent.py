import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.investment import (
    calculate_future_value,
    calculate_monthly_investment_future_value,
    calculate_total_investment_value,
    calculate_investment_gain,
)

from rules.investment_rules import (
    check_risk_profile,
    check_investment_horizon,
)

from rag.retriever import retrieve

load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


def _extract_content(response):

    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict) and "text" in item:
                parts.append(item["text"])

        return " ".join(parts)

    return str(content)


def analyze_investment(
    user_id: str,
    user_message: str,
    current_investment: float,
    monthly_investment: float,
    years: int,
    assumed_return: float = 10,
    risk_category: str = "Moderate",
):

    # -------------------------
    # Investment calculations
    # -------------------------

    current_value = calculate_future_value(
        current_amount=current_investment,
        annual_return=assumed_return,
        years=years,
    )

    monthly_value = calculate_monthly_investment_future_value(
        monthly_investment=monthly_investment,
        annual_return=assumed_return,
        years=years,
    )

    projected_value = calculate_total_investment_value(
        current_amount=current_investment,
        monthly_investment=monthly_investment,
        annual_return=assumed_return,
        years=years,
    )

    total_contributions = (
        current_investment
        + (monthly_investment * years * 12)
    )

    projected_gain = calculate_investment_gain(
        invested_amount=total_contributions,
        projected_value=projected_value,
    )

    # -------------------------
    # Rules
    # -------------------------

    risk_result = check_risk_profile(
        risk_category
    )

    horizon_result = check_investment_horizon(
        years
    )

    # -------------------------
    # NISM RAG
    # -------------------------

    rag_results = retrieve(
        "investment planning financial goals "
        "risk profile asset allocation time horizon "
        "required return savings"
    )

    # -------------------------
    # Evidence
    # -------------------------

    evidence = {

        "investment": {
            "current_investment": current_investment,
            "monthly_investment": monthly_investment,
            "years": years,
        },

        "risk_profile": risk_category,

        "assumptions": {
            "annual_return": assumed_return,
        },

        "calculations": {
            "current_value_future": current_value,
            "monthly_investment_future_value": monthly_value,
            "projected_value": projected_value,
            "total_contributions": total_contributions,
            "projected_gain": projected_gain,
        },

        "rules": {
            "risk_profile": risk_result,
            "investment_horizon": horizon_result,
        },

        "nism_evidence": rag_results,
    }

    # -------------------------
    # Gemini explanation
    # -------------------------

    prompt = f"""
You are the FinSource Investment Planning Agent.

Analyze the user's investment situation using ONLY the supplied evidence.

USER QUESTION:
{user_message}

EVIDENCE:
{evidence}

IMPORTANT:

- Do not invent numbers.
- Do not recalculate supplied values.
- The {assumed_return}% return is only a scenario assumption.
- Do not guarantee investment returns.
- Consider the user's risk profile.
- Consider the investment time horizon.
- Clearly distinguish calculations, assumptions, rules and NISM evidence.
- Do not claim a particular investment is universally suitable.

Return exactly these sections:

### ANSWER

### INVESTMENT DETAILS

### CALCULATION

### RISK PROFILE

### WHY

### IMPACT

### WHAT NEXT

### ASSUMPTIONS

### SOURCES
"""

    test_mode = os.getenv(
        "AGENT_TEST_MODE",
        "false"
    ).lower() == "true"

    print(
        "INVESTMENT_AGENT_TEST_MODE =",
        test_mode
    )

    if test_mode:

        final_text = (
            "INVESTMENT AGENT TEST MODE\n\n"
            "Investment Agent successfully received the request.\n"
            "Investment calculations were completed successfully.\n"
            "Investment rules were evaluated successfully.\n"
            "NISM RAG retrieval was completed successfully.\n"
            "Gemini explanation was skipped because "
            "AGENT_TEST_MODE=true."
        )

    else:

        response = model.invoke(prompt)

        final_text = _extract_content(response)

    return {
        "analysis": evidence,
        "response": final_text,
    }