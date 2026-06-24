#!/bin/bash
set -euo pipefail

# Auto-stage, commit, and push agent+opencode changes
# Usage: ./git_sync.sh [commit message suffix]

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
SUFFIX="${1:-sync}"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")

git add agents/ .opencode/ .playwright-mcp/ 2>/dev/null || true

if git diff --cached --quiet; then
  echo "[git_sync] nothing to commit"
  exit 0
fi

git commit -m "[BR-EZRA-001] auto ${SUFFIX} ${TIMESTAMP}"
git push origin "$BRANCH" 2>/dev/null && echo "[git_sync] pushed to ${BRANCH}" || echo "[git_sync] push skipped (no remote or offline)"
