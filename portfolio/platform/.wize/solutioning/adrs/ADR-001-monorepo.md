---
status: accepted
owner: Tony Stark
created: 2026-09-18
---

# ADR-001 — Monorepo Turborepo com workspaces TS + Python

## Context

9 produtos compartilham motor de laudos, auth, modelo de tenant, cofre WORM e componentes de UI. Duplicar lógica crítica entre repositórios violaria o princípio "laudo válido" (P1) por divergência de implementação.

## Decision

Monorepo `ezra/` com Turborepo (workspaces TypeScript: apps/, packages/) + pyproject.toml (workspace Python: services/). Uma mudança no LaudoEngine propaga a todos os produtos.

## Consequences

- (+) Propagação única do motor crítico; tipos compartilhados via packages/types.
- (+) Uma pipeline CI para tudo.
- (-) Gate de build mais pesado; disciplina de boundaries entre workspaces exigida (ADR-006).
- Fonte: PRD §2.1.