# RAG Chatbot (Gemini + Chroma + Streamlit)

This project uses **Google AI Studio (Gemini API)** for chat and **text-embedding-004** for embeddings.
It supports both **CSV** and **TXT** files under the `data/` folder.

## Quickstart (Windows / CMD)
```bat
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
Create `.env` from `.env.example` and set `GOOGLE_API_KEY`.
Put your CSV/TXT files into `data/` (a copy of your CSV may already be included).

Build index:
```bat
python src\ingest.py
```

Run app:
```bat
streamlit run app.py
```
The app runs on `http://127.0.0.1:8601` (change in `.streamlit/config.toml` if needed).

## Notes
- If your CSV uses `;` as separator, set `CSV_DELIMITER=;` in `.env`.
- If you see Turkish encoding issues, try `CSV_ENCODING=cp1254`.
