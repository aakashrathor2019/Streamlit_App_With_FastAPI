import psycopg2

conn = psycopg2.connect(
    dbname="postgres",  
    user="postgres",
    password="newpassword",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("""
CREATE SCHEMA IF NOT EXISTS documents;

CREATE TABLE IF NOT EXISTS documents.files (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    filetype TEXT,
    filedata BYTEA  -- allows the storage of binary strings or what is typically thought of as raw bytes
);
""")

conn.commit()
cursor.close()
conn.close()

