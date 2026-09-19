from rag.retriever import retrieve
from rag.citations import format_citations


TEST_QUESTIONS = [
    "What should be considered before taking a loan?",
    "What is risk profiling?",
    "What factors should be considered in retirement planning?",
    "What is investment planning?",
    "What is the importance of financial planning?",
]


def test_rag():

    for question in TEST_QUESTIONS:

        print("\n" + "=" * 70)
        print("QUESTION:")
        print(question)

        results = retrieve(question, k=3)

        citations = format_citations(results)

        print("\nRETRIEVED SOURCES:")

        for citation in citations:
            print(
                f"- {citation['source']} "
                f"| Page {citation['page']}"
            )

        assert len(results) > 0


if __name__ == "__main__":
    test_rag()