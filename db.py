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


# def search(user_id, embedding, limit):
#     """Search for messages"""
#     results = message_search(user_id, embedding, limit)
#     ret = []
#     for row in results:
#         ret.extend(json.loads(row["conversation_history"]))
#     pprint(ret)
#     return ret

# def message_search(user_id, embedding, limit):
#     """Vector search messages"""
#     cur = conn.cursor(dictionary=True)
#     query = "SELECT created_at, conversation_history FROM chat_history WHERE user_id = ? ORDER BY VEC_DISTANCE_EUCLIDEAN(embedding, VEC_FromText(?)) LIMIT ?"
#     payload = (user_id, embedding, limit)
#     cur.execute(query, payload)
#     result = cur.fetchall()
#     return result


# def message_last(user_id):
#     """Get the last messages"""
#     cur = conn.cursor(dictionary=True)
#     query = "SELECT conversation_history FROM chat_history WHERE user_id = ? ORDER BY created_at DESC LIMIT 1"
#     cur.execute(query, (user_id,))
#     result = cur.fetchone() or {"conversation_history": "[]"}
#     return result

# def calls_insert(user_id, name, payload):
#     """Insert tool calls"""
#     cur = conn.cursor()
#     query = "INSERT INTO tool_calls (user_id, name, payload) VALUES (?,?,?)"
#     params = (user_id, name, payload)
#     cur.execute(query, params)
#     conn.commit()

# def user_details_get(user_id):
#     """Get user details"""
#     cur = conn.cursor(dictionary=True)
#     query = "SELECT * FROM user_details WHERE user_id = ?"
#     cur.execute(query, (user_id,))
#     result = cur.fetchone()
#     return result

# def user_details_insert(user_id, important):
#     """Insert user details"""
#     cur = conn.cursor()
#     query = "INSERT INTO user_details (user_id, important) VALUES (?,?) ON DUPLICATE KEY UPDATE important = ?"
#     params = (user_id, important, important)
#     cur.execute(query, params)
#     conn.commit()

# def prompt_history_insert(user_id, prompt, response):
#     """Insert prompt history"""
#     cur = conn.cursor()
#     query = "INSERT INTO prompt_history (user_id, prompt, response) VALUES (?,?,?)"
#     params = (user_id, prompt, response)
#     cur.execute(query, params)
#     conn.commit()
