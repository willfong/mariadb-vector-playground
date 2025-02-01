import mariadb
import os
import sys
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

try:
    conn = mariadb.connect(
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

def files_chunk_insert(data, embedding):
    """Insert a message into the messages table"""
    cur = conn.cursor()
    query = "INSERT INTO files (data, embedding) VALUES (?,VEC_FromText(?))"
    payload = (data, embedding)
    cur.execute(query, payload)
    conn.commit()

def files_search(embedding, limit):
    """Vector search messages"""
    cur = conn.cursor(dictionary=True)
    query = "SELECT data, VEC_DISTANCE_EUCLIDEAN(embedding, VEC_FromText(?)) AS similarity FROM files ORDER BY VEC_DISTANCE_EUCLIDEAN(embedding, VEC_FromText(?)) LIMIT ?"
    payload = (embedding, embedding, limit)
    cur.execute(query, payload)
    results = cur.fetchall()
    return results
