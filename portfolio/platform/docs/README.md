# Plataforma EZRA — monorepo

Governança de IA + municipal com **laudo pericial auditável** (WORM 10 anos + cadeia SHA-256).

## Stack (PRD, spec congelada — ADR-001/005/008)

| Camada | Tecnologia |
|---|---|
| Web / Admin | Next.js 14+ App Router, TypeScript (strict) |
| Serviços | FastAPI + Python, um serviço por produto |
| Banco | PostgreSQL 16, schema-per-tenant (ADR-002) |
| Nuvem | AWS **sa-east-1** (RDS Multi-AZ, S3 Object Lock **COMPLIANCE**, SQS, ECS Fargate) |
| Dev | Docker Compose + LocalStack; Turborepo; uv |

## Estrutura (PRD §2.2)

```
apps/web            Portal autenticado dos tenants
apps/admin          Admin EZRA + white-label
services/shared     Núcleo compartilhado Python (config, chain, laudo)
services/gov-ai/    Ramo 1: sentinel, aegis, guardian
services/gov-municipal/  Ramo 2: radar, vigilia, compras, executa, alerta, prova
packages/           types | ui | api-contracts | crypto
infra/              terraform (sa-east-1) + docker
scripts/            seed_controls, seed_normative_map, generate_api_types, verify_chain
```

## Quickstart

```bash
npm install && npm run build   # workspaces TS
python3 -m compileall services # sanity do Python
pip install -e ./services/shared  # ou: uv --workspace ./services
```

## Documentação do ciclo

Planejamento e decisões vivem em `.wize/` (Wize Dev Kit): `planning/`, `solutioning/` (architecture + ADRs), `implementation/tea/` (risk-profile).