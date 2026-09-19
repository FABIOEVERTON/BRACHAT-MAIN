---
epic_id: E0-monorepo-core
status: ready
owner: Tony Stark + Maria Hill
linked_prd: FASE 0
priority: 1
estimate: XL
---

# Epic E0: Núcleo da Plataforma EZRA — Monorepo + Shared Core

## Outcome

A plataforma EZRA existe como monorepo compilável e testável com o núcleo compartilhado funcional: auth + RBAC, modelo de tenant, motor de laudos, cadeia SHA-256, cofre WORM, white-label e dashboard shell rodando em Docker Compose dev. Pré-requisito para todos os produtos (PRD §10.1 FASE 0: "Nenhum produto pode ser entregue sem esta fase").

## Stories

- E0-S01: Scaffold monorepo (Turborepo + workspaces TS + pyproject Python) (FASE 0:1)
- E0-S02: Docker Compose dev + LocalStack (FASE 0:10)
- E0-S03: Auth + RBAC (NextAuth v5 + JWT middleware Python) (FASE 0:2)
- E0-S04: Modelo de tenant schema-per-tenant (FASE 0:3)
- E0-S05: LaudoEngine + PDF generator (FASE 0:4)
- E0-S06: HashChain SHA-256 encadeado (FASE 0:5)
- E0-S07: WORMVault S3 Object Lock COMPLIANCE (FASE 0:6)
- E0-S08: White-label ThemeProvider + resolução de subdomínio (FASE 0:7)
- E0-S09: Dashboard shell Next.js App Router por ramo (FASE 0:8)
- E0-S10: CI/CD pipeline GitHub Actions → ECS staging (FASE 0:9)

## Dependencies

- ADRs 001-008 (todos aplicáveis ao núcleo)
- Nenhuma externa até S10 (credenciais AWS staging na FASE 0 final)

## Success

Todos os ACs de todas as stories PASS gate. `docker compose up` sobe web + shared services com LocalStack; laudo de teste emitido com hash encadeado e gravado no WORM local; verificação externa do SHA-256 demonstrada.