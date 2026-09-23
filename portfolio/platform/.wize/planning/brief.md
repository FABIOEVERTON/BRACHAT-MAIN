# Product Brief — Plataforma BRACHATEC

## 1. Visão Geral do Produto
A **BRACHATEC** é uma plataforma SaaS B2B/B2G de **Governança Probatória**. Ela converte requisitos de conformidade regulatória, fiscal e algorítmica em **provas forenses com validade jurídica irrefutável**, estruturadas através de uma cadeia criptográfica SHA-256 e custodiadas em cofre WORM (*Write Once Read Many*).

## 2. Proposta Única de Valor (UVP)
* **Governança que resiste:** Blindagem contra litígios, multas regulatórias (até R$ 50 mi / LGPD), rejeição de contas pelo TCE/TCU e bloqueios no CAUC.
* **Efeito Flywheel Criptográfico:** Cada ação na plataforma emite um Laudo Pericial que encadeia o hash SHA-256 da ação anterior. O histórico do cliente torna-se uma linha do tempo matematicamente incontestável, gerando um lock-in técnico fundamentado em segurança jurídica.

## 3. Os Três Ramos Oficiais de Atuação
1. **Ramo 1: Governança de IA (`/aigovernance`)**
   - *Público:* Escritórios de Advocacia (Tech Law), DPOs, Bancos, Fintechs e plataformas SaaS.
   - *Dores:* Shadow AI, vazamento de PII, viés algorítmico, multas da ANPD e falta de explicabilidade técnica.
   - *Diferencial:* 129 Filtros de validação contínua em 5 camadas (L1 a L5) com interceptação *Commit-Bound* (milissegundos) via Controlador CPT.
2. **Ramo 2: Setor Público (`/publicsector`)**
   - *Público:* Prefeituras Municipais, Câmaras de Vereadores, Autarquias e Assessorias Contábeis/Jurídicas.
   - *Dores:* Bloqueios no CAUC/SICONFI, perda de repasses federais e convênios (Transferegov.br), e risco de inelegibilidade/improbidade do gestor público.
   - *Diferencial:* Monitoramento de 27 itens de conformidade do CAUC, auditoria de licitações na Lei 14.133 e laudo pericial para prestação de contas.
3. **Ramo 3: Risco Legislativo / RIG Tech (`/rigtech`)**
   - *Público:* Assessorias Parlamentares, Agências de Relações Públicas, Jurídico Corporativo e Associações Setoriais.
   - *Dores:* Projetos de Lei aprovados em urgência ("Leis Surpresa"), perda de prazos de consultas públicas e impacto tributário não antecipado.
   - *Diferencial:* Coleta e indexação de diários oficiais e APIs legislativas via IA (Módulo LEX), alertas em tempo real e carimbo de tempo SHA-256 (Módulo PROVA) contra apagão de dados.

## 4. Estrutura de Preços & Modelo White-Label (Fonte da Verdade)
* **Sem termos "a partir de"** nas propostas oficiais — valores cravados por plano.
* **Governança de IA:** Standard (R$ 2.900/mês + Setup R$ 7.500 isento no Prog. Fundador) | Enterprise (R$ 8.900/mês + Setup R$ 15.000).
* **Setor Público:** Pacote Dispensa de Licitação (R$ 3.900/mês + Setup R$ 9.500 = R$ 56.300/ano, respeitando o teto de R$ 59.906,02 da Lei 14.133 / Art. 75, II).
* **RIG Tech:** Plano Corporativo (R$ 3.500/mês + Setup R$ 5.900).
* **Modelo White-Label Unificado:** R$ 1.350/mês base (inclui 2 clientes ativos) + R$ 450/mês por cliente adicional, com **Setup Isento**.
* **Condições Comerciais:** 15% de desconto para pagamento anual à vista; reajuste anual pelo IPCA.

## 5. Status de Infraestrutura & Front-end Existente
* **Site Oficial em Produção:** Todo o front-end estático das páginas de marketing e estrutura visual do app já está **100% construído em `site_oficial/` e já se encontra publicado/deployado na Cloudflare**.
* **Diretriz de Engenharia:** O site público existente é a fonte visual definitiva. O trabalho de desenvolvimento foca exclusivamente na **construção do Back-end real (FastAPI/PostgreSQL), segurança e na dinamização da área logada (`site_oficial/app/`)** conectando-a aos serviços de API.
