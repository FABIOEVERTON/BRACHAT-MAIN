---
name: auditor
id: S08
cluster: avaliacao
description: Auto-inspeção completa do sistema: responde quem é, como pensa, que arquivos existem e quanto custou cada decisão.
---

### Objetivo
Auto-inspecção completa do Ezra: responder quem é, como pensa, que arquivos existem, quem carregou o quê, quanto custou, qual skill foi escolhida e por quê.

### Entradas
- Pergunta de auditoria (ex: "Quem sou?", "Quanto custou a última execução?", "Por que escolheu SK-014?")
- Acesso ao state.json, governance-ledger (.opencode/governance-ledger.jsonl), logs de observabilidade

### Saídas
- Resposta auditável com: fato, fonte, timestamp, custo associado
- Chain of thought da decisão original quando relevante

### Dependências
- SK-026 (Observability) para acessar logs e tracing
- Governance.md (classificação de dados para resposta)
- state.json e .opencode/governance-ledger.jsonl

### Token Budget
- 300-800 tokens por consulta de auditoria

### Custos
- Baixo. Consulta a registros existentes.

### Segurança
- Auditor pode expor decisões internas → limitar resposta ao estritamente perguntado.
- Não revelar secrets, tokens ou PII mesmo em auditoria interna.
- Toda consulta de auditoria é também registrada (meta-auditoria).

### Testes
1. Resposta cita fonte específica (arquivo, linha, timestamp)?
2. Custo reportado confere com o registrado no ledger?
3. Chain of thought da decisão original é recuperável?

---
