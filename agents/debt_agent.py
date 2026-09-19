import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.debt import (
    calculate_emi,
    calculate_total_interest,
    calculate_total_repayment,
    calculate_existing_emi,
    calculate_debt_burden,
    calculate_post_loan_cashflow,
)

from rules.debt_rules import check_debt
from rules.cashflow_rules import check_cashflow
from rag.retriever import retrieve

from audit.tool_audit import execute_with_audit


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


with open(
    "prompts/debt.txt",
    "r",
    encoding="utf-8",
) as file:

    DEBT_PROMPT = file.read()


def analyze_debt(
    user_id: str,
    user_message: str,
    loan_amount: float,
    interest_rate: float,
    tenure_months: int,
    session_id: str | None = None,
) -> dict:
    """
    Analyze a loan request using deterministic calculations,
    financial rules, NISM RAG evidence, and Gemini explanation.
    """

    # ------------------------------------------------
    # Audit session
    # ------------------------------------------------

    if session_id is None:
        session_id = f"debt-{user_id}"

    # ------------------------------------------------
    # 1. Financial calculations
    # ------------------------------------------------

    emi = execute_with_audit(
        calculate_emi,
        "calculate_emi",
        user_id,
        session_id,
        loan_amount,
        interest_rate,
        tenure_months,
    )

    total_interest = execute_with_audit(
        calculate_total_interest,
        "calculate_total_interest",
        user_id,
        session_id,
        loan_amount,
        interest_rate,
        tenure_months,
    )

    total_repayment = execute_with_audit(
        calculate_total_repayment,
        "calculate_total_repayment",
        user_id,
        session_id,
        loan_amount,
        interest_rate,
        tenure_months,
    )

    existing_emi = execute_with_audit(
        calculate_existing_emi,
        "calculate_existing_emi",
        user_id,
        session_id,
        user_id,
    )

    current_debt_burden = execute_with_audit(
        calculate_debt_burden,
        "calculate_debt_burden",
        user_id,
        session_id,
        user_id,
    )

    post_loan_cashflow = execute_with_audit(
        calculate_post_loan_cashflow,
        "calculate_post_loan_cashflow",
        user_id,
        session_id,
        user_id,
        emi,
    )

    # ------------------------------------------------
    # 2. Rule engine
    # ------------------------------------------------

    debt_rules = check_debt(
        user_id=user_id,
        session_id=session_id,
    )

    cashflow_rules = check_cashflow(
        user_id=user_id,
        session_id=session_id,
    )

    # ------------------------------------------------
    # 3. NISM RAG
    # ------------------------------------------------

    rag_query = """
    What should be considered before borrowing money,
    including repayment ability, debt servicing,
    cash flow impact and responsible borrowing?
    """

    rag_results = retrieve(
        rag_query,
        k=3,
        user_id=user_id,
        session_id=session_id,
    )

    # ------------------------------------------------
    # 4. Prepare evidence for Gemini
    # ------------------------------------------------

    evidence = {
        "loan": {
            "amount": loan_amount,
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
            "emi": emi,
            "total_interest": total_interest,
            "total_repayment": total_repayment,
        },

        "existing_financial_position": {
            "existing_emi": existing_emi,
            "current_debt_burden": current_debt_burden,
            "post_loan_cashflow": post_loan_cashflow,
        },

        "rules": {
            "debt": debt_rules,
            "cashflow": cashflow_rules,
        },

        "nism_evidence": rag_results,
    }

    # ------------------------------------------------
    # 5. Ask Gemini to explain the evidence
    # ------------------------------------------------

    prompt = f"""
{DEBT_PROMPT}

USER QUESTION:
{user_message}

FINANCIAL ANALYSIS:
{evidence}

Use ONLY the supplied calculations and evidence.

Explain the result clearly.

Do not perform new calculations yourself.

Return:

ANSWER
CALCULATION
WHY
IMPACT
ASSUMPTIONS
WHAT NEXT
SOURCES
"""

    test_mode = os.getenv(
        "AGENT_TEST_MODE",
        "false",
    ).lower() == "true"

    if test_mode:

        final_text = (
            "DEBT AGENT TEST MODE\n\n"
            "Debt calculations were completed successfully.\n"
            "Debt rules were evaluated successfully.\n"
            "NISM RAG retrieval was completed successfully.\n"
            "Gemini explanation was skipped because "
            "AGENT_TEST_MODE=true."
        )

    else:

        response = model.invoke(prompt)

        content = response.content

        # Gemini can return either string or content blocks
        if isinstance(content, str):

            final_text = content

        elif isinstance(content, list):

            parts = []

            for item in content:

                if isinstance(item, str):
                    parts.append(item)

                elif isinstance(item, dict):

                    if "text" in item:
                        parts.append(item["text"])

            final_text = " ".join(parts)

        else:

            final_text = str(content)

    # ------------------------------------------------
    # 6. Return analysis
    # ------------------------------------------------

    return {
        "analysis": evidence,
        "response": final_text,
    }