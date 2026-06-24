#!/bin/bash
# [BR-AGENT-DAEMON] start_agent.sh — Manage BRACHAT agent daemons
# Usage:
#   ./start_agent.sh start ezra              # Start temporal loop
#   ./start_agent.sh start agent artur       # Start Artur background daemon
#   ./start_agent.sh start agent aisio       # Start Aisio background daemon
#   ./start_agent.sh start agent baruch      # Start Baruch background daemon
#   ./start_agent.sh stop ezra               # Stop temporal loop
#   ./start_agent.sh stop agent artur        # Stop Artur daemon
#   ./start_agent.sh list                    # Show running daemons

CMD=$1
TYPE=${2:-}
NAME=${3:-}
AGENTS_DIR="$(cd "$(dirname "$0")" && pwd)"
EZRA_DIR="$AGENTS_DIR/orchestrator_agents/ezra"
if [ "$TYPE" = "ezra" ]; then
  SCREEN_SESSION="br-ezra-temporal"
elif [ "$TYPE" = "agent" ]; then
  SCREEN_SESSION="br-agent-${NAME}"
else
  SCREEN_SESSION="br-${TYPE}-${NAME}"
fi

case "$CMD" in
  start)
    if [ "$TYPE" = "ezra" ]; then
      screen -dmS "$SCREEN_SESSION" /usr/bin/python3 "$EZRA_DIR/temporal_loop.py"
      echo "[DAEMON] Started $SCREEN_SESSION (Ezra temporal loop)"
    elif [ "$TYPE" = "agent" ]; then
      screen -dmS "$SCREEN_SESSION" /usr/bin/python3 "$AGENTS_DIR/agent_daemon.py" --agent "$NAME" --interval 120
      echo "[DAEMON] Started $SCREEN_SESSION ($NAME agent daemon)"
    else
      echo "Usage: $0 start (ezra|agent <name>)"
      exit 1
    fi
    ;;
  stop)
    screen -S "$SCREEN_SESSION" -X quit 2>/dev/null
    echo "[DAEMON] Stopped $SCREEN_SESSION"
    ;;
  list)
    screen -ls 2>/dev/null | grep "br-" || echo "[DAEMON] No BRACHAT daemons running"
    ;;
  *)
    echo "Usage: $0 {start|stop|list} [ezra|agent <name>]"
    echo ""
    echo "Examples:"
    echo "  $0 start ezra              Start Ezra's temporal memory loop"
    echo "  $0 start agent artur       Start Artur as background daemon"
    echo "  $0 stop agent artur        Stop Artur daemon"
    echo "  $0 list                    List all running daemons"
    exit 1
    ;;
esac
