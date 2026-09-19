from typing import Any


UNSAFE_PHRASES = [
    "guaranteed return",
    "guaranteed returns",
    "guaranteed profit",
    "risk-free",
    "no risk",
    "zero risk",
    "will definitely",
    "definitely make money",
    "must buy",
    "you should buy",
    "buy this immediately",
    "sell immediately",
    "invest all your money",
    "invest all your savings",
    "borrow now",
]


def find_unsafe_phrases(text: str) -> list[str]:
    """
    Detect overly certain or imperative financial advice.
    """

    text_lower = text.lower()

    found = []

    for phrase in UNSAFE_PHRASES:
        if phrase in text_lower:
            found.append(phrase)

    return found


def validate_advice_context(
    context: dict[str, Any],
) -> dict[str, Any]:
    """
    Check whether enough financial context exists
    before giving personalized investment guidance.
    """

    missing = []

    if not context.get("risk_profile"):
        missing.append("risk profile")

    if not context.get("goals"):
        missing.append("financial goals")

    if not context.get("income"):
        missing.append("income")

    if not context.get("expenses"):
        missing.append("expenses")

    return {
        "valid": len(missing) == 0,
        "missing": missing,
    }


def guard_advice(
    text: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:

    context = context or {}

    unsafe_phrases = find_unsafe_phrases(text)

    context_result = validate_advice_context(context)

    warnings = []

    if unsafe_phrases:
        warnings.append(
            "The response contains overly certain or "
            "imperative financial language."
        )

    if not context_result["valid"]:
        warnings.append(
            "Personalized financial guidance should be "
            "qualified because important financial context "
            "is missing."
        )

    return {
        "safe": (
            len(unsafe_phrases) == 0
            and context_result["valid"]
        ),
        "unsafe_phrases": unsafe_phrases,
        "missing_context": context_result["missing"],
        "warnings": warnings,
    }