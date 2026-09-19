from guardrails.output_safety_guardrail import (
    find_unsafe_output_phrases,
    has_nism_claim,
    validate_output,
    sanitize_output,
)


def test_safe_output():

    text = (
        "The projected value is based on the assumed "
        "annual return. Actual returns can vary."
    )

    result = find_unsafe_output_phrases(text)

    assert result == []


def test_guaranteed_output():

    text = (
        "This investment provides guaranteed returns."
    )

    result = find_unsafe_output_phrases(text)

    assert "guaranteed returns" in result


def test_risk_free_output():

    text = (
        "This is a risk-free investment."
    )

    result = find_unsafe_output_phrases(text)

    assert "risk-free" in result


def test_nism_claim_detection():

    text = (
        "According to NISM, investors should consider risk."
    )

    assert has_nism_claim(text) is True


def test_no_nism_claim():

    text = (
        "The calculated EMI is ₹10,000."
    )

    assert has_nism_claim(text) is False


def test_unsafe_nism_claim():

    text = (
        "According to NISM, this investment is guaranteed."
    )

    result = validate_output(
        text,
        nism_grounded=False,
    )

    assert result["safe"] is False
    assert len(result["warnings"]) >= 1


def test_safe_nism_claim():

    text = (
        "According to NISM, investors should consider "
        "their risk profile."
    )

    result = validate_output(
        text,
        nism_grounded=True,
    )

    assert result["safe"] is True


def test_sanitize_safe_output():

    text = (
        "Your projected corpus is ₹25 lakh "
        "under the stated assumptions."
    )

    result = sanitize_output(text)

    assert result["allowed"] is True
    assert result["response"] == text


def test_sanitize_unsafe_output():

    text = (
        "You must invest all your savings because "
        "this investment has guaranteed returns."
    )

    result = sanitize_output(text)

    assert result["allowed"] is False
    assert result["response"] is None
    assert len(result["warnings"]) > 0