"""Quick no-argument demo runner."""

from .schemas import DealResearchRequest, DealType, ResearchDepth
from .memo_writer import build_deal_memo, render_markdown


def run_demo() -> str:
    request = DealResearchRequest(
        target="Perplexity AI",
        sector="AI search and answer engine",
        deal_type=DealType.STARTUP,
        research_depth=ResearchDepth.DEEP,
        investment_question="Should we invest, partner, or monitor?",
        regions=["US", "Global", "SEA"],
        comparables=["Google", "OpenAI SearchGPT", "You.com", "Genspark", "Kagi"],
        custom_context="AI growth, enterprise demand, API, partnerships, funding, users, competitive market, regulatory and copyright risk",
    )
    memo = build_deal_memo(request)
    return render_markdown(memo)


if __name__ == "__main__":
    print(run_demo())
