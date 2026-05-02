import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()
COLLECTION_NAME = "project_documents"

qdrant = QdrantClient(host="localhost", port=6333)
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def search_documents(question: str, limit: int = 8):
    query_vector = embedding_model.encode(question).tolist()

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        with_payload=True,
        limit=limit
    )

    return results.points


def ask_rag(question: str):
    results = search_documents(question)

    context_parts = []
    for r in results:
        text = r.payload.get('text', '')
        file_name = r.payload.get('file_name', 'Bilinmeyen')
        page = r.payload.get('page', '?')
        context_parts.append(f"--- KAYNAK: {file_name} (Sayfa {page}) ---\n{text}")

    context = "\n\n".join(context_parts)

    prompt = f"""
Sen, T.C. Sağlık Bakanlığı rehberleri ve tıbbi dökümanlar konusunda uzmanlaşmış, son derece detaycı bir sağlık asistanısın. Kullanıcının sorusuna, elindeki doküman bağlamını kullanarak mümkün olan en kapsamlı, detaylı ve açıklayıcı cevabı ver.

TALİMATLAR:
1. SADECE verilen "DOKÜMAN BAĞLAMI" içindeki bilgilere dayanarak cevap ver.
2. Cevabını mümkün olduğunca uzun, detaylı ve kapsamlı tut. Kısa cevaplardan kaçın.
3. Konuyu açıklarken neden-sonuç ilişkisi kur, eğer belgelerde varsa istatistikleri, önerileri ve uyarıları mutlaka ekle.
4. Bilgiler doğrudan mevcut değilse ama belgelerden mantıklı bir çıkarım yapılabiliyorsa, bu çıkarımı "Belgelere dayanarak..." diyerek detaylandır.
5. Cevaplarını hem paragraflar hem de detaylı maddeler kullanarak yapılandır.
6. Eğer hiçbir şekilde bilgi yoksa "Üzgünüm, bu konu hakkında yüklü belgelerde yeterli detayda bilgi bulunamadı." de.
7. Eğer cevap kaynaklarda yoksa ve verilen cevap api üzerinden sağlandıysa bunu mutlaka belirt. 

KULLANICI SORUSU: {question}

DOKÜMAN BAĞLAMI:
{context}
"""

    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Sen güvenilir, son derece detaylı ve açıklayıcı cevaplar veren profesyonel bir tıbbi asistanısın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.35
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