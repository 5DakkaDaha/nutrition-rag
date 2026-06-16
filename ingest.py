from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="vector_db")

collection = client.get_or_create_collection(
    name="nutrition_docs"
)

with open(
    "data/nutrition_docs.txt",
    "r",
    encoding="utf-8"
) as file:

    text = file.read()

chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]

embeddings = model.encode(chunks)

ids = [str(i) for i in range(len(chunks))]

collection.add(
    documents=chunks,
    embeddings=embeddings.tolist(),
    ids=ids
)

print("Beslenme verileri başarıyla yüklendi.")