---
status: aligned
owner: Nick Fury
created: 2026-09-18
---

# Tech Vision — Plataforma EZRA

## Stack family

Monorepo fullstack: **Next.js-class SSR frontend (web + admin)** com **serviços Python FastAPI modulares** (um serviço por produto), PostgreSQL multi-tenant e infraestrutura AWS soberana brasileira (sa-east-1). Nenhum componente fora da família declarada no PRD (spec congelada).

## Runtime envelope

| Dimension | Decision |
|---|---|
| Languages of record | TypeScript (frontend/packages) · Python (backend/IA) |
| Runtime(s) | Node (Next.js App Router) · Python 3.12 (FastAPI, um serviço por produto) |
| Persistence | PostgreSQL 16 · schema-per-tenant (isolamento por construção) · Redis (cache/cooldown) |
| Deploy target | AWS sa-east-1 — ECS Fargate por serviço · RDS Multi-AZ · S3 WORM · SQS |
| Edge vs origin | Origin-first (dados soberanos; CDN CloudFront apenas para static) |
| Dev local | Docker Compose + LocalStack (S3/SQS/KMS simulados) |

## Build / buy / borrow

| Capability | Decision |
|---|---|
| Auth | Borrow — NextAuth.js v5 (frontend) + JWT middleware Python (backend) |
| Laudo Engine (PDF) | Build — motor proprietário (valor central) |
| WORM vault | Buy — AWS S3 Object Lock COMPLIANCE (nativo, único modo defensável) |
| Queues | Buy — AWS SQS (prod) · LocalStack (dev) |
| Hash chain SHA-256 | Build — módulo proprietário `laudo/hash_chain.py` |
| Tenant isolation | Build — schema-per-tenant no PostgreSQL |
| White-label | Build — ThemeProvider + resolução de subdomínio (modo de 1ª classe) |
| OCR (ALERTA) | Build camada 1 (pdfplumber) · Buy AWS Textract (PDF scan) · Build LLM local (classificador) |
| Integrações públicas (PNCP, Painel Preços, SEFAZ, SINAPI, DOU, Transferegov) | Integrações via API pública documentada — build de conectores |
| Billing (FASE 5) | Defer — Stripe ou Pagar.me (decisão na FASE 5) |

## Non-negotiables

1. Nenhum dado de cliente trafega fora de **AWS sa-east-1** (LGPD Art. 33 + argumento comercial). Verificador: AWS Config rule + VPC flow log alerts.
2. **WORM imutável**: S3 Object Lock **COMPLIANCE** (não GOVERNANCE) — deleção impossível mesmo com permissões elevadas. Verificador: teste de deleção via AWS CLI deve falhar.
3. **Cadeia SHA-256 encadeada** ininterrupta: hash do laudo N entrado no laudo N+1; âncora = tenant_id. Verificador: script público de verificação independente.
4. **Zero vazamento cross-tenant**: schema-per-tenant por construção; teste de penetração por tenant isolado.
5. **Laudo como saída universal**: nenhum produto entrega só dashboard — todo produto emite laudo com validade probatória.
6. API contrato: RFC 7807 (Problem Details) · versionamento /v1 · x-tenant-id header · 202 + job_id para operações longas · rate limit 100 req/min/tenant.

## Deferred (com trigger)

- SSO/SAML 2.0 — trigger: 1º cliente enterprise (FASE 2+)
- Billing engine (Stripe vs Pagar.me) — trigger: início da FASE 5
- Multi-região — trigger: NUNCA por default (soberania); revisit only se lei brasileira mudar
- TCE conectores além de SP/MG/RJ/RS/PR/BA — trigger: demanda de municípios de outros estados (FASE 4)

## Constraints that drove this

- LGPD (Arts. 33, 37, 38) + validade jurídica em litígio → soberania sa-east-1 + WORM COMPLIANCE + cadeia hash.
- PRD P5 (multi-tenant isolado) → schema-per-tenant, rejeitando row-level security como único mecanismo.
- PRD P6 (white-label nativo) → white-label como modo de primeira classe, não feature.
- 9 produtos compartilhando laudo/auth/tenant/WORM → monorepo com workspaces (elimina duplicação no motor crítico).