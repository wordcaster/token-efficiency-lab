r"""
Budget guardrails (v0.1)

Goal: estimate if an input fits within a token budget and optionally trim.

Examples (PowerShell, from repo root):
  .\.venv\Scripts\python.exe .\src\budget.py --text "Hello world" --max 50
  .\.venv\Scripts\python.exe .\src\budget.py --file .\examples\sample_doc.txt --max 120
  .\.venv\Scripts\python.exe .\src\budget.py --file .\examples\sample_doc.txt --max 120 --trim
"""

from __future__ import annotations

import argparse
from pathlib import Path

import tiktoken


def encode(text: str, encoding_name: str) -> list[int]:
    enc = tiktoken.get_encoding(encoding_name)
    return enc.encode(text)


def decode(tokens: list[int], encoding_name: str) -> str:
    enc = tiktoken.get_encoding(encoding_name)
    return enc.decode(tokens)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check if text/file fits a token budget; optionally trim.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Input text.")
    group.add_argument("--file", type=str, help="Path to input file (utf-8).")
    parser.add_argument("--encoding", type=str, default="cl100k_base", help="tiktoken encoding (default: cl100k_base).")
    parser.add_argument("--max", type=int, required=True, help="Max allowed tokens for the input.")
    parser.add_argument("--trim", action="store_true", help="Trim input to fit the budget and print trimmed text.")
    args = parser.parse_args()

    if args.text is not None:
        text = args.text
        source = "inline text"
    else:
        p = Path(args.file)
        text = p.read_text(encoding="utf-8")
        source = str(p)

    toks = encode(text, args.encoding)
    n = len(toks)

    print(f"source: {source}")
    print(f"encoding: {args.encoding}")
    print(f"max_tokens: {args.max}")
    print(f"tokens: {n}")
    print(f"fits: {n <= args.max}")

    if args.trim and n > args.max:
        trimmed = decode(toks[: args.max], args.encoding)
        print("\n--- trimmed_text_start ---")
        print(trimmed)
        print("--- trimmed_text_end ---")


if __name__ == "__main__":
    main()
