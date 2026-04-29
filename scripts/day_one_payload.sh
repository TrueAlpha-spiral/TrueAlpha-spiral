#!/usr/bin/env bash
set -euo pipefail

# Day One payload launcher for TrueAlpha-spiral.
#
# PR #106 is historical substrate (already merged). The Day One gate is now
# the release-docker / sovereign-intent / receipt-emission process run against
# the active head SHA.
#
# Default behavior:
# 1) Verify the working tree is clean.
# 2) Resolve the active head SHA (or accept HEAD_SHA override).
# 3) Trigger deterministic release workflow against that SHA.
#
# Usage:
#   GH_REPO="owner/repo" ./scripts/day_one_payload.sh
#   GH_REPO="owner/repo" WORKFLOW_FILE=release-docker.yaml RELEASE_REF=main ./scripts/day_one_payload.sh
#   GH_REPO="owner/repo" HEAD_SHA=<sha> ./scripts/day_one_payload.sh

: "${GH_REPO:?Set GH_REPO to <owner>/<repo> before running.}"
WORKFLOW_FILE="${WORKFLOW_FILE:-blank.yml}"
RELEASE_REF="${RELEASE_REF:-main}"
HEAD_SHA="${HEAD_SHA:-$(git rev-parse HEAD)}"

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

echo "[1/2] Active head SHA: $HEAD_SHA"
echo "      PR #106 is historical substrate (already merged); skipping merge gate."

echo "[2/2] Trigger deterministic workflow against head SHA..."
gh workflow run "$WORKFLOW_FILE" \
  --repo "$GH_REPO" \
  --ref "$HEAD_SHA"

echo "Day One payload initiated: workflow '$WORKFLOW_FILE' on ref '$HEAD_SHA'."
