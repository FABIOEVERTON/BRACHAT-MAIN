---
status: accepted
owner: Tony Stark
created: 2026-09-18
---

# ADR-006 — White-label como modo de primeira classe

## Context

P6: white-label não é feature adicionada — é modo de operação. Bancas, contabilidades e associações operam sob sua marca; laudos carregam a identidade do operador como signatário, mas hash/WORM são sempre da EZRA.

## Decision

Desde a base: `WhitelabelConfig` tipado (brandName, logoUrl, colors, signatory name/title/register, customDomain, hidePoweredBy), resolução de tenant por subdomínio/domínio custom, ThemeProvider com CSS vars, hierarquia `EZRA → WhitelabelOperator → EndClient`, RBAC com roles WHITELABEL_ADMIN/OPERATOR.

## Consequences

- (+) Sem refactor futuro; laudo emitido sob white-label com signatário correto por construção.
- (+) Regra crítica: hash + WORM sempre EZRA, nunca transferíveis (declarado em contrato).
- (-) Gestão de domínios custom e certificados por operador (fase 5).
- Fonte: PRD §3.6, §8.