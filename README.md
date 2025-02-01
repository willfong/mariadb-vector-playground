# MariaDB Vector Search with ChatGPT

A simple playground to experiment with vector searching using MariaDB and ChatGPT. This project demonstrates how to:

- Scrape and ingest reference data from webpages (e.g., Wikipedia)
- Chunk the text and generate vector embeddings using ChatGPT
- Store these embeddings in MariaDB with vector search capabilities
- Execute vector search queries to retrieve relevant text chunks
- Combine search results with a ChatGPT prompt to generate a response

## Features

- Web Scraping: Download and convert webpages (e.g., Wikipedia) into Markdown.
- Data Chunking & Embeddings: Split the scraped data into chunks and generate vector embeddings using ChatGPT.
- Vector Search: Store embeddings in MariaDB and perform similarity searches.
- Chat Integration: Use search results as context to generate a full response via ChatGPT.

## Prerequisites

Before you begin, ensure you have:

- MariaDB with Vector Search: Version 11.7 or later is required.
- ChatGPT API Token: You can obtain one here.
- Basic LLM Familiarity: Understanding of large language models and embeddings is helpful.

## Setup Instructions

Environment Setup:

1. Clone the repository.
2. Create a .env file in the root directory and modify it as needed. Below is an example configuration:

   ```sh
   # Database configuration
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_USER=root
   DB_PASS=
   DB_NAME=playground

   # Search parameters
   SEARCH_LIMIT=10

   # Chunking parameters for LLM
   LLM_CHUNK_SIZE=1000
   LLM_CHUNK_OVERLAP=200

   # OpenAI API configuration
   OPENAI_KEY=sk-svcacct-ABC...123
   OPENAI_TIMEOUT=10
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   OPENAI_EMBEDDING_URL=https://api.openai.com/v1/embeddings
   OPENAI_CHAT_URL=https://api.openai.com/v1/chat/completions
   ```

3. Set up the Python environment:

   ```sh
   python -m venv .venv
   source .venv/bin/activate # Use `.venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

## Database Schema

Create the following table in your MariaDB instance. This schema stores the text data along with its corresponding embedding vector:

```sql
CREATE TABLE `files` (
`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
`data` mediumtext NOT NULL,
`embedding` vector(1536) NOT NULL,
PRIMARY KEY (`id`),
VECTOR KEY `embedding` (`embedding`) `M`=6 `DISTANCE`=cosine
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
```

Note: The embedding vector length (1536) and the use of cosine distance are based on ChatGPT’s embedding recommendations. Adjust these parameters if needed for your environment.

## Seeding Initial Data

You can seed the database with reference data by scraping any webpage. For example, to scrape a Wikipedia page about MariaDB:

```sh
python3 scrape.py https://en.wikipedia.org/wiki/MariaDB | python3 playground.py --embed
```

- `scrape.py`: Downloads the webpage and converts it to Markdown.
- `playground.py --embed`: Reads the Markdown input, chunks the text (based on LLM_CHUNK_SIZE), generates embeddings via ChatGPT, and stores the data in MariaDB.

You are free to use any URL that interests you.

## Running Searches

To test the vector search, run:

```sh
python3 playground.py --search "Tell me about dinosaurs"
```

This will query the database for matching text chunks. The “similarity” values returned can help verify that the data is coming from your database and not directly from the LLM. For example, a high similarity value (above 1.0) indicates a weak match.

For a search that should match your seeded data more precisely, try:

```sh
python3 playground.py --search "Who created MariaDB?"
```

A lower similarity value (below 1.0) means a stronger match.

## Generating a Chat Response

You can also generate a full response using the search results as context. In this basic example, the same prompt is sent to both the vector search and ChatGPT.

```sh
python3 playground.py --prompt "Who created MariaDB?"
```

Sample Output

```text
╭──────────────────────────── Search query ─────────────────────────────╮
│ Who created MariaDB?                                                  │
╰───────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────── Results ───────────────────────────────╮
│ MariaDB was created by Michael "Monty" Widenius, who is one of the    │
│ founders of MySQL AB. He initiated the development of MariaDB after   │
│ concerns arose over MySQL's acquisition by Oracle Corporation. The    │
│ initial development was supported by other original MySQL developers  │
│ as well as various organizations.                                     │
╰───────────────────────────────────────────────────────────────────────╯
```

## Schema Details

- Embedding Length: The schema uses an embedding vector length of 1536, which matches ChatGPT’s vector embedding size. [source](https://platform.openai.com/docs/guides/embeddings#how-to-get-embeddings)
- Distance Metric: The schema is set up to use the cosine distance function for vector similarity, as recommended by ChatGPT. [source](https://platform.openai.com/docs/guides/embeddings#which-distance-function-should-i-use)

## Notes

- Customization: Adjust the chunk size, overlap, and other parameters in your `.env` file to fit your use case.
- Extensibility: While this example uses a single prompt for both search and chat, you can extend this playground to include more sophisticated retrieval-augmented generation (RAG) techniques.
- Debugging: Ensure MariaDB is configured to support vector search and that your API keys are correct.
