#!/bin/bash
set -euo pipefail

echo "=== STARTUP CHECKS $(date '+%Y-%m-%d %H:%M') ==="
FAIL=0

check() {
  local label="$1" cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    echo "  [OK] $label"
  else
    echo "  [FAIL] $label"
    FAIL=1
  fi
}

check "date" "date"
check "git repo" "git rev-parse --git-dir"
check "agents/state.json" "test -f agents/state.json"
check "agents/index.json" "test -f agents/index.json"
check "context_memory.json" "test -f agents/orchestrator_agents/ezra/context_memory.json"
check "governance.md exists" "test -f agents/governance/governance.md"
check "governance-ledger.jsonl" "test -f agents/governance/governance-ledger.jsonl"
check "skills_memory.json" "test -f agents/orchestrator_agents/ezra/skills_memory.json"
check "n8n reachable" "curl -sf http://localhost:5678/healthz >/dev/null 2>&1 || curl -sf http://localhost:5678/ >/dev/null 2>&1"

if [ -f integrations/apis/ssh-key-2026-06-11.key ]; then
  check "VM SSH (147.15.0.196)" "ssh -i integrations/apis/ssh-key-2026-06-11.key -o ConnectTimeout=5 -o StrictHostKeyChecking=no ubuntu@147.15.0.196 'echo ok'"
else
  echo "  [SKIP] VM SSH (key not found)"
fi

echo ""
echo "=== RESULT: $([ $FAIL -eq 0 ] && echo 'ALL CHECKS PASSED' || echo 'SOME CHECKS FAILED') ==="
exit $FAIL
