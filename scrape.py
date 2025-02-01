#!/usr/bin/env python
import argparse
import html2text
import requests

def main():
    parser = argparse.ArgumentParser(
        description="Convert an HTML webpage to Markdown and print it to stdout."
    )
    parser.add_argument(
        "url",
        help="The URL of the HTML webpage to convert."
    )
    args = parser.parse_args()

    try:
        response = requests.get(args.url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    html_content = response.text
    markdown_text = html2text.html2text(html_content)

    print(markdown_text)

if __name__ == "__main__":
    main()