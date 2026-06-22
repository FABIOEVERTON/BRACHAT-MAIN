#!/usr/bin/env bash
set -euo pipefail

REPO="/Users/mac/brachat-main"
cd "$REPO"

git add agents/ .opencode/

if ! git diff --cached --quiet; then
    git commit -m "auto-sync $(date '+%F %H:%M')"
fi
