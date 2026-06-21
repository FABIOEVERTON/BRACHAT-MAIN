# BUILDER — BRACHÁT Software Factory

Operational root for all autonomous projects.
Scripts, daemons and cloud live here.

## Scripts
- `clickup_daemon.py` — ClickUp synchronization (CRUD tasks)

## Daemons (launchd macOS)
Run on Mac while powered on:
- `com.brachat.opencode.plist` → EZRA bridge (Telegram → Zen API)
- `com.brachat.nice.plist` → NICE bridge (Telegram → Zen API)

## Cloud (VPS — 24/7)
Bridges can also run on a VPS (Hetzner €4/month):
→ `cloud/README.md` contains full deploy instructions.
