# Product Requirements Document (PRD) — Plataforma BRACHATEC

## 1. Identificação & Objetivos do Produto
* **Nome do Produto:** BRACHATEC Engine & Platform
* **Versão do Documento:** 1.0.0 (Consolidado Master)
* **Status:** Aprovado para Arquitetura & Implementação
* **Objetivo Primário:** Entregar um ecossistema SaaS multi-tenant unificado que automatiza a governança probatória nos 3 ramos (Gov IA, Setor Público, RIG Tech), operando sob isolamento estrito de dados (*schema-per-tenant*), trilhas de auditoria SHA-256 e emissão de Laudos Periciais em PDF/JSON auditáveis.

---

## 2. Requisitos Funcionais & Critérios de Aceite (ACs)

### Módulo Transversal: Autenticação, Sessão & Multi-Tenancy
* **RF-01 (Autenticação Corporativa):** Login seguro (`/app/login.html`) e cadastro pós-pagamento (`/app/cadastro.html`) com suporte a múltiplos perfis (Admin, Tenant, White-Label Partner).
  * **AC-01.1:** Autenticação via JWT com refresh tokens seguros e política de expiração.
  * **AC-01.2:** Cada tenant opera em um schema isolado do PostgreSQL 16 (`tenant_{id}`).
  * **AC-01.3:** Parceiros White-Label visualizam painel consolidado com a sua marca e subtenants vinculados.

### Módulo 1: Governança de IA (Ezra / Sentinel / CPT / Time-Travel)
* **RF-02 (Discovery & Sentinel):** Inventário contínuo de endpoints e detecção de Shadow AI corporativa.
  * **AC-02.1:** Registro de chamadas de LLM com classificação de risco criptográfico.
  * **AC-02.2:** Detecção e mascaramento de PII (CPFs, cartões, senhas) antes do envio para provedores de IA.
* **RF-03 (Controlador CPT Inline):** Interceptação Commit-Bound em milissegundos (< 50ms) com avaliação dos 129 filtros em 5 camadas (L1 a L5).
  * **AC-03.1:** Se houver infração de regra ou viés discriminatório, a requisição é bloqueada em modo *fail-closed*.
  * **AC-03.2:** Geração de evento forense com hash SHA-256 vinculado à cadeia do tenant.
* **RF-04 (Time-Travel & Explicabilidade):** Emissão de RIPD de IA e reconstrução do contexto exato da decisão algorítmica.
  * **AC-04.1:** Geração de Laudo Pericial de Explicabilidade com assinatura digital e recibo WORM.

### Módulo 2: Setor Público (Radar / Vigília / Compras / Executa)
* **RF-05 (Radar & Vigília do CAUC):** Monitoramento de 27 itens de conformidade fiscal e certidões municipais.
  * **AC-05.1:** Disparo de alertas automáticos (WhatsApp/E-mail) 15, 7 e 2 dias antes do vencimento de certidões ou prazos do SICONFI (RREO/RGF).
  * **AC-05.2:** Status em tempo real no Dashboard: Verde (Regular), Amarelo (Atenção), Vermelho (Risco de Bloqueio).
* **RF-06 (Módulo Compras & Lei 14.133):** Auditoria preventiva de editais, contratos e dispensas de licitação.
  * **AC-06.1:** Verificação automática de enquadramento em limites legais de dispensa (Art. 75, II).
* **RF-07 (Módulo Executa):** Rastreabilidade de convênios (Transferegov.br) com ateste de execução e prova para o TCE.

### Módulo 3: RIG Tech (Lex / Alerta / Prova)
* **RF-08 (Módulo LEX):** Ingestão e indexação contínua de proposições legislativas e diários oficiais.
  * **AC-08.1:** Web scraping legal e integração com APIs de Câmaras, Assembleias e Congresso.
  * **AC-08.2:** Busca semântica e classificação de risco por árvore de palavras-chave.
