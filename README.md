# Token Efficiency Lab

## Status: superseded, with the useful parts moving on

This started as a lab for measuring, budgeting, and compressing the context going into LLM prompts. The literal tooling here has largely been overtaken by the field: prompt caching now does most of what manual compression promised, tokenizers are free and built in, and the conversation has shifted from counting tokens to context engineering and retrieval quality.

What held up is the thinking underneath: budget what goes into context, retrieve instead of dumping, and structure content so it survives chunking. Those ideas are being carried forward into retrieval-ready documentation work, where the same discipline improves both retrieval accuracy and token cost. See CONCEPTS.md for the distilled, still-useful ideas.

Kept public as a record of the exploration. Not actively maintained as a tool.

A practical, experiment-driven exploration of token-efficient context building for LLM systems.

## Why this exists

LLM applications often fail due to excess context, ignored budgets, or unpredictable costs.

This repo demonstrates guardrails-first, explainable context pipelines.

## Pipeline

Document -> Token Count -> Budget -> Chunking -> Retrieval-lite -> Context

## How to run

.venv\Scripts\python src\context_builder.py --file examples\sample_doc.txt --query "offline sync conflicts resolve" --max 120

## Experiments

Exp001–Exp007 documented in /experiments

## Status

Actively evolving

