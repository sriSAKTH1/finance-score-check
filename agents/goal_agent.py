import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.goals import (
    future_value,
    future_value_with_monthly_contribution,
    required_future_value,
    required_monthly_contribution,
    calculate_goal_gap,
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


def analyze_goal(
    user_id: str,
    user_message: str,
    goal_name: str,
    current_corpus: float,
    target_amount: float,
    years: int,
    monthly_contribution: float,
    assumed_return: float = 10,
    assumed_inflation: float = 6,
):

    # -------------------------
    # Goal calculations
    # -------------------------

    current_corpus_future_value = future_value(
        present_value=current_corpus,
        annual_return=assumed_return,
        years=years,
    )

    projected_corpus = future_value_with_monthly_contribution(
        current_corpus=current_corpus,
        monthly_contribution=monthly_contribution,
        annual_return=assumed_return,
        years=years,
    )

    inflation_adjusted_target = required_future_value(
        current_goal_amount=target_amount,
        inflation_rate=assumed_inflation,
        years=years,
    )

    required_contribution_nominal = required_monthly_contribution(
        target_amount=target_amount,
        current_corpus=current_corpus,
        annual_return=assumed_return,
        years=years,
    )

    nominal_gap = calculate_goal_gap(
        target_amount=target_amount,
        projected_amount=projected_corpus,
    )

    # -------------------------
    # NISM RAG
    # -------------------------

    rag_results = retrieve(
        "financial goals inflation time horizon required savings "
        "investment planning goal corpus"
    )

    # -------------------------
    # Evidence
    # -------------------------

    evidence = {

        "goal": {
            "name": goal_name,
            "current_corpus": current_corpus,
            "target_amount": target_amount,
            "years": years,
            "monthly_contribution": monthly_contribution,
        },

        "assumptions": {
            "annual_return": assumed_return,
            "inflation_rate": assumed_inflation,
        },

        "calculations": {
            "current_corpus_future_value":
                current_corpus_future_value,

            "projected_corpus":
                projected_corpus,

            "inflation_adjusted_target":
                inflation_adjusted_target,

            "required_monthly_contribution_nominal":
                required_contribution_nominal,

            "nominal_goal_gap":
                nominal_gap,
        },

        "nism_evidence": rag_results,
    }

    # -------------------------
    # Gemini explanation
    # -------------------------

    prompt = f"""
You are the FinSource Goal Planning Agent.

Analyze the user's financial goal using ONLY the supplied evidence.

USER QUESTION:
{user_message}

EVIDENCE:
{evidence}

IMPORTANT:

- Do not invent numbers.
- Do not recalculate the supplied values.
- Do not mix the nominal target with the inflation-adjusted target.
- The assumed return of {assumed_return}% is only a scenario assumption.
- The assumed inflation rate of {assumed_inflation}% is only a scenario assumption.
- Actual investment returns and inflation may differ.
- Do not guarantee that the goal will be achieved.
- Clearly explain the difference between nominal and inflation-adjusted scenarios.

Return exactly these sections:

### ANSWER

### GOAL DETAILS

### CALCULATION

### GAP

### WHY

### IMPACT

### WHAT NEXT

### ASSUMPTIONS

### SOURCES
"""

# -------------------------
# Gemini explanation
# -------------------------

    test_mode = os.getenv("AGENT_TEST_MODE", "false").lower() == "true"

    print("AGENT_TEST_MODE =", test_mode)

    if test_mode:

        final_text = (
            "GOAL AGENT TEST MODE\n\n"
            "Goal Agent successfully received the request.\n"
            "Goal calculations were completed successfully.\n"
            "NISM RAG retrieval was completed successfully.\n"
            "LangGraph routing to Goal Agent is working correctly.\n"
            "Gemini explanation was skipped because AGENT_TEST_MODE=true."
        )

    else:

        response = model.invoke(prompt)

        final_text = _extract_content(response)

    return {
        "analysis": evidence,
        "response": final_text,
    }