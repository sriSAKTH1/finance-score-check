import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.cashflow import (
    calculate_total_income,
    calculate_total_expenses,
    calculate_monthly_cashflow,
    calculate_savings_rate,
    calculate_net_worth,
)

from rules.cashflow_rules import check_cashflow
from rag.retriever import retrieve


load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


def analyze_cashflow(
    user_id: str,
    user_message: str,
):
    try:
        # -------------------------
        # Financial calculations
        # -------------------------

        total_income = calculate_total_income(user_id)
        total_expenses = calculate_total_expenses(user_id)
        monthly_cashflow = calculate_monthly_cashflow(user_id)
        savings_rate = calculate_savings_rate(user_id)
        net_worth = calculate_net_worth(user_id)

        # -------------------------
        # Rule engine
        # -------------------------

        rule_results = check_cashflow(user_id)

        # -------------------------
        # NISM RAG
        # -------------------------

        rag_query = f"""
        FinSource financial planning question:
        {user_message}

        Relevant financial concepts:
        financial planning, budgeting, income, expenses, savings,
        cash flow, emergency fund, emergency reserve, monthly expenses
        """

        rag_results = retrieve(
            rag_query,
            user_id=user_id,
        )

        # -------------------------
        # Evidence
        # -------------------------

        evidence = {
            "user_id": user_id,
            "user_message": user_message,
            "calculations": {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "monthly_cashflow": monthly_cashflow,
                "savings_rate": savings_rate,
                "net_worth": net_worth,
            },
            "rules": rule_results,
            "nism_evidence": rag_results,
        }

        # -------------------------
        # Test mode
        # -------------------------

        test_mode = (
            os.getenv("AGENT_TEST_MODE", "false").lower() == "true"
        )

        if test_mode:
            final_text = (
                "CASHFLOW AGENT TEST MODE\n\n"
                f"Monthly income: ₹{total_income:,.2f}\n"
                f"Monthly expenses: ₹{total_expenses:,.2f}\n"
                f"Monthly cash flow: ₹{monthly_cashflow:,.2f}\n"
                f"Savings rate: {savings_rate:.2f}%\n\n"
                "Cash flow calculations completed successfully.\n"
                "Financial rules evaluated successfully.\n"
                "NISM RAG retrieval completed successfully.\n"
                "Gemini explanation skipped because "
                "AGENT_TEST_MODE=true."
            )

        else:
            # -------------------------
            # Prompt
            # -------------------------

            prompt = f"""
You are the FinSource Cash Flow Agent.

Analyze the user's financial question using ONLY the supplied evidence.

USER QUESTION:
{user_message}

FINANCIAL EVIDENCE:
{evidence}

Important:
- Do not invent numbers.
- Do not perform alternative calculations.
- Use the supplied calculator results.
- Clearly distinguish calculations from interpretation.
- Prototype FinSource rules are not universal financial standards.
- Do not make guarantees.
- Keep the explanation practical and understandable.

Return the answer using exactly these sections:

### ANSWER

### CALCULATION

### WHY

### IMPACT

### WHAT NEXT

### ASSUMPTIONS

### SOURCES
"""

            response = model.invoke(prompt)
            final_text = _extract_content(response)

        return {
            "analysis": evidence,
            "response": final_text,
            "rag_results": rag_results,
            "rule_findings": rule_results,
            "tool_results": {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "monthly_cashflow": monthly_cashflow,
                "savings_rate": savings_rate,
                "net_worth": net_worth,
            },
        }

    except Exception as exc:
        print("\n[CASHFLOW DEBUG ERROR]")
        print(type(exc).__name__)
        print(str(exc))
        print("[END CASHFLOW DEBUG]\n")

        return {
            "analysis": {},
            "response": "I could not complete the cash flow analysis.",
            "rag_results": [],
            "rule_findings": [],
            "tool_results": {},
            "errors": [
                f"Cashflow analysis error: {type(exc).__name__}: {str(exc)}"
            ],
        }