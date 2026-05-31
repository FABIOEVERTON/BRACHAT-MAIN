# 🛠️ Brachat Construtor: Fábrica de Software Local (Mac)

> **Status da Esteira:** 🟢 Ativo & Resiliente  
> **Gerenciador de Serviços:** macOS `launchd` (LaunchAgents)  
> **Modelos de Raciocínio:** Hugging Face (Llama 3.3 70B) + Groq (Llama 3.1 8B) + ClickUp Fallback (Gemini/Claude)  

Este diretório contém a infraestrutura isolada do **Construtor de Software** local no Mac do Fábio. Ele orquestra o desenvolvimento de features do produto principal (`brachat-main`) sob regras físicas estritas de cibersegurança, DevSecOps e o modelo de governança **AGCP + QUILIS**.

---

## 📂 Árvore de Diretórios Operacional

```text
/Users/mac/brachat_builder/
├── README.md               <-- Este manual de produção do construtor
├── GOVERNANCE_WORKFLOW.md   <-- Manual das 8 fases, AGCP e QUILIS
├── clickup_daemon.py       <-- Daemon de 8 fases (Gemini + Claude + Groq)
├── bot_hermes.py           <-- Bot local do Telegram (Hugging Face + Groq)
├── active_project.json     <-- Estado de apontamento do projeto ativo
├── agentes/                <-- Especificações de cada agente do time (Spec-Kit)
│   ├── ezra.md
│   ├── hermes.md
│   ├── gilmario.md
│   ├── researcher.md
│   ├── architect.md
│   ├── coder.md
│   └── documenter.md
├── memories/               <-- Arquivos JSON de contextos locais dos agentes
├── logs/                   <-- Logs de stdout/stderr gerenciados pelo launchd
├── hooks/                  <-- Git Pre-Commit Hooks rígidos de injeção automática
├── lazy-gravity-suite/     <-- Ponte WebSocket + Bot Telegram de Controle Remoto
└── governance_repos/       <-- Repositórios de cibersegurança e conformidade clonados
    ├── awesome-ai-agent-governance
    └── Anthropic-Cybersecurity-Skills
```

---

## 🛡️ Governança de IA & Cibersegurança

### A. Divisão de Partições (AGCP)
* **Partição de Análise (Cognitiva):** A IA atua de forma sandboxed nas fases de pesquisa e especificação (`researcher.md` / `architect.md`), gerando propostas de modificações lógicas em texto.
* **Partição de Efeito (Física):** O `clickup_daemon.py` e o `bot_hermes.py` executam comandos locais, testes e controlam as travas físicas de escrita do macOS.

### B. Workspace Guard (Zero-Trust de Escrita)
Os arquivos de código do Mac permanecem bloqueados como **Somente Leitura (`chmod 444`)** por padrão. A escrita só é liberada dinamicamente para **`chmod 644`** após a aprovação manual do CEO Fábio no Telegram (Fase 3 ➔ Fase 4).

### C. Limite de Commit (Commit Limit)
O Git Pre-Commit Hook local valida se as alterações de código correspondem estritamente ao escopo aprovado no `implementation_plan.md` e aborta o commit na hora se houver modificações intrusas.

---

## 🔌 Resiliência contra Quedas e Suspensão

1. **Auto-Start macOS:** O Daemon, os Bots e a Ponte Lazy-Gravity estão integrados como **LaunchAgents do macOS**. Eles iniciam automaticamente com o boot do computador e se auto-recuperam em caso de crash.
2. **Anti-Repouso:** O Mac está configurado via Amphetamine para **nunca dormir** ao fechar a tampa ou ao bloquear a tela, mantendo a esteira de robôs online 24h/dia (conectado à tomada).

---

## 🚀 Como Operar a Fábrica de Software

Pelo chat do **Hermes** no Telegram:
1. **Selecionar Projeto:** `/switch <caminho_do_projeto_no_mac>` (Ex: `/switch /Users/mac/brachat-main`).
2. **Disparar Tarefa:** `/trabalhar <instrução de desenvolvimento>` (Ex: `/trabalhar criar rota de healthcheck`).
3. **Aprovar Planos:** Interagir com o card criado no ClickUp e enviar aprovação no chat.
