---
name: revisao-de-diffs
id: S29
cluster: avaliacao
description: Audita código produzido identificando abstrações desajeitadas, suposições silenciosas e inchaço, comparando contra a especificação original.
---

### Objetivo
Auditar código ou conteúdo produzido, identificando abstrações desajeitadas, suposições silenciosas ou "slop" (código inchado).

### Entradas
- Código ou conteúdo produzido (diff)
- Especificação original (SK-001)

### Saídas
- Auditoria com: escopo violado, exclusões suspeitas, suposições ocultas, sugestões de elegância

### Dependências
- SK-001 (precisa da spec para comparar)

### Token Budget
- 600-1000 tokens por revisão

### Custos
- Baixo. Leitura e análise, sem execução externa.

### Segurança
- Opera sobre código já produzido. Sem privilégios extras.

### Testes
1. Detectou alterações fora do escopo?
2. Identificou exclusões suspeitas?
3. Sugeriu simplificações sem mudar comportamento?

---
