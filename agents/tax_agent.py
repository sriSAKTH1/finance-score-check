import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.tax import (
    calculate_taxable_income,
    calculate_tax_saving,
    calculate_post_tax_return,
    calculate_tax_impact,
)

from rules.tax_rules import evaluate_tax

from rag.retriever import retrieve


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


with open(
    "prompts/tax.txt",
    "r",
    encoding="utf-8",
) as file:
    TAX_PROMPT = file.read()


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


def analyze_tax(
    user_id: str,
    user_message: str,
    gross_income: float,
    deductions: float,
    tax_rate: float,
    deduction_amount: float,
    pre_tax_return: float,
):

    # --------------------------------
    # CALCULATIONS
    # --------------------------------

    taxable_income = calculate_taxable_income(
        gross_income=gross_income,
        deductions=deductions,
    )

    estimated_tax_saving = calculate_tax_saving(
        deduction_amount=deduction_amount,
        applicable_tax_rate=tax_rate,
    )

    post_tax_return = calculate_post_tax_return(
        pre_tax_return=pre_tax_return,
        tax_rate=tax_rate,
    )

    tax_impact = calculate_tax_impact(
        income=gross_income,
        deductions=deductions,
        tax_rate=tax_rate,
    )

    estimated_tax = tax_impact["estimated_tax"]

    # --------------------------------
    # RULES
    # --------------------------------

    rules = evaluate_tax(
        gross_income=gross_income,
        deductions=deductions,
        tax_rate=tax_rate,
        estimated_tax=estimated_tax,
    )

    # --------------------------------
    # NISM RAG
    # --------------------------------

    rag_query = (
        "tax planning financial planning "
        "tax impact savings investment returns "
        "financial goals"
    )

    nism_evidence = retrieve(
        rag_query,
        k=4,
    )

    # --------------------------------
    # EVIDENCE
    # --------------------------------

    evidence = {

        "tax_inputs": {
            "gross_income": gross_income,
            "deductions": deductions,
            "tax_rate": tax_rate,
            "deduction_amount": deduction_amount,
            "pre_tax_return": pre_tax_return,
        },

        "calculations": {
            "taxable_income": taxable_income,
            "estimated_tax": estimated_tax,
            "estimated_tax_saving": estimated_tax_saving,
            "post_tax_return": post_tax_return,
        },

        "rules": rules,

        "nism_evidence": nism_evidence,
    }

    # --------------------------------
    # PROMPT
    # --------------------------------

    prompt = f"""
{TAX_PROMPT}

USER QUESTION:

{user_message}


USER ID:

{user_id}


TAX INPUTS:

{evidence["tax_inputs"]}


VERIFIED CALCULATIONS:

{evidence["calculations"]}


FINSOURCE RULE FINDINGS:

{rules}


NISM RAG EVIDENCE:

{nism_evidence}


Explain the tax analysis using only the supplied
calculations, assumptions, rules and retrieved evidence.

Clearly state that the tax rate and other tax inputs
are assumptions unless they come from a verified,
current tax-rule source.

Do not invent tax slabs, deductions, exemptions,
regime rules or other tax provisions.
"""

    # --------------------------------
    # TEST MODE
    # --------------------------------

    test_mode = os.getenv(
        "AGENT_TEST_MODE",
        "false",
    ).lower() == "true"

    print(
        "TAX_AGENT_TEST_MODE =",
        test_mode,
    )

    if test_mode:

        final_text = (
            "TAX AGENT TEST MODE\n\n"
            "Tax Agent successfully received the request.\n"
            "Tax calculations were completed successfully.\n"
            "Tax rules were evaluated successfully.\n"
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