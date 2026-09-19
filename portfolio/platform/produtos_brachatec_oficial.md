# ARQUITETURA DEFINITIVA DE PRODUTOS & ESTRATÉGIA DE ESCALA — PLATAFORMA BRACHATEC

**Documento Estratégico Consolidado:** Cobertura Técnica do Ciclo de Risco + Arquitetura de Três Ramos + Análise de Viabilidade White-Label + Brachatec Academy.

---

## 1. PRINCÍPIOS DE DESIGN & DIRETRIZES DA ENGENHARIA BRACHATEC

Toda a arquitetura da BRACHATEC é regida por quatro princípios estruturais inegociáveis:

* **Módulo vs. Produto Distinto** — A distinção é orientada a mercado, não apenas técnica. Um componente é classificado como produto distinto quando:
  * Possui comprador (Ideal Customer Profile - ICP) diferente do produto de origem;
  * Possui proposta de valor autossuficiente e precificação isolada;
  * Sua ausência não inviabiliza a operação do produto de entrada. Caso contrário, é integrado como módulo funcional.
* **Laudo Pericial como Saída Universal (Moat Probatório)** — Todo produto da plataforma emite laudos periciais estruturados com validade jurídica (Arts. 464+ do CPC, Art. 38 da LGPD, normas do TCU/TCE e regimento do Congresso). Cada laudo gerado recebe um hash criptográfico SHA-256 encadeado e registrado em cofre WORM (Write Once, Read Many).
* **Lock-in Estrutural Cumulativo** — A cadeia de custódia é contínua e histórica. A migração para concorrentes não invalida o passado, mas quebra a integridade da trilha probatória futura, elevando o custo de troca a níveis proibitivos.
* **Modalidades Claras de Aquisição** — Todos os produtos operam em três formatos comerciais: Licença Direta, White-Label e Bundles de Ciclo.

---

## 2. ESTRUTURA GERAL DOS TRÊS RAMOS

```text
                              BRACHATEC ENGINE
               (Motor Central de IA, Parser Regimental & Laudos SHA-256)
                                     │
    ┌────────────────────────────────┼────────────────────────────────┐
    ▼                                ▼                                ▼
 RAMO 1                           RAMO 2                           RAMO 3
Governança de IA              Governança Municipal             Governança Regulatória
(Compliance de Algoritmos)   (Ciclo de Convênios & Gestão)       & Legislativa (RIG Tech)
    │                                │                                │
  • SENTINEL (P1)                  • RADAR (P1)                     • LEX (P1)
  • AEGIS (P2)                     • VIGÍLIA (P2)                   • VANGUARDA MINERAL (P2)
  • GUARDIAN (P3)                  • COMPRAS (P3)
                                   • EXECUTA (P4)
                                   • ALERTA (P5)
                                   • PROVA (P6)
```

---

## 3. DETALHAMENTO TÉCNICO DOS PRODUTOS POR RAMO

### RAMO 1 — GOVERNANÇA DE IA (COMPLIANCE DE ALGORITMOS)
*Focado em diretores de tecnologia (CTO/CISO), encarregados de dados (DPOs), diretores de compliance e departamentos jurídicos corporativos.*

#### PRODUTO 1 (R1-P1) — SENTINEL: Scanner de Shadow AI & Inventário Contínuo
* **O que entrega:** Varredura automática e contínua de rede, APIs, repositórios de código e tráfego SaaS de terceiros (Microsoft Copilot, Notion AI, Grammarly, Adobe Firefly, etc.) para catalogar todos os ativos de IA em operação, gerando inventário padronizado em AI Factsheets.
* **Módulo incorporado — Shadow SaaS Detection:** Rastreamento de IA embutida em serviços em nuvem via DNS corporativo, logs OAuth e conectores de diretório (Azure AD / Google Workspace).
* **Laudo gerado:** Laudo Pericial de Inventário e Exposição a Riscos Algorítmicos.
* **Dependência:** Pré-requisito obrigatório para o AEGIS.
* **Modalidades:** Licença direta (por volume de ativos descobertos); White-label (para bancas de compliance e DPOs); Bundle obrigatório com AEGIS.

