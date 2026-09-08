#!/usr/bin/env bash
set -e
SRC="$HOME/.opencode"
DRIVE="$HOME/Library/CloudStorage/GoogleDrive-jae.engenharia@gmail.com/My Drive/brachat-main"
VM="ubuntu@163.176.111.95"
KEY="$HOME/.ssh/id_rsa"
EXC=(
  --exclude .DS_Store
  --exclude node_modules
  --exclude package.json
  --exclude package-lock.json
  --exclude state.json
  --exclude state
  --exclude governance-ledger.jsonl
  --exclude logs
  --exclude cache
  --exclude data
  --exclude repos
  --exclude credentials
  --exclude .git
)
for d in skills plugin instructions reference proposals; do
  rsync -a --delete "${EXC[@]}" "$SRC/$d/" "$DRIVE/.opencode/$d/"
done
rsync -a "${EXC[@]}" "$SRC/plugin.json" "$DRIVE/.opencode/plugin.json"
cd "$DRIVE"
git add .opencode/
if git diff --cached --quiet; then
  echo "sem mudancas"
else
  git commit -q -m "sync: $(date +%Y-%m-%dT%H:%M:%S)"
  git push -q origin main
  echo "pushed"
fi
ssh -i "$KEY" "$VM" "cd /home/ubuntu/brachat-main && git pull -q && sudo systemctl restart ezra-serve && echo 'VM atualizada'"
