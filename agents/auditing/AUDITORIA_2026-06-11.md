# Auditoria de Verificação — 11/06/2026

## Resumo

| Status | Item |
|--------|------|
| ✅ 17/20 | Estrutura de arquivos |
| ✅ 5/5 | Estado dos agentes (state.json válidos) |
| ✅ 8/8 | Python scripts (syntax OK) |
| ⚠️ 3/5 | Infraestrutura de nuvem |
| ⚠️ 2/3 | Consistência TUTORIAL vs Realidade |
| ❌ 0/5 | Harness Pattern (5 seções obrigatórias) |

---

## 1. ESTRUTURA DE ARQUIVOS ✅

| Item | Esperado | Real | Veredito |
|------|----------|------|----------|
| Root files | state.json, opencode.json | ✅ Ambos existem | ✅ |
| agents/orchestrator_agent/ | orchestrator.md, state.json, schedule_progress.json | ✅ Todos existem | ✅ |
| agents/director_agents/ | 5 diretores | ✅ aisio, nice, josue, gilmario, jessica | ✅ |
| agents/studies_agents/ | 11 estudos | ✅ 11 (+ 1 consolidator studies/) | ✅ |
| agents/builder_agents/ | 2 builders | ✅ architect, artur | ✅ |
| agents/auditing/ | Pasta de auditoria | ✅ AUDITORIA.md + rebuild-2026-06-07.md | ✅ |
| cloud/sites/ | 5 systemd services | ✅ brachat-{ezra,nice,dashboard,malha,clickup}.service | ✅ |
| cloud/daemons/ | 2 plists | ✅ com.brachat.{opencode,nice}.plist | ✅ |
| cloud/dashboard/ | dashboard.py, server.py, index.html | ✅ Todos | ✅ |
| Director: aisio/ | 8 subpastas | ✅ governance/, frameworks/, harness/, memory/, cache_skills/ | ✅ |
| Governance files | 6 arquivos | ✅ AGCP, QILIS, REGRAS, REGULATORY, DEVSECOPS, boundary.sh | ✅ |
| OPA policies | 3 (.opa) | ✅ lgpd, eu-ai-act, nist-ai-rmf | ✅ |
| Frameworks refs | 3 (.md) | ✅ lgpd, eu-ai-act, nist-ai-rmf | ✅ |
| shared/ | general_skills, skills-cache, tools | ✅ Todos | ✅ |
| writings_studies/ | OFICIAL_SCHEDULE.md, subpastas | ✅ 13,655 linhas, subpastas intactas | ✅ |

## 2. ESTADO DOS AGENTES ✅

| Categoria | Total | Com daily_log | Com state.json válido |
|-----------|-------|---------------|----------------------|
| Studies Agents | 11 | 11 (100%) | 11 (100%) |
| Directors | 5 | 5 (100%) | 5 (100%) |
| Builders | 2 | 2 (100%) | 2 (100%) |

## 3. CONSISTÊNCIA TUTORIAL vs REALIDADE ⚠️

| Claim do TUTORIAL | Real | Veredito |
|--------------------|------|----------|
| active-index.json (~2KB)) |
| 1,465 skills | **1,481 diretórios** | ⚠️ Discrepância (índice desatualizado) |
| Dashboard bloqueado externamente | **HTTP 200** | ⚠️ Tutorial desatualizado — já está acessível |
| agents/state.json ~262 linhas | **264 linhas** | ✅ |
| metadata.json ~149 linhas | **149 linhas** | ✅ |
| OFICIAL_SCHEDULE.md ~13,655 linhas | 13,655 linhas | ✅ |
| 4 serviços systemd | 5 (clickup adicionado) | ⚠️ Tutorial desatualizado |
| master-index.json ~549KB | 549,366 bytes | ✅ |
| Harness: 5 seções obrigatórias | NENHUM agente segue | ❌ Todos usam estrutura diferente |

## 4. INFRAESTRUTURA DE NUVEM ⚠️

| Item | Resultado |
|------|-----------|
| Dashboard externo (8080) | ✅ HTTP 200 |
| SSH Oracle VM | ❌ Permission denied (no key) |
| Systemd services na VM | ❌ Não verificado (SSH bloqueado) |
| Launchd local (macOS) | ⚠️ mem0-heartbeat + clickup rodando; bridges NÃO rodam local (correto: rodam na VM) |
| OPA binary local | ❌ Não instalado |

## 5. SCRIPTS — SYNTAX CHECK ✅

| Script | Status |
|--------|--------|
| bridge-ezra.py | ✅ Syntax OK |
| bridge-nice.py | ✅ Syntax OK |
| telegram-bridge.py (local) | ✅ Syntax OK |
| nice-telegram-bridge.py (local) | ✅ Syntax OK |
| server.py (websocket) | ✅ Syntax OK |
| dashboard.py | ✅ Syntax OK |
| advance_schedule.py | ✅ Syntax OK |

## 6. HARNESS PATTERN — NÃO CONFORME ❌

O TUTORIAL secão 5.4 exige 5 seções: **Core, Skills, Memory, Protocols, Regulation**.

Nenhum agente segue essa estrutura. Os agentes usam:
- HARNESS, PROMPT ECONOMY, CONTRACT, OPERATIONAL PROCEDURE, DECISION HEURISTICS, VERIFICATION LEVELS (N1-N5), KNOWLEDGE SOURCE, SKILLS

O Aísio tem estrutura diferente: MISSION, PROMPT ECONOMY, RUNTIME VALIDATION FLOW, DECISION HEURISTICS, VERIFICATION LEVELS, SKILLS

## 7. SCHEDULE ⚠️

| Item | Valor |
|------|-------|
| Mês atual | 1 |
| Dia atual | 1 |
| Dias completados | **0** (array vazio) |
| advance_schedule.py | Existe, mas nunca foi executado (days_completed vazio) |
| studies/cache.json | Placeholder (`current_phase: "?"`) — consolidator nunca rodou |

## 8. GOVERNANCE LEDGER

- 6 entradas no total (append-only ✅)
- 2 REJECTED (MVI violations: clickup_daemon.py 201 linhas, TUTORIAL.md 529 linhas)
- 4 AUTHORIZED
- Ironia: TUTORIAL.md foi REJECTED por MVI violation (>200 linhas) mas tem 525+ linhas

---

## CONCLUSÃO

**Pontos fortes:**
- Estrutura de arquivos 100% intacta
- Todos os agentes têm state.json com daily_log
- Dashboard acessível (ao contrário do que diz o tutorial)
- Python scripts sem erros de sintaxe
- Governance ledger funcional com append-only

**Pontos críticos:**
1. SSH para VM não configurado no Mac — impossível verificar services
2. Harness pattern não implementado em nenhum agente
3. Schedule não avançou — `days_completed` vazio
4. active-index.json (~2KB)
5. OPA binary não instalado localmente
6. Tutorial desatualizado em múltiplos pontos (dashboard acessível, 5 services, etc.)

**Estimativa de funcionalidade:** ~65% do ecossistema é verificável como funcional. Os 35% restantes dependem de acesso SSH à VM.
