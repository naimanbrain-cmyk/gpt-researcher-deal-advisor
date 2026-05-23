"""
Deterministic scoring fallback for offline demos.
In production, this layer is replaced/enhanced by LLM scorer agents.
"""

from .schemas import DealResearchRequest, DealScoreCard, DimensionScore


def _keyword_score(text: str, positives: list[str], negatives: list[str], base: float = 5.5) -> tuple[float, list[str], list[str]]:
    lower = text.lower()
    evidence = [f"Found positive signal: {p}" for p in positives if p.lower() in lower]
    risks = [f"Found risk signal: {n}" for n in negatives if n.lower() in lower]
    score = base + min(2.5, len(evidence) * 0.55) - min(2.5, len(risks) * 0.65)
    return max(0.0, min(10.0, score)), evidence, risks


def score_deal(request: DealResearchRequest, notes: str = "") -> DealScoreCard:
    context = " ".join([request.target, request.sector, request.custom_context, notes])
    ai_sector_bonus = 0.4 if any(x in request.sector.lower() for x in ["ai", "artificial intelligence", "agent", "automation"]) else 0.0

    market, market_ev, market_risk = _keyword_score(
        context,
        ["growth", "large market", "tam", "enterprise", "global", "demand", "ai"],
        ["shrinking", "commodity", "small market", "decline"],
        6.0 + ai_sector_bonus,
    )
    team, team_ev, team_risk = _keyword_score(
        context,
        ["ex-google", "ex-meta", "serial founder", "technical founder", "experienced", "research"],
        ["founder conflict", "turnover", "inexperienced"],
        5.7,
    )
    product, product_ev, product_risk = _keyword_score(
        context,
        ["api", "workflow", "automation", "proprietary", "real-time", "multi-agent", "open source"],
        ["undifferentiated", "buggy", "low retention"],
        6.0 + ai_sector_bonus,
    )
    traction, traction_ev, traction_risk = _keyword_score(
        context,
        ["revenue", "users", "customers", "partnership", "funding", "growth", "arr"],
        ["layoff", "churn", "stagnant", "declining"],
        5.5,
    )
    moat, moat_ev, moat_risk = _keyword_score(
        context,
        ["network effect", "switching cost", "data advantage", "brand", "ecosystem", "patent"],
        ["easy to copy", "crowded", "low switching cost"],
        5.2,
    )
    financial, financial_ev, financial_risk = _keyword_score(
        context,
        ["profitable", "gross margin", "revenue", "funding", "efficient", "enterprise pricing"],
        ["burn", "runway risk", "negative margin", "debt"],
        5.2,
    )
    risk_score, risk_ev, risk_risk = _keyword_score(
        context,
        ["compliance", "security", "governance", "transparent", "audited"],
        ["lawsuit", "regulatory", "privacy", "security incident", "controversy", "dependency"],
        6.0,
    )

    return DealScoreCard(
        market_opportunity=DimensionScore("Market Opportunity", market, 0.62, market_ev or [f"Sector focus: {request.sector}"], market_risk),
        team_quality=DimensionScore("Team Quality", team, 0.45, team_ev or ["Team requires deeper source verification"], team_risk),
        product_strength=DimensionScore("Product Strength", product, 0.55, product_ev or ["Product analysis based on provided context"], product_risk),
        traction=DimensionScore("Traction & Growth", traction, 0.40, traction_ev or ["Traction needs live-source verification"], traction_risk),
        competitive_moat=DimensionScore("Competitive Moat", moat, 0.42, moat_ev or ["Moat hypothesis needs competitor research"], moat_risk),
        financial_health=DimensionScore("Financial Health", financial, 0.35, financial_ev or ["Financial data likely private or incomplete"], financial_risk),
        risk_profile=DimensionScore("Risk Profile", risk_score, 0.50, risk_ev or ["Risk scan requires live web/news review"], risk_risk),
    )