#### PRODUTO 2 (R1-P2) — AEGIS: Plataforma de Auditoria, Monitoramento & Ciclo de Vida de Modelos
* **O que entrega:** Plataforma de auditoria contínua dos ativos inventariados pelo SENTINEL sob 4 níveis (L1 Jurídico/PL 2338, L2 Dados/LGPD, L3 Segurança da Informação, L4 Perícia Forense), emitindo Score de Maturidade (0 a 100) e RIPD automatizado.
* **Módulo incorporado — Model Lifecycle Monitor:** Detecta atualizações de versões de modelos em produção (OpenAI, Anthropic, Google ou modelos proprietários) e reexecuta os 122 controles normativos mapeados (ISO 42001, NIST AI RMF, LGPD e PL 2338), emitindo delta de risco.
* **Laudo gerado:** Laudo Pericial de Conformidade Algorítmica & RIPD Oficial + Laudo de Transição de Versão.
* **Dependência:** Requer SENTINEL ativo. Produto âncora do Ramo 1.
* **Modalidades:** Licença direta (por ativos monitorados/mês); White-label (fee por laudo emitido); Bundle completo (SENTINEL + AEGIS).

#### PRODUTO 3 (R1-P3) — GUARDIAN: Gateway de Runtime, Firewall de Agentes & Human-in-the-Loop
* **O que entrega:** Proxy de execução em milissegundos posicionado entre usuários/agentes autônomos e os modelos de linguagem. Bloqueia injeções de prompt (prompt injection), vazamento de PII/segredos industriais e retém chamadas críticas de agentes para aprovação humana.
* **Modelos de Deploy:** Nuvem Soberana Brasileira, VPC Dedicada ou On-Premise (para defesa, saúde e bancos).
* **Laudo gerado:** Laudo Pericial de Integridade de Runtime e Trilha Forense de Bloqueios (hash SHA-256 em cofre WORM).
* **Modalidades:** Licença direta (por milhão de tokens/chamadas interceptadas); White-label exclusivo; Bundle Premium (SENTINEL + AEGIS + GUARDIAN).

### RAMO 2 — GOVERNANÇA MUNICIPAL (CICLO DE CONVÊNIOS FEDERAIS)
*Focado em prefeitos, secretários de finanças/administração, controladores internos e pregoeiros.*

#### PRODUTO 1 (R2-P1) — RADAR: Inteligência de Captação Federal & Emendas
* **O que entrega:** Monitoramento 24/7 do Diário Oficial da União, ministérios, SIOP e painéis parlamentares para identificar editais abertos e emendas impositivas (EC 105/2019) compatíveis com o perfil do município.
* **Laudo gerado:** Relatório Técnico Pericial de Elegibilidade Orçamentária e Emendas Identificadas.
* **Modalidades:** Licença direta por CNPJ; White-label para assessorias parlamentares; Bundle de entrada (RADAR + VIGÍLIA).

#### PRODUTO 2 (R2-P2) — VIGÍLIA: Guardião da Regularidade Fiscal (CAUC + TCE 24/7)
* **O que entrega:** Monitoramento preditivo das obrigações da prefeitura junto ao CAUC/Transferegov e aos Tribunais de Contas Estaduais (TCEs), apontando certidões em risco e emitindo planos de ação de saneamento.
* **Laudo gerado:** Certidão Pericial de Regularidade Fiscal para Transferências Voluntárias.
* **Modalidades:** Licença direta mensal; White-label para contabilidades públicas; Canal associativo (federações estaduais de municípios).

#### PRODUTO 3 (R2-P3) — COMPRAS: Fábrica de Licitações & Instrução Processual (Lei 14.133)
* **O que entrega:** Geração automatizada de Estudos Técnicos Preliminares (ETP) e Termos de Referência (TR) com integração nativa via API aos bancos de preços oficiais (Painel de Preços e PNCP), blindando contra sobrepreço.
* **Laudo gerado:** Laudo Pericial de Justificativa de Preços e Conformidade Contratual.
* **Modalidades:** Licença por processo licitatório instruído; White-label para escritórios de licitação; Bundle Mid-Cycle (VIGÍLIA + COMPRAS).

#### PRODUTO 4 (R2-P4) — EXECUTA: Monitor de Execução & Conformidade de Objeto
* **O que entrega:** Rastreamento do cronograma físico-financeiro de convênios em andamento, confrontando medições de obras, desembolsos e metas para evitar inadimplência técnica durante a vigência.
* **Laudo gerado:** Laudo Pericial de Conformidade de Objeto e Execução Financeira.
* **Modalidades:** Licença direta por convênio monitorado; White-label para consultorias de engenharia e convênios; Bundle de Execução (COMPRAS + EXECUTA).

