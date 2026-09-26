# WIZE CLEAN CODE POLICY — Manual Canônico de Qualidade de Código

Esta política formaliza as 30 categorias de excelência de engenharia de software para o **Wize Developer Kit**, transformando os princípios clássicos de Clean Code (Robert C. Martin e literatura consolidada) em regras operacionais, verificáveis e seguras.

---

## 1. Nomenclatura

### [WCC-01] Intenção Revelada no Identificador
* **Classificação:** HIGH
* **Princípio:** O nome de uma variável, função ou classe deve responder por que ela existe, o que ela faz e como é usada, dispensando comentários explicativos.
* **Regra obrigatória:** Todo identificador deve ser inequívoco no seu contexto. Evite abreviações obscuras ou nomes de uma única letra fora de contadores matemáticos padrão (`i`, `j`).
* **Quando aplicar:** Na criação ou modificação de qualquer símbolo no código.
* **Como verificar:** Inspeção no diff e linter semântico.
* **Ação exigida:** Renomear imediatamente para refletir a intenção semântica.
* **Exceções permitidas:** Índices em loops curtos (`for i in range(len(items))`) ou tuplas de coordenadas (`x, y`).
* **Proibições:** Uso de nomes como `data`, `res`, `val`, `temp`, `manager`, `helper`, `proc`.
* **Exemplo mínimo:**
  - *Incorreto:* `def get_d(t): return t.amt * 0.15`
  - *Correto:* `def calculate_annual_discount(contract: Contract) -> Decimal: return contract.amount * ANNUAL_DISCOUNT_RATE`
* **Checklist:** O nome explica o propósito do dado sem precisar ler a implementação interna?
* **Rastreabilidade:** `ciembor/agent-rules-books — Meaningful Names` | `ryanmcdermott/clean-code-javascript`

---

## 2. Funções

### [WCC-02] Responsabilidade e Tamanho de Funções
* **Classificação:** HIGH
* **Princípio:** Funções devem fazer uma única coisa (Single Responsibility) e possuir um nível consistente de abstração.
* **Regra obrigatória:** Limite funções a executar uma única tarefa lógica. Separe estritamente validação de regras de negócio, persistência de banco e I/O de rede.
* **Quando aplicar:** Criação de novos métodos ou refatoração de rotinas existentes.
* **Como verificar:** Revisão estática de complexidade ciclomática e linhas de código (>30 linhas é alerta para análise).
* **Ação exigida:** Extrair sub-rotinas com nomes expressivos que representem passos da computação.
* **Exceções permitidas:** Funções orquestradoras declarativas com chamadas sequenciais legíveis.
* **Proibições:** Funções com parâmetros de flag booleana que bifurcam todo o fluxo interno (`render(is_admin=True)`).
* **Exemplo mínimo:**
  - *Incorreto:* `def process_user(data): ... valida email, calcula taxa, faz hash da senha, salva no banco e manda email ...`
  - *Correto:* Separar em `validate_registration()`, `hash_password()`, `persist_user()` e `dispatch_welcome_notification()`.
* **Checklist:** Consigo descrever o que a função faz sem usar a palavra "E"?
* **Rastreabilidade:** `nghorbani/clean-code-skill — Functions` | `ciembor/agent-rules-books`

---

## 3. Responsabilidade Única (SRP)

### [WCC-03] Coesão de Módulos e Classes
* **Classificação:** CRITICAL
* **Princípio:** Uma classe ou módulo deve ter uma única razão para mudar.
* **Regra obrigatória:** Módulos de infraestrutura (banco, HTTP, fila) não devem conter lógica de negócio de domínio; entidades de domínio não devem conter detalhes de renderização ou SQL.
* **Quando aplicar:** Arquitetura de novos pacotes e serviços.
* **Como verificar:** Mapeamento de imports e dependências circulares.
* **Ação exigida:** Isolar responsabilidades em camadas distintas (Domain, Service, Repository, Controller).
* **Exceções permitidas:** Scripts utilitários monolíticos CLI descartáveis de um único arquivo.
* **Proibições:** Modelos ActiveRecord contendo lógica pesada de validação de cartões e envio de emails.
* **Exemplo mínimo:** Separar o modelo de dados `Tenant` do serviço de criptografia `ForensicLedgerService`.
* **Checklist:** Se a regra de impostos mudar, apenas uma classe/módulo precisa ser editada?
* **Rastreabilidade:** `ciembor/agent-rules-books — Single Responsibility Principle`

---

## 4. Complexidade e Acoplamento

### [WCC-04] Minimização de Complexidade Ciclomática e Acoplamento
* **Classificação:** HIGH
* **Princípio:** Menos ramificações aninhadas facilitam raciocínio, testes e manutenção.
* **Regra obrigatória:** Limite o aninhamento a no máximo 2 níveis (`if` dentro de `for`). Utilize cláusulas de guarda (*early returns*) para tratar casos extremos e erros antes do fluxo principal.
* **Quando aplicar:** Escrita de blocos condicionais e loops.
* **Como verificar:** Métricas de complexidade estática (flake8 / radon / eslint complexity <= 6).
* **Ação exigida:** Refatorar utilizando cláusulas de guarda ou polimorfismo/estratégias.
* **Exceções permitidas:** Interpretadores de AST ou parsers léxicos especializados.
* **Proibições:** Escadas de `if/else if/else if` com 5+ níveis e blocos `try/catch` aninhados profundamente.
* **Exemplo mínimo:**
  - *Incorreto:*
    ```python
    if user:
        if user.is_active:
            if not user.is_suspended:
                return user.data
    ```
  - *Correto:*
    ```python
    if not user or not user.is_active or user.is_suspended:
        raise UnauthorizedTenantError()
    return user.data
    ```
