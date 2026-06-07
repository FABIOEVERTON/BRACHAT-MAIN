# BRACHÁT — Startup Protocol

## Mandatory steps at session start

1. Run `date` — discover current time and day
2. Read `/Users/mac/brachat-main/TUTORIAL.md` — ecosystem overview, harness pattern, schedule
3. Read `/Users/mac/brachat-main/assistant_agents/state.json` — user profile, routine, pipeline
4. Read `/Users/mac/brachat-main/assistant_agents/REGRAS.md` — system rules, contract
5. Read `/Users/mac/brachat-main/assistant_agents/skills-cache/active-index.json` — available agents + skill categories (~4KB). **NUNCA** ler master-index.json (549KB) ou SKILL.md individuais a menos que necessário para a tarefa.
6. Read `daily/estudos/cache.json` — current phase/module/day and which checkpoints are delivered
7. Read `writings_studies/shared/official_schedule.md` — find the topic for the current day
8. Read all other `daily/*/cache.json` in `assistant_agents/` — what was done yesterday
9. Report to user: "Shalom Fábio. Ontem você fez [X]. Ficou pendente [Y]. Agora são [Z] — horário de [atividade]. Voce esta no Módulo [M] Dia [D] — aqui esta o topico de hoje."

10. Load `shared/governance/` — AGCP, QILIS, regulatory compliance framework. Aísio ativo — toda ação passa por commit-bound authorization.
11. Check `assistant_agents/.opencode/governance-ledger.jsonl` — pending governance items
12. Economy: `skills-cache/POLICY.md` — NUNCA carregar mais que active-index.json em contexto.

## Response format
- Max 5 lines for default answers
- Deeper only if asked
- Always run `date` before reporting schedule
- All actions subject to Aísio governance validation
