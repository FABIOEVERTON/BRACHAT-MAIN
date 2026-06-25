#!/usr/bin/env bash
set -euo pipefail
export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:$PATH"

# Source: integrations/apis/.env.json (única fonte de verdade)
ENV_JSON="/Users/mac/brachat-main/integrations/apis/.env.json"
MEM0_API_KEY=$(grep MEM0_API_KEY "$ENV_JSON" | head -1 | cut -d= -f2 | tr -d '\n\r')
MEM0_API="https://api.mem0.ai/v1/memories/"
REPO="/Users/mac/brachat-main"
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

SUMMARY=$(/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -c "
import json, os, glob
basedir = '$REPO/agents'
summaries = []

# Study agents
for f in glob.glob(os.path.join(basedir, 'studies_agents', '*', 'state.json')):
    try:
        with open(f) as fp:
            data = json.load(fp)
        agent = os.path.basename(os.path.dirname(f))
        summaries.append(f'{agent}:active')
    except: pass

# Directors
for f in glob.glob(os.path.join(basedir, 'director_agents', '*', 'state.json')):
    try:
        with open(f) as fp:
            data = json.load(fp)
        agent = os.path.basename(os.path.dirname(f))
        summaries.append(f'{agent}:active')
    except: pass

# Orchestrator (Ezra)
try:
    with open(os.path.join(basedir, 'orchestrator_agents', 'ezra', 'state.json')) as f:
        oz = json.load(f)
    summaries.append(f'orch:last={oz.get(\"last_session\",\"?\")}')
except: pass

result = ' | '.join(summaries) if summaries else 'no agents'
print(result[:500])
")

curl -s -X POST "$MEM0_API" \
  -H "Authorization: Token $MEM0_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "fabio",
    "agent_id": "ezra",
    "messages": [
      {"role": "user", "content": "heartbeat"},
      {"role": "assistant", "content": "HB '"$DATE"' — '"$SUMMARY"'"}
    ],
    "metadata": {
      "type": "heartbeat",
      "source": "launchd_30min",
      "date": "'"$DATE"'"
    }
  }' > /dev/null 2>&1
