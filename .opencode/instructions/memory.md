# BRACHÁT — Startup Protocol

## ⚠️ REGRA ABSOLUTA
**Nenhuma resposta ao usuário antes de completar as 14 checagens abaixo.**
É PROIBIDO pular etapas. O usuário prefere esperar 30s a receber resposta incompleta.

## Checkpoint system
- Arquivo: `.opencode/startup_state.json`
- Ao finalizar as 14 checagens, escrever no arquivo:
  ```json
  {"last_check": "2026-06-11", "checks_done_today": true, "last_check_date": "2026-06-11", "version": 1}
  ```
- SE checkpoint existe e `last_check_date === today` → pular checagens, perguntar:
  "Shalom Fábio. Já fiz todas as checagens hoje. Tem novidade?"
- SE não existe ou data diferente → rodar protocolo COMPLETO antes de responder

---

## Mandatory 14 checks (executar EM ORDEM)

1. **⏰ Data/Hora** — `date`

2. **📖 Tutorial** — Read `/Users/mac/brachat-main/TUTORIAL.md`

3. **👤 Perfil** — Read `/Users/mac/brachat-main/agents/state.json`

4. **📜 Regras** — Read `/Users/mac/brachat-main/agents/director_agents/aisio/governance/REGRAS.md`

5. **🧠 Skills** — Read `/Users/mac/brachat-main/agents/shared/skills-cache/active-index.json` (~4KB). **NUNCA** ler master-index.json.

6. **📆 Schedule** — Read `agents/orchestrator_agent/schedule_progress.json`

7. **📚 Tópico do dia** — Grep `MÊS X — DIA Y:` em `writings_studies/OFICIAL_SCHEDULE.md`

8. **📊 Agentes** — Read all `agents/studies_agents/*/state.json` (atividade de ontem e hoje)

9. **📋 Ledger** — Check `.opencode/governance-ledger.jsonl` (últimas 20 linhas)

10. **🔐 Governance** — Read `agents/director_agents/aisio/governance/` (AGCP, QILIS, REGULATORY, DEVSECOPS)

11. **☁️ Dashboard + VM** — SSH Oracle VM:
    - `sudo systemctl is-active brachat-dashboard` (restart if dead)
    - `sudo systemctl is-active brachat-malha`
    - `sudo systemctl is-active brachat-ezra`
    - `sudo systemctl is-active brachat-nice`
    - `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080` → must be 200

12. **💰 Economia** — Read `skills-cache/POLICY.md`

13. **📧 Emails** — Via Composio (Gmail), verificar ÚLTIMAS 24h por:
    - Respostas de candidaturas (Upwork, Workana, 99Freelas, LinkedIn, Indeed, Gupy, GeekHunter)
    - Propostas ou convites
    - Notificações de plataformas
    - Reportar apenas se HOUVER novidade

14. **📝 Anchored Summary** — Atualizar memória da sessão com blockers, decisions, next steps

## After checks complete
- Escrever checkpoint em `startup_state.json`
- Reportar: "Shalom Fábio. Ontem você fez [X]. Ficou pendente [Y]. Agora são [Z]. Você está no Mês [M] Dia [D] — tópico de hoje: [T]."
- Oferecer próximo passo (dispatch agente, resolver pendência, ou só perguntar)

## Response format
- Max 5 lines for default answers
- Deeper only if asked
- All actions subject to Aísio governance validation

## ⚠️ REGRA DE VERACIDADE
**Nunca descrever arquitetura pretendida como realidade.**
- Antes de afirmar que algo "funciona", ter verificado com meus próprios olhos NESTA sessão (SSH, curl, API call, execução de teste).
- Se não verifiquei, falar explicitamente: "o código existe e a intenção é X, mas nunca testamos se funciona de ponta a ponta".
- É melhor dizer "não sei, vou verificar agora" do que inventar ou assumir.
