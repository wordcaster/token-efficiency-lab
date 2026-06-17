# CONCEPTS

> Mining source for a future retrieval-ready documentation case study. Not a spec.

Durable, still-relevant ideas distilled from this repo's existing experiments and tools. Each entry is a one-line description plus a pointer to the file it was drawn from. Nothing here is invented beyond what the repo already contains.

## Token measurement as a baseline and quality signal
Count tokens (not characters) before optimizing, and record a baseline so later changes can be measured against it.
Source: `src/token_count.py`, `experiments/exp002_sample_doc_baseline.md`

## Context budgeting with guardrails
Set an explicit token budget for what goes into a prompt, check whether the input fits, and trim deterministically when it does not.
Source: `src/budget.py`

## Chunk independence (chunk on natural boundaries)
Split on paragraph boundaries and keep whole chunks, so each unit stays self-contained and nothing is truncated mid-sentence.
Source: `src/chunk.py`

## Retrieval instead of dumping (retrieval-lite)
Score chunks by query relevance and select only the relevant subset under budget, rather than sending the whole document — here via keyword overlap, with no embeddings or APIs.
Source: `src/retrieval_lite.py`, `experiments/exp005_retrieval_lite.md`

## Budget-aware packing strategy
When filling a budget, rank by relevance first, then prefer smaller chunks so more useful content fits.
Source: `src/retrieval_lite.py`, `src/context_builder.py`

## Explainable, composable context pipeline
Compose the steps — chunking, relevance scoring, budget packing, context output — into one predictable pipeline, and present selected chunks in original order for readability.
Source: `src/context_builder.py`, `experiments/exp006_context_builder.md`

## Relevance-scoring trade-offs (synonym expansion)
A small synonym map raises relevance recall at near-zero token cost; the trade-off is simple-and-predictable scoring versus broader semantic recall.
Source: `src/context_builder.py`, `experiments/exp007_synonym_scoring.md`
