#!/usr/bin/env bash
# E0-S02 F0-05: provisiona LocalStack e valida WORM COMPLIANCE (teste PESSIMISTA — R-1).
# put/head OK; DELETE DEVE FALHAR (modo COMPLIANCE 10 anos, ADR-003).
set -euo pipefail

ENDPOINT_URL="${AWS_ENDPOINT_URL:-http://localhost:4566}"
REGION="${AWS_REGION:-sa-east-1}"
BUCKET="${S3_WORM_BUCKET:-ezra-worm}"
DAYS="${S3_WORM_DAYS:-3650}"

echo "==> aguardando LocalStack em ${ENDPOINT_URL}"
until curl -sf "${ENDPOINT_URL}/_localstack/health" >/dev/null; do sleep 2; done
echo "==> LocalStack healthy (regiao ${REGION})"

aws --endpoint-url="${ENDPOINT_URL}" --region "${REGION}" s3api create-bucket \
  --bucket "${BUCKET}" --create-bucket-configuration LocationConstraint="${REGION}" >/dev/null

echo "==> habilitando Object Lock COMPLIANCE (${DAYS} dias)"
aws --endpoint-url="${ENDPOINT_URL}" --region "${REGION}" s3api put-object-lock-configuration \
  --bucket "${BUCKET}" \
  --object-lock-configuration "ObjectLockEnabled=Enabled,Rule={DefaultRetention={Mode=COMPLIANCE,Days=${DAYS}}}"

echo "==> put object"
aws --endpoint-url="${ENDPOINT_URL}" --region "${REGION}" s3api put-object \
  --bucket "${BUCKET}" --key "laudos/prova.txt" --body <(echo "laudo-teste-worm")

echo "==> head object"
aws --endpoint-url="${ENDPOINT_URL}" --region "${REGION}" s3api head-object \
  --bucket "${BUCKET}" --key "laudos/prova.txt" --query "ObjectLockMode" --output text

echo "==> delete object (DEVE FALHAR em COMPLIANCE)"
if aws --endpoint-url="${ENDPOINT_URL}" --region "${REGION}" s3api delete-object \
  --bucket "${BUCKET}" --key "laudos/prova.txt" 2>/dev/null; then
  echo "FALHA DO GATE: deletion succeeded — modo COMPLIANCE nao respeitado" >&2
  exit 1
fi
echo "==> DELETE FALHOU como esperado — WORM COMPLIANCE valido"
echo "F0-05 PASS"