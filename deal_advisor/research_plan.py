"""
Research planning layer for Deal Advisor Intelligence Engine.
The live version can hand these query sets to GPT-Researcher retrievers.
"""

from .schemas import DealResearchRequest, ResearchDepth


DIMENSIONS = [
    "Market Opportunity",
    "Team Quality",
    "Product Strength",
    "Traction & Growth",
    "Competitive Moat",
    "Financial Health",
    "Risk Profile",
]


def build_research_plan(request: DealResearchRequest) -> dict[str, list[str]]:
    target = request.target
    sector = request.sector
    regions = " OR ".join(request.regions)
    comps = " OR ".join(request.comparables) if request.comparables else f"{sector} competitors"

    base_plan = {
        "Market Opportunity": [
            f"{sector} market size growth forecast {regions}",
            f"{target} total addressable market {sector}",
            f"{sector} adoption trends customer demand pain points",
        ],
        "Team Quality": [
            f"{target} founders leadership team background",
            f"{target} CEO CTO founder previous companies education",
            f"{target} hiring engineering product leadership",
        ],
        "Product Strength": [
            f"{target} product features technology architecture reviews",
            f"{target} customers product differentiation {sector}",
            f"{target} patents research technical moat",
        ],
        "Traction & Growth": [
            f"{target} revenue users growth funding customers",
            f"{target} ARR valuation funding round investors",
            f"{target} customer case studies partnerships",
        ],
        "Competitive Moat": [
            f"{target} vs {comps}",
            f"{sector} competitive landscape leading startups incumbents",
            f"{target} defensibility switching costs network effects",
        ],
        "Financial Health": [
            f"{target} funding runway burn rate revenue business model",
            f"{target} pricing unit economics gross margin",
            f"{target} investors cap table latest valuation",
        ],
        "Risk Profile": [
            f"{target} risks lawsuits regulatory controversy",
            f"{sector} regulatory risk platform risk market risk",
            f"{target} negative reviews churn layoffs security incident",
        ],
    }

    if request.research_depth == ResearchDepth.QUICK:
        return {k: v[:2] for k, v in base_plan.items()}
    if request.research_depth == ResearchDepth.DEEP:
        deep_additions = {
            "Market Opportunity": [f"{sector} analyst report Gartner McKinsey BCG market"],
            "Team Quality": [f"{target} LinkedIn leadership hiring departures"],
            "Product Strength": [f"{target} API documentation developer adoption GitHub"],
            "Traction & Growth": [f"{target} web traffic app downloads social growth"],
            "Competitive Moat": [f"{target} pricing comparison alternatives"],
            "Financial Health": [f"{target} financial statements SEC filings if public"],
            "Risk Profile": [f"{target} data privacy security compliance risk"],
        }
        for dim, queries in deep_additions.items():
            base_plan[dim].extend(queries)
    return base_plan


def estimate_token_usage(request: DealResearchRequest, query_count: int) -> int:
    if request.research_depth == ResearchDepth.QUICK:
        return max(2_000_000, query_count * 150_000)
    if request.research_depth == ResearchDepth.DEEP:
        return max(12_000_000, query_count * 450_000)
    return max(6_000_000, query_count * 300_000)
