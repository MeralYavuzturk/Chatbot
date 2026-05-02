from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

COLLECTION_NAME = "project_documents"

question = "Diyabet hastaları nasıl beslenmeli?"

query_vector = model.encode(question).tolist()

results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=5
)

for r in results.points:
    print("Skor:", r.score)
    print("Dosya:", r.payload.get("file_name"))
    print("Sayfa:", r.payload.get("page"))
    print("Metin:", r.payload.get("text")[:300])
    print("-" * 50)