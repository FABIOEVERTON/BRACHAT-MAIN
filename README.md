<h1 align="center">BRACHAT-MAIN</h1>

<p align="center">
  <strong>Hub central do ecossistema Brachát</strong><br/>
  <em>Monorepo com o cérebro (Ezra) e os agentes de produção: bots Telegram, estudo da Parashá, curadoria e projetos de portfólio.</em>
</p>

---

## Arquitetura de Infraestrutura

O ecossistema roda em 3 camadas:

```
┌──────────────────────────────┐     ┌──────────────────────────────┐
│  MAC (Fabio)                 │     │  GITHUB                     │
│  ─ ponto de produção         │◄───►│  BRACHAT-MAIN.git           │
│  - git + Drive (backups)     │     └──────────────────────────────┘
│  - launchd: backup/commit/   │
│    sync a cada 3 min         │     ┌──────────────────────────────┐
│  - ~/.opencode (cérebro)     │◄──► │  OCI ezra_bot_1 (163.176.111.95)
│  - secrets.env (fonte)       │sync │  - bots Telegram em produção │
└──────────────────────────────┘     │  - cérebro espelhado        │
                                     └──────────────────────────────┘
                                     ┌──────────────────────────────┐
                                     │  OCI ezra_bot_2 (137.131.242.180)
                                     │  - acquirer A1.Flex 12GB     │
                                     └──────────────────────────────┘
```

### Papel de cada camada

| Camada | Função |
|--------|--------|
| **Mac** | Fonte de verdade. Edição do cérebro, git (commit 17h), backups no Drive (4x/dia), secrets.env |
| **GitHub** | Repositório `BRACHAT-MAIN.git` — versiona código e cérebro (com exceção de segredos) |
| **OCI ezra_bot_1** | VM de produção com bots ativos: parashat, bot_ezra (opencode serve :3791), bridge Telegram |
| **OCI ezra_bot_2** | VM dedicada ao acquirer (busca A1.Flex 2 OCPU / 12GB no OCI) |

### Fluxo de sincronização

- **Mac ⇄ OCI (cérebro)**: `sync-cerebro.sh` (rsync bidirecional `--update`) espelha `~/.opencode` a cada **3 min** via LaunchAgent `com.ezra.sync-cerebro`. Inclui `mcp/credentials/secrets.env`; exclui `.git`, `node_modules`, `mcp/audit.log`.
- **Mac → GitHub**: `commit-diario.sh` (17h, LaunchAgent `com.ezra.commit`).
- **Mac → Drive**: `backup-diario.sh` (09/13/17/21h, LaunchAgent `com.ezra.backup`) — snapshots datados em `My Drive/brachat-main/_backups/YYYY-MM-DD/`.
- **Segredos**: vivem SOMENTE em `~/.opencode/mcp/credentials/secrets.env` (Mac, sincronizado p/ OCI). Nunca no git. Acesso exclusivo via MCP (`mcp_secrets_get`).

---

## Repositório: Estrutura Real

```
brachat-main/
├── portfolio/                # Agentes de produção + projetos
│   ├── ezra_bot/             # Cérebro do Ezra (.opencode) + deploy
│   │   ├── .opencode/        # skills, instructions, plugin (espelhado p/ OCI)
│   │   └── deploy/           # systemd units, bridge, warmup, anti-reclaim
│   ├── parashat_bot/         # Bot Telegram de estudo da Parashá (GROQ + NotebookLM)
│   ├── agent_nice/           # Dr. Nice — rotina doméstica (memória, compras, despensa)
│   ├── ezra_curator/         # Curadoria com Chroma/embedding
│   ├── essay-creator/        # Pipeline multi-agente de ensaios (LangGraph)
│   ├── exec-email-assistant/ # Assistente de email com memória semântica
│   ├── code-connect/         # Aplicação web + API (NestJS/React)
│   ├── langchain_hands_on/   # Estudos LangChain (RAG multi-agente)
│   └── langraph_hands_on/    # Estudos LangGraph (workflow com estado)
├── tests/                    # Testes de configuração/validação
├── opencode.json             # Config do opencode (MCP, permissões)
├── requirements.txt          # Deps raiz
├── pyproject.toml
├── pytest.ini / ruff.toml
└── .github/workflows/ci.yml  # CI/CD (lint + type check)
```

