---
epic_id: 01-auth-multitenancy-whitelabel
status: ready-for-dev
owner: Tony Stark + Maria Hill
linked_prd: ÉPICO 1
trigger_map_row: 1
priority: 1
estimate: L
---

# Epic 01: Autenticação, Multi-tenancy e White-Label

## Outcome

Um sócio de banca cadastra o tenant, configura subdomínio e marca própria, e convida a equipe com RBAC e MFA ativo — base multi-tenant isolada por RLS.

## Stories
- E01-S01: Provisionamento de tenant isolado + subdomínio (AC-01-1, AC-01-2) — R-1
- E01-S02: Propagação DNS/SSL de subdomínio com fallback (AC-01-3) — R-1
- E01-S03: Gestão de usuários, convites e RBAC (AC-01-D1) — R-1
- E01-S04: MFA compulsório + SSO corporativo (AC-01-D2) — R-7

## Dependencies
- OCI Postgres 16 + RLS (ADR-001) provisionado
- Edge Cloudflare com roteamento CNAME de subdomínio

## Success
Todos os ACs PASS no gate; teste cross-tenant (R-1) verde no CI.