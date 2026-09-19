def format_citations(results: list[dict]) -> list[dict]:
    citations = []

    for result in results:
        metadata = result.get("metadata", {})

        citations.append({
            "source": metadata.get("source"),
            "page": metadata.get("page")
        })

    return citations