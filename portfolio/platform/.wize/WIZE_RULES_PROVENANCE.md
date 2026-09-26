# WIZE RULES PROVENANCE — Registro de Proveniência e Fontes

Este documento registra a rastreabilidade conceitual, fontes abertas consultadas, versões e transformações autorais aplicadas na criação da política oficial de qualidade de código do **Wize Developer Kit**.

---

## 1. Fontes Conceituais Consultadas

### Fonte 1: `ciembor/agent-rules-books`
* **URL:** `https://github.com/ciembor/agent-rules-books`
* **Licença:** MIT License
* **Arquivos Consultados:** `clean-code/clean-code.md`, `clean-code/clean-code.mini.md`, `_rule-workbench/clean-code/traceability.md`, `docs/USAGE.md`.
* **Conceitos Aproveitados:** Estrutura de regras para agentes de IA, princípios de legibilidade local, funções coesas, minimização de efeitos colaterais e disciplina de escopo.
* **Transformação Realizada:** Redação autoral e operacionalização em regras com severidade (BLOCKER a ADVISORY), adaptadas para o ecossistema multi-agente do Wize.

### Fonte 2: `nghorbani/clean-code-skill`
* **URL:** `https://github.com/nghorbani/clean-code-skill`
* **Licença:** MIT License
* **Arquivos Consultados:** `SKILL.md`, `cheatsheet.md`, `glossary.md`, `patterns.md`.
* **Conceitos Aproveitados:** Heurísticas de design de funções, patterns de refatoração segura, isolamento de testes e tratamento de exceções.
* **Transformação Realizada:** Estruturação em formato de manual de compliance técnico com checklist integrado para Test Architects (Hawkeye).

### Fonte 3: `ryanmcdermott/clean-code-javascript`
* **URL:** `https://github.com/ryanmcdermott/clean-code-javascript`
* **Licença:** MIT License
* **Arquivos Consultados:** `README.md`.
* **Conceitos Aproveitados:** Aplicação prática dos princípios SOLID em linguagens dinâmicas (JS/TS/Python), cláusulas de guarda, imutabilidade e concorrência sem efeitos colaterais.
* **Transformação Realizada:** Síntese em diretrizes operacionais de código seguro e tipagem estrita para front-end e microserviços.

---

## 2. Declaração de Autoria e Direitos Autorais
* As regras contidas nesta política constituem uma **obra autoral independente** desenvolvida para o Wize Developer Kit.
* Nenhuma cópia literal de textos protegidos dos livros de Robert C. Martin foi realizada. Todos os princípios foram reescritos em linguagem técnica objetiva, operacional e verificável.
