#!/bin/bash
set -euo pipefail

PENDING_FILE="agents/pending_orders.json"
ORDER_ID="${1:-}"

if [ -z "$ORDER_ID" ]; then
  echo "Uso: mark_order_done.sh <order-id>"
  echo "Ordens pendentes:"
  python3 -c "
import json
orders = json.load(open('$PENDING_FILE'))
for o in orders:
    if o.get('status') == 'pending':
        print(f\"  {o['id']}: {o['order']}\")
  "
  exit 1
fi

python3 -c "
import json
path = '$PENDING_FILE'
orders = json.load(open(path))
found = False
for o in orders:
    if o['id'] == '$ORDER_ID':
        o['status'] = 'done'
        o['done_at'] = __import__('datetime').datetime.now().isoformat()
        found = True
        break
if found:
    json.dump(orders, open(path, 'w'), indent=2, ensure_ascii=False)
    print(f'✅ Ordem {$ORDER_ID} marcada como concluida')
else:
    print(f'❌ Ordem {$ORDER_ID} nao encontrada')
    exit(1)
"
