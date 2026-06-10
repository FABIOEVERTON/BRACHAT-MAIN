# GUIA DE ARQUITETURA DO ECOSSISTEMA BRACHÁT

Este guia descreve de ponta a ponta o funcionamento técnico do ecossistema pessoal do Fábio, integrando os bots de Telegram, a máquina local (Mac), o controle de tarefas (ClickUp), o controle de versão (Git) e o servidor de nuvem (Oracle Cloud).

---

## 1. FLUXO DE COMUNICAÇÃO GERAL

O ecossistema opera de forma integrada e distribuída entre a máquina local de desenvolvimento (Mac) e o servidor de produção na nuvem (Oracle Cloud).

```
  [ Fábio (Usuário) ]
     │      │
     │      └─── (Telegram Chat com @Baruch_Everton_bot) ──┐
     │      └─── (Telegram Chat com @luevertonbot) ──────┐│
     ▼                                                    ▼▼
[ Mac Local ]  ◄─────────[ Sync via GitHub ]─────────► [ Oracle Cloud ]
- OpenCode CLI                                         - IP: 147.15.18.252
- Git Hooks (Pre-commit)                               - Bots (Ezra & Nice)
- ClickUp Daemon (Sincronização)                       - Dashboard (Porta 8080)
- Obsidian DB                                          - Malha WS (Porta 8765)
```

---

## 2. OS BOTS DO TELEGRAM (NUVEM 24/7)

Os dois bots principais do ecossistema rodam 24/7 como serviços gerenciados pelo `systemd` no servidor da Oracle Cloud. Eles realizam chamadas HTTP via `getUpdates` para a API do Telegram e utilizam o **OpenCode Zen (big-pickle)** como motor de inteligência, com fallback local para o **Ollama (llama3.2:1b)**.

### 2.1. Bot Ezra (@Baruch_Everton_bot)
*   **Papel**: Orquestrador central e interface direta de estudos/rotinas com o Fábio.
*   **Ações**:
    *   Lê e exibe o cronograma diário com base no `writings_studies/OFICIAL_SCHEDULE.md`.
    *   Monitora as janelas de estudo e despacha tarefas para os 20 agentes especialistas.
    *   **Não altera arquivos de código locais**: O Ezra atua estritamente na camada de coordenação, diálogos e registros de status. Ele pode inserir marcações especiais como `[CREATE_TASK: Nome]` em suas respostas, as quais são interpretadas para criar tarefas no ClickUp.
*   **Serviço**: `brachat-ezra.service` (executa `/opt/brachat/bridge-ezra.py` sob o usuário `opc`).

### 2.2. Bot Nice (@luevertonbot)
*   **Papel**: Governança doméstica e finanças.
*   **Ações**:
    *   Interage com o chat da Dona Lu e do Fábio.
    *   **Modifica arquivos físicos no repositório**: Quando comandada a adicionar/remover itens ou atualizar finanças, ela edita diretamente os arquivos JSON correspondentes:
        *   `integrations/nice/shopping_list.json`
        *   `integrations/nice/pantry.json`
        *   `integrations/nice/finance.json`
    *   **Commit & Push Automático**: Logo após alterar os arquivos locais na VM, o script executa um ciclo de `git pull` -> `git add` -> `git commit` -> `git push` para sincronizar os dados atualizados com o repositório do GitHub.
*   **Serviço**: `brachat-nice.service` (executa `/opt/brachat/bridge-nice.py` sob o usuário `opc`).
*   *Nota de Correção*: O erro persistente de escrita (`Permission denied: /tmp/nice-state.json`) que ocorria no antigo VPS da Hetzner foi totalmente resolvido ao configurar o serviço na Oracle para rodar sob o usuário comum `opc` (dono de `/opt/brachat`), em vez do usuário restrito `nobody`.

---

## 3. O MÁQUINA LOCAL (MACBOOK)

O Mac é o cérebro de engenharia onde o código do ecossistema é refinado e executado em modo de desenvolvimento.
*   **OpenCode CLI**: Utilizado para gerenciar sessões interativas dos agentes com o comando `opcode run --continue`.
*   **Daemons locais**: Executam agentes e rotinas periódicas por meio de arquivos `.plist` configurados no `launchd` do macOS.
*   **Obsidian DB**: Banco de dados de notas e documentações integrado para o acúmulo de conhecimento de longo prazo.

---

## 4. INTEGRAÇÃO GIT + CLICKUP (`git_clickup` & GOVERNANÇA)

A governança do ecossistema aplica o conceito de **Commit Limit** local no Mac por meio de um Git Hook do tipo `pre-commit`.

### 4.1. Fluxo de Commit Limit & Rastreabilidade
1.  **Plano de Implementação**: Nenhuma alteração entra no repositório sem um arquivo `implementation_plan.md` aprovado pelo usuário.
2.  **Git Hook de Pre-Commit**:
    *   Intercepta o commit e analisa a lista de arquivos modificados (`git diff --cached`).
    *   Valida a regra de **MVI (Minimum Viable Information)**: nenhum arquivo de código ou documentação alterado pode ter mais de 200 linhas (e prompts de `AGENT.md` são limitados a 60 linhas).
    *   Garante que nenhum segredo crítico (como tokens ou chaves privadas) seja incluído de forma hardcoded nos arquivos.
    *   Verifica se o padrão Harness (presença de "🧠 Núcleo Central" e "⚙️ Operational Procedure") é mantido em arquivos `AGENT.md` novos ou modificados.
    *   Registra a transação como `AUTHORIZED` ou `REJECTED` no ledger de auditoria append-only (`.opencode/governance-ledger.jsonl`).
3.  **ClickUp Gatekeeper**:
    *   O commit é validado e associado a uma tarefa ativa com status `Development` no painel do ClickUp.
    *   A sincronização bidirecional das tarefas é realizada pelo daemon de tarefas (`clickup_daemon.py`), que busca e atualiza periodicamente as tasks e salva seu cache em `integrations/clickup/cache/clickup.json`.

---

## 5. NOVA INFRAESTRUTURA ORACLE CLOUD (ALWAYS FREE)

Toda a infraestrutura do ecossistema em nuvem foi migrada para a Oracle Cloud, garantindo estabilidade e custo zero permanente.

*   **IP da VM**: `147.15.18.252`
*   **Sistema Operacional**: Oracle Linux 9
*   **Instância**: `VM.Standard.E2.1.Micro` (AMD, 1 vCPU, 1 GB RAM física, 50 GB de disco SSD).
*   **Mecanismo de Estabilização de Memória (Swap)**:
    *   Para mitigar as limitações de 1 GB de RAM física da máquina Always Free e evitar falhas por Out-Of-Memory (OOM) ao rodar o Ollama ou instalações pesadas, configurou-se **4 GB de Swap permanente** alocado diretamente em disco no arquivo `/swapfile` (gerando um total de 5 GB de memória virtual ativa).
*   **Segurança de Rede (Firewall)**:
    *   As portas públicas foram liberadas no `firewalld` interno da VM para comunicação com o exterior:
        *   **Porta 8080**: Servidor HTTP que serve o Dashboard Organograma do Brachát (`http://147.15.18.252:8080`).
        *   **Porta 8765**: WebSocket de transmissão em tempo real de métricas e status dos agentes especialistas (`ws://147.15.18.252:8765`).
*   **Status da Hetzner**: A antiga máquina no IP `167.233.30.115` foi completamente desativada. Os serviços foram finalizados e a VM foi desligada via comando `poweroff`. A exclusão física da conta de faturamento da Hetzner deve ser concluída manualmente pelo Fábio devido a requisitos de autenticação de segurança do console web.
