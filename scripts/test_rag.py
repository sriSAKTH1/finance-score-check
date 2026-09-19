from rag.retriever import retrieve


query = """
What should be considered before borrowing money
and taking a loan?
"""


results = retrieve(query, k=4)


print("\nNISM RAG RESULTS")
print("================")


for index, result in enumerate(results, start=1):

    metadata = result["metadata"]

    print(f"\nRESULT {index}")
    print("-----------")

    print(
        f"Source: {metadata.get('source')}"
    )

    print(
        f"Page: {metadata.get('page')}"
    )

    print("\nText:")

    print(
        result["text"][:1000]
    )