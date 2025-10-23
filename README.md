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

##RAG Chatbot Çalışma Kılavuzu
(Gemini + LangChain + Chroma + Streamlit)
Bu kılavuz, projeyi yerelde çalıştırma, veri ekleme/indeksleme, Streamlit Cloud’a deploy, ayarlar ve sorun giderme adımlarını tek sayfada özetler.

1) Gereksinimler
Python 3.10–3.12
pip (Python paket yöneticisi)
Google AI Studio’dan Gemini API anahtarı (Developer API)
(Deploy için) GitHub ve Streamlit Community Cloud hesabı
##Çalıştırma
    python src\ingest.py     # data/ içeriğini indeksler (Chroma)
    streamlit run app.py     # arayüzü başlatır

##Kullandığım Teknolojiler
LLM: Google Gemini (gemini-2.5-flash)
Embedding: Google text-embedding-004
Vektör DB: Chroma (lokal, chroma_db/)
Çerçeve: LangChain ≥ 0.2 (LCEL; retriever.invoke)
UI: Streamlit (web arayüz + yeniden indeksleme butonu)
Kod: Python 3.10–3.12
Deploy: Streamlit Community Cloud
Yapılandırma: .env veya Streamlit Secrets (TOML)

##Web Arayüzü & Product Kılavuzu
1) Ürün Özeti
MentalChat, kurum içi CSV/TXT içeriklerinden RAG (Retrieval-Augmented Generation) yöntemiyle kısa, anlaşılır ve kaynak parçalarla destekli yanıt üreten bir web sohbet uygulamasıdır. Kullanıcı bir soru yazar; uygulama önce vektör veritabanından en ilgili metin parçalarını bulur, ardından Gemini modeli bu bağlamla güvenilir yanıt üretir.
Canlı: https://mentalchat.streamlit.app/

2) Hedef Kullanıcılar & Değer Önermesi
Danışan/öğrenci/çalışan: Ruh sağlığı SSS içeriklerini hızlı ve sade öğrenir.
Eğitmen/KO: Kurum içi içeriklerin aynı dille, uydurmadan anlatılmasını sağlar.
Operasyon: Veri güncellemesini (CSV ekleyip yeniden indeksleme) kendileri yapabilir.
Değer: Yanıtlar veriye dayalıdır; “bağlamımda yok” politikasıyla uydurma azaltılır; kaynak parça görünürlüğüyle şeffaflık sağlanır.

3) Arayüz ve Ana Akış
3.1 Giriş Ekranı
Başlık: “RAG Chatbot (Gemini + Chroma)”
Soru Alanı: “Soru” metin girişi (ör. Depresyon belirtileri nelerdir?)
Butonlar:
Sor: Sorguyu çalıştırır.
Veriyi Yeniden İndeksle: data/ klasöründeki CSV/TXT içeriğini yeniden indeksler (veri güncellendiğinde bir kez tıklayın).

3.2 Yan Panel (Ayarlar)
Model: Varsayılan gemini-2.5-flash (metin üretimi). İsteğe göre değiştirilebilir.
Kaynak sayısı (k): Retriever’ın kaç parça döndüreceği (öneri: 3–6).

3.3 Sonuç Ekranı
Yanıt: Kısa, maddeli ve net bir çıktı.
Kaynak parçaları (expander): Getirilen metin parçalarının özet/snippet’ları ve (varsa) temel metaverileri. Kullanıcı cevapların hangi bağlama dayandığını görür.

4) Kullanım Adımları (Son Kullanıcı)
Tarayıcıda mentalchat.streamlit.app adresine gidin.
Sol yandaki Ayarlar bölümünden gerekirse Model ve k değerini ayarlayın.
“Soru” alanına sorunuzu yazın → Sor.
“Yanıt” bölümünü okuyun; gerekirse “Kaynak parçaları”nı açarak dayanak metni görün.
Veri değiştiyse (CSV eklediniz/yenilediniz), Veriyi Yeniden İndeksle butonuna bir kez tıklayın ve ardından sorularınızı tekrar sorun.
Örnek sorular
“Depresyon nedir? 4 maddeyle özetle.”
“Anksiyete ile normal kaygı arasındaki fark nedir?”
“Panik atağın tipik belirtileri neler?”
“Bağlamında yoksa ‘bağlamımda yok’ de: Bipolar DSM-5 ölçütleri?”

