---
status: aligned
owner: Nick Fury
created: 2026-09-17
---

# NFR Principles — EZRA AI Governance Platform

Derivado de: `tech-vision.md` + PRD Parte 2 (§2.4/§2.5). Os níveis abaixo são o contrato; Tony projeta dentro deles, Hawkeye testa contra eles.

## Performance

| # | Nível | Critério |
|---|---|---|
| PERF-1 | Non-negotiable | CRUD p95 < 200 ms na região BR |
| PERF-2 | Non-negotiable | Compilação do laudo (PDF + hash + WORM) p90 < 10 s |
| PERF-3 | Target | API p99 < 500 ms |
| PERF-4 | Deferred | Edge-first para leituras fora do BR (não ativo no MVP) |

## Segurança

| # | Nível | Critério |
|---|---|---|
| SEC-1 | Non-negotiable | RLS + FORCE em 100% das tabelas de negócio; filtro `tenant_id` explícito em toda query |
| SEC-2 | Non-negotiable | PII nunca deixa a região BR; criptografia at-rest (AES-256) e in-transit (TLS 1.3 + HSTS) |
| SEC-3 | Non-negotiable | MFA compulsório (RFC 6238) para admin/auditor antes de qualquer escopo elevado |
| SEC-4 | Non-negotiable | Hash SHA-256 de payload em todo evento crítico do `Audit_Logs` |
| SEC-5 | Target | OWASP Top 10 API + regras LLM no WAF da borda |

## Confiabilidade

| # | Nível | Critério |
|---|---|---|
| REL-1 | Non-negotiable | Disponibilidade 99.9% mensal |
| REL-2 | Non-negotiable | Erro 5xx < 0.05% do tráfego |
| REL-3 | Non-negotiable | Circuit breaker em integrações externas (abre com >40% falhas em 30 s) |
| REL-4 | Non-negotiable | Retries com backoff exponencial + jitter; DLQ após 5 tentativas |
| REL-5 | Target | RTO ≤ 1 h, RPO ≤ 15 min (backups OCI criptografados) |

## Acessibilidade

| # | Nível | Critério |
|---|---|---|
| A11Y-1 | Target | WCAG 2.2 AA para telas públicas (validação QR) e fluxos de login |
| A11Y-2 | Deferred | WCAG completo no console de auditoria (pós-MVP) |

## Custo

| # | Nível | Critério |
|---|---|---|
| COST-1 | Non-negotiable | Entry plan viável a R$ 1.890/mês → custo de infra por tenant ativo < R$ 90/mês |
| COST-2 | Target | Autoscaling de workers orientado a fila (Celery) para evitar idle pago |

## Gate Strategy (para Hawkeye)

- **Advisory**: preenchimento dos 122 controles permite gaps com aviso por nível (L1–L4).
- **Enforcing**: ALTO RISCO (Art. 17) sem testes de viés (Art. 19) e supervisão humana (Art. 21) → bloqueia `CERTIFIED` e emissão de laudo positivo, no motor de compliance (não só na UI).