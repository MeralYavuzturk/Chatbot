import os
import uuid
from pathlib import Path

from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer


COLLECTION_NAME = "project_documents"
DOCS_DIR = Path("docs")

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def read_pdf(pdf_path):
    reader = PdfReader(str(pdf_path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


def ingest():
    pdf_files = list(DOCS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("docs klasöründe PDF bulunamadı.")
        return

    points = []

    for pdf_file in pdf_files:
        print(f"Okunuyor: {pdf_file.name}")
        pages = read_pdf(pdf_file)

        for page in pages:
            chunks = chunk_text(page["text"])

            for chunk_index, chunk in enumerate(chunks, start=1):
                vector = model.encode(chunk).tolist()

                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={
                            "text": chunk,
                            "file_name": pdf_file.name,
                            "page": page["page"],
                            "chunk_id": chunk_index
                        }
                    )
                )

    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

    print(f"Tamamlandı. Toplam {len(points)} parça Qdrant'a eklendi.")


if __name__ == "__main__":
    ingest()