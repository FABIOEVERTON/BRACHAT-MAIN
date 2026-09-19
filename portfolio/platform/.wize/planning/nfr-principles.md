---
status: aligned
owner: Nick Fury
created: 2026-09-18
---

# NFR Principles — Plataforma EZRA

## Why these numbers

Plataforma SaaS regulada (LGPD, PL 2338, ISO 42001, Lei 14.133) onde cada ação gera laudo com validade **probatória em litígio**. Isso muda tudo: disponibilidade e imutabilidade são requisitos jurídicos, não só técnicos. Público: empresas brasileiras reguladas (Ramo 1) e municípios + ONGs (Ramo 2), operação 24/7 com picos em janelas de diligência (Ramo 2) e revalidação de modelos (Ramo 1). Auditoria externa por peritos independentes exige verificabilidade pública do hash e trilhas imutáveis. Firmamos cada número abaixo a um verificador executável — nenhum é meta aspiracional.

## Performance

| Tier | Targets | Verifier |
|---|---|---|
| Non-negotiable | Endpoints síncronos p95 < 300ms (PRD §11.1) | Grafana + teste de carga k6/stress no pipeline |
| Non-negotiable | Laudo simples < 60s; auditoria completa < 5min (processamento assíncrono) | job_id monitorado; SLO de duração por tipo de laudo |
| Non-negotiable | GUARDIAN proxy adiciona < 50ms p95 por chamada (FASE 3) | teste de latência no gate do epic |
| Non-negotiable | Detecção de mudança de modelo AEGIS < 6h; alerta CAUC CRITICAL < 5min | testes de integração com clock simulado + smoke |
| Stretch | Endpoints síncronos p95 < 200ms | idem |
| Deferred | Edge/CDN para conteúdo estático — revisit quando DAU > 10k | — |

## Security

| Tier | Items | Verifier |
|---|---|---|
| Non-negotiable | Dados nunca fora de sa-east-1 (LGPD Art. 33) | AWS Config rule + VPC flow log alerts |
| Non-negotiable | WORM S3 Object Lock **COMPLIANCE**, retenção 10 anos (LGPD Art. 37) | teste automatizado: deleção via AWS CLI deve FALHAR |
| Non-negotiable | TLS 1.3 em todos os endpoints; scan SSL Labs ≥ A | CI check + alerta de drift |
| Non-negotiable | JWT 1h + refresh 7d; MFA obrigatório p/ TENANT_ADMIN e WHITELABEL_OPERATOR | testes de auth + policy |
| Non-negotiable | Zero cross-tenant | schema-per-tenant + teste de penetração por tenant |
| Non-negotiable | OWASP Top 10 coberto; segredos nunca em logs; secrets via AWS Secrets Manager | SAST no pipeline (gitleaks + ruff/lint) |
| Stretch | SOC2 type-I — revisit antes de FASE 5 (billing) | — |
| Deferred | Pentest externo — trigger: 1º cliente em setor regulado (banco/saúde) | — |

## Reliability

| Tier | Targets | Verifier |
|---|---|---|
| Non-negotiable | SLA 99,5% (PRD §11.1); error budget ≤ 0,5%/mês | Statuspage + error budget tracker |
| Non-negotiable | Jobs assíncronos idempotentes com dedup key (job_id) | testes de idempotência no motor de jobs |
| Non-negotiable | Backup RDS diário, retenção 35d (PRD §6.2) | AWS Backup policy + teste de restore trimestral |
| Non-negotiable | WORM: versioning obrigatório no bucket | Config rule |
| Stretch | 99,9% mensal | idem |
| Deferred | Multi-região — NUNCA por default (soberania legal) | — |

## Maintainability

| Tier | Items | Verifier |
|---|---|---|
| Non-negotiable | Cobertura de testes ≥ 80% (Python: pytest; TS: Vitest) | cobertura no CI (fail abaixo de 80%) |
| Non-negotiable | TypeScript strict mode, zero `any` explícito | `tsc --strict` no CI |
| Non-negotiable | Linting: Ruff (Python) · ESLint + Biome (TS) | CI lint stage |
| Non-negotiable | ADR para toda decisão arquitetural | política: PR sem ADR não merge; gate TEA review |
| Non-negotiable | Testes de integração: ≥ 1 por endpoint público; E2E Playwright por produto (PRD §11.3) | CI |
| Stretch | Complexidade ciclomática < 15; arquivos < 300 LOC | biome/lizard report mensal |

## Accessibility

| Tier | Items | Verifier |
|---|---|---|
| Non-negotiable | WCAG 2.2 AA em toda página pública do web (overlay web) | axe-core no CI + revisão Hawkeye |
| Non-negotiable | Navegação completa por teclado; contraste AA | axe-core |
| Stretch | AAA em fluxos críticos (login, emissão de laudo) | — |
| Deferred | Auditoria manual com leitor de tela — trigger: release de white-label para banca | — |

## Cost

| Tier | Targets | Verifier |
|---|---|---|
| Non-negotiable | Infra dev local zero-custo real (Docker + LocalStack) | sem credenciais AWS no dev |
| Non-negotiable | Estratégia de degradação documentada para pico 10× | runbook em docs/ |
| Stretch | Stage + prod dentro do free-tier/commitment AWS para early stage | monthly cost report |
| Deferred | Atribuição de custo por tenant/feature — trigger: financeiro pedir (FASE 5 billing) | — |

## Hand-off

> NFRs em `.wize/planning/nfr-principles.md`. Tony: architecture deve respeitar Perf-01 (jobs assíncronos) e Security-01/02 (soberania + WORM) desde o dia 1. Hawkeye: gate NFR por epic é mandatório, mesmo com policy advisory. Shuri: cada story traz o endereço do verificador no teste.