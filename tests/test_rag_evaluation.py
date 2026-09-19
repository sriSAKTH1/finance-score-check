from rag.retriever import retrieve


def run_rag_query(name, query, expected_keywords):

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("QUERY:")
    print(query)

    results = retrieve(query, k=4)

    print("\nRESULT COUNT:", len(results))

    assert len(results) > 0, "RAG returned no results"

    combined_text = ""

    for i, result in enumerate(results, start=1):

        text = result.get("text", "")
        metadata = result.get("metadata", {})

        print(f"\nRESULT {i}")
        print("-" * 50)

        print("Source:", metadata.get("source"))
        print("Page:", metadata.get("page"))

        print("Content:")
        print(text[:500])

        combined_text += " " + text.lower()

    # --------------------------------------------------
    # Keyword evaluation
    # --------------------------------------------------

    missing = []

    for keyword in expected_keywords:

        if keyword.lower() not in combined_text:
            missing.append(keyword)

    print("\nExpected concepts:")
    print(expected_keywords)

    if missing:

        print("Missing concepts:", missing)
        print("RESULT: FAIL")

        return False

    print("RESULT: PASS")

    return True


def main():

    tests = [

        # --------------------------------------------------
        # TEST 1
        # --------------------------------------------------

        (
            "TEST 1 - Financial Planning",

            "What is financial planning and why is it important?",

            [
                "financial planning",
                "savings",
            ],
        ),

        # --------------------------------------------------
        # TEST 2
        # --------------------------------------------------

        (
            "TEST 2 - Debt Management",

            "What should be considered before taking a loan?",

            [
                "borrowing",
                "repay",
            ],
        ),

        # --------------------------------------------------
        # TEST 3
        # --------------------------------------------------

        (
            "TEST 3 - Investment Planning",

            "How should investment planning consider goals and risk?",

            [
                "investment",
                "risk",
            ],
        ),

        # --------------------------------------------------
        # TEST 4
        # --------------------------------------------------

        (
            "TEST 4 - Risk Profiling",

            "What factors are considered when determining an investor's risk profile?",

            [
                "risk",
                "income",
            ],
        ),

        # --------------------------------------------------
        # TEST 5
        # --------------------------------------------------

        (
            "TEST 5 - Retirement Planning",

            "What factors are important for retirement planning?",

            [
                "retirement",
                "inflation",
            ],
        ),

        # --------------------------------------------------
        # TEST 6
        # --------------------------------------------------

        (
            "TEST 6 - Suitability",

            "What factors should be considered when determining whether investment advice is suitable?",

            [
                "risk",
                "objectives",
            ],
        ),

        # --------------------------------------------------
        # TEST 7
        # --------------------------------------------------

        (
            "TEST 7 - Portfolio Management",

            "Why is diversification important in an investment portfolio?",

            [
                "diversification",
                "risk",
            ],
        ),
    ]

    passed = 0
    failed = 0

    for name, query, keywords in tests:

        try:

            success = run_rag_query(
                name,
                query,
                keywords,
            )

            if success:
                passed += 1
            else:
                failed += 1

        except Exception as e:

            print("\nRESULT: ERROR")
            print("Error:", e)

            failed += 1

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("RAG EVALUATION SUMMARY")
    print("=" * 70)

    print("Total :", len(tests))
    print("Passed:", passed)
    print("Failed:", failed)

    if failed == 0:

        print("\nALL RAG EVALUATION TESTS PASSED")

    else:

        print("\nSOME RAG EVALUATION TESTS FAILED")


if __name__ == "__main__":
    main()