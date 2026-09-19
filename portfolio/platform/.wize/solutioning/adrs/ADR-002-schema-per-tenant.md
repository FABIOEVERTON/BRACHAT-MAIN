---
status: accepted
owner: Tony Stark
created: 2026-09-18
---

# ADR-002 — Multi-tenancy com schema-per-tenant

## Context

Laudos têm validade jurídica → vazamento cross-tenant é inaceitável por construção. Row-level security depende de query correta a cada chamada; risco residual não defensável em litígio.

## Decision

PostgreSQL 16, schema `tenant_{id}` por tenant. Tabelas de plataforma (tenants, whitelabel_configs) em `public`. Tenant context injetado via header `x-tenant-id` → ContextVar → `SET search_path TO tenant_{id}, public`.

## Consequences

- (+) Isolamento garantido por construção; nenhuma query cross-tenant possível.
- (+) Modelo defensável perante perito independente.
- (-) Custo operacional maior (migrations por tenant); migrations versionadas e aplicadas por schema.
- Fonte: PRD §3.2.