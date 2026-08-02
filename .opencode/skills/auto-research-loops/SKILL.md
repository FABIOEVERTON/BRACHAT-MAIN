---
name: auto-research-loops
id: S09
cluster: avaliacao
description: Roda experimentos iterativos para otimizar processos e comportamento de agentes com métricas e convergência.
---

### Objetivo
Rodar experimentos iterativos para otimizar processos, prompts e comportamento de agentes, medindo métricas e convergindo para soluções ótimas.

### Entradas
- Hipótese (H0 atual vs H1 proposta)
- Métrica alvo e critério de melhoria
- Número máximo de iterações

### Saídas
- Resultado do experimento: variante vencedora, métricas, significância, recomendação

### Dependências
- SK-003 (Eval Design) para configurar métricas
- SK-012 (Causa Raiz) se resultados forem inconclusivos

### Token Budget
- 2000-5000 tokens por ciclo completo (hipótese → execução → análise)

### Custos
- Alto. Experimentos iterativos consomem muitos tokens.

### Segurança
- Dados de teste não devem conter PII.
- Early stop para evitar gastos excessivos.

### Testes
1. Métrica escolhida é relevante para o objetivo?
2. Significância estatística calculada?
3. Early stop funcionou quando convergiu?

---
