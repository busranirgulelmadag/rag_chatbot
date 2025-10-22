@echo off
call .venv\Scripts\activate
python src\ingest.py
streamlit run app.py
