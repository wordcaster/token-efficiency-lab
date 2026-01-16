# Exp007 — Synonym-aware retrieval-lite scoring

Date: 2026-01-16  
Encoding: cl100k_base  
Tool: src/context_builder.py (synonym-aware tokenize_words)  
Input: examples/sample_doc.txt  
Budget: 120 tokens  
Query: "offline sync conflicts resolve"

Result:
- chunks_selected: 1
- tokens_used: 36
- selected_chunk:
  - chunk 4 (score=5, tokens=36)

Notes:
- Added a small synonym map (e.g., sync ≈ synchronize, resolve ≈ resolved).
- Increased relevance score (2 → 5) without changing selected context or token cost.
- Design trade-off: simple + predictable vs. broader semantic recall.
