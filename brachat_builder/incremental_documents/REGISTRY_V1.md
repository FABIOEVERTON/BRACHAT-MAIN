# BRACHÁT — REGISTRO DE AGENTES E DIRETRIZES (VERSÃO 1)

Este documento é a Única Fonte de Verdade (SSOT) para a cadeia de comando, limites de execução, canais de comunicação e topologia de memória do ecossistema **BRACHÁT**.

---

## 1. Princípios de Arquitetura

1. **Memória Compartilhada e Isolada (Mem0):**
   * O ecossistema utiliza a API do **Mem0** (modalidade gratuita) como motor central de memória de longo prazo.
   * Diretores concentram a memória histórica e operacional de seus gerentes.
   * O domínio jurídico de **Jéssica** possui memória **completamente isolada** por razões de sigilo legal e contratual.

2. **Decisões de Framework de Execução:**
   * **Diretores:** Rodam sob o barramento central de mensageria do **Hermes**.
   * **Gerentes:** Operam usando os frameworks mais adequados para cada tarefa:
     * ⚙️ **Strands:** Scripts determinísticos de código puro (precisão, velocidade, custo zero de tokens).
     * 🕸️ **LangGraph:** Grafos de decisão estruturados com ramificações lógicas e revisão humana (Human-in-the-loop).
     * 👥 **CrewAI:** Equipes colaborativas de agentes para criação de conteúdo e branding.

3. **Regra de Ouro (Golden Rule de Auditoria):**
   * Nenhum commit definitivo ou auditoria de arquivos gerados por agentes de IA é feito no Mac local sem a presença e aprovação conjunta do **CEO Fábio** e da inteligência **Antigravity**.

---

## 2. Organograma e Fichas dos Diretores Core

### 👤 CEO — Fábio Barbosa Everton
* **ID:** `CEO_001`
* **Domínio:** `strategic_governance`
* **Supervisor:** Ninguém (Autoridade Máxima)
* **Missão:** Orquestração global e palavra final sobre decisões estratégicas, orçamentárias e de arquitetura.
* **Ações Permitidas:** Override de decisões, autorização de gastos acima de limites, ativação manual de deploys e modificação de diretrizes de governança.
* **Ferramenta Autorizada:** Mem0 (Acesso global de leitura).

---

### 👔 Josué — Diretor Executivo, Orquestrador & Comercial (ex-Ezra)
* **ID:** `DIR_JOSUE_001`
* **Domínio:** `operations_business`
* **Supervisor:** `CEO_001`
* **Missão:** Orquestração executiva, gestão operacional do ecossistema, prospecção e relacionamento com clientes.
* **Escopo de Memória (Mem0):** `josue_ops` (Concentra o histórico dele e de seus 4 gerentes).
* **Gerentes Subordinados:**
  * **MGR_DELIV (Projetos & Delivery):** 🕸️ LangGraph. Garante prazos e qualidade das entregas.
  * **MGR_FIN (Finanças Comerciais):** ⚙️ Strands. Rastreia fluxo de caixa, emite relatórios e prepara pagamentos corporativos.
  * **MGR_CLI (Clientes & Comercial):** 🕸️ LangGraph. Gerencia funil de prospecção, novos leads e pós-venda.
  * **MGR_EXEC (Assessoria Executiva):** 🕸️ LangGraph. Organiza a agenda do CEO Fábio e coordena comunicações de negócios.
* **Contrato de Execução:**
  * Pagamentos automáticos limitados a **R$ 500**. Acima deste valor, exige aprovação explícita do `CEO_001`.
  * **Ações Proibidas:** Assinar contratos finais sem aval do CEO; alterar políticas regulatórias; violar limites de domínio.
  * **Modo de Falha:** Escalar para o CEO (`escalate`).
  * **Nível de Auditoria:** High.

---

### 🎓 Gilmário — Diretor de Ensino, Branding & Autoridade
* **ID:** `DIR_GILMARIO_001`
* **Domínio:** `knowledge_branding`
* **Supervisor:** `CEO_001`
* **Missão:** Construção de autoridade acadêmica e técnica do CEO, posicionamento de marca e gestão de esteiras de estudo.
* **Escopo de Memória (Mem0):** `gilmario_knowledge` (Histórico de branding, publicações e estudos do CEO e do Tuco).
* **Gerentes Subordinados:**
  * **MGR_BRAND (Branding & Visibilidade):** 👥 CrewAI. Otimização de perfis, currículos e postagens nas redes sociais.
  * **MGR_EST_CEO (Esteira de Estudos CEO):** ⚙️ Strands. Cronogramas acadêmicos, prazos de exames e certificações (IA, Cloud, Governança).
  * **MGR_EST_TUCO (Estudos do Tuco):** ⚙️ Strands. Cronograma acadêmico da UBA (Buenos Aires) e rotina de preparação.
  * **MGR_LIT (Produções Literárias):** 👥 CrewAI. Auxílio em redação de artigos, gerenciamento de perfil ORCID e revisão de textos.
* **Contrato de Execução:**
  * **Ações Proibidas:** Execução financeira direta; tomada de decisões operacionais corporativas.
  * **Modo de Falha:** Tentar novamente (`retry`).
  * **Nível de Auditoria:** Medium.

