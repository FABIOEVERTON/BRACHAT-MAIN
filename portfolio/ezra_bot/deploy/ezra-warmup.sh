#!/bin/bash
PASS=$(grep OPENCODE_SERVER_PASSWORD /home/ubuntu/brachat-main/.env | cut -d= -f2)
[ -z "$PASS" ] && exit 1
AUTH=$(printf "opencode:%s" "$PASS" | base64)
BASE=http://127.0.0.1:3791
for i in $(seq 1 90); do
  curl -s -m 2 $BASE/session >/dev/null 2>&1 && break
  sleep 2
done
SID=$(curl -s -m 10 -X POST -H "Authorization: Basic $AUTH" $BASE/session | python3 -c 'import sys,json;print(json.load(sys.stdin).get("id",""))')
[ -z "$SID" ] && { echo "warmup: sem sessao"; exit 1; }
curl -s -m 900 -X POST -H "Authorization: Basic $AUTH" -H "Content-Type: application/json" \
  -d '{"parts":[{"type":"text","text":"responda apenas: warm-ok"}]}' \
  $BASE/session/$SID/message >/dev/null 2>&1
echo "ezra-warmup done $(date +%H:%M:%S)"
