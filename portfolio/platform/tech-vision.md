---
status: aligned
owner: Nick Fury
created: 2026-09-17
---

# Tech Vision — BRACHATTECH | EZRA AI Governance Platform

## Stack family

Web SaaS fullstack, origin-first, soberano em solo brasileiro. Frontend TypeScript/Next.js (SSR) + API Python 3.12 (FastAPI) + PostgreSQL 16 com RLS como sistema de registro, filas Redis/Celery para jobs pesados (PDF/hashing), deploy em OCI Região Valinhos/SP com edge Cloudflare (terminação TLS/WAF) na frente da origem OCI.

## Runtime envelope

| Dimension | Decision |
|---|---|
| Language(s) | TypeScript (frontend), Python 3.12 (API/workers) |
| Runtime(s) | Node (Next.js SSR) + ASGI (FastAPI/Uvicorn) + Celery workers containers |
| Persistence | PostgreSQL 16 Enterprise (OCI) com RLS + pgvector; Redis Cluster 7.2 (cache/broker) |
| Deploy target | OCI Compute (containers) + OCI Object Storage (cofre WORM); edge Cloudflare |
| Edge vs origin | Origin-first: dados e computação pericial na origem soberana; edge só para TLS/WAF/CDN |

## Build / buy / borrow

| Capability | Decision |
|---|---|
| Auth (JWT JWE RS256 + MFA TOTP + SSO SAML/OIDC) | Build — sobre libs OSS (`python-jose`/`argon2-cffi`); PRD exige controle total da cadeia criptográfica |
| Payments (BRL) | Buy — Stripe / Pagar.me via API com webhooks idempotentes (escopo negativo do PRD) |
| Fila de jobs (Celery) | Borrow — Celery + Redis gerenciado OCI |
| Search vetorial (RAG auditável) | Borrow — pgvector (Postgres 16), sem engine extra |
| Observabilidade | Borrow — OpenTelemetry + Prometheus/Grafana; tracing distribuído com `X-Trace-Id` |
| E-mail transacional | Buy — OCI Email Delivery / Resend |
| Armazenamento forense | Buy — OCI Object Storage (WORM lock 5 anos) |
| Verificação pública de laudo (QR) | Build — página pública stateless com verificação de hash no manifesto |

## Non-negotiables

1. PII e dados de evidência pericial nunca saem da região BR (soberania BACEN/ANPD).
2. RLS ativo e forçado em 100% das tabelas de negócio + defesa em profundidade no backend (filtro `tenant_id` explícito).
3. SLOs contratuais: disponibilidade 99.9%; CRUD p95 < 200 ms; compilação do laudo p90 < 10 s; erro 5xx < 0.05%.
4. Cadeia de custódia imutável: todo laudo tem hash SHA-256 congelado no cofre WORM antes de qualquer entrega ao cliente.
5. MFA compulsório para administradores e auditores; nada além de `mfa:pending` sem o código TOTP.

## Deferred

- Schema-per-tenant (Tier 3): revisit quando o primeiro contrato governamental/banco exigir instância dedicada.
- On-premises: revisit quando um contrato Enterprise > R$ 150k/ano exigir (PRD escopou fora do MVP).
- Multi-região: revisit quando houver demanda de dados fora do Brasil (hoje violaria o non-negotiable #1).
- Fine-tuning de LLMs: revisit somente se o produto migrar de auditor para ambiente de treinamento (fora do PRD).

## Constraints that drove this

- LGPD (Art. 11/38) + PL 2338/2023 (Arts. 13/17/19/21/27) → soberania total, evidência forense, HITL obrigatório no MCP.
- Custo de entrada R$ 1.890/mês → banco compartilhado com RLS (não db-per-tenant).
- OCI Valinhos/SP → origem soberana; Cloudflare apenas como borda WAF/CDN.
- PRD North Star (LPCV/mês) → pipeline Celery/RreportLab dedicado e SLO de compilação < 10 s.