import os
from dotenv import load_dotenv
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

SYSTEM_PROMPT = """Aşağıdaki bağlamı KESİNLİKLE kullanarak soruyu Türkçe yanıtla.
Uydurma yapma; bağlamda yoksa "bağlamımda yok" de.
Cevabın kısa, açık ve kaynak parçalarının ana fikirlerini özetlesin.
Gerekirse maddeler kullan.
"""

def ensure_api_key():
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyasına ekleyin.")
        st.stop()

def get_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004")
    return Chroma(persist_directory="chroma_db", embedding_function=embeddings)

def rag_answer(query, model_name="gemini-2.5-flash", k=4):
    vs = get_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query) 
    context = "\\n\\n".join([d.page_content for d in docs])

    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
    prompt = f"{SYSTEM_PROMPT}\\n\\n[BAĞLAM]\\n{context}\\n\\n[SORU]\\n{query}\\n\\n[Cevap]:"
    resp = llm.invoke(prompt)
    return resp.content, docs

st.set_page_config(page_title="RAG Chatbot (Gemini)", page_icon="💬")
st.title("💬 RAG Chatbot (Gemini + Chroma)")

ensure_api_key()

st.sidebar.header("Ayarlar")
model_name = st.sidebar.text_input("Model", value="gemini-2.5-flash")
top_k = st.sidebar.slider("Kaynak sayısı (k)", 2, 8, 4, 1)

st.write("Bir şeyler sor:")
user_q = st.text_input("Soru", placeholder="Örn: Depresyon belirtileri nelerdir?")

col1, col2 = st.columns(2)
with col1:
    run = st.button("Sor")
with col2:
    reindex = st.button("Veriyi Yeniden İndeksle (data/ değiştiyse)")

if reindex:
    import subprocess, sys
    with st.spinner("İndeksleniyor..."):
        r = subprocess.run([sys.executable, "src/ingest.py"], capture_output=True, text=True)
        st.code((r.stdout or "") + "\\n" + (r.stderr or ""))
    st.success("İndeksleme bitti.")

if run and user_q.strip():
    with st.spinner("Yanıt hazırlanıyor..."):
        answer, docs = rag_answer(user_q, model_name=model_name, k=top_k)
    st.markdown("### Yanıt")
    st.write(answer)

    with st.expander("Kaynak parçaları"):
        for i, d in enumerate(docs, 1):
            meta = ", ".join([f"{k}={v}" for k, v in (d.metadata or {}).items() if isinstance(v, (str, int, float))])
            st.markdown(f"**Parça {i}:** {'(' + meta + ')' if meta else ''}\\n\\n{d.page_content[:1000]}{' ...' if len(d.page_content) > 1000 else ''}")
