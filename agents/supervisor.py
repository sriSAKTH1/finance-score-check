import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from graph.intents import FinancialIntent


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)


with open(
    "prompts/supervisor.txt",
    "r",
    encoding="utf-8"
) as file:

    SUPERVISOR_PROMPT = file.read()


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


def classify_intent(user_message: str) -> str:

    message = user_message.lower()

    if (
        "insurance" in message
        or "life cover" in message
        or "life insurance" in message
        or "health insurance" in message
        or "health cover" in message
        or "medical insurance" in message
        or "protection" in message
    ):
        return FinancialIntent.INSURANCE.value

    if (
        "financial health" in message
        or "financial analysis" in message
        or "analyze my finances" in message
        or "financial situation" in message
        or "financial review" in message
        or "financially" in message
    ):
        return FinancialIntent.FINANCIAL_HEALTH.value

    # --------------------------------
    # Test mode
    # --------------------------------

    test_mode = os.getenv(
        "SUPERVISOR_TEST_MODE",
        "false"
    ).lower() == "true"

    if test_mode:

        message = user_message.lower()

        # Debt
        if (
            "loan" in message
            or "borrow" in message
            or "emi" in message
            or "debt" in message
        ):
            return FinancialIntent.DEBT.value

        # Cash Flow
        if (
            "cash flow" in message
            or "income" in message
            or "expense" in message
            or "expenses" in message
            or "salary" in message
            or "spending" in message
            or "save" in message
            or "saving" in message
            or "savings" in message
        ):
            return FinancialIntent.CASHFLOW.value

        # SCENARIO
        if (
            "what if" in message
            or "what happens if" in message
            or "if i" in message
            or "instead" in message
            or "increase" in message
            or "decrease" in message
            or "raise" in message
            or "lower" in message
            or "change" in message
        ):
            return FinancialIntent.SCENARIO.value

        # INVESTMENT
        if (
            "invest" in message
            or "investment" in message
            or "mutual fund" in message
            or "portfolio" in message
            or "asset allocation" in message
            or "stocks" in message
            or "shares" in message
            or "equity" in message
        ):
            return FinancialIntent.INVESTMENT.value

        # Goal
        if (
            "goal" in message
            or "education" in message
            or "corpus" in message
            or "target amount" in message
        ):
            return FinancialIntent.GOAL.value

        if (
            "retirement" in message
            or "retire" in message
            or "retirement corpus" in message
            or "pension" in message
        ):
            return FinancialIntent.RETIREMENT.value
        
        if (
        "tax" in message
        or "taxation" in message
        or "tax planning" in message
        or "tax saving" in message
        or "tax savings" in message
        or "taxable income" in message
        or "deduction" in message
        or "deductions" in message
    ):
            return FinancialIntent.TAX.value

        return FinancialIntent.GENERAL_FINANCIAL_KNOWLEDGE.value

    # --------------------------------
    # Gemini mode
    # --------------------------------

    prompt = f"""
{SUPERVISOR_PROMPT}

User question:

{user_message}

Return exactly one intent from the allowed list.
"""

    response = model.invoke(prompt)

    text = _extract_content(response)

    intent = text.strip().upper()

    try:

        return FinancialIntent(intent).value

    except ValueError:

        return FinancialIntent.GENERAL_FINANCIAL_KNOWLEDGE.value