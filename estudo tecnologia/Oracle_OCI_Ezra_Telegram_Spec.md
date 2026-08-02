# SPEC — Ezra OS na OCI (controle via Telegram, Mac desligado)

**Data:** 2026-07-31 · **Status:** PENDENTE DE APROVACAO (Fabio) · **Roteada por:** S12 deployment
**Custo:** R$0 (Oracle Always Free)

---

## 1. Objetivo / Estado final

Depois desta entrega, o Ezra OS roda 24/7 na OCI e é controlado pelo Fabio **pelo Telegram**, com o Mac desligado. O LLM (opencode/big-pickle via Zen) continua na nuvem — o OCI só orquestra (cliente). Nenhuma porta pública além de SSH.

## 2. Topologia (tenancy real)

| Instância | SO | Papel |
|---|---|---|
| `ezra_bot_2` (22.04 Minimal) | Ubuntu 22.04 | **PROD** — opencode serve + bridge + mem0 MCP |
| `ezra_bot_2` (20.04) | Ubuntu 20.04 | **STANDBY** — parado (evita reclaim por ociosidade; reativável em failover) |

- Shape: 2× `VM.Standard.E2.1.Micro` (1 OCPU c/ 1/8, **1 GB RAM** cada), VCN `ezra_VCN`, AD-1, região sa-saopaulo-1.
- **1 GB RAM é o gargalo** → swap de 1 GB no boot volume (47–50 GB disponíveis).

## 3. Arquitetura de fluxo

```
Telegram (app) ⇄ Bot API (nuvem)
               ⇅ long-polling (outbound, HTTPS 443)
bridge (VM PROD, Node) ⇄ opencode serve (VM PROD, 127.0.0.1:8080)
                        ↕
        Ezra brain: skills, plugins, state.json, mem0 MCP
```

- O bridge **puxa** mensagens do Telegram (outbound) e fala com o serve via localhost. **Nenhuma porta de entrada** além do SSH (22) necessária.
- `opencode serve` roda com o `opencode.json` do projeto + `.opencode/plugin/` (mesmo runtime de plugins) — **não** usar `--pure`.

## 4. Componentes

### 4.1 opencode serve (PROD)
- Instalar Node 22 + opencode (versão alinhada com a local: 1.18.5) na VM.
- `opencode serve --port 8080 --hostname 127.0.0.1 --log-level INFO`.
- Config global na VM (`~/.config/opencode/opencode.jsonc`): model `opencode/big-pickle`, provider API key, MCP mem0. Segredos via env (Seção 6).

### 4.2 Bridge Telegram (`ezra-bridge`)
Script Node único, zero dependências além de Node (usa `globalThis.fetch`), long-polling no `getUpdates`.

API do serve consumida (validade contra o SDK — caminhos reais):
- `POST /session` → criar sessão por `chat_id`
- `POST /session/{id}/message` com `parts: [{type:"text",text}]` → resposta `{ info, parts }` (bloqueante até concluir)
- `POST /session/{id}/abort` → comando `/abort`
- `GET /session/{id}` → status (busy/idle) para `/status`

Regras do bridge:
- 1 sessão por `chat_id` (mapa persistente `chats.json`), histórico contínuo.
- Concorrência: fila por chat (1 request por vez; novos turnos aguardam o atual terminar).
- Rate limit: ignorar mensagens duplicadas (`update_id`), intervalo mínimo entre comandos.
- Comandos: `/start`, `/status`, `/abort`, `/reset` (nova sessão), `/resumo`.
- Resposta: extrai `parts` de tipo `text` da resposta; se vazia, envia "concluído".
- Falhas de rede: retry com backoff; log em `bridge.log`.

### 4.3 mem0 MCP (PROD)
- Python + `mem0-mcp-server` na VM (como no Mac). Chave em env.

### 4.4 systemd (PROD)
- `ezra-serve.service` — `ExecStart` do serve; `Restart=on-failure`, `RestartSec=5`.
- `ezra-bridge.service` — bridge; `After=ezra-serve.service`; `Restart=always`.
- `ezra-synth.service` — carga sintética (Seção 8), ativo.

## 5. Sync do cérebro (recomendação: git remote privado)

**Melhor solução:** repo **GitHub privado** para o `brachat-main`.

