#!/bin/bash
set -euo pipefail

PENDING_FILE="agents/pending_orders.json"
PENDING_PATH="$PWD/$PENDING_FILE"

# Ensure git is up to date
git pull --rebase origin "$(git rev-parse --abbrev-ref HEAD)" 2>/dev/null || true

if [ ! -f "$PENDING_PATH" ]; then
  echo '[]' > "$PENDING_PATH"
  git add "$PENDING_FILE" 2>/dev/null || true
fi

# Count pending orders
PENDING=$(python3 -c "
import json
orders = json.load(open('$PENDING_PATH'))
pending = [o for o in orders if o.get('status') == 'pending']
print(len(pending))
")

if [ "$PENDING" -gt 0 ]; then
  echo ""
  echo "=== 📦 ORDENS PENDENTES ($PENDING) ==="
  python3 -c "
import json
orders = json.load(open('$PENDING_PATH'))
for o in orders:
    if o.get('status') == 'pending':
        print(f\"  [{o['id']}] {o['order']}\")
        print(f\"       criada: {o['created_at']}\")
  "
  echo "=== Execute com: source agents/scripts/exec_pending_order.sh <id> ==="
  echo ""
else
  echo "[check_orders] Nenhuma ordem pendente"
fi
