# Implementation Plan — Deal Advisor Intelligence Engine

## Objective

Fork GPT-Researcher and customize it into an autonomous deal diligence engine suitable for the MiMo 100T Token Creator Incentive Program.

## MVP Scope

Implemented now:

1. Deal research request schema
2. Dimension-specific query planner
3. Deterministic offline scoring fallback
4. Markdown investment memo writer
5. CLI runner
6. Example Perplexity AI task
7. Sample output memo
8. MiMo submission draft and architecture docs

## Production Integration Plan

Next steps after GitHub push:

1. Connect research plan queries to GPT-Researcher retrievers.
2. Add LLM analyst agent per dimension.
3. Add source citation collector and evidence table.
4. Add reviewer/reviser loop.
5. Add PDF/DOCX export using GPT-Researcher publisher.
6. Configure MiMo endpoint through `OPENAI_BASE_URL` or `DEAL_ADVISOR_BASE_URL`.
7. Run 3 proof cases: Perplexity AI, xAI/Grok, and an Indonesian AI startup/market entry case.

## Why this fits MiMo 100T

The system is intentionally token-heavy and multi-agent: planner → retriever → analyst → scorer → writer → reviewer → publisher. Deep mode estimates 12M–20M tokens per full research run.
