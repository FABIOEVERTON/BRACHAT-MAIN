---
name: skill-creator
id: S30
cluster: memoria
description: Cria skills reutilizáveis no formato SKILL.md a partir de padrões identificados — template, registro e versionamento.
---

### Objetivo
Transformar padrões recorrentes, workflows não-triviais ou recuperações de erro em skills reutilizáveis, seguindo o Hermes loop (Evaluate → Extract → Refine).

### Gatilhos
Criar skill quando:
- Mesmo padrão de tarefa repetir 3+ vezes
- Workflow envolveu 5+ tool calls ou recuperação de erro
- Usuário corrigiu algo manualmente que deve ser automatizado
- Abordagem bem-sucedida é não-obvia (não está em skill existente)

### Template Obrigatório
```
---
name: <kebab-case-id>
description: <uma linha em português>
---

### Objetivo
<o que faz, em 1-2 frases>

### Entradas
- <o que precisa receber>

### Saídas
- <o que produz>

### Dependências
- <skills ou arquivos necessários>

### Token Budget
- <estimativa de tokens>

### Custos
- <Baixo/Médio/Alto>

### Segurança
- <riscos e controles>

### Testes
1. <teste 1>
2. <teste 2>
3. <teste 3>

---
```

### Registro
1. Salvar em `.opencode/skills/<nome>/SKILL.md`
2. Adicionar ao catálogo em `state.json → context.available_skills`
3. Se substitui skill existente → remover a antiga do catálogo
4. Registrar em mem0 como `[melhoria] skill: <nome>`

### Refinamento
- Se abordagem melhor for descoberta depois → editar skill existente, não criar nova
- Se skill ficar obsoleta → remover do catálogo e arquivar (não deletar)
- Se skill crescer demais (>80 linhas) → dividir em duas menores

### Token Budget
- 300-600 tokens para criar template
- Custo único (skill é reutilizada depois)

### Custos
- Baixo. Skill é criada uma vez, reusada infinitas vezes.

### Segurança
- Skills são markdown legível — sem execução de código.
- Segue Least Privilege: skill só tem o contexto necessário.

### Testes
1. Skill criada segue o template obrigatório?
2. Skill está registrada no catálogo?
3. Skill substitui/refina alguma existente sem duplicar?
