# Exp005 — Retrieval-lite chunk selection under budget

Date: 2026-01-16  
Encoding: cl100k_base  
Tool: src/retrieval_lite.py  
Input: examples/sample_doc.txt  
Budget: 120 tokens  
Query: "offline sync conflicts resolve"

Result:
- chunks_total: 5
- chunks_selected: 1
- tokens_used: 36
- selected_chunks:
  - chunk 4 (score=2, tokens=36)

Selected text quality:
- Highly relevant chunk returned (offline sync + conflict handling).
- No mid-sentence truncation (chunk boundary preserved).

Notes:
- v0.1 uses keyword overlap scoring (fast + explainable).
- Next improvement: add a tiny synonym map (e.g., sync ≈ synchronize) and/or allow top-N even when score=0 if budget remains.
