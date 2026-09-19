---
status: accepted
owner: Tony Stark
created: 2026-09-18
---

# ADR-008 — Soberania de dados: AWS sa-east-1 exclusiva

## Context

LGPD Art. 33 (transferência internacional) + argumento comercial (única solução brasileira com inventário + postura + runtime em laudo único). Nenhum dado do cliente pode trafegar fora do território nacional.

## Decision

Toda infraestrutura em AWS São Paulo (sa-east-1): RDS Multi-AZ, S3 WORM, SQS, ECS. Proibido por construção: nenhum data plane fora da região. AWS Config rules + alertas de VPC flow log como verificadores (NFR Sec-01). Deploy do GUARDIAN em VPC/on-premise do cliente mantém o mesmo princípio.

## Consequences

- (+) Compliance LGPD Art. 33 por construção; não por política.
- (+) Diferencial competitivo vs concorrentes globais.
- (-) Região única: indisponibilidade regional = indisponibilidade da plataforma (SLA 99,5% mitigado via Multi-AZ).
- (-) Multi-região descartada por default (ADR explícito de não-decisão até mudança legal).
- Fonte: PRD §1.2 (P3), §6.1.