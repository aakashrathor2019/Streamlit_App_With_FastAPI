from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import tempfile
import os
import psycopg2

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(await file.read())
    temp_file.close()


    loader = PyPDFLoader(temp_file.name)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    print("CONNECTION---->>",conn)
    cursor = conn.cursor()
    print("CURSOR---->>",cursor)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            filetype TEXT NOT NULL,
            filedata BYTEA NOT NULL
        );
    """)
    conn.commit()

    with open(temp_file.name, 'rb') as f:
        binary_data = f.read()
        cursor.execute(
            "INSERT INTO files (filename, filetype, filedata) VALUES (%s, %s, %s)",
            (file.filename, file.content_type, binary_data)
        )
        conn.commit()
    cursor.close()
    conn.close()

    os.remove(temp_file.name)

    return {"status": "success", "message": "PDF uploaded and stored"}
