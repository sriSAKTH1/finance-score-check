from typing import Any


UNSAFE_OUTPUT_PHRASES = [
    "guaranteed return",
    "guaranteed returns",
    "guaranteed profit",
    "risk-free",
    "no risk",
    "zero risk",
    "will definitely",
    "definitely make money",
    "cannot lose",
    "you must invest",
    "you must buy",
    "you should buy",
    "sell immediately",
    "invest all your money",
    "invest all your savings",
]


def find_unsafe_output_phrases(
    text: str,
) -> list[str]:
    """
    Detect unsafe or overly certain language
    in the final AI response.
    """

    text_lower = text.lower()

    found = []

    for phrase in UNSAFE_OUTPUT_PHRASES:
        if phrase in text_lower:
            found.append(phrase)

    return found


def has_nism_claim(
    text: str,
) -> bool:
    """
    Detect whether the response makes an explicit
    NISM attribution.
    """

    text_lower = text.lower()

    nism_phrases = [
        "nism recommends",
        "nism says",
        "according to nism",
        "nism advises",
        "as per nism",
    ]

    return any(
        phrase in text_lower
        for phrase in nism_phrases
    )


def validate_output(
    text: str,
    nism_grounded: bool = False,
) -> dict[str, Any]:
    """
    Validate the final AI response.
    """

    unsafe_phrases = find_unsafe_output_phrases(text)

    warnings = []

    if unsafe_phrases:
        warnings.append(
            "The response contains overly certain "
            "or imperative financial language."
        )

    if has_nism_claim(text) and not nism_grounded:
        warnings.append(
            "The response makes an NISM attribution "
            "without supporting NISM evidence."
        )

    return {
        "safe": len(warnings) == 0,
        "unsafe_phrases": unsafe_phrases,
        "warnings": warnings,
    }


def sanitize_output(
    text: str,
    nism_grounded: bool = False,
) -> dict[str, Any]:
    """
    Final output safety check.

    This function does not silently rewrite financial
    claims. It flags unsafe output so the application
    can regenerate or review it.
    """

    validation = validate_output(
        text,
        nism_grounded=nism_grounded,
    )

    if validation["safe"]:
        return {
            "allowed": True,
            "response": text,
            "warnings": [],
        }

    return {
        "allowed": False,
        "response": None,
        "warnings": validation["warnings"],
    }