---
name: data-sensemaking
id: S11
cluster: avaliacao
description: Interpreta criticamente inputs e outputs de IA para derivar significado estratégico e detectar alucinações e viés.
---

### Objetivo
Interpretar criticamente inputs e outputs de IA para derivar significado estratégico e detectar alucinações.

### Entradas
- Dados brutos (outputs de IA, relatórios, métricas)
- Contexto do problema

### Saídas
- Análise de veracidade, contextualização, causalidade, detecção de viés

### Dependências
- Nenhuma

### Token Budget
- 500-1000 tokens por análise

### Custos
- Baixo. Operação interna de análise.

### Segurança
- Dados de entrada podem conter PII → classificar antes de processar.

### Testes
1. Detectou inconsistência factual?
2. Identificou viés no output?
3. Estabeleceu relação causal válida?

---