#### PRODUTO 5 (R2-P5) — ALERTA: SOS Diligências & Destravador Transferegov
* **O que entrega:** Pipeline de OCR e NLP que lê notificações da Caixa e ministérios, classifica a pendência e gera a minuta oficial do Ofício de Resposta fundamentado dentro do prazo fatal.
* **Laudo gerado:** Dossiê Pericial de Saneamento de Pendências e Atendimento de Diligência.
* **Modalidades:** Outcome-based (por diligência sanada); White-label; Entrada emergencial para municípios travados.

#### PRODUTO 6 (R2-P6) — PROVA: Auditor de Despesas, Conciliação & Prestação de Contas
* **O que entrega:** Cruzamento de extratos bancários de contas vinculadas, NF-e (via webservice SEFAZ) e tabelas SINAPI, bloqueando inconsistências e montando a prestação de contas final para o TCU/TCE.
* **Laudo gerado:** Laudo Pericial de Prestação de Contas e Regularidade Financeira.
* **Modalidades:** Licença direta por convênio encerrado; White-label para auditorias públicas; Bundle de Encerramento (EXECUTA + PROVA).

### RAMO 3 — GOVERNANÇA REGULATÓRIA & LEGISLATIVA (RIG TECH)
*Aproveita o motor de análise documental, a esteira de dados abertos e a infraestrutura de laudos da BRACHATEC para o xadrez do Congresso Nacional e agências reguladoras setoriais.*

#### PRODUTO 1 (R3-P1) — LEX: Inteligência Legislativa Contínua & Risco Normativo
* **O que entrega:** Varredura em tempo real sobre a Câmara dos Deputados e Senado Federal, monitorando comissões permanentes com poder conclusivo (Art. 24, II do RICD), substitutivos de relatores e requerimentos de urgência (Art. 155 do RICD). Realiza redline semântico imediato após o protocolo formal, entregando matriz de calor de impacto aos setores econômicos antes do início das sessões.
* **Módulo incorporado — Gestor de Emendas, Votos & DVS:** Estruturação automática de minutas regimentais para subsidiar parlamentares em Pedidos de Vista (Art. 57), Votos em Separado e Destaques para Votação em Separado (DVS).
* **Laudo gerado:** Laudo Pericial de Impacto Legislativo e Risco Normativo (com carimbo temporal e hash SHA-256).
* **Modalidades:** Licença direta para grandes corporações e federações; White-label para bancas de advocacia de RIG e consultorias governamentais; Bundle Federativo (aditivo ao RADAR do Ramo 2 para estados e capitais).

#### PRODUTO 2 (R3-P2) — VANGUARDA MINERAL: Hub de Inteligência em Minerais Críticos & Terras Raras
* **O que entrega:** Vertical especializada de inteligência regulatória e geopolítica para a cadeia de transição energética (lítio, nióbio, níquel, terras raras, grafite, cobre e cobalto). Monitora em 360°:
  * **Executivo e Agências:** Resoluções e leilões de áreas da ANM, portarias do MME, diretrizes do IBAMA/MMA e publicações do DOU;
  * **Congresso:** Projetos de lei sobre marcos de mineração estratégica, regimes de licenciamento e tributação da CFEM;
  * **Regulação Global:** Rastreamento de normas internacionais de exportação (ex.: Critical Raw Materials Act da União Europeia e Inflation Reduction Act dos EUA).
* **Módulo incorporado — Radar de Títulos & Áreas ANM:** Alertas preditivos sobre prazos de pesquisa mineral, guias de utilização, relatórios finais de pesquisa e editais de oferta pública de áreas.
* **Laudo gerado:** Dossiê Pericial de Viabilidade Regulatória e Mineração Estratégica (sustentação jurídica para captação de investimento estrangeiro e auditorias ESG).
* **Modalidades de aquisição:**
  * **White-Label Institucional (Canal Instituto):** O Instituto de Terras Raras opera como distribuidor e parceiro de negócio exclusivo, comercializando os relatórios para mineradoras, montadoras e fundos com sua chancela. A BRACHATEC atua como technology provider e recebe taxa de plataforma + fee por laudo emitido.
  * **Licença Direta:** Venda para indústrias e mineradoras fora do escopo associativo.
  * **Bundle Setorial:** LEX + VANGUARDA MINERAL.

---

