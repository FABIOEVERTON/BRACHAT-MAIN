#!/bin/bash
# [BR-AGENT-DAEMON] Install/Uninstall BRACHAT launchd daemons
# Usage:
#   ./install.sh install          # Load all plists
#   ./install.sh uninstall        # Unload all plists
#   ./install.sh status           # Check loaded plists

CMD=${1:-status}
LAUNCHD_DIR="$(cd "$(dirname "$0")" && pwd)"
PLISTS="com.brachat.ezra.temporal com.brachat.agent.artur"

case "$CMD" in
  install)
    for p in $PLISTS; do
      plist="$LAUNCHD_DIR/$p.plist"
      if [ -f "$plist" ]; then
        launchctl load -w "$plist" 2>/dev/null
        echo "[LAUNCHD] Loaded $p"
      fi
    done
    echo "[LAUNCHD] To add more agents: edit this script's PLISTS list"
    ;;
  uninstall)
    for p in $PLISTS; do
      plist="$LAUNCHD_DIR/$p.plist"
      if [ -f "$plist" ]; then
        launchctl unload -w "$plist" 2>/dev/null
        echo "[LAUNCHD] Unloaded $p"
      fi
    done
    ;;
  status)
    echo "=== BRACHAT Daemons ==="
    for p in $PLISTS; do
      load=$(launchctl list | grep "$p" || echo "  not loaded")
      echo "  $p: $load"
    done
    echo ""
    echo "=== Screen sessions ==="
    screen -ls 2>/dev/null | grep "br-" || echo "  none"
    echo ""
    echo "=== Heartbeat ==="
    cat "/Users/mac/brachat-main/agents/orchestrator_agents/ezra/heartbeat.json" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(f\"  Last: {d.get('timestamp','never')}\"); print(f\"  Schedule: M{d.get('schedule_month','?')}D{d.get('schedule_day','?')}\"); print(f\"  Blockers: {len(d.get('blockers',[]))}\")" 2>/dev/null || echo "  no heartbeat yet"
    ;;
  *)
    echo "Usage: $0 {install|uninstall|status}"
    exit 1
    ;;
esac
