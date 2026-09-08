#!/bin/bash
# deep-dep-check.sh — Verificação profunda de dependências antes de qualquer mutação
# Uso: ./deep-dep-check.sh <target_path_or_id>
# Retorna: 0 = seguro, 1 = breaking refs encontrados, 2 = erro

set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Uso: $0 <caminho_arquivo|skill_id|tool_id|state_key>" >&2
  exit 2
fi

ROOT_DIRS=(
  "/Users/mac/brachat-main"
  "/Users/mac/ezra_ai_governance_framework"
  "/Users/mac/.opencode"
)

SEARCH_PATTERNS=(
  # Skills
  "manifest.txt"
  "manifest_tools.txt"
  "manifest_native_tools.txt"
  "pending_tasks.txt"
  "worklog.txt"
  "state.json"
  "governance-ledger.jsonl"
  # Skills specs
  "SKILL.txt"
  "SUBMODULES.md"
  # Framework
  "*.md"
  "*.txt"
  "*.yaml"
  "*.yml"
  "*.json"
  "*.sh"
  "*.py"
  "*.toml"
  "Dockerfile"
  "docker-compose.yml"
  "Makefile"
)

echo "=== DEEP DEPENDENCY CHECK ==="
echo "Target: $TARGET"
echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%S.000Z")"
echo

BREAKING=0
DEGRADED=0
TOTAL_REFS=0

# Normaliza target para busca
TARGET_ESCAPED=$(printf '%s\n' "$TARGET" | sed 's/[[\.*^$()+?{|\\]/\\&/g')

for ROOT in "${ROOT_DIRS[@]}"; do
  [[ -d "$ROOT" ]] || continue

  echo "--- Scanning: $ROOT ---"

  for PATTERN in "${SEARCH_PATTERNS[@]}"; do
    while IFS= read -r -d '' FILE; do
      [[ -f "$FILE" ]] || continue

      # Busca referência (case-sensitive para IDs, insensitive para paths)
      if grep -q "$TARGET_ESCAPED" "$FILE" 2>/dev/null; then
        TOTAL_REFS=$((TOTAL_REFS + 1))

        # Classifica impacto baseado no tipo de arquivo
        FILE_BASENAME=$(basename "$FILE")

        case "$FILE_BASENAME" in
          manifest.txt|manifest_tools.txt|manifest_native_tools.txt|pending_tasks.txt|state.json|governance-ledger.jsonl)
            IMPACT="BREAKING"
            BREAKING=$((BREAKING + 1))
            ;;
          SKILL.txt)
            # Verifica se é no campo DEPS ou AGCP_REF
            if grep -E "DEPS|AGCP_REF" "$FILE" | grep -q "$TARGET_ESCAPED"; then
              IMPACT="BREAKING"
              BREAKING=$((BREAKING + 1))
            else
              IMPACT="DEGRADED"
              DEGRADED=$((DEGRADED + 1))
            fi
            ;;
          SUBMODULES.md|*.md|*.txt|*.yaml|*.yml|*.json|*.sh|*.py|*.toml|Dockerfile|docker-compose.yml|Makefile)
            IMPACT="DEGRADED"
            DEGRADED=$((DEGRADED + 1))
            ;;
          *)
            IMPACT="DEGRADED"
            DEGRADED=$((DEGRADED + 1))
            ;;
        esac

        # Mostra contexto da referência
        CONTEXT=$(grep -n "$TARGET_ESCAPED" "$FILE" | head -3 | sed 's/^/    /')
        echo "  [$IMPACT] $FILE"
        echo "$CONTEXT"
      fi
    done < <(find "$ROOT" -type f -name "$PATTERN" -print0 2>/dev/null)
  done
done

echo
echo "=== SUMMARY ==="
echo "Total references: $TOTAL_REFS"
echo "BREAKING (hard deps): $BREAKING"
echo "DEGRADED (soft refs): $DEGRADED"

if [[ $BREAKING -gt 0 ]]; then
  echo
  echo "❌ BLOCKED: $BREAKING breaking reference(s) found."
  echo "   Mutation REQUIRES mitigation plan + Fabio approval."
  exit 1
elif [[ $DEGRADED -gt 0 ]]; then
  echo
  echo "⚠️  WARNING: $DEGRADED degraded reference(s) found."
  echo "   Safe to proceed but update soft refs after mutation."
  exit 0
else
  echo
  echo "✅ CLEAN: No references found. Safe to mutate."
  exit 0
fi