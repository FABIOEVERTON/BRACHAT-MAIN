---
status: draft
owner: Tony Stark
created: "2026-09-18"
stepsCompleted: [1,2,3,4,5,6,7,8]
inputDocuments: [".wize/planning/prd.md", ".wize/planning/tech-vision.md", ".wize/planning/nfr-principles.md", "EZRA_PRD_Arquitectural_v1.md", "# ARQUITETURA DEFINITIVA DE PRODUTOS — P.md"]
---

# Architecture — Plataforma EZRA

## Summary

SaaS multi-produto, multi-ramo (Governança de IA + Governança Municipal), multi-tenant com validade jurídica: monorepo Turborepo (Next.js App Router web+admin / TypeScript) + serviços FastAPI Python (um por produto) + PostgreSQL 16 schema-per-tenant + AWS sa-east-1 (RDS Multi-AZ, S3 Object Lock COMPLIANCE, SQS, ECS Fargate, CloudFront). Diferencial irredutível: laudo pericial como saída universal, cadeia SHA-256 encadeada e cofre WORM imutável. Spec congelada: `EZRA_PRD_Arquitectural_v1.md`.

## Stack

- Language: TypeScript (frontend/packages) · Python 3.12 (backend)
- Front-end: Next.js 14+ App Router, shadcn/ui, Recharts, NextAuth.js v5
- Back-end: FastAPI (um serviço por produto) + SQLAlchemy + Pydantic
- DB: PostgreSQL 16 (schema-per-tenant), Redis 7
- Auth: NextAuth.js v5 + JWT middleware Python (1h + refresh 7d); MFA roles privilegiadas
- Hosting: AWS sa-east-1 — ECS Fargate, RDS Multi-AZ, S3 WORM, SQS, LocalStack (dev)
- Observability: cloudwatch + structured logs (fase 0 básica)
- Test: pytest (Python) · Vitest + Playwright (TS/E2E)

## Components

| Component | Responsibility | Boundary |
|---|---|---|
| apps/web | Frontend Next.js — auth, dashboard shell, rotas gov-ai e gov-municipal, white-label theme | Browser → API gateway (x-tenant-id header) |
| apps/admin | Painel interno EZRA — tenants, billing, white-label config | Acesso exclusivo EZRA_ADMIN |
| services/shared | Módulos Python compartilhados — auth, tenant context, laudo engine, hash chain, worm vault, db, queue | Importado por todos os serviços; nunca exposto via API própria |
| services/gov-ai/* | SENTINEL (8001), AEGIS (8002), GUARDIAN (8003) | API própria por produto; consomem shared |
| services/gov-municipal/* | RADAR, VIGÍLIA, COMPRAS, EXECUTA, ALERTA, PROVA | API própria por produto; consomem shared |
| packages/* | Tipos TS compartilhados, design system (ui), api-contracts, crypto | Pacotes de workspace TS |
| infra/terraform | VPC, RDS, S3 WORM, SQS, ECS, CloudFront | AWS sa-east-1 |
| infra/docker | docker-compose.dev.yml + Dockerfiles | Ambiente dev local (LocalStack) |
| scripts | seed_controls (122), seed_normative_map, generate_api_types | Automação de seed e geração |

## Data model

Schema-per-tenant (`tenant_{id}`), tabelas de plataforma em `public`:

- `public.tenants` — id, slug, branch (gov_ai|gov_municipal), plan (direct|whitelabel), whitelabel_config_id, active_products[], chain_anchor_hash, status
- `public.whitelabel_configs` — brandName, logoUrl, colors, signatory (name/title/register), customDomain, hidePoweredBy
- Por schema de tenant: `laudos` (id, number, type, sha256_hash, chain_hash, worm_key, emitted_at), `users` + RBAC roles, dados de produto (inventory, controls, jobs, etc.)
- `jobs` (shared) — id, status (queued/processing/completed/failed), progress_pct, type, laudo_id

Hash chain: `chain_hash = SHA256(content_hash + previous_chain_hash)`; âncora = tenant_id (primeiro laudo).

## Sequences

1. **Emissão de laudo:** produto conclui análise → LaudoEngine.emit → PDF render → hash content → chain com hash anterior → grava WORM (Object Lock COMPLIANCE, 10y, SSE-KMS) → persiste registro → retorna LaudoResult (pdf_url assinada 1h).
2. **Operação longa (scan/auditoria):** POST → 202 + job_id → SQS → worker processa → job completed → webhook opcional → laudo emitido.
3. **Autenticação/RBAC:** NextAuth session → JWT → FastAPI verifica JWT → injeta tenant context (x-tenant-id) → permission check → handler.
4. **White-label:** request por subdomínio → resolveTenant → ThemeProvider aplica cores/marca → laudo assinado pelo signatário do tenant.
5. **Model Lifecycle (AEGIS):** a cada 6h consulta versões dos providers → detecta change → revalida 122 controles → Laudo de Transição com delta.

## Cross-cutting concerns

- **X-Tenant:** todo request ao backend carrega x-tenant-id; tenant context via ContextVar; search_path por schema.
- **WORM:** bucket S3 Object Lock COMPLIANCE + versioning; retenção 10 anos; SSE-KMS chave por tenant (prod).
- **Jobs:** operações longas sempre 202 + job_id; idempotência por job_id; rate limit 100 req/min/tenant.
- **White-label:** modo de primeira classe; laudo carrega identidade do signatário white-label; hash/WORM sempre da EZRA.
- **Erros:** RFC 7807 Problem Details; versão /v1; paginação por cursor.
- **Soberania:** região sa-east-1 exclusiva; proibido tráfego de dados fora (LGPD Art. 33).
- **Laudo universal:** nenhum produto entrega apenas dashboard; todo ativo auditável gera laudo.

## NFR check

- Perf-01: jobs assíncronos p/ operações > 300ms → pré-requisito de design em todos os serviços. ✓
- Perf: laudo < 60s simples / < 5min completo; proxy GUARDIAN < 50ms (fase 3). ✓
- Sec-01: soberania sa-east-1 — Config rules + VPC flow logs. ✓
- Sec-02: WORM COMPLIANCE — teste de deleção deve falhar. ✓
- Rel-01: SLA 99,5%, jobs idempotentes, backup 35d. ✓
- Maint-01: cobertura ≥ 80%, strict TS, Ruff/Biome/ESLint, ADR obrigatório. ✓
- Cost-01: dev local zero-custo (Docker+LocalStack). ✓

## ADRs

Ver `.wize/solutioning/adrs/`:
- ADR-001 monorepo · ADR-002 schema-per-tenant · ADR-003 WORM COMPLIANCE · ADR-004 cadeia SHA-256 · ADR-005 serviço-por-produto · ADR-006 white-label primeira classe · ADR-007 phygital jobs assíncronos · ADR-008 AWS sa-east-1 soberania