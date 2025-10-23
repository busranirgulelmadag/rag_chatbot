# 💬 RAG Chatbot — Gemini + LangChain + Chroma + Streamlit

**Canlı Uygulama:** **https://mentalchat.streamlit.app/**

Kısa, anlaşılır ve **kaynak parça** referanslı cevaplar veren; CSV/TXT verinizle çalışan **RAG** tabanlı bir sohbet uygulaması.

---

## 🖼️ Ön İzleme

> Görselin görünmesi için **proje kökünde** `docs/mentalchat-ui.png` dosyası bulunmalıdır.
![WhatsApp Görsel 2025-10-23 saat 02 49 14_a5497ab9](https://github.com/user-attachments/assets/ed2c7b0a-5e62-4248-8183-2b2b20374088)

![Uygulama ekran görüntüsü](docs/mentalchat-ui.png)

---

## 📚 İçindekiler
- [Özellikler](#özellikler)
- [Mimari](#mimari)
- [Veri Seti](#veri-seti)
- [Kurulum (Yerel)](#kurulum-yerel)
- [Çalıştırma](#çalıştırma)
- [Streamlit Cloud (Deploy)](#streamlit-cloud-deploy)
- [Yapı](#yapı)
- [İpuçları](#ipuçları)
- [Sorun Giderme](#sorun-giderme)
- [Yol Haritası](#yol-haritası)

---

## ✨ Özellikler
- **RAG Pipeline:** Soru → Chroma ile en ilgili parçalar → Gemini ile yanıt
- **Gemini modelleri:** Varsayılan `gemini-2.5-flash`, embedding `text-embedding-004`
- **Ayarlanabilir:** Sol panelden **model** ve **k (kaynak sayısı)**
- **Tek tık indeks:** “**Veriyi Yeniden İndeksle**” butonuyla veri güncelleme sonrası hızlı re-indeks

---

## 🧩 Mimari

```mermaid
flowchart LR
    U[👤 Kullanıcı] -->|Soru| UI[🖥️ Streamlit UI]
    UI -->|Arama| RET[🔎 Chroma Retriever (k)]
    RET -->|Bağlam| LLM[🤖 Gemini (gemini-2.5-flash)]
    LLM -->|Yanıt + Kaynak| UI
    Metin parçalama: RecursiveCharacterTextSplitter (chunk_size=800, overlap=120)
    Vektör veritabanı: Chroma (kalıcı klasör: chroma_db/)
    LangChain 0.2+ uyumlu retriever.invoke(query) çağrısı kullanılır.

##Veri Seti

    Varsayılan: data/Mental_Health_FAQ (1).csv (ruh sağlığı SSS)
    İsteğe bağlı: data/ içerisine yeni CSV/TXT dosyaları ekleyin. Sonrasında Veriyi Yeniden İndeksle.
##Kurulum (Yerel)

    python -m venv .venv
    .\.venv\Scripts\activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

##Çalıştırma
    python src\ingest.py     # data/ içeriğini indeksler (Chroma)
    streamlit run app.py     # arayüzü başlatır

##Streamlit Cloud (Deploy)

    Streamlit Cloud → New app (Repo: bu proje, Main file path: app.py)
    Secrets (TOML):
    GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
    App açılınca Veriyi Yeniden İndeksle butonuna bir kez basın.
    Canlı: https://mentalchat.streamlit.app/
##Yapı
.
├─ app.py                 # Streamlit arayüz + RAG akışı
├─ src/
│  └─ ingest.py           # CSV/TXT loader, splitter, embedding, Chroma persist
├─ data/                  # Veri dosyaları (CSV/TXT)
├─ requirements.txt
├─ README.md
└─ .env.example