* **Checklist:** O código flui linearmente de cima para baixo sem indentações profundas?
* **Rastreabilidade:** `ryanmcdermott/clean-code-javascript — Conditionals`

---

## 5. Tratamento de Erros e Exceções

### [WCC-05] Exceções Explícitas com Contexto Semântico
* **Classificação:** BLOCKER
* **Princípio:** Erros são fatos operacionais esperados e devem ser tratados com máxima clareza e rastreabilidade.
* **Regra obrigatória:** Crie exceções customizadas de domínio (`TenantSuspendedError`, `InvalidHashChainError`). Nunca capture exceções genéricas sem relançar ou registrar o contexto exato.
* **Quando aplicar:** Qualquer operação de I/O, banco, rede, parsing ou validação.
* **Como verificar:** Linter para capturas cegas (`bare except:`, `catch (e) {}` vazio).
* **Ação exigida:** Tratar a exceção específica e fornecer mensagem diagnóstica contextualizada.
* **Exceções permitidas:** Handlers globais de último nível em API Gateways que convertem erros não tratados em HTTP 500 sem vazar dados.
* **Proibições:** Retorno de código de erro numérico ou booleanos que escondem o motivo do fracasso.
* **Exemplo mínimo:**
  - *Incorreto:* `try: db.save() except: return False`
  - *Correto:* `try: db.save() except DatabaseConnectionError as err: logger.error("Falha ao salvar ledger", extra={"tenant_id": t_id}); raise LedgerPersistenceError(f"Erro ao persistir evento no tenant {t_id}") from err`
* **Checklist:** O log e a exceção dizem exatamente quem, onde e por que falhou?
* **Rastreabilidade:** `ciembor/agent-rules-books — Error Handling`

---

## 6. Segurança & Privacidade de Dados

### [WCC-06] Blindagem contra Injeção e Vazamento de Segredos / PII
* **Classificação:** BLOCKER
* **Princípio:** A segurança e privacidade (LGPD/NIST) têm precedência sobre qualquer conveniência.
* **Regra obrigatória:**
  1. Uso exclusivo de consultas SQL parametrizadas / ORM tipado.
  2. Proibição absoluta de segredos (senhas, tokens, JWT secrets) em arquivos do repositório (uso de variáveis de ambiente com validação Pydantic).
  3. Mascaramento obrigatório de dados pessoais (PII) em qualquer log ou saída de erro.
* **Quando aplicar:** Toda manipulação de credenciais, queries, logs e APIs.
* **Como verificar:** Varredura estática de segredos (gitleaks) e SAST (bandit / eslint-plugin-security).
* **Ação exigida:** Bloquear imediatamente o commit e isolar o segredo em `.env`.
* **Exceções permitidas:** Nenhuma para segredos em produção.
* **Proibições:** `eval()`, interpolação de strings em SQL (`f"SELECT * FROM users WHERE id = {user_input}"`), logar senhas em texto puro.
* **Checklist:** Existe algum dado confidencial, chave de API ou query insegura neste código?
* **Rastreabilidade:** `Wize Security Standards` | `OWASP Top 10`

---

## 7. Testabilidade e TDD

### [WCC-07] Cobertura Efetiva e Isolamento de Testes
* **Classificação:** CRITICAL
* **Princípio:** Código sem testes automatizados é código legado desde o primeiro minuto.
* **Regra obrigatória:** Toda nova função de domínio ou rota de API deve possuir testes unitários e de integração correspondentes cobrindo o caminho feliz e cenários de falha.
* **Quando aplicar:** Ciclo de desenvolvimento em TDD (Test-Driven Development).
* **Como verificar:** Execução de `pytest` / `vitest` com relatório de cobertura e assertividade de ACs.
* **Ação exigida:** Escrever os testes antes de dar a tarefa por encerrada.
* **Exceções permitidas:** Interfaces puramente declarativas sem lógica interna (apenas HTML estático).
* **Proibições:** Testes com asserts vazios (`assert True`), testes que dependem de ordem de execução ou de conexão com internet real em testes unitários.
* **Checklist:** Se eu alterar a regra interna do método, o teste quebra acusando a divergência?
* **Rastreabilidade:** `nghorbani/clean-code-skill — Testing`

---

## 8. Manutenção de Código Legado e Boy Scout Rule

### [WCC-08] Regra do Escoteiro Aplicada ao Escopo
* **Classificação:** MEDIUM
* **Princípio:** Deixe o código mais limpo do que quando você o encontrou, respeitando estritamente o escopo da tarefa.
* **Regra obrigatória:** Ao tocar em um arquivo para uma alteração planejada, corrija pequenos nomes confusos ou adicione tipos estritos naquele trecho específico.
* **Quando aplicar:** Edição em código existente.
* **Como verificar:** Diff focado e testes passando.
* **Ação exigida:** Melhorar a clareza local sem realizar refatorações em massa fora do escopo.
* **Exceções permitidas:** Módulos legados congelados prestes a serem descontinuados.
* **Proibições:** Reescrever módulos inteiros que não faziam parte da demanda solicitada.
* **Checklist:** A alteração melhorou o trecho sem expandir o risco do PR?
* **Rastreabilidade:** `ciembor/agent-rules-books — Boy Scout Rule`
