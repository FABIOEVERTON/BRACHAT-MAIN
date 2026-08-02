---
name: ai-job-search-agent
id: S02
cluster: integracao
description: Automatiza busca, filtragem, candidatura e preparação para entrevistas em vagas de emprego.
---

### Objetivo
Automatizar busca, filtragem, candidatura e preparação para entrevistas em vagas de emprego.

### Entradas
- Comando do usuário (/start, /setup, /scrape, /apply [link], /interview [tipo])
- Perfil LinkedIn (PDF ou texto)
- Vagas encontradas via scrapers

### Saídas
- Perfil consolidado (Profile_master.json), vagas filtradas e ranqueadas, cover letter + CV customizados, guia de entrevista STAR

### Dependências
- SK-011 (Estratégia) para cargos-alvo
- SK-001 (Spec) para estado final de cada candidatura
- SK-006 (Data Sensemaking) para interpretação de vagas
- SK-007 (HITL) para confirmação antes de aplicar
- Ferramentas: Composio (Gmail), Integrations/APIS/ (scrapers)

### Token Budget
- /start: 500 tokens | /setup: 1500 tokens | /scrape: 2000 tokens | /apply: 3000 tokens | /interview: 2000 tokens

### Custos
- Alto. Cada candidatura gera tokens de pesquisa + geração + carta.

### Segurança
- Currículo e perfil são dados pessoais → LGPD.
- Links de candidatura são External → seguir External Integrations Rule.
- Proibido inventar experiências que não estão no perfil.

### Testes
1. Perfil consolidado contém todas as skills do LinkedIn?
2. /apply gera carta única por empresa?
3. /interview identifica gaps reais do candidato?

---
