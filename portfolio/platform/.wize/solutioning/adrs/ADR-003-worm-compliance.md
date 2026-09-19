---
status: accepted
owner: Tony Stark
created: 2026-09-18
---

# ADR-003 — Cofre WORM com S3 Object Lock COMPLIANCE

## Context

Cadeia probatória exige imutabilidade: nem a EZRA, nem administradores AWS podem deletar/alterar laudos dentro do período de retenção. Modo GOVERNANCE permite deleção por permissões elevadas — insuficiente para validade judicial.

## Decision

AWS S3 com Object Lock em modo **COMPLIANCE** (não GOVERNANCE), bucket dedicado `ezra-worm-vault-prod`, versioning obrigatório, retenção 10 anos (LGPD Art. 37), SSE-KMS com chave por tenant (prod), região sa-east-1.

## Consequences

- (+) Imutabilidade real: deleção falha mesmo com permissões elevadas — testável (NFR Sec-02).
- (+) Atende LGPD Arts. 37/38 e validade pericial.
- (-) Direito ao esquecimento (LGPD Art. 18) limitado: dado no WORM não pode ser deletado no período — declarado em contrato (base legal Art. 16, II e Art. 37).
- Fonte: PRD §3.5, §7.2.