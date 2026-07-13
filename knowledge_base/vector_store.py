from pathlib import Path

from langchain_community.vectorstores import FAISS

from .chunker import chunk_documents
from .document_loader import load_documents
from .embeddings import get_embedding_model


BASE_DIR = Path(__file__).resolve().parent.parent

FAISS_DIR = BASE_DIR / "faiss_index"


def build_vector_store() -> FAISS:
    """
    Build a FAISS vector store from all runbooks
    and save it to disk.
    """

    documents = load_documents()

    chunks = chunk_documents(documents)

    embeddings = get_embedding_model()

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    FAISS_DIR.mkdir(
        exist_ok=True,
    )

    vector_store.save_local(str(FAISS_DIR))

    return vector_store


def load_vector_store() -> FAISS:
    """
    Load an existing FAISS vector store.
    """

    embeddings = get_embedding_model()

    return FAISS.load_local(
        folder_path=str(FAISS_DIR),
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )