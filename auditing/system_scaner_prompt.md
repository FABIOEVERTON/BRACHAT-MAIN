# BRACHÁT — Prompts de Auditoria

---

## PROMPT 1 — DESCOBERTA (rodar uma vez)

> Colar no Antigravity após clonar o repo.

```
MISSÃO: Auditoria de descoberta do sistema BRACHÁT.

Clona o repositório e lê TODOS os ficheiros na seguinte ordem:
1. Regras e configs do OpenCode (.opencode/rules/)
2. Definições de agentes (operational_agents/)
3. Memória e contexto (qualquer referência a Mem0, mem0, JSON de sessão)
4. Estrutura de portfolio e branding (portfolio/, branding_agents/)
5. Estudos e escritos (writings_studies/)
6. README e qualquer documentação de intenção arquitectural

Após leitura completa, produz um relatório com as seguintes secções:

### 1. MAPA DO SISTEMA
- Lista todos os agentes identificados com papel declarado
- Lista todas as regras activas com escopo de aplicação
- Diagrama textual do fluxo de orquestração (BigPickle → agentes)

### 2. INTEGRIDADE
- Ficheiros quebrados, referências mortas, imports inválidos
- Regras que se contradizem entre si
- Agentes definidos mas não referenciados, ou referenciados mas não definidos

### 3. CONSISTÊNCIA
- Divergências entre o que a documentação declara e o que o código/regras implementam
- Inconsistências de nomenclatura entre ficheiros
- Gaps de cobertura: funções do sistema sem agente ou regra responsável

### 4. ECONOMIA DE TOKENS
- Regras duplicadas ou redundantes (conteúdo equivalente em ficheiros diferentes)
- Prompts ou instruções verbosas que podem ser comprimidos sem perda semântica
- Contexto de memória carregado desnecessariamente (fora da disciplina read-most-recent)

### 5. EFICIÊNCIA E LATÊNCIA
- Dependências desnecessárias entre agentes (acoplamento excessivo)
- Fluxos com mais de um salto onde um seria suficiente
- Ausência de paralelismo onde seria aplicável

### 6. ACHADOS CRÍTICOS
- Lista priorizada por severidade: CRÍTICO / ALTO / MÉDIO / BAIXO
- Para cada achado: localização exacta no repo, descrição, impacto, acção recomendada

### 7. RECOMENDAÇÕES DE REORGANIZAÇÃO
- Proposta de estrutura de pastas optimizada (se aplicável)
- Ordem sugerida de resolução dos achados

Salva o relatório em: auditoria/descoberta-YYYY-MM-DD.md
Cria a pasta auditoria/ na raiz do repo se não existir.
Não modifica nenhum ficheiro existente. Apenas lê e reporta.
```

---

## PROMPT 2 — AUDITORIA DIÁRIA (rodar todos os dias)

> Colar no Antigravity no início de cada sessão de trabalho.

```
MISSÃO: Auditoria diária do sistema BRACHÁT.

Lê o estado actual do repositório. Lê também a auditoria mais recente em auditoria/ para comparação de delta.

Verifica os seguintes critérios em ordem:

### CHECK 1 — INTEGRIDADE
[ ] Nenhuma referência morta (ficheiro mencionado mas inexistente)
[ ] Nenhuma regra com conflito directo com outra regra
[ ] Todos os agentes declarados têm definição completa (nome, papel, modelo, ferramentas)
[ ] BigPickle tem rota definida para cada agente activo

### CHECK 2 — CONSISTÊNCIA
[ ] Nomenclatura uniforme entre todos os ficheiros (agentes, pastas, variáveis)
[ ] Documentação alinhada com implementação actual
[ ] Estrutura de pastas corresponde à arquitectura declarada
[ ] Mem0 e ficheiros JSON locais (~/mem0/) seguem a disciplina: apenas o ficheiro mais recente é lido no início de sessão

### CHECK 3 — ECONOMIA DE TOKENS
[ ] Nenhuma regra duplicada ou com conteúdo equivalente a outra
[ ] Nenhum prompt com verbosidade eliminável (instruções repetidas, contexto redundante)
[ ] Ficheiros de memória consolidados (máximo dois ficheiros em ~/mem0/)
[ ] Nenhum agente carrega contexto que não usa na sua função declarada

### CHECK 4 — EFICIÊNCIA E LATÊNCIA
[ ] Nenhum fluxo com saltos de agente desnecessários
[ ] Hermes não é invocado para tarefas que BigPickle pode resolver directamente
[ ] Ausência de loops ou dependências circulares entre agentes
[ ] Paralelismo aplicado onde agentes são independentes entre si

### OUTPUT DO RELATÓRIO
Para cada check: PASS / FAIL / AVISO
Para cada FAIL ou AVISO: localização exacta, descrição do problema, severidade (CRÍTICO / ALTO / MÉDIO / BAIXO)

Secção final obrigatória:
DELTA vs auditoria anterior — o que melhorou, o que regrediu, o que é novo

Salva o relatório em: auditoria/YYYY-MM-DD.md
Não modifica nenhum ficheiro existente. Apenas lê e reporta.
```

---

## NOTAS DE USO

- **Ordem**: rodar Prompt 1 primeiro. Depois usar Prompt 2 diariamente.
- **~/mem0/**: os prompts não tocam nesta pasta — ela vive fora do repo intencionalmente.
- **Modificações**: nenhum dos prompts altera ficheiros existentes. São read-only por design.
- **Delta diário**: o Prompt 2 compara sempre com a auditoria anterior — permite rastrear regressões.
