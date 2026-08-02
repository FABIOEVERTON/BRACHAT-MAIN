---
name: analise-causa-raiz
id: S04
cluster: avaliacao
description: Diagnostica a origem real de falhas categorizando problemas em 6 eixos para evitar soluções paliativas.
---

### Objetivo
Diagnosticar a origem real de qualquer falha (técnica ou humana), categorizando problemas em 6 eixos para evitar soluções paliativas.

### Entradas
- Descrição do sintoma/erro
- Logs ou evidências disponíveis

### Saídas
- Síntoma isolado, categorização 6Ms, 5 Porquês concluídos, plano de blindagem

### Dependências
- Nenhuma

### Token Budget
- 500-900 tokens

### Custos
- Baixo. Análise interna.

### Segurança
- Logs podem conter dados operacionais sensíveis → mascarar antes.

### Testes
1. 5 Porquês chegam a causa raiz?
2. Plano de blindagem torna erro impossível de repetir?
3. Categorização 6Ms cobre todas as dimensões?

---
