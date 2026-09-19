from typing import Any


def validate_nism_evidence(
    rag_results: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """
    Check whether the response has supporting NISM evidence.
    """

    rag_results = rag_results or []

    valid_sources = []

    for result in rag_results:
        metadata = result.get("metadata", {})

        source = metadata.get("source")
        page = metadata.get("page")

        if source:
            valid_sources.append(
                {
                    "source": source,
                    "page": page,
                }
            )

    if valid_sources:
        return {
            "grounded": True,
            "sources": valid_sources,
            "warning": None,
        }

    return {
        "grounded": False,
        "sources": [],
        "warning": (
            "No supporting NISM evidence was retrieved. "
            "Do not attribute this statement to NISM."
        ),
    }


def build_nism_citations(
    rag_results: list[dict[str, Any]] | None,
) -> list[str]:
    """
    Build human-readable NISM source references.
    """

    rag_results = rag_results or []

    citations = []

    for result in rag_results:
        metadata = result.get("metadata", {})

        source = metadata.get("source")
        page = metadata.get("page")

        if not source:
            continue

        if page is not None:
            citation = f"{source}, page {page}"
        else:
            citation = source

        if citation not in citations:
            citations.append(citation)

    return citations


def apply_nism_grounding(
    response: str,
    rag_results: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """
    Apply NISM grounding information to an AI response.
    """

    evidence = validate_nism_evidence(rag_results)

    citations = build_nism_citations(rag_results)

    return {
        "response": response,
        "grounded": evidence["grounded"],
        "citations": citations,
        "warning": evidence["warning"],
    }