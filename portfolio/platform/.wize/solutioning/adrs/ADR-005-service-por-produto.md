---
status: accepted
owner: Tony Stark
created: 2026-09-18
---

# ADR-005 — Um serviço FastAPI por produto

## Context

9 produtos com ciclos de release e scaling independentes; integrações externas específicas (SEFAZ, SINAPI, Painel de Preços, DOU, Transferegov) e requisitos de deploy distintos (GUARDIAN on-premise/VPC).

## Decision

`services/gov-ai/{sentinel,aegis,guardian}` e `services/gov-municipal/{radar,vigilia,compras,executa,alerta,prova}` — cada um um FastAPI com main.py próprio, Dockerfile próprio e ECS service próprio. Compartilham via `services/shared`.

## Consequences

- (+) Deploy/scale independente; GUARDIAN pode rodar on-premise/VPC sem arrastar os demais.
- (+) Falha isolada por serviço.
- (-) Mais superfícies de deploy (gerenciadas via terraform ECS por serviço).
- Fonte: PRD §2.2 (services/), §4.3 (deploy GUARDIAN).