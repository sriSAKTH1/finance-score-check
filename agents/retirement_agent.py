import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.retirement import (
    calculate_years_to_retirement,
    calculate_future_expense,
    calculate_retirement_corpus,
    calculate_future_value,
    calculate_required_monthly_investment,
    calculate_retirement_gap,
)

from rules.retirement_rules import evaluate_retirement

from rag.retriever import retrieve


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


with open(
    "prompts/retirement.txt",
    "r",
    encoding="utf-8",
) as file:
    RETIREMENT_PROMPT = file.read()


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


def analyze_retirement(
    user_id: str,
    user_message: str,
    current_age: int,
    retirement_age: int,
    current_monthly_expense: float,
    inflation_rate: float,
    years_in_retirement: int,
    current_corpus: float,
    expected_return: float,
):

    # --------------------------------
    # RETIREMENT CALCULATIONS
    # --------------------------------

    years_to_retirement = calculate_years_to_retirement(
        current_age=current_age,
        retirement_age=retirement_age,
    )

    future_monthly_expense = calculate_future_expense(
        current_monthly_expense=current_monthly_expense,
        inflation_rate=inflation_rate,
        years=years_to_retirement,
    )

    required_corpus = calculate_retirement_corpus(
        future_monthly_expense=future_monthly_expense,
        years_in_retirement=years_in_retirement,
        annual_return=expected_return,
    )

    future_current_corpus = calculate_future_value(
        current_amount=current_corpus,
        annual_return=expected_return,
        years=years_to_retirement,
    )

    required_monthly_investment = (
        calculate_required_monthly_investment(
            target_corpus=required_corpus,
            current_corpus=current_corpus,
            annual_return=expected_return,
            years=years_to_retirement,
        )
    )

    retirement_gap = calculate_retirement_gap(
        required_corpus=required_corpus,
        projected_corpus=future_current_corpus,
    )

    # --------------------------------
    # RULES
    # --------------------------------

    rules = evaluate_retirement(
        years_to_retirement=years_to_retirement,
        required_corpus=required_corpus,
        projected_corpus=future_current_corpus,
        inflation_rate=inflation_rate,
        expected_return=expected_return,
    )

    # --------------------------------
    # NISM RAG
    # --------------------------------

    rag_query = (
        "retirement planning time horizon inflation "
        "years to retirement years in retirement "
        "periodic income expected return "
        "retirement corpus"
    )

    nism_evidence = retrieve(
        rag_query,
        k=4,
    )

    # --------------------------------
    # EVIDENCE
    # --------------------------------

    evidence = {

        "retirement": {
            "current_age": current_age,
            "retirement_age": retirement_age,
            "years_to_retirement": years_to_retirement,
            "current_monthly_expense": current_monthly_expense,
            "inflation_rate": inflation_rate,
            "years_in_retirement": years_in_retirement,
            "current_corpus": current_corpus,
            "expected_return": expected_return,
        },

        "calculations": {
            "future_monthly_expense": future_monthly_expense,
            "required_corpus": required_corpus,
            "future_current_corpus": future_current_corpus,
            "required_monthly_investment": required_monthly_investment,
            "retirement_gap": retirement_gap,
        },

        "rules": rules,

        "nism_evidence": nism_evidence,
    }

    # --------------------------------
    # LLM PROMPT
    # --------------------------------

    prompt = f"""
{RETIREMENT_PROMPT}

USER QUESTION:

{user_message}


USER ID:

{user_id}


RETIREMENT INPUTS:

{evidence["retirement"]}


VERIFIED CALCULATIONS:

{evidence["calculations"]}


FINSOURCE RULE FINDINGS:

{rules}


NISM RAG EVIDENCE:

{nism_evidence}


Explain the retirement analysis using only the supplied
calculations, assumptions, rules and retrieved evidence.

Do not invent additional financial information.
"""

    # --------------------------------
    # TEST MODE
    # --------------------------------

    test_mode = os.getenv(
        "AGENT_TEST_MODE",
        "false",
    ).lower() == "true"

    print(
        "RETIREMENT_AGENT_TEST_MODE =",
        test_mode,
    )

    if test_mode:

        final_text = (
            "RETIREMENT AGENT TEST MODE\n\n"
            "Retirement Agent successfully received the request.\n"
            "Retirement calculations were completed successfully.\n"
            "Retirement rules were evaluated successfully.\n"
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