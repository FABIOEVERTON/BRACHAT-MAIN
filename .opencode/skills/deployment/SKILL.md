---
name: deployment
id: S12
cluster: integracao
description: Empacota, versiona e implanta agentes e skills em produção com backup, rollback e health check.
---

### Objetivo
Empacotar, versionar e implantar agentes e skills em produção (Docker, VM, OCI) com backup, rollback e atualizações seguras.

### Regra de Produção — Imagem Própria (aprovada por Fabio, 02/ago/2026)
- **Todo projeto de produção no git DEVE ter imagem própria (Dockerfile)**.
- Motivo: quem receber o repo não precisa saber configurar o ambiente — `docker compose up` sobe.
- Execução nativa apenas para desenvolvimento.
- Ezra é dockerizado via `docker/Dockerfile.ezra`.
- Portfólio: Dockerfile próprio quando produção; compartilhar via imagem, não via instruções de setup.
- Segredos nunca na imagem: injetar por env/volume (`.env`/secrets).

### Entradas
- Artefato a ser deployado (agente, skill, configuração)
- Ambiente alvo (produção, staging, teste)
- Estratégia de deploy (blue-green, canary, rolling)

### Saídas
- Artefato empacotado e versionado
- Deploy executado com sucesso
- Backup do estado anterior
- Rollback documentado e testado
- Health check pós-deploy

### Dependências
- SK-010 (Arquitetura de Harness) para infraestrutura
- SK-023 (Agent Factory) se deploy de novo agente

### Token Budget
- 800-1500 tokens por ciclo de deploy

### Custos
- Médio-Alto. Depende da infraestrutura alvo (Docker, cloud).

### Segurança
- Toda imagem/artefato deve ser assinado antes do deploy.
- Rollback automático se health check falhar nos primeiros 5 minutos.
- Credenciais de ambiente não devem estar no artefato (usar secrets externos).

### Testes
1. Backup do estado anterior foi criado antes do deploy?
2. Health check passou após deploy?
3. Rollback restaurou estado anterior sem perda de dados?
4. Versão foi incrementada corretamente?

---
