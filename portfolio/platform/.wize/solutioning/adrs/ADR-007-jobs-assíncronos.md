---
status: accepted
owner: Tony Stark
created: 2026-09-18
---

# ADR-007 — Operações longas: 202 + job_id + SQS

## Context

Scans, auditorias de 122 controles e geração de laudos excedem o budget síncrono (< 300ms p95). Necessário padrão uniforme de assíncronidade com observabilidade e idempotência.

## Decision

Todo endpoint de operação longa retorna `202 Accepted` + `job_id`; job enfileirado no SQS; worker processa; status consultado via `GET /jobs/{job_id}`; webhook opcional no completamento; laudo anexado quando aplicável. Idempotência por job_id (dedup key).

## Consequences

- (+) Contrato uniforme entre os 9 produtos; observável e testável.
- (+) Respeita NFR Perf-01 (laudo < 60s simples, < 5min completo) via processamento de fundo.
- (+) Satisfaz convenção RFC 7807 + paginação por cursor.
- (-) Requer infra de fila em dev (LocalStack) e tratamento de retry/failure.
- Fonte: PRD §9.1-9.2, arquitetura de jobs.