# Cronograma de Desenvolvimento (Zero à Produção)

Este cronograma define as entregas diárias do projeto BRACHATEC, servindo como memória para os agentes sobre o status de evolução da plataforma.

## Fase 1: Fundação & Planejamento (CONCLUÍDO)
- [x] **Setup do QG Global:** Configuração dos agentes (Wizer, Shuri, Tony Stark, Visão).
- [x] **Políticas de Qualidade (Clean Code):** Estabelecimento das regras globais, obrigatoriedade de Idempotência e exigência estrita de isolamento de pastas (frontend/backend/infra).
- [x] **Importação da Fonte de Verdade:** Importação das páginas HTML do `site_oficial` e adequação das nomenclaturas (BTScan, BTMonitor, superXAi, BTGestor, BTLicita, BTCapta, BTLex, BTAlerta, BTProva).
- [x] **PRD & Visão Técnica de Infraestrutura:** 
  - Definição do Funil de Vendas (Site -> Produto -> Pagamento -> Ramo).
  - Restrição de Isolamento White-Label: Módulos (Gov IA, Gov Muni, RIG) como aplicações 100% autônomas.
  - Separação mandatória de Backends (`backend/gov_ai`, `backend/gov_muni`, `backend/rig_tech`) e seus respectivos Bancos de Dados.
  - Desacoplamento de frontends logados para permitir personalização de White-Label.

## Fase 2: Infraestrutura Base & Engenharia Core (Próximos Passos)
- [ ] **Dia 1:** Configuração do Monorepo e Infra. Setup do `docker-compose` com os 3 bancos de dados independentes (PostgreSQL 16) e LocalStack (S3 para o cofre WORM).
- [ ] **Dia 2:** Criação do API Gateway e serviço de Autenticação/Tenancy. Setup da infraestrutura de schemas por cliente.
- [ ] **Dia 3:** Setup base do Frontend App Next.js com autenticação, conectando-se ao Gateway.

## Fase 3: Ramo 1 - Governança de IA (superXAi & AGCP)
- [ ] **Dia 4:** Backend: Implementação do AGCP (Advanced Governance Control Proxy) com as restrições de latência <50ms.
- [ ] **Dia 5:** Backend: Integração do motor matemático superXAi para validação semântica e cálculo de intenção.
- [ ] **Dia 6:** Backend/Integração: Desenvolvimento do gerador de Trilhas de Auditoria (Cadeia SHA-256) e integração com o S3 WORM.
- [ ] **Dia 7:** Frontend: Telas de relatórios forenses e dashboards do BTMonitor e BTScan.

## Fase 4: Ramo 2 - Setor Público (BTGestor, BTLicita, BTCapta)
- [ ] **Dia 8:** Backend: Integração com APIs externas (SIAFI, Transferegov) e desenvolvimento do motor do BTGestor.
- [ ] **Dia 9:** Backend/Frontend: Construção do fluxo passo a passo de licitação (BTLicita) garantindo conformidade com a Lei 14.133.
- [ ] **Dia 10:** Backend: Implementação dos scrapers e rastreadores de emendas parlamentares para o BTCapta.

## Fase 5: Ramo 3 - RIG Tech (BTLex, BTAlerta, BTProva)
- [ ] **Dia 11:** Backend: Setup dos scrapers do BTLex focados em Câmara, Senado e Diários Oficiais.
- [ ] **Dia 12:** Backend: Implementação do BTAlerta (classificação de risco via árvore de palavras-chave).
- [ ] **Dia 13:** Integração e Frontend: Painel do RIG Tech e integração do módulo BTProva (Time-Stamp inalterável).

## Fase 6: Módulo Master (Super Admin) & Faturamento
- [ ] **Dia 14:** Implementação do portal Super Admin (`SUPER_ADMIN`).
- [ ] **Dia 15:** Integração de Webhooks de Pagamento (freemium, travamento de inadimplência após 7 dias) e automações do Slack.

## Fase 7: Testes, Auditoria & Produção (Deploy)
- [ ] **Dia 16:** Penetration Testing (wize-sec-red-teamer) e auditoria de Clean Code final.
- [ ] **Dia 17:** Testes de carga simulando múltiplos tenants em paralelo nas 3 instâncias.
- [ ] **Dia 18:** Go-Live. Implantação nos servidores de produção AWS (sa-east-1).
