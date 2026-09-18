---
status: in-progress
owner: Tony Stark
created: 2026-09-17
stepsCompleted: 01,02,03,04,05,06,07
---

# Architecture — EZRA AI Governance Platform

Frame: `tech-vision.md` (Fury). Fontes: `prd.md` (validado 2026-09-17). Tony detalha dentro do frame — ADRs em `adrs/`.

## 1. Componentes e fronteiras

```
[Edge Cloudflare: TLS 1.3, WAF OWASP+LLM, anti-DDoS, roteamento CNAME subdomínio]
        │ HTTPS/WSS
        ▼
[Frontend Next.js (TS) — SSR, tenant-aware (subdomínio), SSR com sessão JWE]
        │ REST/SSE
        ▼
[API FastAPI (Python 3.12) — middleware de tenant (JWT→tenant_id), Pydantic v2, rate limit]
        │                     │
        │ síncrono (CRUD)     │ jobs pesados → Redis → Celery workers
        ▼                     ▼
[PostgreSQL 16 RLS + pgvector]   [Worker pool: discovery | reportlab | hasher]
        ▲                              │
        └──── [OCI Object Storage WORM (PDF + validation_manifest.json)]
```

- **Fronteira A (pública):** validação por QR code — página stateless lê `Forensic_Manifests` via hash; nenhum dado de tenant exposto.
- **Fronteira B (autenticada):** console de auditoria (inventário, 122 controles, compilação de laudo).
- **Fronteira C (integrada):** gateway MCP auditado para agentes do cliente (callbacks `tools.*`) — deny-by-default + Human-in-the-Loop.
- **Fronteira D (interna):** workers Celery não expõem API pública; consomem filas com chaves de idempotência.

## 2. Modelo de dados (núcleo)

`Tenants` → `Users` (RBAC: TENANT_ADMIN/AUDITOR/TECH/VIEWER) → `AI_Assets` → `Compliance_Assessments` (payload 122 controles JSONB) → `Forensic_Manifests` (protocolo + master_hash + WORM) + `Audit_Logs` (eventos com payload_hash).

Regra invariante: **toda** tabela de negócio tem `tenant_id` + RLS `FORCE` + índice composto em `tenant_id` — ver `ADR-001`.

## 3. Fluxo crítico: compilação do laudo (sequência)

1. `POST /compile` (cota + token validados) → 202 Accepted + `task_id`.
2. Celery worker lê `controls_payload` da assessment (RLS no tenant).
3. Worker hasher calcula SHA-256 de prompts/regras/evidências → `validation_manifest.json`.
4. Worker reportlab compila PDF 20 páginas white-label (cores/logo do tenant).
5. Escrita no cofre WORM da OCI → ETag de imutabilidade confirmada.
6. `Forensic_Manifests.master_hash = SHA-256(manifesto)` registrado; status CONCLUÍDO; SSE/poll devolve hash + link.
7. Retry: 5 tentativas com idempotência (chave = protocolo) — ver `ADR-004`.

## 4. Decisões de projeto (resumo; detalhe nos ADRs)

| # | Trade-off | Decisão | ADR |
|---|---|---|---|
| 1 | Multi-tenancy: db-per-tenant / schema / shared | Shared DB + RLS nativo | ADR-001 |
| 2 | Imutabilidade probatória | OCI WORM 5 anos + manifest hash | ADR-002 |
| 3 | Governança de agentes (MCP) | Gateway deny-by-default + HITL + Decision Ledger | ADR-003 |
| 4 | Pipeline do laudo | Celery (3 workers) + ReportLab + idempotência | ADR-004 |

## 5. Fronteiras de implementação (para Shuri)

- `apps/web` — Next.js (SSR), middleware de subdomínio→tenant, páginas de validação pública.
- `apps/api` — FastAPI: routers `auth/`, `tenants/`, `assets/`, `assessments/`, `compile/`, `mcp/gateway`.
- `apps/workers` — Celery: `discovery`, `reportlab`, `hasher`.
- `libs/contracts` — Pydantic v2 + TS tipos compartilhados (schemas de contrato).
- `libs/compliance` — motor de regras dos 122 controles + gate advisory/enforcing (puro, testável).
- `infra/` — IaC OCI (VCN, Postgres, Redis, Object Storage WORM, containers) + Cloudflare.

Regra de conflito entre agentes: `libs/compliance` é a única fonte do gate ALTO RISCO; UI/API nunca decidem conformidade.

## Validação (step-07)

- Cobertura: 5 épicos mapeados a fronteiras A–D ✓.
- NFR: PERF-2 (p90 < 10 s) atendido por workers dedicados + idempotência ✓.
- Pronto para Hawkeye (`tea-risk.md`) e Shuri (epics/stories via `wize-create-epics-and-stories`).