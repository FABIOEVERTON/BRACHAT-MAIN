---
name: prompt-optimizer
id: S28
cluster: avaliacao
description: Refina prompts usando eval loops com variantes testadas e métricas comparativas para convergir à versão de maior performance.
---

### Objetivo
Refinar prompts systematicamente usando eval loops, testando variantes e convergindo para a versão de maior performance.

### Entradas
- Prompt atual com baixa performance
- Test cases para validação
- Métricas de avaliação (accuracy, relevance, conciseness, safety)

### Saídas
- Diagnóstico, variantes testadas, métricas comparativas, prompt vencedor, registro de evolução

### Dependências
- SK-003 (Eval Design)
- SK-012 (Causa Raiz) para diagnóstico

### Token Budget
- 1500-4000 tokens por ciclo de otimização

### Custos
- Alto. Múltiplas variantes consumindo tokens cada uma.

### Segurança
- Prompts podem expor lógica interna → classificar como Confidential.
- Test cases não devem conter PII.

### Testes
1. Variante vencedora tem melhoria > 5%?
2. Baixa variância entre execuções da vencedora?
3. Evolução registrada para auditoria?

---
