# Manual de Governança do Construtor: QUILIS, AGCP e Controle Local (Mac)

Este documento define a implementação prática dos conceitos do **AI Governance Control Plane (AGCP)**, o **Limite de Commit (Commit Limit)** e a explicabilidade do **QUILIS** dentro do fluxo de desenvolvimento local do Mac.

---

## 🧠 1. AGCP: Separação de Partições no Construtor

Impomos a divisão física e lógica entre raciocínio probabilístico de IA e ações reais de escrita no Mac:

### A. Partição de Análise (Análise Sandboxed)
*   **Quem:** A IA (Gemini/Claude) nas fases de `Researcher`, `Specification` e `Development`.
*   **Regra de Segurança:** A IA opera em um sandbox cognitivo. Ela **não pode** realizar commits diretamente, executar comandos arbitrários no terminal ou efetuar deploys. Ela apenas gera propostas de alteração de código ou especificações técnicas em formato de texto.

### B. Partição de Efeito (Execução Determinística)
*   **Quem:** O ClickUp Daemon (`clickup_daemon.py`) e o Git Pre-Commit Hook local.
*   **Regra de Segurança:** Operam sob regras determinísticas em Python/Bash. São os únicos autorizados a modificar arquivos físicos no macOS, realizar commits de fato e subir alterações para a nuvem.

---

## 🚪 2. O Limite de Commit (Commit Limit) Local

O **Limite de Commit** é o portão de controle onde o código gerado na Partição de Análise se torna imutável no histórico Git. Aplicamos os 3 Invariantes Determinísticos locais:

### I. Invariante de Rastreabilidade (QUILIS / Decision Ledger)
*   Nenhum código entra em produção sem o arquivo [@implementation_plan.md](file:///Users/mac/brachat_builder/GOVERNANCE_WORKFLOW.md) de especificação associado.
*   O pre-commit hook valida se as alterações de arquivos no diff do Git condizem estritamente com os caminhos declarados e aprovados no plano técnico.

### II. Invariante de Co-assinatura Humana (HITL)
*   **Assinatura do CEO:** O desenvolvimento físico de código e o commit permanecem fisicamente bloqueados até que o Fábio assine digitalmente ou envie o comando "Aprovado" no Telegram.
*   O daemon só roda o `chmod 644` (destravamento de escrita de arquivos) após registrar o `"plan_approved": true` no estado local `.brachat-state.json`.

### III. Invariante de Proveniência e Identidade
*   O Git Hook e o Hermes validam se o commit provém de um terminal autorizado e se a tarefa de desenvolvimento correspondente está com status `Development` ativo no ClickUp.

---

## 🚫 3. Limites de Domínio e Compliance (Regras Invariantes do NotebookLM)

Seguindo as diretrizes de conformidade herdadas do caderno de estudos do usuário:

1.  **Auditoria por Aísio (Runtime Monitor):**
    *   Toda saída gerada pelos agentes locais é submetida a um scanner de segurança no `clickup_daemon.py` antes da gravação física. Se contiver termos anômalos ou injeções de prompt que tentem acessar credenciais globais `/Users/mac/apis/apis.env`, a ação é barrada por violação de domínio.
2.  **Isolamento de Projetos Paralelos:**
    *   O comando `/switch` cria sandboxes lógicos. Agentes ativos em um projeto paralelo (`/Users/mac/projeto_paralelo/`) são fisicamente impedidos de ler ou escrever nos diretórios de outros projetos como o `brachat-main` corporativo.
3.  **Kill Switch & Rollback:**
    *   Em caso de falha crítica nos testes locais (`Testing`) ou violação técnica, o daemon imediatamente reverte a árvore de diretórios local para a última versão limpa (Git Rollback), bloqueia as permissões para `chmod 444` e notifica o Fábio no Telegram de forma imediata.
