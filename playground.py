#!/usr/bin/env python3
import argparse
import json
import os
import sys
from dotenv import load_dotenv
from pprint import pprint
from rich.console import Console
from rich.panel import Panel

import db
import llm

load_dotenv()
SEARCH_LIMIT = int(os.getenv('SEARCH_LIMIT', 10))

READ_FROM_STDIN = "__READ_FROM_STDIN__"

def embed(text):
    """
    Vectorize data and insert into the database.
    """
    chunks = llm.split_text(text)
    for i, chunk in enumerate(chunks):
        print(f"[Chunk {i+1}/{len(chunks)}] {chunk[:50].replace('\n', ' ')}...")
        embedding = llm.get_embedding(chunk)
        db.files_chunk_insert(chunk, json.dumps(embedding))

def prompt(prompt):
    """
    Send a prompt to the LLM with search results.
    """
    search_results = search(prompt)
    prompt = f"""Here are some search results for "{prompt}":\n\n

=== Start of search results ===
{json.dumps(search_results)}
=== End of search results ===

Base your answer only on the provided context. If the information needed is not in the context, please say so.

{prompt}
"""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = llm.chat(messages)
    return response

def search(query):
    """
    Search the vector database for the given prompt.
    """
    embedding = llm.get_embedding(query)
    results = db.files_search(embedding, SEARCH_LIMIT)
    return results

def main():
    console = Console()
    parser = argparse.ArgumentParser(
        description="Playground for testing MariaDB vector search with ChatGPT."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--embed',
        nargs='?',
        const=READ_FROM_STDIN,
        help="Embed text. If no text is provided, the script reads from stdin."
    )
    group.add_argument(
        '--search',
        help="Perform a vector search for the given text."
    )
    group.add_argument(
        '--prompt',
        help="Send search results to the LLM with a prompt."
    )

    args = parser.parse_args()
    print("\n")
    if args.embed is not None:
        if args.embed == READ_FROM_STDIN:
            if sys.stdin.isatty():
                print("Error: No input provided via stdin for --embed.", file=sys.stderr)
                sys.exit(1)
            text = sys.stdin.read()
        else:
            text = args.embed
        embed(text)

    if args.search is not None:
        panel = Panel(
            args.search,
            title="Search query",
            border_style="yellow"
        )
        console.print(panel)
        print("\n")
        results = search(args.search)
        for i, row in enumerate(results, start=1):
            panel = Panel(
                row['data'],
                title=f"Result: {i} (Similarity: {row['similarity']})",
                border_style="green"
            )
            console.print(panel)

    if args.prompt is not None:
        panel = Panel(
            args.prompt,
            title="Search query",
            border_style="yellow"
        )
        console.print(panel)
        print("\n")
        results = prompt(args.prompt)
        panel = Panel(
            results,
            title="Results",
            border_style="green"
        )
        console.print(panel)

    print("\n")

if __name__ == '__main__':
    main()