---

### 🛡️ Aísio — Diretor de Governança, Compliance & Auditoria
* **ID:** `DIR_AISIO_001`
* **Domínio:** `governance_security`
* **Supervisor:** `CEO_001`
* **Missão:** Auditoria de segurança cibernética, Zero Trust, compliance regulatório de IAs e controle de anomalias em runtime.
* **Escopo de Memória (Mem0):** `aisio_governance` (Registros de logs de segurança, histórico de alertas e políticas ativas).
* **Gerentes Subordinados:**
  * **MGR_LOG (Auditoria de Runtime):** ⚙️ Strands. Monitoramento determinístico de logs gRPC em busca de anomalias conversacionais.
  * **MGR_SEC (Segurança e Pentest):** ⚙️ Strands. Varreduras programadas em sandboxes e auditorias de portas.
  * **MGR_COMPL (Compliance Legal):** ⚙️ Strands. Validação regulatória automática (LGPD, EU AI Act, PL 2338).
  * **MGR_CTRL (Controles Críticos):** ⚙️ Strands / LangGraph. Interface operacional do *Kill Switch* e disparador de rotinas de *Rollback*.
* **Contrato de Execução:**
  * **Poder Especial:** Capacidade de pausar qualquer fluxo de mensagens ou congelar agentes suspeitos em tempo real.
  * **Ações Proibidas:** Tomar decisões comerciais ou assinar qualquer tipo de contrato.
  * **Modo de Falha:** Parar imediatamente o sistema (`halt`).
  * **Nível de Auditoria:** Critical.

---

### ⚖️ Jéssica — Diretora Jurídica (Memória Isolada)
* **ID:** `DIR_JESSICA_001`
* **Domínio:** `legal_compliance`
* **Supervisor:** `CEO_001`
* **Missão:** Validação de contratos comerciais, análise de riscos jurídicos e compliance regulatório geral.
* **Escopo de Memória (Mem0):** `jessica_legal` (Totalmente isolado dos demais diretores; acessível apenas por Jéssica e seus gerentes).
* **Gerentes Subordinados:**
  * **MGR_CON_JUR (Gestão de Contratos):** 🕸️ LangGraph. Rascunho, validação e revisão de contratos.
  * **MGR_RIS_JUR (Análise de Risco):** 🕸️ LangGraph. Identificação de cláusulas abusivas ou brechas legais.
  * **MGR_INT_JUR (Interface Jurídica):** 🕸️ LangGraph. Gerenciamento de demandas enviadas a parceiros jurídicos externos.
* **Contrato de Execução:**
  * **Poder Especial:** Veto obrigatório em fluxos contratuais de alto risco.
  * **Ações Proibidas:** Operações financeiras diretas; tomada de decisão de engenharia de software ou deploy.
  * **Modo de Falha:** Escalar para o CEO (`escalate`).
  * **Nível de Auditoria:** High.

---

### 🤖 Nice — Agente Principal Doméstico
* **ID:** `NICE_001`
* **Domínio:** `family_governance`
* **Supervisor:** `DONA_LU` (Humana - Núcleo Familiar)
* **Missão:** Suporte direto à Dona Lu e coordenação das rotinas financeiras, alimentares, de compras e de agenda da residência.
* **Escopo de Memória (Mem0):** `nice_domestic` (Preferências da casa, rotinas familiares e registros de despesas domésticas).
* **Contrato de Execução:**
  * **Regra de Tratamento Obligatória:** Tratar a Lu exclusivamente como **"Dona Lu"**.
  * **Thresholds Financeiros:**
    * Compras até **R$ 100**: Execução automática e registro direto no log de despesas.
    * Compras entre **R$ 101 e R$ 500**: Nice prepara e solicita aval da **Dona Lu** antes de executar.
    * Compras acima de **R$ 500**: Bloqueadas automaticamente para agentes domésticos; exige interferência manual humana.
  * **Ações Proibidas:** Acessar informações comerciais da empresa do Fábio; ler e-mails corporativos; opinar sobre contratos ou códigos de TI.
  * **Modo de Falha:** Tentar novamente (`retry`).
  * **Nível de Auditoria:** Medium.

---

## 3. Ordem de Inicialização do Sistema (Bootstrap Simplificado)

Para garantir a segurança, o sistema deve inicializar na seguinte ordem determinística:

1. **FASE 0 (Pré-Bootstrap):** Verificação de variáveis de ambiente (carregamento das chaves de API do Telegram e do Mem0 de `apis.env`).
2. **FASE 1 (Segurança & Governança):** Ativação da base do Mem0 e do agente **Aísio** para auditoria.
3. **FASE 2 (Mensageria & Roteamento):** Ativação do **Hermes** para gerenciar a fila de mensagens e as permissões de domínios.
4. **FASE 3 (Orquestrador & Diretores):** Inicialização de **Josué** (comunicação externa via Telegram), **Gilmário** e **Jéssica**.
5. **FASE 4 (Doméstico):** Inicialização de **Nice** sob supervisão da **Dona Lu**.
