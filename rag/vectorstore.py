from langchain_chroma import Chroma

from rag.embeddings import get_embeddings


PERSIST_DIRECTORY = "data/chroma_nism"


def create_vectorstore(chunks: list[dict]):

    embeddings = get_embeddings()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        chunk["metadata"]
        for chunk in chunks
    ]

    vectorstore = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name="nism_knowledge"
    )

    return vectorstore


def load_vectorstore():

    embeddings = get_embeddings()

    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        collection_name="nism_knowledge",
        embedding_function=embeddings
    )