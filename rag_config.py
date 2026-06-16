import chromadb

RAG_COLLECTION = "nutrition_docs"

RAG_RESULTS = 3

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_collection(
    RAG_COLLECTION
)