from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)

RUNBOOKS_DIR = (
    Path(__file__).resolve().parent / "runbooks"
)


def load_documents() -> list[Document]:
    """
    Load all Markdown and PDF runbooks from the runbooks folder.
    """

    documents: list[Document] = []

    for file in RUNBOOKS_DIR.iterdir():

        if file.suffix.lower() == ".md":
            loader = TextLoader(
                str(file),
                encoding="utf-8",
            )
            documents.extend(loader.load())

        elif file.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file))
            documents.extend(loader.load())

    return documents