---

## Bots em Produção (OCI ezra_bot_1)

Serviços systemd ativos na VM `163.176.111.95`:

| Serviço | Descrição |
|---------|-----------|
| `parashat-bot` | Estudo diário da Parashá às 09:00 (America/Sao_Paulo) no grupo YESHIVA. GROQ via MCP. |
| `ezra-serve` | `opencode serve --port 3791` — cérebro Ezra 24/7 (protegido por senha). |
| `bridge_telegram` | Ponte Telegram → opencode serve (usuário conversa com o Ezra pelo Telegram). |
| `anti-reclaim` | Mantém a instância A1.Flex ativa (uso de CPU/memória). |

### Parashat Bot
- Escolhe a Parashá da semana (fonte: btf.org.br/parashot) e gera estudo com **GROQ** (`llama-3.3-70b-versatile`) + contexto do **NotebookLM** (caderno TORAH_STUDIES, citações `[1][2]`).
- **Chave GROQ via MCP**: `bot.py` usa `mcp_client.py` → `server.mjs` → `mcp_secrets_get("GROQ_API_KEY")` do `secrets.env` sincronizado. Sem chave embutida no ambiente.
- Comandos: `/parashat <nome ou data>` | sem argumento envia o da semana.

### bot_ezra (opencode serve + bridge)
- O Ezra roda no OCI e fala com o Fabio pelo Telegram via `bridge_telegram.js`.
- Cérebro em `/home/ubuntu/ezra_bot1/.opencode/` — espelho do Mac.
- Config do opencode no repo: `opencode.json` (MCP local `brachat-mcp` = `server.mjs`, permissões deny em `**/mcp/**`).

### Acquirer (OCI ezra_bot_2)
- `acquirer.service` busca instância **A1.Flex (2 OCPU / 12GB)** no OCI, tentando todos os ADs em loop (retry 180s).
- Ao adquirir, notifica via Telegram. Habilita a migração dos bots (tarefa 49).

---

## MCP (Model Context Protocol)

O servidor local `brachat-mcp` (`server.mjs`) fornece ao Ezra:

- `mcp_list` — navega dentro da boundary `mcp/`
- `mcp_read` / `mcp_write` — arquivos de memória/estado
- `mcp_secrets_list` / `mcp_secrets_get` — credenciais de `credentials/secrets.env` (auditadas em `audit.log`)

Regras: **nunca** ler/escrever credenciais fora do fluxo MCP; configs referenciam `${VAR}`, nunca valores.

---

## Governance

- **Zero-trust**: cérebro espelhado, `mcp/**` bloqueado para edição direta por ferramentas.
- **Segredos**: só em `secrets.env`; proibido no git (`.gitignore` cobre `**/secrets.env`, `**/.env`, `credentials/`).
- **Commits**: hook AGCP (pre-commit) valida antes de qualquer push.
- **Estado**: `state.json` é a fonte de verdade; mutações passam por validação + governance-ledger.

---

## Quick Start

```bash
git clone git@github.com:FABIOEVERTON/BRACHAT-MAIN.git
cd BRACHAT-MAIN

# Cérebro (skills/instruções) — necessário para o opencode
cp -r portfolio/ezra_bot/.opencode ~/.opencode

# Parashat bot
cd portfolio/parashat_bot
python3 -m venv venv && venv/bin/pip install -r requirements.txt
cp bot.env.example bot.env   # preencher (ou usar MCP/secrets.env)
sudo cp parashat-bot.service /etc/systemd/system/ && sudo systemctl enable --now parashat-bot

# Projetos de estudo
cd ../langraph_hands_on && pip install -e .
```

---

<p align="center">
  <em>Ecosystem governed locally via AI Agent Specification.</em><br/>
  <strong>Fabio Everton</strong> — <a href="mailto:jae.engenharia@gmail.com">jae.engenharia@gmail.com</a>
</p>
