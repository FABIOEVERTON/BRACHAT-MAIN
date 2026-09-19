---
epic_id: E0-shirt-core
status: ready
owner: Tony Stark + Maria Hill
linked_prd: FASE 0 + FASE 1/2 preview
priority: 1
estimate: L
---

# Epic E0B: Shared Core — convenções de API + jobs + seeds

## Outcome

A camada compartilhada de API (RFC 7807, /v1, x-tenant-id, rate limit), o motor de jobs assíncronos (202 + job_id + SQS) e os seeds do domínio (122 controles AGCP, mapeamento normativo, geração de tipos OpenAPI) funcionais — base sobre a qual os produtos das Fases 1+ constroem sem re-trabalho.

## Stories

- E0B-S01: Conventions de API shared (RFC 7807, /v1, x-tenant-id, rate limit 100/min) (FASE 0 convenções)
- E0B-S02: Motor de jobs assíncronos (202 + job_id + SQS/LocalStack + status + webhook) (FASE 0:4)
- E0B-S03: scripts/seed_controls.py — 122 controles AGCP (FASE 1 pré-req)
- E0B-S04: scripts/seed_normative_map.py — mapeamento norma→artigo→cláusula (FASE 1 pré-req)
- E0B-S05: scripts/generate_api_types.sh — tipos TS do OpenAPI (FASE 0 tooling)

## Dependencies

- Epic E0 (monorepo + shared core) completo — E0B consome estrutura e conventions.
- S03/S04 referenciam distribuição dos 122 controles (L1:38, L2:31, L3:28, L4:25 — PRD §4.2).

## Success

Qualquer serviço novo nasce com conventions + jobs funcionais; `seed_controls` e `seed_normative_map` populam o banco dev; tipos TS regenerados do OpenAPI compilam em strict mode.