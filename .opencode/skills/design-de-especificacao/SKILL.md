---
name: design-de-especificacao
id: S13
cluster: arquitetura
description: Define precisamente o estado final de uma tarefa antes da execução, transformando desejos vagos em restrições técnicas acionáveis.
---

### Objetivo
Definir precisamente o "estado final" de uma tarefa antes da execução, transformando desejos vagos em restrições técnicas acionáveis e limites de segurança.

### Entradas
- Descrição vaga da tarefa
- Sistema/alvos impactados
- Restrições conhecidas

### Saídas
- Especificação com: resultado esperado, arquivos afetados, invariantes, critério de aceite

### Dependências
- Nenhuma (skill fundamental)

### Token Budget
- 500-800 tokens por especificação

### Custos
- Baixo. Operação de design, sem execução externa.

### Segurança
- Não acessa dados externos. Sem riscos de privacidade.

### Testes
1. Especificação gerada elimina ambiguidades da entrada original?
2. Invariantes cobrem todos os riscos identificados?
3. Critério de aceite é mensurável?

---