## 4. QUADRO CONSOLIDADO DE PRODUTOS — PLATAFORMA BRACHATEC

| Ramo | Código | Produto | ICP Principal | Entrega Central | Laudo Emitido (SHA-256) |
|---|---|---|---|---|---|
| R1: IA | R1-P1 | SENTINEL | CISO, CTO, DPO | Varredura de Shadow AI e SaaS | Laudo de Inventário e Exposição |
| R1: IA | R1-P2 | AEGIS | DPO, Compliance, Legal | Auditoria 4 Níveis e 122 Controles | Laudo de Conformidade & RIPD |
| R1: IA | R1-P3 | GUARDIAN | CISO, Eng. de IA | Proxy de Runtime e Firewall | Laudo de Integridade de Runtime |
| R2: Gov | R2-P1 | RADAR | Sec. Finanças, Captação | Monitoramento DOU e Emendas | Relatório de Elegibilidade |
| R2: Gov | R2-P2 | VIGÍLIA | Prefeito, Finanças | Monitoramento CAUC e TCE 24/7 | Certidão Pericial de Regularidade |
| R2: Gov | R2-P3 | COMPRAS | Pregoeiro, Compras | ETP, TR e Pesquisa de Preços 14.133 | Laudo de Justificativa de Preços |
| R2: Gov | R2-P4 | EXECUTA | Controle Interno, Obras | Acompanhamento Físico-Financeiro | Laudo de Execução de Objeto |
| R2: Gov | R2-P5 | ALERTA | Gestor de Convênios | Resposta Rápida a Diligências | Dossiê de Saneamento de Pendência |
| R2: Gov | R2-P6 | PROVA | Contabilidade, Controle | Conciliação Bancária e NF-e SEFAZ | Laudo de Prestação de Contas |
| R3: RIG | R3-P1 | LEX | Associações, Bancas RIG | Monitoramento Comissões e DVS | Laudo de Risco Normativo |
| R3: RIG | R3-P2 | VANGUARDA | Mineradoras, Instituto | Inteligência ANM, MME e Terras Raras | Dossiê de Viabilidade Mineral |

---

## 5. AVALIAÇÃO ESTRATÉGICA: LUCRATIVIDADE E RISCOS DO WHITE-LABEL

A operação de canais White-Label (WL) simultâneos apresenta alta viabilidade financeira, mas exige separação operacional estrita devido aos perfis discrepantes de canais.

### Comparativo Estrutural de Canais White-Label

| Dimensão | Ramo 1 (Governança IA) | Ramo 2 (Gov Municipal) | Ramo 3 (RIG & Minerais) |
|---|---|---|---|
| **Perfil do Operador** | Bancas de advocacia corporativa, DPOs externos | Contabilidades públicas, empresas de convênios | Consultorias de RIG, Instituto de Minerais |
| **Ciclo de Venda do Canal** | 30 a 90 dias (decisão societária) | 60 a 180 dias (político/institucional) | 15 a 45 dias (parceria institucional) |
| **Volume por Operador** | 5 a 30 clientes corporativos | 10 a 200 municípios | 20 a 100 mineradoras/indústrias |
| **Ticket Médio Cliente Final** | R$ 3.000 a R$ 20.000 / mês | R$ 1.000 a R$ 5.000 / mês | R$ 10.000 a R$ 50.000 / mês |
| **Margem por Unidade** | Alta | Média/Baixa | Muito Alta |
| **Escala Total** | Média (bancas especializadas) | Massiva (5.570 municípios + ONGs) | Nichada e de altíssimo valor |
| **Risco Reputacional** | Alto (litígio e multas ANPD) | Médio (rejeição de contas) | Crítico (decisões de investimento/M&A) |

### Diretrizes de Implementação do White-Label
* **Ramo 1 (IA):** Piloto restrito a no máximo 3 a 5 bancas jurídicas altamente qualificadas. A qualidade e o rigor técnico da emissão dos laudos devem prevalecer sobre a velocidade de distribuição.
* **Ramo 2 (Municipal):** Priorizar a negociação institucional com Federações Estaduais de Municípios. Um único acordo federativo credencia a BRACHATEC para centenas de prefeituras de forma padronizada.
* **Ramo 3 (Minerais Críticos):** Operar o modelo de Parceria Institucional Exclusiva com o Instituto de Terras Raras. A BRACHATEC fornece a tecnologia e o cofre probatório; o Instituto realiza o GTM e a validação de mercado.

