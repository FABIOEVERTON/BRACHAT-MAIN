---
epic_id: 04-mcp-runtime-governance
status: ready-for-dev
owner: Tony Stark + Maria Hill
linked_prd: ÉPICO 4
trigger_map_row: 3
priority: 4
estimate: M
---

# Epic 04: Governança de Runtime e Agentes via MCP

## Outcome

Tech Lead configura permissões de ferramentas dos agentes; gateway auditado nega por padrão e retém ações sensíveis para aprovação humana (Decision Ledger).

## Stories
- E04-S01: Console de ACL de ferramentas por tenant (AC-04-D1) — R-3
- E04-S02: Gateway MCP deny-by-default + trilha indelével (AC-04-2, AC-04-3) — R-3
- E04-S03: Fluxo HITL para ações sensíveis > R$ 5k (AC-04-1) — R-3

## Dependencies
- ADR-003 (gateway MCP) + Audit_Logs + Decision Ledger

## Success
Nenhuma chamada sensível executa sem linha no Decision Ledger; custo de gate < 50 ms p95.