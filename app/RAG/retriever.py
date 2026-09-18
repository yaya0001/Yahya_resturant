from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

def get_retriever():

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model_name
    )

    vector_store = FAISS.load_local(
        settings.faiss_index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

