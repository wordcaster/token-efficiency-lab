r"""
Token counter utility (v0.1)

Run examples (PowerShell, from repo root):
  .\.venv\Scripts\python.exe .\src\token_count.py --text "Hello world"
  .\.venv\Scripts\python.exe .\src\token_count.py --file .\examples\sample.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path

import tiktoken


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    enc = tiktoken.get_encoding(encoding_name)
    return len(enc.encode(text))


def main() -> None:
    parser = argparse.ArgumentParser(description="Count tokens for a text string or file.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text to count tokens for.")
    group.add_argument("--file", type=str, help="Path to a text file to count tokens for.")
    parser.add_argument(
        "--encoding",
        type=str,
        default="cl100k_base",
        help="tiktoken encoding name (default: cl100k_base).",
    )
    args = parser.parse_args()

    if args.text is not None:
        text = args.text
        source = "inline text"
    else:
        p = Path(args.file)
        text = p.read_text(encoding="utf-8")
        source = str(p)

    n = count_tokens(text, args.encoding)
    print(f"source: {source}")
    print(f"encoding: {args.encoding}")
    print(f"chars: {len(text)}")
    print(f"tokens: {n}")


if __name__ == "__main__":
    main()
