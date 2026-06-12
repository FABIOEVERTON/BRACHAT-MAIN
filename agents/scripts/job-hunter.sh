#!/bin/bash
# Job Hunter Automation — dispatched by launchd daily at 07:00
# Mr. Justus — 15 apps/day across 7 platforms

LOGFILE="/tmp/com.brachat.jobhunter.log"
echo "[$(date)] JUSTUS START" >> "$LOGFILE"

cd /Users/mac/brachat-main

/opt/homebrew/bin/opencode run --agent justus \
  "Justus, execute your full procedure from agents/job/justus/justus.md now" \
  >> "$LOGFILE" 2>&1

echo "[$(date)] JUSTUS END — Exit: $?" >> "$LOGFILE"
