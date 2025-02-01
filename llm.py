import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

LLM_CHUNK_SIZE = int(os.getenv('LLM_CHUNK_SIZE', 1000))
LLM_CHUNK_OVERLAP = int(os.getenv('LLM_CHUNK_OVERLAP', 200))

OPENAI_KEY = os.getenv('OPENAI_KEY')
OPENAI_TIMEOUT = os.getenv('OPENAI_TIMEOUT', 10)
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')
OPENAI_EMBEDDING_URL = os.getenv('OPENAI_EMBEDDING_URL', 'https://api.openai.com/v1/embeddings')
OPENAI_CHAT_URL = os.getenv('OPENAI_CHAT_URL', 'https://api.openai.com/v1/chat/completions')

HEADERS = {
    "Authorization": f"Bearer {OPENAI_KEY}",
    "Content-Type": "application/json"
}

def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=LLM_CHUNK_SIZE,
        chunk_overlap=LLM_CHUNK_OVERLAP
    )
    chunks = text_splitter.split_text(text)
    return chunks

def call_api(url, payload):
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error generating embedding: {e}")
        raise

def get_embedding(text):
    payload = {
        "model": OPENAI_EMBEDDING_MODEL,
        "input": text
    }
    response = call_api(OPENAI_EMBEDDING_URL, payload)
    return response["data"][0]["embedding"]

def chat(messages):
    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
    }
    response = call_api(OPENAI_CHAT_URL, payload)
    return response["choices"][0]["message"]["content"]
