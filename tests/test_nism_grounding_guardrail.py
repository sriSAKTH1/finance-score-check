from guardrails.nism_grounding_guardrail import (
    validate_nism_evidence,
    build_nism_citations,
    apply_nism_grounding,
)


def test_valid_nism_evidence():

    rag_results = [
        {
            "text": "Borrowing uses future income.",
            "metadata": {
                "source": "NISM-Series-X-A",
                "page": 71,
            },
        }
    ]

    result = validate_nism_evidence(rag_results)

    assert result["grounded"] is True
    assert len(result["sources"]) == 1


def test_missing_nism_evidence():

    result = validate_nism_evidence([])

    assert result["grounded"] is False
    assert len(result["sources"]) == 0
    assert result["warning"] is not None


def test_none_nism_evidence():

    result = validate_nism_evidence(None)

    assert result["grounded"] is False


def test_build_citations():

    rag_results = [
        {
            "text": "Financial planning is holistic.",
            "metadata": {
                "source": "NISM-Series-X-A",
                "page": 25,
            },
        }
    ]

    citations = build_nism_citations(rag_results)

    assert citations == [
        "NISM-Series-X-A, page 25"
    ]


def test_duplicate_citations_removed():

    rag_results = [
        {
            "text": "Example 1",
            "metadata": {
                "source": "NISM-Series-X-A",
                "page": 25,
            },
        },
        {
            "text": "Example 2",
            "metadata": {
                "source": "NISM-Series-X-A",
                "page": 25,
            },
        },
    ]

    citations = build_nism_citations(rag_results)

    assert len(citations) == 1


def test_apply_grounding_with_evidence():

    response = "Borrowing affects future income."

    rag_results = [
        {
            "text": "Borrowing uses future income.",
            "metadata": {
                "source": "NISM-Series-X-A",
                "page": 71,
            },
        }
    ]

    result = apply_nism_grounding(
        response,
        rag_results,
    )

    assert result["grounded"] is True
    assert result["response"] == response
    assert len(result["citations"]) == 1
    assert result["warning"] is None


def test_apply_grounding_without_evidence():

    response = "This is a financial calculation."

    result = apply_nism_grounding(
        response,
        [],
    )

    assert result["grounded"] is False
    assert result["warning"] is not None