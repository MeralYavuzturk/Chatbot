# 🌌 Aether AI: Sağlık Bakanlığı Verileri ile Güçlendirilmiş RAG Asistanı

**Aether AI**, T.C. Sağlık Bakanlığı'nın resmi dökümanlarını temel alarak kronik hastalık yönetimi ve sağlıklı yaşam konularında uzmanlaşmış, son derece detaylı cevaplar verebilen bir **RAG (Retrieval-Augmented Generation)** asistanıdır.

---

## 🎯 Proje Vizyonu
Geleneksel yapay zekâ modellerinin aksine, **Aether AI** sadece doğrulanmış tıbbi dökümanlar üzerinden konuşur. Bu sayede tıbbi konularda "halüsinasyon" (yanlış bilgi uydurma) riskini minimize ederek, kullanıcılara kaynak odaklı ve güvenilir bilgiler sunar.

## 🚀 Öne Çıkan Özellikler
*   **Tamamen Kaynak Odaklı:** Verilen cevaplar doğrudan sistemdeki PDF rehberlere dayandırılır.
*   **Gelişmiş RAG Mimarisi:** Qdrant vektör veritabanı ve semantik arama teknolojisi.
*   **Yüksek Performans:** Groq API üzerinden Llama 3.3 70B modeli ile anlık ve detaylı yanıtlar.
*   **Modern Arayüz:** Kullanıcı dostu, temiz ve hızlı React (Vite) arayüzü.

## 🛠️ Teknoloji Yığını
| Katman | Teknoloji |
| :--- | :--- |
| **Frontend** | React (Vite), Tailwind CSS, Lucide Icons |
| **Backend** | FastAPI (Python 3.10+) |
| **LLM Motoru** | Groq Cloud (Llama-3.3-70b-versatile) |
| **Vektör Veritabanı** | Qdrant (Docker üzerinden) |
| **Embedding Model** | Sentence-Transformers (all-MiniLM-L6-v2) |

---

## 📂 Proje Yapısı
```text
Chatbot/
├── backend/            # FastAPI Sunucusu & RAG Mantığı
│   ├── docs/           # Tıbbi PDF Kaynakları
│   ├── venv/           # Python Sanal Ortamı
│   ├── main.py         # API Uç Noktaları
│   ├── rag_engine.py   # Arama ve LLM Mantığı
│   └── ingest_pdfs.py  # PDF'leri Vektörize Etme Aracı
├── frontend/           # React Uygulaması (Vite)
└── .env                # API Anahtarları ve Yapılandırma
```

---

## ⚙️ Kurulum ve Çalıştırma

Sistemi ayağa kaldırmak için aşağıdaki adımları sırasıyla uygulayın:

### 1. Vektör Veritabanını Başlatın (Qdrant)
Docker yüklü terminalinizde Qdrant konteynerini çalıştırın:
```powershell
docker run -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

### 2. Verileri İndeksleyin (Ingestion)
PDF dökümanlarını vektör veritabanına yüklemek için (sadece ilk kurulumda veya yeni dosya eklendiğinde gereklidir):
```powershell
cd backend
.\venv\Scripts\python ingest_pdfs.py
```

### 3. Backend Servisini Başlatın
API sunucusunu çalıştırmak için:
```powershell
cd backend
.\venv\Scripts\python main.py
```
*Backend şu adreste çalışacaktır: `http://localhost:8000`*

### 4. Frontend Uygulamasını Başlatın
Yeni bir terminalde arayüzü başlatın:
```powershell
cd frontend
npm install  # (İlk kurulumda gerekli)
npm run dev
```
*Uygulamaya şu adresten erişebilirsiniz: `http://localhost:5173`*

---

## 🏥 Kapsanan Tıbbi Alanlar
Sistem şu an aşağıdaki resmi rehberler üzerinde uzmanlaşmıştır:
*   Diyabet ve Şeker Hastalığı Yönetimi.
*   Kalp ve Damar Hastalıkları Beslenme Protokolleri.
*   Obezite ile Mücadele ve Egzersiz Stratejileri.
*   Kronik Hastalıklarda Fiziksel Aktivite Rehberliği.

## 📄 Lisans
Bu proje **MIT Lisansı** ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.

---

**⚠️ Önemli Uyarı:** Bu uygulama bilgilendirme amaçlıdır. Tıbbi kararlar almadan önce mutlaka profesyonel bir sağlık uzmanına danışılmalıdır.
