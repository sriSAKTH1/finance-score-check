import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.insurance import (
    calculate_insurance_gap,
    calculate_life_cover_multiple,
    calculate_health_cover_per_dependent,
    calculate_total_insurance_cover,
)

from rules.insurance_rules import evaluate_insurance
from rag.retriever import retrieve

load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


with open(
    "prompts/protection.txt",
    "r",
    encoding="utf-8",
) as file:
    PROTECTION_PROMPT = file.read()


def _extract_content(response):

    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, str):
                text_parts.append(item)

            elif isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])

        return " ".join(text_parts)

    return str(content)


def analyze_protection(
    user_id: str,
    user_message: str,
    required_life_cover: float,
    existing_life_cover: float,
    health_cover: float,
    dependents: int,
    annual_income: float,
):

    # -------------------------
    # CALCULATIONS
    # -------------------------

    life_cover_gap = calculate_insurance_gap(
        required_cover=required_life_cover,
        existing_cover=existing_life_cover,
    )

    life_cover_multiple = calculate_life_cover_multiple(
        annual_income=annual_income,
        life_cover=existing_life_cover,
    )

    health_cover_per_dependent = calculate_health_cover_per_dependent(
        health_cover=health_cover,
        dependents=dependents,
    )

    total_cover = calculate_total_insurance_cover(
        life_cover=existing_life_cover,
        health_cover=health_cover,
    )

    # -------------------------
    # RULES
    # -------------------------

    rules = evaluate_insurance(
        required_life_cover=required_life_cover,
        existing_life_cover=existing_life_cover,
        health_cover=health_cover,
        dependents=dependents,
    )

    # -------------------------
    # NISM RAG
    # -------------------------

    rag_query = (
        "insurance planning life insurance health insurance "
        "dependents liabilities financial goals "
        "risk protection financial planning"
    )

    nism_evidence = retrieve(rag_query, k=4)

    evidence = {
        "insurance": {
            "required_life_cover": required_life_cover,
            "existing_life_cover": existing_life_cover,
            "health_cover": health_cover,
            "dependents": dependents,
            "annual_income": annual_income,
        },
        "calculations": {
            "life_cover_gap": life_cover_gap,
            "life_cover_multiple": life_cover_multiple,
            "health_cover_per_dependent": health_cover_per_dependent,
            "total_recorded_cover": total_cover,
        },
        "rules": rules,
        "nism_evidence": nism_evidence,
    }

    # -------------------------
    # PROMPT
    # -------------------------

    prompt = f"""
{PROTECTION_PROMPT}

USER QUESTION:
{user_message}

USER ID:
{user_id}

VERIFIED CALCULATIONS:
{{
    "life_cover_gap": {life_cover_gap},
    "life_cover_multiple": {life_cover_multiple},
    "health_cover_per_dependent": {health_cover_per_dependent},
    "total_recorded_cover": {total_cover}
}}

INSURANCE DATA:
{{
    "required_life_cover_assumption": {required_life_cover},
    "existing_life_cover": {existing_life_cover},
    "health_cover": {health_cover},
    "dependents": {dependents},
    "annual_income": {annual_income}
}}

FINSOURCE RULE FINDINGS:
{rules}

NISM RAG EVIDENCE:
{nism_evidence}

Explain the result without inventing information.

Clearly identify the required life-cover figure as an assumption if it was supplied by the application rather than derived from a documented user-specific methodology.
"""

    # -------------------------
    # TEST MODE
    # -------------------------

    test_mode = os.getenv(
        "AGENT_TEST_MODE",
        "false",
    ).lower() == "true"

    print("PROTECTION_AGENT_TEST_MODE =", test_mode)

    if test_mode:

        final_text = (
            "PROTECTION AGENT TEST MODE\n\n"
            "Protection Agent successfully received the request.\n"
            "Insurance calculations were completed successfully.\n"
            "Insurance rules were evaluated successfully.\n"
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