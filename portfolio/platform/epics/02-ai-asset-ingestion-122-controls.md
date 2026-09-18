---
epic_id: 02-ai-asset-ingestion-122-controls
status: ready-for-dev
owner: Tony Stark + Maria Hill
linked_prd: ÉPICO 2
trigger_map_row: 2
priority: 2
estimate: L
---

# Epic 02: Ingestão de Ativos de IA e Varredura dos 122 Controles AGCP

## Outcome

DPO/auditor cadastra um pipeline de IA e descobre enquadramento (Art. 13/17 PL 2338) e gaps dos 122 controles — incluindo Shadow AI.

## Stories
- E02-S01: Cadastro de ativo de IA (LLM/RAG/agente) (AC-02-D1) — R-9
- E02-S02: Motor de regras PL 2338 — alto risco / prática vedada (AC-02-1, AC-02-2) — R-2
- E02-S03: Questionário 122 controles L1–L4 + score (AC-02-D2) — R-2
- E02-S04: Parser seguro de configs + detecção de Shadow AI (AC-02-3) — R-9

## Dependencies
- `libs/compliance` (motor de regras) + pgvector
- Arquitetura §1 Fronteira B

## Success
ALTO RISCO sem viés/supervisão bloqueia `CERTIFIED` (gate enforcing).