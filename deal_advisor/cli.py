"""
CLI entrypoint for Deal Advisor Intelligence Engine.

Usage:
  python -m deal_advisor.cli --task examples/deal_advisor_task.json --output examples/sample_outputs/perplexity_deal_memo.md
"""

import argparse
import json
from pathlib import Path

from .schemas import DealResearchRequest
from .memo_writer import build_deal_memo, render_markdown
from .research_plan import build_research_plan


def main() -> None:
    parser = argparse.ArgumentParser(description="Deal Advisor Intelligence Engine")
    parser.add_argument("--task", required=True, help="Path to JSON task file")
    parser.add_argument("--output", default="deal_memo.md", help="Path to output markdown memo")
    parser.add_argument("--notes", default="", help="Optional research notes/context string")
    parser.add_argument("--print-plan", action="store_true", help="Print generated research plan")
    args = parser.parse_args()

    task_path = Path(args.task)
    data = json.loads(task_path.read_text())
    request = DealResearchRequest.from_dict(data)

    if args.print_plan:
        plan = build_research_plan(request)
        print(json.dumps(plan, indent=2))

    memo = build_deal_memo(request, research_notes=args.notes)
    markdown = render_markdown(memo)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown)

    print(f"Deal memo written: {output_path}")
    print(f"Recommendation: {memo.recommendation}")
    print(f"Overall score: {memo.scorecard.overall_score}/10")
    print(f"Confidence: {memo.scorecard.overall_confidence}")
    print(f"Estimated token budget: {memo.token_usage_estimate:,}")


if __name__ == "__main__":
    main()
