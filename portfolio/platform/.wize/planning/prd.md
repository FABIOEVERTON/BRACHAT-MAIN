---
status: validated
owner: Maria Hill
validated: true
source: "EZRA_PRD_Arquitectural_v1.md (raiz do repo)"
created: 2026-09-18
---

# PRD — Plataforma EZRA

**Fonte de verdade:** `EZRA_PRD_Arquitectural_v1.md` (raiz de `BRACHAT-MAIN/portfolio/platform/`) + `# ARQUITETURA DEFINITIVA DE PRODUTOS — P.md`. Este arquivo é o contrato Wize apontando para a spec congelada.

## Escopo (resumo executivo)

SaaS multi-produto, multi-ramo, multi-tenant com validade jurídica brasileira. Toda ação auditável gera Laudo Pericial Oficial com hash SHA-256 encadeado gravado em cofre WORM.

**Ramo 1 — Governança de IA:** SENTINEL (P1, inventário/shadow AI) → AEGIS (P2, auditoria 122 controles AGCP + RIPD) → GUARDIAN (P3, gateway runtime + HITL).

**Ramo 2 — Governança Municipal:** RADAR (P1, captação DOU/emendas EC 105), VIGÍLIA (P2, CAUC+TCE), COMPRAS (P3, ETP/TR Lei 14.133), EXECUTA (P4, execução de convênio), ALERTA (P5, SOS diligências — MVP Ramo 2), PROVA (P6, prestação de contas).

## Princípios não negociáveis (PRD §1.2)

- P1 Laudo como saída universal · P2 Cadeia de custódia SHA-256 encadeada · P3 Soberania de dados (AWS sa-east-1 exclusivo) · P4 Outcome-based pricing · P5 Multi-tenant isolado (schema-per-tenant) · P6 White-label nativo.

## Stack (PRD §stack)

- Frontend/web: Next.js 14+ App Router + TypeScript (web + admin)
- Backend: FastAPI + Python; um serviço por produto
- Monorepo: Turborepo (TS workspaces) + pyproject.toml (Python)
- DB: PostgreSQL 16, schema-per-tenant
- Infra: AWS sa-east-1 (RDS Multi-AZ, S3 Object Lock WORM, SQS, ECS Fargate, CloudFront); LocalStack em dev
- WORM: S3 Object Lock COMPLIANCE, retenção 10 anos
- Auth: NextAuth.js v5 + JWT middleware Python

## FASE 0 — Núcleo (pré-requisito global, PRD §10.1)

Monorepo configurado · Auth+RBAC · Tenant model e schema-per-tenant · LaudoEngine · HashChain · WORMVault · White-label (ThemeProvider + subdomínio) · Dashboard shell · Docker Compose dev · CI/CD.

## Critérios de aceitação globais (PRD §11)

- Latência P95 sincrônica < 300ms · Laudo simples < 60s · Auditoria completa < 5min
- SLA 99,5% · Zero dado cross-tenant · WORM imutável · SHA-256 verificável externamente
- Cobertura testes ≥ 80% · TypeScript strict sem `any` explícito · Ruff (Python) · ESLint+Biome (TS) · Playwright E2E por produto

## Fases de implementação (PRD §10.1)

FASE 0 (núcleo) → FASE 1 (MVP Ramo 1: SENTINEL+AEGIS L1) → FASE 2 (MVP Ramo 2: ALERTA+VIGÍLIA) → FASE 3 (AEGIS L2-L4 + GUARDIAN) → FASE 4 (RADAR, COMPRAS, EXECUTA, PROVA) → FASE 5 (White-label & Admin + Billing).