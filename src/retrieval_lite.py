r"""
Retrieval-lite chunk selection (v0.1)

No embeddings, no APIs. Uses simple keyword overlap scoring.

Example (PowerShell, from repo root):
  .\.venv\Scripts\python.exe .\src\retrieval_lite.py --file .\examples\sample_doc.txt --query "offline sync conflict resolution" --max 120
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import tiktoken


WORD_RE = re.compile(r"[a-zA-Z0-9]+")


def tokenize_words(s: str) -> set[str]:
    return {w.lower() for w in WORD_RE.findall(s)}


def count_tokens(text: str, encoding_name: str) -> int:
    enc = tiktoken.get_encoding(encoding_name)
    return len(enc.encode(text))


@dataclass
class Chunk:
    idx: int
    text: str
    tokens: int
    score: int


def main() -> None:
    p = argparse.ArgumentParser(description="Select most relevant chunks under a token budget (retrieval-lite).")
    p.add_argument("--file", type=str, required=True, help="Path to input file (utf-8).")
    p.add_argument("--query", type=str, required=True, help="Query describing what we care about.")
    p.add_argument("--max", type=int, required=True, help="Max tokens budget for selected chunks.")
    p.add_argument("--encoding", type=str, default="cl100k_base", help="tiktoken encoding.")
    args = p.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    raw_chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

    q_words = tokenize_words(args.query)

    chunks: list[Chunk] = []
    for i, ch in enumerate(raw_chunks, start=1):
        words = tokenize_words(ch)
        score = len(words & q_words)
        toks = count_tokens(ch, args.encoding)
        chunks.append(Chunk(idx=i, text=ch, tokens=toks, score=score))

    # Sort by score desc, then shorter chunks first (pack more), then stable by original idx
    ranked = sorted(chunks, key=lambda c: (-c.score, c.tokens, c.idx))

    used = 0
    chosen: list[Chunk] = []
    for c in ranked:
        if c.score == 0:
            continue
        if used + c.tokens > args.max:
            continue
        chosen.append(c)
        used += c.tokens

    # Present chosen chunks in original order for readability
    chosen_sorted = sorted(chosen, key=lambda c: c.idx)

    print(f"source: {args.file}")
    print(f"encoding: {args.encoding}")
    print(f"query: {args.query}")
    print(f"max_tokens: {args.max}")
    print(f"chunks_total: {len(raw_chunks)}")
    print(f"chunks_selected: {len(chosen_sorted)}")
    print(f"tokens_used: {used}")

    print("\n--- selected_chunks ---")
    for c in chosen_sorted:
        print(f"[chunk {c.idx}] score={c.score} tokens={c.tokens}")

    print("\n--- selected_text_start ---")
    print("\n\n".join(c.text for c in chosen_sorted))
    print("--- selected_text_end ---")


if __name__ == "__main__":
    main()
