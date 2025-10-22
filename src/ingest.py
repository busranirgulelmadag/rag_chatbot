import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

DB_DIR = "chroma_db"
DATA_DIR = "data"

def load_txt_docs():
    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader,
        use_multithreading=True,
        show_progress=True
    )
    return loader.load()

def load_csv_docs():
    load_dotenv()
    delimiter = os.getenv("CSV_DELIMITER", ",")
    encoding  = os.getenv("CSV_ENCODING", "utf-8")
    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.csv",
        loader_cls=CSVLoader,
        loader_kwargs={
            "csv_args": {"delimiter": delimiter},
            "encoding": encoding,
        },
        use_multithreading=True,
        show_progress=True
    )
    return loader.load()

def build_vectorstore():
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in .env")

    docs_txt = load_txt_docs()
    docs_csv = load_csv_docs()
    docs = docs_txt + docs_csv
    if not docs:
        raise ValueError("data/ klasöründe .txt veya .csv bulunamadı.")

    print(f"→ Yüklenen döküman sayısı: TXT={len(docs_txt)}  CSV={len(docs_csv)}  TOPLAM={len(docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=['\n\n', '\n', ' ', '']
    )
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004")
    vs = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_DIR)
    vs.persist()
    print(f"✅ İndeksleme tamam: {len(chunks)} parça → {DB_DIR}")

if __name__ == "__main__":
    Path(DB_DIR).mkdir(exist_ok=True)
    build_vectorstore()
