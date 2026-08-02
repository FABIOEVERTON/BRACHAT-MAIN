---
name: design-de-loops-de-avaliacao
id: S14
cluster: avaliacao
description: Cria infraestrutura para medir eficácia de sistemas não determinísticos através de avaliações quantitativas (custo, tokens, latência, precisão).
---

### Objetivo
Criar infraestrutura para medir eficácia de sistemas não determinísticos e executar avaliações quantitativas (custo, tokens, latência, precisão, alucinação, pass rate), movendo de impressões subjetivas para evidências mensuráveis.

### Entradas
- Descrição do sistema a ser avaliado
- Critérios de qualidade, métricas alvo e thresholds
- Dados de exemplo (golden set)

### Saídas
- Rubricas de avaliação, golden set, LLM-as-Judge config, plano de monitoramento de drift
- Relatório de avaliação: custo total, tokens gastos, latência, retrabalho, ROI, precisão, taxa de alucinação, pass rate

### Dependências
- Nenhuma

### Token Budget
- 1000-2000 tokens por ciclo completo (design + execução)

### Custos
- Médio. Pode exigir execução de avaliações múltiplas.

### Segurança
- Golden sets podem conter dados sensíveis → anonimizar antes.
- Relatórios podem conter dados de execução → classificar conforme Governance.

### Testes
1. Rubricas são mensuráveis e não ambíguas?
2. LLM-as-Judge tem acurácia > 85% vs ground truth?
3. Métricas calculadas refletem a execução real?
4. Pass rate distingue falha de erro tolerável?

---
