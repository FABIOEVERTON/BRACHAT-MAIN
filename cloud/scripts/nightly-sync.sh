#!/usr/bin/env bash
set -euo pipefail

REPO="/Users/mac/brachat-main"
DATE=$(date +%F)
LOG="/tmp/brachat-nightly-${DATE}.log"

cd "$REPO"

echo "[$(date +%H:%M)] === NIGHTLY SYNC $DATE ===" >> "$LOG"

# Stage only state files + schedule
git add agents/ writings_studies/official_schedule.md integrations/state.json .opencode/ 2>>"$LOG"

if git diff --cached --quiet; then
    echo "[$(date +%H:%M)] No changes to commit" >> "$LOG"
else
    git commit -m "nightly sync $DATE" 2>>"$LOG"
    git push origin main 2>>"$LOG"
    echo "[$(date +%H:%M)] Pushed to origin + huggingface" >> "$LOG"
fi

# Sync VPS repo + restart services
ssh -o ConnectTimeout=5 -i /Users/mac/brachat-main/integrations/apis/ssh-key-2026-06-10.key opc@147.15.18.252 '
    git -C /opt/brachat/repo pull origin main 2>/dev/null
    sudo systemctl is-active brachat-dashboard.service && sudo systemctl restart brachat-dashboard.service 2>/dev/null || true
    echo "VPS: repo pulled, dashboard restarted"
' 2>>"$LOG" && echo "[$(date +%H:%M)] VPS sync done" >> "$LOG" || echo "[$(date +%H:%M)] VPS sync skipped (offline?)" >> "$LOG"

echo "[$(date +%H:%M)] === DONE ===" >> "$LOG"
cat "$LOG"
