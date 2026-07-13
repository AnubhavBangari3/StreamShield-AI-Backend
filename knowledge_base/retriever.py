from langchain_core.documents import Document

from .vector_store import load_vector_store


def retrieve_documents(
    query: str,
    k: int = 3,
) -> list[Document]:
    """
    Retrieve the top-k most relevant documents
    from the FAISS vector store.
    """

    vector_store = load_vector_store()

    return vector_store.similarity_search(
        query=query,
        k=k,
    )