5) İçerik Yönetimi (Operasyon)
Yeni veri ekleme: CSV/TXT dosyalarını repo’daki data/ klasörüne ekleyin ve push edin (ya da yerelde bu klasöre kopyalayın).
İndeksleme:
Yerel: python src/ingest.py (veya app’te Veriyi Yeniden İndeksle).
Cloud: Uygulama açıldıktan sonra Veriyi Yeniden İndeksle butonunu bir kez tıklayın.
CSV ayarları (gerekirse):
CSV_DELIMITER=";" → noktalı virgül ayracı kullanan dosyalar için
CSV_ENCODING="cp1254" → Türkçe içeriklerde encoding sorunu varsa

6) Etkileşim Kuralları & UX İlkeleri
Uydurmama: Bağlamda bilgi yoksa model “bağlamımda yok” der.
Kısalık: Yanıtlar kısa, maddeli ve ana fikri özetleyen yapıda tutulur.
Şeffaflık: “Kaynak parçaları” paneli her yanıttan sonra erişilebilir.
Hata Mesajları:
API Key yok/yanlış → “GOOGLE_API_KEY bulunamadı…” uyarısı (Secrets veya .env’e ekleyin).
Redacted hata (embedding) → genellikle key env’e set edilmemiştir; ensure_api_key() bunu otomatik yapar (mevcut sürümde etkin).

7) Rol ve Yetkiler (Basit Model)
Kullanıcı: Soru sorma, kaynak parçalarını görme.
İçerik Operatörü: data/ klasörünü güncelleme, yeniden indeksleme.
Yönetici (opsiyonel): Streamlit Secrets yönetimi (API key, opsiyonel APP_PASSWORD).
Basit parola koruması istenirse Secrets’a APP_PASSWORD konur; uygulama yan panelde şifre isteyebilir.

8) Başarı Ölçütleri (KPI) & Geri Bildirim
Cevaplama kalitesi: Kullanıcı memnuniyeti/geri bildirim puanları (1–5).
İlk denemede doğru yanıt oranı (%).
Yanıt süresi (ortalama, p95).
Hallucination şikâyet sayısı (düşmesi hedeflenir).
Kullanım: Günlük/haftalık sorgu sayısı, tekrarlı kullanıcı oranı.
Geri bildirim toplama (opsiyonel):
Sonuç kartına “Faydalıydı / Faydalı değildi” kısa oylaması ve yorum alanı.
Basit bir Google Form bağlantısı.

9) Erişilebilirlik, Güvenlik ve Gizlilik
Erişilebilirlik: Kısa başlıklar, madde işaretleri, klavye odaklı kullanım; metinlerin kontrastı korunur.
Gizlilik: Public repo ise data/ herkes tarafından görülebilir. Hassas veri varsa private repo önerilir.
Sır Yönetimi: API anahtarları .env/Secrets içinde tutulur; repoya girmez.
Rate Limit: Gerekirse yanıt başına gecikme/limit eklenebilir (opsiyonel).

10) Performans & Ölçeklenebilirlik (Kullanıcı Etkisi)
Hız: k yükseldikçe yanıt biraz uzayabilir; 3–6 arası dengelidir.
Büyük Veri: Chroma tek nodda onbinlerce parça ile çalışır. Daha büyük yükte dış vektör DB çözümlerine geçilebilir (PGVector, Pinecone gibi).

11) SSS (Kullanıcı Gözüyle)
“Veri ekledim ama görünmüyor?”
→ Veriyi Yeniden İndeksle butonuna basın.

“Çok uzun cevap veriyor”
→ Soruya “kısa, 4 madde” gibi kısıt ekleyin.

“Cevapta kaynak görmüyorum”
→ “Kaynak parçaları” panelini açın.

“Yanıt yanlış”
→ Soruyu daraltın; gerekirse k değerini 4–6 yapın; verinin data/da mevcut olduğundan emin olun.

12) Yol Haritası (Ürün Geliştirme)
Dosya çeşitleri: PDF/DOCX yükleyici
Arama: Hibrid (BM25 + dense), MMR ve yeniden sıralama
Kaynak vurgusu: Yanıt içinde pasaj/ID vurguları
Basit kimlik doğrulama: Kurumsal erişim kontrolü
Analitik: Sorgu/yanıt telemetrisi, kalite panosu
Özet: MentalChat, veriye dayalı, kısa ve kaynaklı yanıtları sade bir arayüzle sunar. Son kullanıcı sadece soru sorar; operasyon ekibi data/ya dosya ekleyip tek tıkla indeksler. Böylece içeriğin güncelliği ve yanıtların doğruluğu kolayca korunur.
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
