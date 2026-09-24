# WIZE RULES INDEX — Índice de Regras Operacionais

| ID | Nome da Regra | Categoria | Severidade | Gatilho | Automatizável | Ferramenta de Verificação | Arquivo de Origem |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WCC-01** | Intenção Revelada no Identificador | Nomenclatura | HIGH | Declaração de variáveis/funções | Sim | Linter / AST | `WIZE_CLEAN_CODE_POLICY.md` |
| **WCC-02** | Responsabilidade e Tamanho de Funções | Funções | HIGH | Criação/edição de métodos | Sim | Radon / ESLint Complexity | `WIZE_CLEAN_CODE_POLICY.md` |
| **WCC-03** | Coesão de Módulos e Classes (SRP) | Arquitetura | CRITICAL | Criação de serviços/classes | Parcial | Análise Estática / Review | `WIZE_CLEAN_CODE_POLICY.md` |
| **WCC-04** | Minimização de Complexidade e Acoplamento | Condicionais | HIGH | Blocos if/else e loops | Sim | Flake8 / Radon | `WIZE_CLEAN_CODE_POLICY.md` |
| **WCC-05** | Exceções Explícitas com Contexto | Tratamento de Erros | BLOCKER | Blocos try/except/catch | Sim | PyLint / ESLint | `WIZE_CLEAN_CODE_POLICY.md` |
| **WCC-06** | Blindagem contra Injeção e Vazamento | Segurança | BLOCKER | Toda query, segredo ou log | Sim | Gitleaks / Bandit / SAST | `WIZE_CLEAN_CODE_POLICY.md` |
| **WCC-07** | Cobertura Efetiva e Isolamento de Testes | Testes & TDD | CRITICAL | Toda nova regra de negócio | Sim | Pytest / Vitest | `WIZE_CLEAN_CODE_POLICY.md` |
| **WCC-08** | Regra do Escoteiro no Escopo | Manutenção | MEDIUM | Edição em código legado | Não | Code Review Manual | `WIZE_CLEAN_CODE_POLICY.md` |
