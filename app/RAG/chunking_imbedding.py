from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class ChunkingEmbedding:

    def __init__(self):
        self.documents = []
        self.split_docs = []
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )
        self.vector_store = None

    def load_documents(self) -> list:
        self.documents = load_documents()
        
        if not self.documents:
            raise ValueError("No Markdown documents were found.")

        return self.documents

    def split_documents(self) -> list:
        if not self.documents:
            raise ValueError(
                "Documents not loaded. Call load_documents() first."
            )

        self.split_docs = split_documents(self.documents)
        return self.split_docs

    def create_vector_store(self):
        if not self.split_docs:
            raise ValueError(
                "Documents not split. Call split_documents() first."
            )

        self.vector_store = FAISS.from_documents(
            self.split_docs,
            self.embedding_model
        )

        return self.vector_store


def load_documents() -> list:
    documents = []

    data_dir = Path("app/RAG/data")

    for file_path in data_dir.rglob("*.md"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        documents.extend(loader.load())

    return documents


def split_documents(documents: list) -> list:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )

    return splitter.split_documents(documents)