---

## 6. BRACHATEC ACADEMY: MOTOR DE CRESCIMENTO E CAPTAÇÃO DE CANAIS

A BRACHATEC ACADEMY é a infraestrutura educacional desenhada para resolver o maior gargalo da governança: a assimetria de conhecimento do comprador. Ela atua como mecanismo de Product-Led Growth (PLG), acelerador de vendas e principal funil de recrutamento de operadores White-Label.

```text
                           BRACHATEC ACADEMY
                                   │
  ┌────────────────────────────────┼────────────────────────────────┐
  ▼                                ▼                                ▼
CAMADA 1: FOUNDATION             CAMADA 2: PRACTITIONER           CAMADA 3: SPECIALIST
(Topo de Funil / Aberto)        (Qualificação / Cadastro)        (Técnico / Habilitação)
  • Consciência de Risco           • Metodologias Práticas          • Laboratórios Práticos
  • Gratuito e Público             • Geração de MQLs                • Certificação Formal
                                                                    │
                                                                    ▼
                                                          CAMADA 4: OPERATOR
                                                          (Exclusivo White-Label)
                                                            • Setup da Plataforma
                                                            • Comercial e Operação
```

### CAMADA 1 — FOUNDATION (Pública, Aberta e Gratuita)
* **Objetivo:** Educar o mercado sobre os riscos regulatórios e atrair tráfego orgânico qualificado via SEO.
* **Formato:** Microaulas em vídeo (5 a 8 minutos) com checklists de fixação. Acesso livre sem necessidade de cadastro.

**Matriz de Conteúdo Foundation**
* **Ramo 1 (Gov IA):**
  * F1.1: O que é Shadow AI e como ela se infiltra na infraestrutura corporativa.
  * F1.2: O marco legal da IA (PL 2338) e os impactos diretos na responsabilidade civil.
  * F1.3: A anatomia de um Relatório de Impacto à Proteção de Dados (RIPD) algorítmico.
  * F1.4: Por que painéis visuais não conferem validade jurídica: o valor probatório do Laudo Pericial SHA-256.
* **Ramo 2 (Gov Municipal):**
  * F2.1: O ciclo financeiro das transferências voluntárias da União aos municípios.
  * F2.2: Bloqueios do CAUC e a perda involuntária de convênios federais.
  * F2.3: Os pontos críticos da Lei 14.133/2021 na instrução de processos licitatórios.
  * F2.4: Como a inadimplência técnica em diligências da CEF desestrutura o orçamento municipal.
* **Ramo 3 (RIG Tech & Minerais):**
  * F3.1: O poder conclusivo das Comissões Permanentes no Congresso Nacional (Art. 24, II do RICD).
  * F3.2: Minerais Críticos e Terras Raras: a nova fronteira regulatória e geopolítica do Brasil.
  * F3.3: Royalties minerários (CFEM) e o impacto das resoluções da ANM na viabilidade de jazidas.

### CAMADA 2 — PRACTITIONER (Lead Qualificado via Cadastro)
* **Objetivo:** Capturar dados completos do lead (nome, cargo, organização, CNPJ) e demonstrar o método resolutivo da BRACHATEC.
* **Formato:** Aulas aplicadas (15 a 25 minutos), templates operacionais para download e avaliação técnica ao término.
* **Gatilho Comercial:** Concluintes recebem automaticamente credenciamento para trial guiado de 14 dias no produto de seu ramo de atuação.

**Matriz de Conteúdo Practitioner**
* **Ramo 1 (Gov IA):**
  * P1.1: Metodologia de Mapeamento de Ativos de IA e elaboração de AI Factsheets.
  * P1.2: Auditoria em 4 Níveis (L1 Jurídico a L4 Pericial): identificação de passivos algorítmicos.
  * P1.3: Protocolos de resposta a incidentes de segurança gerados por agentes autônomos.
* **Ramo 2 (Gov Municipal):**
  * P2.1: Rotinas de monitoramento do DOU e habilitação técnica de emendas impositivas (EC 105).
  * P2.2: Saneamento de certidões e desbloqueio operacional do CAUC/Transferegov.
  * P2.3: Elaboração de ETP e TR blindados contra impugnações de preços.
* **Ramo 3 (RIG Tech & Minerais):**
  * P3.1: Rastreamento de substitutivos e redação de Destaques para Votação em Separado (DVS).
  * P3.2: Rito processual de concessões de lavra e licenciamento ambiental na ANM/IBAMA.

