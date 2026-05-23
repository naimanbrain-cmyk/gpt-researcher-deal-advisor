#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p proof
{
  echo "# Deal Advisor Proof Run"
  echo "Generated: $(date -u)"
  echo
  echo "## Git Commit"
  git rev-parse --short HEAD || true
  echo
  echo "## Repo Status"
  git status --short || true
  echo
  echo "## Demo Run"
  python -m deal_advisor.cli --task examples/deal_advisor_task.json --output examples/sample_outputs/perplexity_deal_memo.md --print-plan
  echo
  echo "## Sample Output Head"
  sed -n '1,80p' examples/sample_outputs/perplexity_deal_memo.md
} | tee proof/deal_advisor_proof.txt
