"""
Configuration for Deal Advisor Intelligence Engine.
Supports any OpenAI-compatible provider (GPT, Claude, DeepSeek, etc.).
"""

import os
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """LLM provider configuration."""
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4-turbo"
    temperature: float = 0.4
    max_tokens: int = 4096

    @classmethod
    def from_env(cls, prefix: str = "DEAL_ADVISOR") -> "LLMConfig":
        return cls(
            api_key=os.getenv(f"{prefix}_API_KEY", os.getenv("OPENAI_API_KEY", "")),
            base_url=os.getenv(f"{prefix}_BASE_URL", os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")),
            model=os.getenv(f"{prefix}_MODEL", os.getenv("OPENAI_MODEL", "gpt-4-turbo")),
            temperature=float(os.getenv(f"{prefix}_TEMPERATURE", "0.4")),
            max_tokens=int(os.getenv(f"{prefix}_MAX_TOKENS", "4096")),
        )


@dataclass
class ResearchConfig:
    """Research behavior configuration."""
    max_search_queries: int = 15       # per research dimension
    max_sources_per_query: int = 5
    max_total_sources: int = 50
    review_rounds: int = 2             # reviewer passes
    writer_temperature: float = 0.6    # higher for writing
    scorer_temperature: float = 0.2    # lower for scoring

    # Estimated token budgets for research planning
    @property
    def estimated_tokens_quick(self) -> int:
        return 2_000_000

    @property
    def estimated_tokens_standard(self) -> int:
        return 8_000_000

    @property
    def estimated_tokens_deep(self) -> int:
        return 18_000_000


# Provider presets for quick configuration
PROVIDER_PRESETS = {
    "deepseek": LLMConfig(
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        temperature=0.3,
        max_tokens=8192,
    ),
    "openai": LLMConfig(
        base_url="https://api.openai.com/v1",
        model="gpt-4o",
        temperature=0.3,
        max_tokens=8192,
    ),
}

# Agent role descriptions (for multi-agent prompts)
AGENT_ROLES = {
    "research_planner": """You are a senior investment research planner. 
Given a target company/sector and investment question, generate a comprehensive 
research plan with specific search queries organized by dimension:
1. Market Opportunity & Size
2. Team & Leadership
3. Product & Technology
4. Traction & Growth Metrics
5. Competitive Landscape
6. Financial Health & Unit Economics
7. Risk Factors

Output as JSON with dimension name -> list of search queries.""",

    "analyst": """You are a senior investment analyst.
Given raw research data from web sources, synthesize insights for ONE specific 
dimension of deal evaluation. Be specific, cite sources, separate facts from 
opinions, and identify data gaps.""",

    "scorer": """You are a deal scoring engine.
Given analysis for one dimension, assign:
- Score: 0.0 to 10.0 (decimal)
- Confidence: 0.0 to 1.0 (how reliable is the data)
- Key evidence: list of supporting facts
- Key risks: list of concerns
Be conservative. Default to lower confidence when data is sparse.""",

    "memo_writer": """You are a senior investment memo writer.
Given scored analysis across all dimensions, write an investment-grade memo 
in markdown. Follow this structure:
1. Executive Summary (3-5 sentences)
2. Company Overview
3. Market Analysis
4. Competitive Landscape
5. Business Model
6. Team Analysis
7. Financial Overview
8. Traction Metrics
9. Risk Analysis
10. Investment Thesis
11. Recommendation (STRONG_BUY / BUY / HOLD / PASS / STRONG_PASS)

Be specific, data-driven, and opinionated. Hedge appropriately when data is thin.""",

    "reviewer": """You are an investment memo reviewer.
Check the memo for:
- Logical consistency
- Unsupported claims
- Missing critical analysis
- Overly optimistic/pessimistic bias
- Citation quality
Return specific revision instructions.""",
}
