# BRACHÁT — Startup Protocol

## Mandatory steps at session start

1. Run `date` — discover current time and day
2. Read `/Users/mac/brachat-main/TUTORIAL.md` — ecosystem overview, harness pattern, schedule
3. Read `/Users/mac/brachat-main/agents/state.json` — user profile, routine, pipeline
4. Read `/Users/mac/brachat-main/agents/director_agents/aisio/governance/REGRAS.md` — system rules, contract
5. Read `/Users/mac/brachat-main/agents/shared/skills-cache/active-index.json` — available agents + skill categories (~4KB). **NUNCA** ler master-index.json (549KB) ou SKILL.md individuais a menos que necessário para a tarefa.
6. Read `agents/orchestrator_agent/schedule_progress.json` — current day/month and which days are delivered
7. Read `writings_studies/OFICIAL_SCHEDULE.md` — find the topic for the current day (grep `MÊS X — DIA Y:`)
8. Read all `agents/studies_agents/*/state.json` — what was done yesterday and today
9. Report to user: "Shalom Fábio. Ontem você fez [X]. Ficou pendente [Y]. Agora são [Z] — horário de [atividade]. Voce esta no Mês [M] Dia [D] — aqui esta o topico de hoje."

10. Load `agents/director_agents/aisio/governance/` — AGCP, QILIS, regulatory compliance framework. Aísio ativo — toda ação passa por commit-bound authorization.
11. Check `.opencode/governance-ledger.jsonl` — pending governance items
12. Start dashboard — `ssh -i /Users/mac/brachat-main/integrations/apis/ssh-key-2026-06-10.key opc@147.15.18.252 'sudo systemctl is-active brachat-dashboard || sudo systemctl restart brachat-dashboard'`; confirm HTTP 200 at `http://147.15.18.252:8080`
13. Economy: `skills-cache/POLICY.md` — NUNCA carregar mais que active-index.json em contexto.
14. Check emails from freelance/job platforms (fabioeverton1704@gmail.com, jae.engenharia@gmail.com, igorbrachat@gmail.com) — search for replies from job applications, proposals, platform notifications (Upwork, Workana, 99Freelas, LinkedIn, Indeed, Gupy, GeekHunter). Report relevant updates.

## Response format
- Max 5 lines for default answers
- Deeper only if asked
- Always run `date` before reporting schedule
- All actions subject to Aísio governance validation
