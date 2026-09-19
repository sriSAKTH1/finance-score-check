from pathlib import Path

from rag.loader import load_pdf
from rag.chunker import chunk_documents
from rag.vectorstore import create_vectorstore


DATA_DIR = Path("data/nism")


def main():

    all_documents = []

    print("Loading NISM X-A...")

    xa_documents = load_pdf(
        DATA_DIR / "nism_xa.pdf",
        "NISM Series X-A"
    )

    print(
        f"X-A pages loaded: {len(xa_documents)}"
    )

    all_documents.extend(xa_documents)

    print("Loading NISM X-B...")

    xb_documents = load_pdf(
        DATA_DIR / "nism_xb.pdf",
        "NISM Series X-B"
    )

    print(
        f"X-B pages loaded: {len(xb_documents)}"
    )

    all_documents.extend(xb_documents)

    print("\nCreating chunks...")

    chunks = chunk_documents(
        all_documents,
        chunk_size=1200,
        chunk_overlap=200
    )

    print(
        f"Total chunks: {len(chunks)}"
    )

    print("\nCreating vector database...")

    create_vectorstore(chunks)

    print("\nNISM RAG ingestion completed.")


if __name__ == "__main__":
    main()