### CAMADA 3 — SPECIALIST (Certificação Profissional Avançada)
* **Objetivo:** Formar especialistas aptos a operar as ferramentas e emitir laudos. Gera receita direta de capacitação ou funciona como diferencial de planos Enterprise.
* **Modelo:** Pago (R$ 997 a R$ 1.997) ou incluso em contratos anuais corporativos/municipais.
* **Formato:** Treinamento técnico profundo, laboratórios práticos em ambiente sandbox da BRACHATEC e projeto final com emissão de laudo auditado.
* **Saída:** Certificação profissional com validade de 2 anos, verificável publicamente por hash e QR Code.

**Especializações Oferecidas:**
* Auditor e Perito em Conformidade Algorítmica BRACHATEC (Ramo 1)
* Especialista em Gestão de Convênios e Instrução Processual Municipal (Ramo 2)
* Analista Sênior de Inteligência Regulatória e Mineral (Ramo 3)

### CAMADA 4 — OPERATOR (Habilitação Exclusiva para White-Label)
* **Objetivo:** Treinar, qualificar e homologar os parceiros comerciais que operarão a plataforma sob sua própria marca.
* **Requisitos:** Conclusão prévia da trilha Specialist, assinatura de termo de compliance/NDA e aprovação em comitê operacional da BRACHATEC.
* **Conteúdo:**
  * Configuração do tenant e parametrização da identidade visual White-Label;
  * Gestão de subcontas, limites de chamadas e controle de emissão de laudos;
  * Treinamento comercial de vendas consultivas e precificação para o cliente final;
  * Melhores práticas de custódia pericial e defesa dos laudos emitidos.
* **Saída:** Habilitação oficial de Operador White-Label Homologado BRACHATEC e inclusão no ecossistema de parceiros credenciados.

---

## 7. STACK TECNOLÓGICO, CRONOGRAMA & MODELO DE RECEITA DA ACADEMY

### Infraestrutura Recomendada da Academy

| Componente | Ferramenta Recomendada | Justificativa Técnica |
|---|---|---|
| **Ambiente de Aprendizagem (LMS)** | Hotmart (Fase 1) → Portal Próprio em Next.js (Fase 2) | Rápido time-to-market na Fase 1; consolidação de dados proprietários na Fase 2 |
| **Certificados Digitais** | Emissão nativa via Engine BRACHATEC (SHA-256) | Coerência com a tese de laudos auditáveis e exportação direta para LinkedIn |
| **Ambiente de Prática (Sandbox)** | Tenants isolados de staging da BRACHATEC | Permite simulações de auditoria e geração de laudos em dados sintéticos |
| **Integração Comercial** | Webhooks com CRM corporativo | Conversão automática de alunos em oportunidades de vendas |

### Fontes de Monetização da Academy
* **Cursos Specialist Avulsos:** Venda direta para profissionais de mercado (DPOs, assessores parlamentares, advogados e engenheiros de minas).
* **Upsell de Assinatura:** Inclusão de vagas de certificação anual como benefício dos planos corporativos da plataforma.
* **Taxa de Homologação White-Label:** Cobrança de onboarding fee para novos operadores credenciados na camada Operator.
* **Reciclagem Bianual:** Taxa de renovação e revalidação técnica da credencial profissional a cada 24 meses.

---

## 8. SÍNTESE E DIRETRIZ ESTRATÉGICA

Com a consolidação deste modelo, a BRACHATEC estrutura suas frentes de atuação de forma clara:

* **A Tecnologia Mãe (BRACHATEC ENGINE):** Centraliza o processamento de linguagem natural, as integrações governamentais/regulatórias e o cofre probatório de Laudos Periciais com hash SHA-256.
* **Os Três Mercados de Atuação:**
  * **Ramo 1:** Vende proteção algorítmica corporativa contra multas e litígios (CISO/DPO).
  * **Ramo 2:** Vende destravamento de receitas e proteção fiscal para prefeituras (Prefeito/Finanças).
  * **Ramo 3:** Vende antecipação de riscos políticos e regulatórios para indústrias e o setor mineral, alavancado pela parceria com o Instituto de Terras Raras.
* **A Força de Vendas Educacional (BRACHATEC ACADEMY):** Elimina a barreira de entrada técnica, forma o mercado consumidor e atua como o principal canal de captação de parceiros White-Label.