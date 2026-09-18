---
status: accepted
date: 2026-09-17
deciders: Tony Stark, Hawkeye (gate), Nick Fury
---

# ADR-003 — Gateway MCP com deny-by-default e Human-in-the-Loop

## Contexto

PRD Épico 4: governar ferramentas de agentes autônomos do cliente. Risco: ação destrutiva ou financeira sem autorização humana (ex.: `execute_wire_transfer` > R$ 5.000,00).

## Opções

1. **Proxy passivo (log-only)** — audita mas não bloqueia; aceitável para observabilidade, insuficiente para responsabilização Art. 27 PL 2338.
2. **Allowlist explícita + deny-by-default com HITL** — ferramentas fora do ACL são negadas; ações sensíveis retidas até aprovação humana registrada no Decision Ledger.
3. **Sem gateway (tool use direto)** — inviável para o produto; sem trilha pericial.

## Decisão

**Adotar opção 2**: gateway MCP da EZRA intercepta todas as chamadas `tools.*`:
- Ferramenta fora do ACL → negação por padrão, evento `UNKNOWN_TOOL`, sugestão de permissão explícita ao admin.
- Ação sensível (transferência > R$ 5k) → retenção + notificação de aprovação obrigatória + registro no `Decision Ledger`.
- Todo resultado (APROVADO/NEGADO/RETIDO) gravado no `Audit_Logs` com hash do payload.

## Consequências

- (+) Responsabilização: decisão humana documentada e congelada (cadeia para Art. 27).
- (+) Alinha ao NFR SEC-3 (MFA) e ao gate enforcing de ALTO RISCO.
- (−) Latência adicional na chamada MCP (gate + ledger) — budget < 50 ms p95 por chamada.
- (−) Requer gestão de ACL por tenant — UI de console + migração de permissões a cada release de ferramenta.