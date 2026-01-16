# Exp006 — Context Builder (unified pipeline)

Date: 2026-01-16  
Encoding: cl100k_base  
Tool: src/context_builder.py  
Input: examples/sample_doc.txt  
Budget: 120 tokens  
Query: "offline sync conflicts resolve"

Result:
- chunks_total: 5
- chunks_selected: 1
- tokens_used: 36
- selected_chunks:
  - chunk 4 (score=2, tokens=36)

Notes:
- Unified pipeline: chunking → retrieval-lite scoring → budget packing → context output.
- Current relevance is keyword overlap (fast + explainable).
- Next improvement: small synonym map + optional budget fill (--allow-zero-score).
