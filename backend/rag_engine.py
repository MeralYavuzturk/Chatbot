import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()
print("API:", os.getenv("GROQ_API_KEY"))
COLLECTION_NAME = "project_documents"

qdrant = QdrantClient(host="localhost", port=6333)
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def search_documents(question: str, limit: int = 5):
    query_vector = embedding_model.encode(question).tolist()

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )

    return results.points


def ask_rag(question: str):
    results = search_documents(question)

    context = "\n\n---\n\n".join([
        f"Kaynak: {r.payload.get('file_name')}, Sayfa: {r.payload.get('page')}\n{r.payload.get('text')}"
        for r in results
    ])

    prompt = f"""
Sen bir doküman asistanısın.
Sadece aşağıdaki doküman bağlamına göre cevap ver.
Cevap belgelerde yoksa "Bu bilgi yüklenen belgelerde bulunamadı." de.
Cevabı Türkçe, açık ve kısa yaz.

KULLANICI SORUSU:
{question}

DOKÜMAN BAĞLAMI:
{context}
"""

    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Sen kaynaklı cevap veren bir RAG doküman asistanısın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    sources = [
        {
            "file_name": r.payload.get("file_name"),
            "page": r.payload.get("page"),
            "score": r.score
        }
        for r in results
    ]

    return {
        "answer": completion.choices[0].message.content,
        "sources": sources
    }


if __name__ == "__main__":
    question = "Diyabet hastaları nasıl beslenmeli?"
    result = ask_rag(question)

    print("\nCEVAP:")
    print(result["answer"])

    print("\nKAYNAKLAR:")
    for source in result["sources"]:
        print(source)