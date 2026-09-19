---
status: accepted
owner: Tony Stark
created: 2026-09-18
---

# ADR-004 — Cadeia de custódia SHA-256 encadeada

## Context

O lock-in legítimo e a integridade probatória dependem de cadeia contínua: cada laudo referencia o anterior. Migrar de plataforma quebra a cadeia — argumento de permanência sem cláusula de fidelidade.

## Decision

`chain_hash = SHA256(content_hash + previous_chain_hash)`; primeiro laudo do tenant usa âncora = tenant_id. Hash do conteúdo = SHA256 do PDF renderizado. Cadeia inicia no primeiro produto contratado e nunca reinicia.

## Consequences

- (+) Cadeia verificável externamente (script público) — VR: perito independente pode re-verificar.
- (+) Lock-in estrutural: trocar de fornecedor fragmenta o histórico probatório.
- (-) Toda emissão deve ler o último chain_hash (serialização por tenant na escrita de laudos).
- Fonte: PRD §3.4, nota final do doc de arquitetura.