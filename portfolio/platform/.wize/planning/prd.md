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

### Módulo 1: Governança de IA (BTScan, BTMonitor & superXAi)
* **RF-02 (BTScan):** Mapeamento e inventário contínuo de endpoints focado estritamente em capturar Shadow AI corporativa.
  * **AC-02.1:** Registro de chamadas de LLM com classificação de risco e mascaramento de PII.
* **RF-03 (BTMonitor):** Controlador CPT inline responsável exclusivo por aplicar os 129 filtros de IA em tempo real.
  * **AC-03.1:** Se houver infração de regra ou viés discriminatório, a requisição é bloqueada em modo *fail-closed* (< 50ms).
* **RF-04 (superXAi):** Motor de expressão matemática e explicabilidade que reconstrói a lógica da decisão algorítmica.
  * **AC-04.1:** Ambos (BTMonitor e superXAi) geram relatórios forenses fortíssimos com assinatura digital SHA-256 e recibo WORM.

### Módulo 2: Setor Público (BTGestor / BTLicita / BTCapta)
* **RF-05 (BTGestor):** Monitoramento de obras no Transferegov e SIAFI.
  * **AC-05.1:** Quando uma obra começa e precisa ser inserida no Transferegov e SIAFI, ele monitora e auxilia o gestor em tudo o que acontecer lá, provendo documentos e ajudando em diligências.
* **RF-06 (BTLicita):** Assistente passo a passo de licitação.
  * **AC-06.1:** Desenvolvido para treinar e ajudar diretamente o pregoeiro ou a equipe de licitação passo a passo na montagem da licitação.
* **RF-07 (BTCapta):** Motor de rastreabilidade de convênios.
  * **AC-07.1:** Rastreia convênios federais, emendas parlamentares ou qualquer outro fundo em que o prefeito deseje realizar buscas de recursos.

### Módulo 3: BTRig (BTLex / BTAlerta / BTProva)
* **RF-08 (BTLex):** Monitoramento de qualquer tipo de órgão (incluindo projetos na Câmara e Senado).
  * **AC-08.1:** Focado em empresas (que pagam caro para assessores fazerem este monitoramento). Realiza ingestão e indexação contínua.
* **RF-09 (BTAlerta & BTProva):** Prevenção e evidências imutáveis.
  * **AC-09.1:** (BTAlerta) Busca semântica e emissão de alertas de risco antecipado.
  * **AC-09.2:** (BTProva) Carimbo de tempo criptográfico (Time-Stamp SHA-256) de publicações oficiais gerando dossiês com prova inalterável.

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

## 3. Regras de Negócio & Arquitetura de Precificação
* **RN-01 (Política Comercial e Planos Homologados):**
  * **Governança de IA:**
    * *Standard:* R$ 2.900/mês + Setup R$ 7.500 (Isento no Programa Fundador).
    * *Enterprise:* Sob Consulta / Personalizado (dimensionamento sob medida conforme volume de filiais, modelos LLM e operadores terceiros de IA auditados).
  * **Setor Público:**
    * *Pacote Dispensa de Licitação (Lei 14.133):* R$ 3.900/mês + Setup R$ 9.500 (R$ 56.300/ano — dentro do teto de compras diretas sem licitação).
    * *Pacote Licitação / Estados:* Sob Consulta (Pregão Eletrônico).
  * **RIG Tech:**
    * *Corporativo:* R$ 3.500/mês + Setup R$ 5.900 (Mapeamento de matriz de risco incluso).
  * **White-Label (Parceiros em todos os ramos):**
    * *Licença Base:* R$ 1.350/mês (inclui 2 clientes ativos) + R$ 450/mês por cliente adicional.
    * *Taxa de Habilitação:* R$ 0,00 (Setup Isento).
* **RN-02 (Imutabilidade Probatória):** Todo registro que entra na cadeia probatória deve ter retenção de integridade por no mínimo 10 anos (política WORM).

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

## 5. Restrição Arquitetural: Isolamento de Ramos (White-Label Strict)
* **RN-03 (Isolamento de Infraestrutura):** Os módulos de Governança de IA, Setor Público e BTRig são produtos fisicamente separados no backend.
  * **AC-03.1:** Obrigatório Back-end separado para cada um dos 3 ramos.
  * **AC-03.2:** Obrigatório Banco de Dados separado e totalmente independente para cada um dos 3 ramos.
  * **AC-03.3:** Frontend da área logada deve ter instâncias separadas por ramo caso haja necessidade de customização extrema para clientes White-Label.
