from app.RAG.chunking_imbedding import ChunkingEmbedding

chunker = ChunkingEmbedding()

docs = chunker.load_documents()

split_docs = chunker.split_documents()

vector_store = chunker.create_vector_store()

vector_store.save_local("faiss_index")