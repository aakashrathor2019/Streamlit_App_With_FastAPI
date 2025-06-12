import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
BACKEND_URL = "http://localhost:8000/upload_pdf/"

st.title("📄 RAG PDF Q&A Bot")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file:
    if st.button("Submit PDF"):
        with st.spinner("Uploading..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post(BACKEND_URL, files=files)

            if response.status_code == 200:
                st.success("✅ PDF uploaded and stored successfully!")
            else:
                st.error("❌ Upload failed!")
