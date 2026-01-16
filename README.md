# Token Efficiency Lab

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

