r"""
Context Builder (v0.1)

Build token-budgeted context from a document given a query.
Uses retrieval-lite keyword overlap + chunk packing under budget.

Example (PowerShell, from repo root):
  .\.venv\Scripts\python.exe .\src\context_builder.py --file .\examples\sample_doc.txt --query "offline sync conflicts resolve" --max 120
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


def chunk_paragraphs(text: str) -> list[str]:
    # Simple, effective v0.1 chunking: split on blank lines
    return [c.strip() for c in text.split("\n\n") if c.strip()]


@dataclass
class Chunk:
    idx: int
    text: str
    tokens: int
    score: int


def rank_chunks(chunks: list[Chunk]) -> list[Chunk]:
    # Sort by relevance desc; then prefer smaller chunks to pack more; stable by original order
    return sorted(chunks, key=lambda c: (-c.score, c.tokens, c.idx))


def pack_under_budget(ranked: list[Chunk], max_tokens: int, allow_zero_score: bool) -> tuple[list[Chunk], int]:
    used = 0
    chosen: list[Chunk] = []

    for c in ranked:
        if (not allow_zero_score) and c.score == 0:
            continue
        if used + c.tokens > max_tokens:
            continue
        chosen.append(c)
        used += c.tokens

    # Return chosen in original order for readability
    chosen_sorted = sorted(chosen, key=lambda c: c.idx)
    return chosen_sorted, used


def main() -> None:
    p = argparse.ArgumentParser(description="Build token-budgeted context from a document using retrieval-lite.")
    p.add_argument("--file", type=str, required=True, help="Path to input file (utf-8).")
    p.add_argument("--query", type=str, required=True, help="Query describing what context is needed.")
    p.add_argument("--max", type=int, required=True, help="Max tokens budget for selected context.")
    p.add_argument("--encoding", type=str, default="cl100k_base", help="tiktoken encoding.")
    p.add_argument(
        "--allow-zero-score",
        action="store_true",
        help="If set, pack additional chunks even if score=0 (fills remaining budget).",
    )
    args = p.parse_args()

    doc = Path(args.file).read_text(encoding="utf-8")
    raw_chunks = chunk_paragraphs(doc)

    q_words = tokenize_words(args.query)

    chunks: list[Chunk] = []
    for i, ch in enumerate(raw_chunks, start=1):
        words = tokenize_words(ch)
        score = len(words & q_words)
        toks = count_tokens(ch, args.encoding)
        chunks.append(Chunk(idx=i, text=ch, tokens=toks, score=score))

    ranked = rank_chunks(chunks)
    chosen, used = pack_under_budget(ranked, args.max, args.allow_zero_score)

    print(f"source: {args.file}")
    print(f"encoding: {args.encoding}")
    print(f"query: {args.query}")
    print(f"max_tokens: {args.max}")
    print(f"chunks_total: {len(raw_chunks)}")
    print(f"chunks_selected: {len(chosen)}")
    print(f"tokens_used: {used}")

    print("\n--- selected_chunks ---")
    for c in chosen:
        print(f"[chunk {c.idx}] score={c.score} tokens={c.tokens}")

    print("\n--- context_start ---")
    print("\n\n".join(c.text for c in chosen))
    print("--- context_end ---")


if __name__ == "__main__":
    main()
