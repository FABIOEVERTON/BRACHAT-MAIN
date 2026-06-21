#!/bin/bash
# Baruch Dispatch Bridge — chamado por Artur (BR-ARTUR-002)
# Uso: ./dispatch_to_baruch.sh <nome_do_projeto>
# Abre um terminal com Claude Code CLI no /portfolio para executar a task

PROJECT_NAME="${1:-task_$(date +%s)}"
TASK_FILE="/Users/mac/brachat-main/portfolio/tasks/${PROJECT_NAME}.md"

if [ ! -f "$TASK_FILE" ]; then
  echo "❌ Task file nao encontrado: $TASK_FILE"
  echo "Artur precisa escrever a spec primeiro em: portfolio/tasks/${PROJECT_NAME}.md"
  exit 1
fi

echo "🟢 Abrindo terminal para Baruch (Claude Code) com a task: ${PROJECT_NAME}.md"
echo "   Task: $TASK_FILE"
echo ""

# Abre nova janela do Terminal com claudecode apontando pra task
osascript <<EOF
tell application "Terminal"
  activate
  do script "cd /Users/mac/brachat-main/portfolio && echo '=== BARUCH — Task: ${PROJECT_NAME} ===' && cat tasks/${PROJECT_NAME}.md && echo '' && echo '⬇️  Claude Code iniciando. Ao terminar, diga: Artur, finalizado.' && echo '' && claudecode"
end tell
EOF
