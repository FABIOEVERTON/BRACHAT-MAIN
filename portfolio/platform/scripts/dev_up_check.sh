#!/usr/bin/env bash
# E0-S02: startup stack dev e validação dos gates F0-04/F0-05/F0-06.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="${ROOT}/infra/docker/docker-compose.dev.yml"
PY="${ROOT}/.venv/bin/python"

echo "==> compose config valido?"
docker compose -f "${COMPOSE_FILE}" config -q && echo "config OK"

echo "==> up -d"
docker compose -f "${COMPOSE_FILE}" up -d --build

echo "==> aguardando healthchecks (F0-04)..."
sleep 12
docker compose -f "${COMPOSE_FILE}" ps

echo "==> web responde 200?"
curl -sf http://localhost:3002/api/health && echo " <- web OK (F0-04 PASS)"

echo "==> F0-05: WORM check no LocalStack"
"${PY}" "${ROOT}/scripts/localstack_worm_check.py"