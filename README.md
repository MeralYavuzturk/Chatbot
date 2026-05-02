# 🌌 Aether AI: Kronik Hastalıklar ve Yaşam Rehberi

**Aether AI**, modern yapay zekâ teknolojilerini resmi sağlık protokolleriyle birleştiren etkileşimli bir asistan projesidir. **Chatbot-Workshop** kapsamında geliştirilen bu sistem, kullanıcıların kronik hastalık yönetimi ve sağlıklı yaşam hakkındaki sorularına, Sağlık Bakanlığı'nın bilimsel dökümanlarını temel alarak yanıt verir.

---

## 🎯 Proje Vizyonu
Geleneksel yapay zekâ modellerinin aksine, **Aether AI** "Retrieval-Augmented Generation" (**RAG**) mimarisini kullanarak sadece doğrulanmış tıbbi dökümanlar üzerinden konuşur. Temel amacımız, karmaşık tıbbi verileri herkesin erişebileceği, güvenilir ve etkileşimli bir sohbet deneyimine dönüştürmektir.

## 🛠️ Teknik Özellikler
*   **Mimari**: RAG (Retrieval-Augmented Generation) tabanlı bilgi geri getirimi.
*   **Veri Kaynağı**: Sağlık Bakanlığı resmi bilimsel yayınları ve rehberleri.
*   **Güvenilirlik**: Sadece sistemdeki dökümanlardan beslenerek halüsinasyon riskini minimize eder.
*   **Etkileşim**: Kullanıcı dostu, modern ve dinamik bir sohbet arayüzü.

## 📂 Proje Yapısı
Proje, dökümanda belirtilen modern chatbot katmanlarına uygun olarak yapılandırılmıştır:
*   **Backend**: FastAPI ile yönetilen API katmanı.
*   **AI Motoru**: LangChain ve Vektör Veritabanı entegrasyonu.
*   **Frontend**: React (Vite) ile geliştirilen etkileşimli kullanıcı arayüzü.

## 🏥 Kapsanan Temel Alanlar
Aether AI şu konularda uzmanlaşmış döküman setlerini kullanır:
*   Diyabet ve Şeker Hastalığı Yönetimi.
*   Kalp ve Damar Hastalıkları Protokolleri.
*   Obezite ve Sağlıklı Yaşam Stratejileri.
*   Kronik Hastalıklarda Egzersiz ve Aktivite Rehberliği.

## 🛠️ Teknik Mimari
Proje, dökümanda belirtilen **Modern Chatbot Mimarisi** ve **Temiz Kod** prensipleri üzerine inşa edilmiştir:

*   **Backend:** FastAPI ile hızlı, modüler ve asenkron bir API katmanı.
*   **AI Katmanı:** LangChain ve LlamaIndex kullanılarak oluşturulan, bağlam odaklı RAG motoru.
*   **Vektör Veritabanı:** Bilgilerin hızlı ve semantik geri getirimi için ChromaDB.
*   **Frontend:** React (Vite) tabanlı, Framer Motion ile güçlendirilmiş  ve etkileşimli kullanıcı arayüzü.

## 📂 Dosya Yapısı
```text
saglik-rag-projesi/
├── backend/            # RAG Motoru & FastAPI API Katmanı
├── frontend/           # React & Antigravity UI Bileşenleri
├── database/           # ChromaDB Vektör Veri Deposu
└── docs/               # Sağlık Bakanlığı Resmi PDF Dökümanları


