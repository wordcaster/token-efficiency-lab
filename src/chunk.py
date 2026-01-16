r"""
Chunking utility (v0.1)

Goal: split text into chunks and select full chunks under a token budget.

Examples (PowerShell, from repo root):
  .\.venv\Scripts\python.exe .\src\chunk.py --file .\examples\sample_doc.txt --max 120
"""

from __future__ import annotations

import argparse
from pathlib import Path

import tiktoken


def count_tokens(text: str, encoding_name: str) -> int:
    enc = tiktoken.get_encoding(encoding_name)
    return len(enc.encode(text))


def main() -> None:
    parser = argparse.ArgumentParser(description="Chunk text and keep full chunks under a token budget.")
    parser.add_argument("--file", type=str, required=True, help="Path to input file (utf-8).")
    parser.add_argument("--encoding", type=str, default="cl100k_base", help="tiktoken encoding.")
    parser.add_argument("--max", type=int, required=True, help="Max allowed tokens.")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    used = 0
    kept_chunks: list[str] = []

    for i, chunk in enumerate(paragraphs, start=1):
        n = count_tokens(chunk, args.encoding)
        if used + n > args.max:
            break
        kept_chunks.append(chunk)
        used += n

    print(f"source: {args.file}")
    print(f"encoding: {args.encoding}")
    print(f"max_tokens: {args.max}")
    print(f"chunks_total: {len(paragraphs)}")
    print(f"chunks_kept: {len(kept_chunks)}")
    print(f"tokens_used: {used}")

    print("\n--- selected_text_start ---")
    print("\n\n".join(kept_chunks))
    print("--- selected_text_end ---")


if __name__ == "__main__":
    main()
