#!/usr/bin/env bash
set -euo pipefail

# Day One payload launcher for TrueAlpha-spiral.
#
# Default behavior:
# 1) Verify the working tree is clean.
# 2) Merge a release gate PR (default: #106) using squash strategy.
# 3) Trigger deterministic release workflow (default: blank.yml) on a target ref.
#
# Usage:
#   GH_REPO="owner/repo" ./scripts/day_one_payload.sh
#   GH_REPO="owner/repo" PR_NUMBER=106 WORKFLOW_FILE=blank.yml RELEASE_REF=main ./scripts/day_one_payload.sh
#   GH_REPO="owner/repo" SKIP_MERGE=1 ./scripts/day_one_payload.sh

: "${GH_REPO:?Set GH_REPO to <owner>/<repo> before running.}"
PR_NUMBER="${PR_NUMBER:-106}"
WORKFLOW_FILE="${WORKFLOW_FILE:-blank.yml}"
RELEASE_REF="${RELEASE_REF:-main}"
SKIP_MERGE="${SKIP_MERGE:-0}"

require_bin() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required binary: $1" >&2
    exit 1
  fi
}

require_bin gh
require_bin git

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree must be clean before Day One payload." >&2
  exit 1
fi

echo "[1/2] Release gate check..."
if [[ "$SKIP_MERGE" == "1" ]]; then
  echo "SKIP_MERGE=1 set. Skipping PR merge gate."
else
  gh pr merge "$PR_NUMBER" \
    --repo "$GH_REPO" \
    --squash \
    --delete-branch
  echo "Merged PR #$PR_NUMBER in $GH_REPO"
fi

echo "[2/2] Trigger deterministic workflow..."
gh workflow run "$WORKFLOW_FILE" \
  --repo "$GH_REPO" \
  --ref "$RELEASE_REF"

echo "Day One payload initiated: workflow '$WORKFLOW_FILE' on ref '$RELEASE_REF'."
