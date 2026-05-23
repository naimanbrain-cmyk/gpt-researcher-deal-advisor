#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m deal_advisor.cli   --task examples/deal_advisor_task.json   --output examples/sample_outputs/perplexity_deal_memo.md   --print-plan
