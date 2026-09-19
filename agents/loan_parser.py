import json
import os
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from schemas.loan_request import LoanRequest

load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


def extract_loan_details_test(user_message: str):
    """
    Deterministic loan parser used during evaluation tests.
    Does not call Gemini.
    """

    text = user_message.lower()

    # -----------------------------
    # Loan amount
    # -----------------------------

    amount = None

    lakh_match = re.search(
        r"(\d+(?:\.\d+)?)\s*lakh",
        text
    )

    if lakh_match:
        amount = float(lakh_match.group(1)) * 100000

    if amount is None:
        amount_match = re.search(
            r"(?:₹|rs\.?|inr)?\s*"
            r"(\d[\d,]*(?:\.\d+)?)",
            text
        )

        if amount_match:
            amount = float(
                amount_match.group(1).replace(",", "")
            )

    # -----------------------------
    # Interest rate
    # -----------------------------

    rate = None

    rate_match = re.search(
        r"(\d+(?:\.\d+)?)\s*%",
        text
    )

    if rate_match:
        rate = float(rate_match.group(1))

    # -----------------------------
    # Tenure
    # -----------------------------

    tenure = None

    month_match = re.search(
        r"(\d+)\s*months?",
        text
    )

    if month_match:
        tenure = int(month_match.group(1))

    year_match = re.search(
        r"(\d+(?:\.\d+)?)\s*years?",
        text
    )

    if year_match:
        tenure = int(float(year_match.group(1)) * 12)

    # --------------------------------------------------
    # Missing-data evaluation mode
    # --------------------------------------------------

    if os.getenv("FINAI_STRICT_INPUT_TEST_MODE") == "1":

        return LoanRequest(
            loan_amount=amount,
            interest_rate=rate,
            tenure_months=tenure,
        )

    # --------------------------------------------------
    # Normal deterministic scenario test mode
    # --------------------------------------------------

    if rate is None:
        rate = 12.0

    if tenure is None:
        tenure = 24

    return LoanRequest(
        loan_amount=amount,
        interest_rate=rate,
        tenure_months=tenure,
    )


def extract_loan_details(user_message: str) -> LoanRequest:

    if os.getenv("FINAI_TEST_MODE") == "1":
        return extract_loan_details_test(user_message)

    prompt = f"""
Extract loan information from the following user message.

User message:
{user_message}

Return ONLY valid JSON.

Required fields:
- loan_amount
- interest_rate
- tenure_months

Optional:
- purpose

Example:

{{
    "loan_amount": 50000,
    "interest_rate": 12,
    "tenure_months": 24,
    "purpose": null
}}

If a required value is missing, use null.
"""

    response = model.invoke(prompt)

    content = response.content

    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and "text" in item:
                parts.append(item["text"])

        text = " ".join(parts)
    else:
        text = str(content)

    text = text.strip()

    # Remove markdown JSON fences if Gemini returns them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    data = json.loads(text)

    return LoanRequest.model_validate(data)