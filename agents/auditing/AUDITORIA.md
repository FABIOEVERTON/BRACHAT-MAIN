# Auditoria Geral — Domingo 06/06

## 1. Estrutura de Diretórios

- [ ] `assistant_agents/` contém apenas: `.apis/`, `.config/`, `.opencode/`, `daily/`(12), `directors/`(5), `orquestrador/`, `shared/`, `skills-cache/`, `state.json`, `metadata.json`, `REGRAS.md`, `README.md`, `LICENSE`, `requirements.txt`
- [ ] `shared/` é cópia única (não há duplicata em `substracts/` ou outro lugar)
- [ ] `daily/` tem exatamente 12 pastas de agente, cada uma com `AGENT.md`, `cache.json`, `metadata.json`
- [ ] `directors/` tem exatamente 5 pastas, cada uma com `AGENT.md`, `cache.json` (+ `metadata.json` para Nice)
- [ ] `orquestrador/` tem `AGENT.md` e `cache.json`
- [ ] Nenhum diretório `substracts/` ou `__pycache__` solto

## 2. state.json (Canônico)

- [ ] `assistant_agents/state.json` existe e é válido (JSON)
- [ ] `metadata.json` aponta para o path correto: `"state_path": "assistant_agents/state.json"`
- [ ] `orquestrador/AGENT.md` referência atualizada
- [ ] `.opencode/agent/orquestrador.md` referência atualizada
- [ ] Conteúdo do state.json reflete estado real (agentes, launchd, comunicação, etc.)

## 3. Agentes — Harness Completo (5 Módulos)

### Orquestrador (1)
- [ ] `orquestrador/AGENT.md`: Núcleo, Skills, Memória, Protocolos, Regulação

### Diretores (5)
- [ ] `directors/josue/AGENT.md` — 5 módulos
- [ ] `directors/gilmario/AGENT.md` — 5 módulos
- [ ] `directors/aisio/AGENT.md` — 5 módulos
- [ ] `directors/jessica/AGENT.md` — 5 módulos
- [ ] `directors/nice/AGENT.md` — 5 módulos

### Daily Agents (12)
- [ ] `daily/ingles/AGENT.md` — 5 módulos
- [ ] `daily/politica/AGENT.md` — 5 módulos
- [ ] `daily/filosofia/AGENT.md` — 5 módulos
- [ ] `daily/certificacoes/AGENT.md` — 5 módulos
- [ ] `daily/google-skills/AGENT.md` — 5 módulos
- [ ] `daily/python/AGENT.md` — 5 módulos
- [ ] `daily/pmp/AGENT.md` — 5 módulos
- [ ] `daily/ml-engineer/AGENT.md` — 5 módulos
- [ ] `daily/job-hunter/AGENT.md` — 5 módulos
- [ ] `daily/freelancer/AGENT.md` — 5 módulos
- [ ] `daily/portfolio/AGENT.md` — 5 módulos
- [ ] `daily/nice/AGENT.md` — (ainda existe em daily/ mesmo com cópia em directors/)

## 4. Launchd Services

- [ ] `com.brachat.opencode` — EZRA Telegram bridge (PID ativo)
- [ ] `com.brachat.nice` — Nice Telegram bridge (PID ativo)
- [ ] `com.brachat.antigravity` — WhatsApp bridge (status OK)
- [ ] `com.brachat.clickup` — ClickUp sync (status OK)
- [ ] Todos com `KeepAlive=true` e `RunAtLoad=true`
- [ ] Plists apontam para `assistant_agents/shared/general_scripts/` (não mais `substracts/`)

## 5. Bridges Telegram — Teste de Resposta

### EZRA (@Baruch_Everton_bot)
- [ ] Bridge responde em <3s (API direta, sem subprocesso)
- [ ] Mensagem enviada recebe resposta coerente
- [ ] Logs em `/tmp/telegram-bridge.log` ativos

### Nice (@luevertonbot)
- [ ] Bridge responde em <3s
- [ ] Mensagem enviada recebe resposta coerente (Nice persona)
- [ ] Logs ativos

## 6. Conexões Ativas

- [ ] Telegram (EZRA) — chat Fábio: `8035491919`
- [ ] Telegram (Nice) — chat Dona Lu: `8722951907`
- [ ] ClickUp — workspace conectado (Composio)
- [ ] LinkedIn — conectado (Composio)
- [ ] WhatsApp (Baileys) — servidor na porta 3456

## 7. Cache.json — Cada Agente

- [ ] `orquestrador/cache.json` válido
- [ ] `directors/*/cache.json` válido (5)
- [ ] `daily/*/cache.json` válido (12)
- [ ] `daily/nice/cache.json` (duplicado com directors/nice/ — decidir qual manter)

## 8. Skills e Scripts

- [ ] `shared/general_scripts/telegram-bridge.py` — API direta, sem subprocesso
- [ ] `shared/general_scripts/nice-telegram-bridge.py` — API direta + broadcast
- [ ] `shared/general_harness/` — template harness disponível
- [ ] `shared/general_skills/` — catálogo de skills (1.480 dirs)

## 9. Pontos de Decisão

- [ ] `daily/nice/` vs `directors/nice/` — remover duplicata de `daily/`
- [ ] `directors/aisio|gilmario|jessica|josue` sem `metadata.json` — criar ou remover dependência
- [ ] WhatsApp Baileys — porta 3456 ainda relevante? Manter ou desligar?
- [ ] Logs antigos em `/tmp/*.log` — limpar

---

**Rodar:** Domingo, passo a passo, marcar cada item.
**Critério:** 100% de cada agente e conexão verificados — sem suposições.