* **RF-09 (Módulo PROVA):** Carimbo de tempo criptográfico (Time-Stamp SHA-256) de publicações oficiais para proteção contra apagão de dados.

### Módulo Central: Painel de Controle (`/app/dashboard.html`) & Relatórios Dinâmicos
* **RF-10 (Dashboard Operacional em Tempo Real):**
  * **AC-10.1:** Cards de métricas dinâmicas com contadores reais (Projetos de Lei monitorados, Requisições de IA validadas, Alertas Críticos ativos).
  * **AC-10.2:** Feed de últimas atividades com badge do ramo, descrição do evento, hash SHA-256 resumido e timestamp.
  * **AC-10.3:** Seletor lateral de módulos (Visão Geral, Radar RIG, Governança IA, Compras Gov, Relatórios Forenses).
* **RF-11 (Motor de Relatórios Dinâmicos & Laudo Pericial):**
  * **AC-11.1:** O botão "Gerar Relatório Geral" processa o estado atual do tenant e emite um Laudo Pericial completo.
  * **AC-11.2:** Exportação em formato PDF com layout formal e em formato JSON estruturado assinado.
  * **AC-11.3:** Cada laudo gerado inclui: Metadados do Tenant, Período, Hash do Laudo Atual, Hash do Laudo Anterior (Chain SHA-256), Sumário Executivo de Riscos e Tabela de Evidências.

---

## 3. Regras de Negócio Inegociáveis
* **RN-01 (Preços Fixos):** Não utilizar "a partir de" nos orçamentos formais e no sistema.
* **RN-02 (White-Label Setup Isento):** Cobrança base de R$ 1.350/mês para parceiros (inclui 2 tenants) + R$ 450/mês por tenant excedente. Taxa de setup = R$ 0,00.
* **RN-03 (Imutabilidade Probatória):** Todo registro que entra na cadeia probatória deve ter retenção de integridade por no mínimo 10 anos (política WORM).

---

## 4. Módulo Master: Super Admin, Gestão Financeira & Observabilidade

### RF-12 (Painel Master do Dono / Super Admin)
* **AC-12.1:** Acesso restrito via autenticação de dois fatores (2FA) e role exclusiva `SUPER_ADMIN`.
* **AC-12.2:** Visão panorâmica consolidada: Total de Tenants Ativos, MRR (Receita Recorrente Mensal), Inadimplência e novos cadastros.
* **AC-12.3:** Controle manual e automático de status do tenant: `ATIVO`, `TRIAL_FREEMIUM`, `SUSPENSO_INADIMPLENCIA`, `CANCELADO`.

### RF-13 (Políticas de Freemium, Liberação & Travamento)
* **AC-13.1 (Freemium):** Acesso degustação limitado (10 requisições de IA, 5 PLs monitorados). Relatórios forenses com marca d'água "VERSÃO DE DEGUSTAÇÃO".
* **AC-13.2 (Liberação Automática):** Webhook de gateway de pagamento (Asaas/Stripe/Pagar.me) ativa a conta e dispara e-mail de boas-vindas imediatamente.
* **AC-13.3 (Travamento por Inadimplência):** Após 7 dias de tolerância sem confirmação de pagamento, o middleware bloqueia o login do tenant e redireciona para a tela de regularização financeira.

### RF-14 (Sistema de Notificações & Alertas via Slack)
* **AC-14.1 (Eventos de Negócio):** Disparo de mensagem no canal `#brachatec-vendas` a cada novo cadastro, upgrade de plano ou fatura paga.
* **AC-14.2 (Alertas de Erros & Incidentes):** Disparo imediato no canal `#brachatec-alertas-dev` para qualquer exceção 500, falha de integridade SHA-256 ou lentidão anormal (>500ms).
* **AC-14.3 (Heartbeat Diário):** Relatório automático diário às 08:00 UTC-3 com métricas de saúde e estabilidade de todos os microserviços.