| Item | Destino |
|---|---|
| Código (skills, plugins, instructions, opencode.json, mcp) | repo git privado → clone na VM |
| Runtime data (`state.json`, `governance-ledger.jsonl`, `proposals/`, mem0) | volume da VM apenas; **excluído do repo** (`.gitignore`) |
| Segredos | env do systemd (nunca no repo) |

- Deploy = `git pull` + `systemctl restart ezra-serve`.
- Rollback = `git checkout <tag>` + restart.
- Alternativa (rsync/scp) descartada: sem histórico, sem rollback limpo, sem rastreio de diffs.

## 6. Segredos (env do systemd, nunca no repo)

- `TELEGRAM_BOT_TOKEN` (já existe no BotFather)
- `MEM0_API_KEY`
- Chave API do provider de modelo (Zen/custom-proxy)

## 7. Segurança

- Firewall (security list / UFW): permitir apenas 22 (SSH) da minha rede; 8080 só localhost.
- Autenticação SSH por chave; `PasswordAuthentication no`; sem root.
- Bridge e serve rodam como usuário dedicado (`ezra`), não root.
- `opencode serve` bound em 127.0.0.1 — não exposto à internet.
- fail2ban (SSH) recomendado, opcional.

## 8. Anti-reclaim + health check

Oracle reivindica instâncias Always Free com <20% de uso por 7 dias. Mitigações:
- `ezra-synth.service`: carga sintética leve e periódica (CPU ~5–15% por ~2 min a cada 30 min) + health check HTTP do serve.
- Health check: `curl localhost:8080/app` (ou endpoint do serve) a cada 5 min; falha → alerta via Telegram (mensagem do próprio bridge).

## 9. Backup / Rollback

- Código: git (tags por deploy).
- Estado: backup noturno `tar` de `.opencode/state.json`, ledger e mem0 → Object Storage (20 GB free) via OCI CLI.
- Pré-deploy: copiar `state.json` para `state.pre-<deploy>.bak` no volume.
- Rollback automatizado se health check falhar nos primeiros 5 min pós-deploy (skill S12).

## 10. Riscos e limitações

| Risco | Mitigação |
|---|---|
| 1 GB RAM insuficiente | Swap 1 GB; monitorar `free`; se estourar, mover mem0 p/ instância standby |
| Reclaim por ociosidade | Carga sintética (Seção 8) |
| Latência Telegram | Aceitável p/ uso interativo; bridge é long-polling |
| Resposta muito longa p/ Telegram | Truncar + `…` + comando `/resumo` para o restante |
| Plugins do Ezra ainda sem prova de runtime | Fazer a validação sentinel NA VM antes de confiar (gate de skills) |
| Mac desligado = sem acesso aos arquivos do Mac | Ezra age só no OCI; repo é o transporte de código |

## 11. Fases de execução (após aprovação)

1. **F1 Pré**: criar repo GitHub privado; `.gitignore` (state/ledger/proposals/mem0/secrets); push do brachat-main.
2. **F2 VM PROD**: anexar IP público (ephemeral), SSH, hardening (chave, UFW), swap 1 GB, instalar Node 22 + opencode.
3. **F3 Config**: `~/.config/opencode/opencode.jsonc` com model + mem0; secrets em env do systemd.
4. **F4 Código**: clone do repo em `/home/ezra/brachat-main`; `opencode serve` rodando.
5. **F5 Bridge**: escrever `ezra-bridge`; systemd; teste manual: Fabio envia msg no Telegram → resposta.
6. **F6 Sentinel + gate**: validar carregamento dos plugins na VM (marca de boot); ativar `skill-gate` lá.
7. **F7 Anti-reclaim + backup**: `ezra-synth`, health check, tar noturno → Object Storage.
8. **F8 Validação final (checklist S12)**: backup pré-deploy ✓, health check ✓, rollback testado ✓, versão tagada ✓.

## 12. Checklist de validação (S12)

- [ ] Backup do estado anterior criado antes de cada deploy?
- [ ] Health check passou após deploy?
- [ ] Rollback restaurou estado sem perda?
- [ ] Versão incrementada/tagada?
- [ ] Plugins provados em runtime (sentinel) na VM?
- [ ] Telegram responde do zero com o Mac desligado?
