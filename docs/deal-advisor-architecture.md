# Deal Advisor Intelligence Engine — Architecture

This repository customizes GPT-Researcher into an autonomous deal diligence system.

## Agent Pipeline

1. **Research Planner** — expands an investment question into dimension-specific research queries.
2. **Retriever / Source Collector** — uses GPT-Researcher's retrievers, scrapers, and source validation.
3. **Dimension Analysts** — synthesize evidence for market, team, product, traction, moat, financial, and risk dimensions.
4. **Scoring Agent** — assigns conservative 0–10 scores and confidence estimates with evidence/risk lists.
5. **Memo Writer** — generates an investment-grade memo.
6. **Reviewer** — detects unsupported claims, bias, missing diligence, and weak citations.
7. **Publisher** — exports Markdown/PDF/DOCX.

## Why this is token-intensive

A full deep diligence run may involve 25–40 search queries, each producing multiple source summaries, followed by multi-round analysis, scoring, memo writing, and review. Estimated budget:

- Quick: 2M+ tokens
- Standard: 6–10M tokens
- Deep: 12–20M tokens

## MiMo Integration

MiMo can be used through OpenAI-compatible config:

```bash
export DEAL_ADVISOR_BASE_URL="https://api.mimo.xiaomi.com/v1"
export DEAL_ADVISOR_API_KEY="..."
export DEAL_ADVISOR_MODEL="MiMo-7B-RL"
```

GPT-Researcher also supports `OPENAI_BASE_URL`, allowing the existing research pipeline to route calls into MiMo-compatible endpoints.
