# Token Efficiency Lab

Hands-on experiments + small Python tools for measuring, budgeting, compressing, and retrieving context for LLM prompts.

## What this repo is
This is a learning + portfolio repo focused on practical token/cost efficiency:
- token counting and budgeting
- prompt compression strategies
- chunking + retrieval-lite (send only what matters)
- simple evaluation notes (quality vs cost)

## Repo structure
- `src/` — scripts and utilities
- `examples/` — sample inputs/outputs and demo reports
- `experiments/` — experiment logs with before/after token counts
- `docs/` — notes and playbooks

## Current status
v0.1 (in progress): repo scaffolding + first token counting experiment next.

## Principles
- Measure first (tokens in/out), then optimize.
- Prefer structure over verbosity.
- Treat quality and cost as a trade-off to manage, not a guess.

## Next milestones
- [ ] Token counter script + baseline log
- [ ] Budget guardrails script
- [ ] Compression experiments
- [ ] Chunking + retrieval-lite demo
