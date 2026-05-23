"""
Data models for Deal Advisor Intelligence Engine.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ResearchDepth(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


class DealType(str, Enum):
    STARTUP = "startup"
    PUBLIC_COMPANY = "public_company"
    ACQUISITION = "acquisition"
    PARTNERSHIP = "partnership"
    MARKET_ENTRY = "market_entry"


@dataclass
class DealResearchRequest:
    """Input for a deal research task."""
    target: str
    sector: str = "technology"
    deal_type: DealType = DealType.STARTUP
    research_depth: ResearchDepth = ResearchDepth.STANDARD
    investment_question: str = "Should we invest?"
    regions: list[str] = field(default_factory=lambda: ["Global"])
    comparables: list[str] = field(default_factory=list)
    max_budget_usd: Optional[float] = None
    custom_context: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "DealResearchRequest":
        return cls(
            target=data["target"],
            sector=data.get("sector", "technology"),
            deal_type=DealType(data.get("deal_type", "startup")),
            research_depth=ResearchDepth(data.get("research_depth", "standard")),
            investment_question=data.get("investment_question", "Should we invest?"),
            regions=data.get("regions", ["Global"]),
            comparables=data.get("comparables", []),
            max_budget_usd=data.get("max_budget_usd"),
            custom_context=data.get("custom_context", ""),
        )


@dataclass
class DimensionScore:
    """Score for a single evaluation dimension."""
    name: str
    score: float
    confidence: float
    evidence: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)

    def clamp(self) -> "DimensionScore":
        self.score = max(0.0, min(10.0, float(self.score)))
        self.confidence = max(0.0, min(1.0, float(self.confidence)))
        return self


@dataclass
class DealScoreCard:
    """Aggregated scoring across all dimensions."""
    market_opportunity: DimensionScore = field(default_factory=lambda: DimensionScore("Market Opportunity", 0, 0))
    team_quality: DimensionScore = field(default_factory=lambda: DimensionScore("Team Quality", 0, 0))
    product_strength: DimensionScore = field(default_factory=lambda: DimensionScore("Product Strength", 0, 0))
    traction: DimensionScore = field(default_factory=lambda: DimensionScore("Traction & Growth", 0, 0))
    competitive_moat: DimensionScore = field(default_factory=lambda: DimensionScore("Competitive Moat", 0, 0))
    financial_health: DimensionScore = field(default_factory=lambda: DimensionScore("Financial Health", 0, 0))
    risk_profile: DimensionScore = field(default_factory=lambda: DimensionScore("Risk Profile", 0, 0))

    def dimensions(self) -> list[DimensionScore]:
        return [
            self.market_opportunity,
            self.team_quality,
            self.product_strength,
            self.traction,
            self.competitive_moat,
            self.financial_health,
            self.risk_profile,
        ]

    @property
    def overall_score(self) -> float:
        dims = self.dimensions()
        weights = [0.20, 0.15, 0.20, 0.15, 0.10, 0.10, 0.10]
        return round(sum(d.score * w for d, w in zip(dims, weights)), 2)

    @property
    def overall_confidence(self) -> float:
        dims = self.dimensions()
        return round(sum(d.confidence for d in dims) / len(dims), 2) if dims else 0.0

    @property
    def recommendation(self) -> str:
        score = self.overall_score
        confidence = self.overall_confidence
        if confidence < 0.35:
            return "HOLD - NEED MORE DATA"
        if score >= 8.2:
            return "STRONG_BUY"
        if score >= 7.0:
            return "BUY"
        if score >= 5.5:
            return "HOLD"
        if score >= 4.0:
            return "PASS"
        return "STRONG_PASS"


@dataclass
class Source:
    """A research source/citation."""
    url: str
    title: str
    snippet: str = ""
    relevance: float = 0.0
    source_type: str = "web"


@dataclass
class DealMemo:
    """Final output: investment-grade deal memo."""
    title: str
    executive_summary: str
    company_overview: str
    market_analysis: str
    competitive_landscape: str
    business_model: str
    team_analysis: str
    financial_overview: str
    traction_metrics: str
    risk_analysis: str
    investment_thesis: str
    recommendation: str
    scorecard: DealScoreCard = field(default_factory=DealScoreCard)
    sources: list[Source] = field(default_factory=list)
    research_questions: list[str] = field(default_factory=list)
    token_usage_estimate: int = 0
