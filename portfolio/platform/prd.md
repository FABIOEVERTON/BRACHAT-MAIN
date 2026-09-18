# DOSSIÊ TÉCNICO E DOCUMENTAÇÃO INTEGRAL DE PRODUTO

**PROJETO:** BRACHATTECH | EZRA AI GOVERNANCE PLATFORM (EZRA ENGINE)

**CLASSIFICAÇÃO:** DOCUMENTAÇÃO EXECUTIVA & ARQUITETURA DE PRODUÇÃO

**AUTORES:** PRINCIPAL PRODUCT MANAGER (CPO) & PRINCIPAL SOFTWARE ARCHITECT

**DATA DE HOMOLOGAÇÃO:** SETEMBRO DE 2026 | VERSÃO: 2.0.8-PROD

---

### VISÃO GERAL PARA LEIGOS: O QUE É ESTE SISTEMA?

Imagine que uma empresa decida colocar um "robô inteligente" (Inteligência Artificial) para atender clientes no WhatsApp, analisar exames médicos em um hospital ou aprovar empréstimos em um banco. Se esse robô cometer um erro grave — como vazar o histórico de saúde de um paciente ou rejeitar o crédito de alguém por preconceito (viés discriminatório) —, a lei brasileira não processa o robô: **processa a empresa, seus diretores e seus advogados**.

A **EZRA PLATFORM** funciona como uma mistura de **empresa de inspeção técnica automatizada e cartório digital para Inteligência Artificial**:

1. **Ela descobre onde a empresa usa IA** (inclusive as ferramentas não autorizadas que funcionários usam escondidos no trabalho, chamadas de *Shadow AI*).
2. **Ela passa um "pente-fino" técnico de 122 itens** checando se a IA cumpre a LGPD e o futuro Marco Legal da IA (PL 2338/2023).
3. **Ela calcula um selo matemático inalterável (hash SHA-256)** que "congela" a verdade técnica daquele momento, impedindo que qualquer pessoa altere os dados depois.
4. **Com 1 único clique, ela gera um Laudo Pericial Oficial de 20 páginas em PDF**, com a marca da banca de advocacia parceira ou da própria empresa, pronto para ser apresentado a juízes, conselhos de administração ou fiscais da ANPD.

---

# PARTE 1: PRODUCT REQUIREMENTS DOCUMENT (PRD)

---

## 1.1 Contexto e Métricas de Sucesso

### Declaração do Problema

O mercado corporativo brasileiro vive o dilema da **"Paralisia por Risco"**: conselhos de administração e departamentos jurídicos estão vetando projetos legítimos de IA generativa e agentes autônomos por receio de multas milionárias da ANPD (de até R$ 50 milhões por infração), escândalos de vazamento de dados pessoais (Art. 11 e 38 da LGPD) e responsabilização civil objetiva com inversão do ônus da prova prevista no **Art. 27 do PL 2338/2023**.

As soluções internacionais existentes (OneTrust, Credo AI, watsonx) são desenhadas para leis americanas e europeias (EU AI Act, GDPR), cobradas em dólar com custos proibitivos, operam servidores fora do Brasil (violando diretrizes de soberania de dados do BACEN e ANPD) e emitem apenas relatórios gerenciais sem validade de **prova pericial forense perante o Código de Processo Civil brasileiro (Arts. 464 e seguintes do CPC)**.

### North Star Metric (Métrica Estrela-Guia)

* **Laudos Periciais Criptografados Válidos Emitidos por Mês (LPCV/mês):** Mede o volume total de laudos periciais de 20 páginas gerados com cadeia de custódia SHA-256 e selo imutável armazenado no cofre OCI. Se o cliente emite laudos, significa que a esteira completa (inventário, 122 controles e custódia) foi executada com sucesso.

### Métricas Secundárias (Ativação, Retenção e Engajamento)

1. **Taxa de Ativação Rápida (Time-to-First-Audit):** Percentual de novos tenants que cadastram seu primeiro ativo de IA e concluem a checagem dos 122 controles em menos de 48 horas após o onboarding (Meta: $\ge 80\%$).
2. **Taxa de Retenção Líquida de Receita (Net Revenue Retention - NRR):** Percentual de expansão de receita recorrente na carteira de bancas White-Label e Enterprises ano contra ano (Meta: $\ge 125\%$).
3. **Índice de Adoção do Academy (Active Certified Users):** Percentual de usuários operacionais do tenant que concluem ao menos 1 trilha formativa do Módulo 3 no primeiro mês (Meta: $\ge 70\%$, indicador direto de redução de churn).

### Escopo Negativo Explícito (O que NÃO será construído no MVP)

Para assegurar prazo, foco e excelência técnica, os seguintes itens **estão formalmente fora do escopo inicial**:

1. **NÃO haverá Fine-Tuning de LLMs dentro da plataforma:** A plataforma audita e governa modelos; ela não atua como ambiente de treinamento ou ajuste fino de pesos de redes neurais.
2. **NÃO haverá desenvolvimento de agentes conversacionais genéricos para o usuário final:** O sistema não é uma ferramenta de chat/atendimento ao cliente; é uma infraestrutura de governança e auditoria regulatória.
3. **NÃO haverá gateway próprio de pagamentos:** O faturamento em BRL utilizará APIs consolidadas de mercado (Stripe / Pagar.me) com webhooks resilientes.
4. **NÃO haverá suporte a ambientes locais (On-Premises) no MVP:** A entrega será 100% Cloud SaaS multi-tenant hospedada na região soberana da Oracle Cloud Infrastructure (OCI Valinhos/São Paulo).
5. **NÃO haverá aplicativo móvel nativo (iOS/Android):** Toda a operação pericial e de auditoria é focada em ambiente desktop/web responsivo devido à densidade de dados e leitura de documentos periciais.
6. **NÃO haverá tradução manual de código legado:** Scanners de código inspecionarão prompts, bibliotecas e guardrails via AST (Abstract Syntax Tree) e regex; não reescreverão código do cliente.

---

## 1.1.1 Trigger Map (WDS Saga)

*Contribuição: Pepper Potts (Business Analyst, Fase 1). Âncora psicologia do usuário → objetivo de negócio para cada métrica do PRD.*

| Trigger Psicológico (Persona) | Dor / Desejo | Âncora de Negócio | Mecânica de Ativação na Plataforma |
| --- | --- | --- | --- |
| Dr. Marcelo (Sócio de Banca) — responsabilização objetiva Art. 27 PL 2338 | Medo de ser processado por IA não governada + desejo de nova fonte de receita em Direito Digital | Monetização White-Label (NRR ≥ 125%, upsell White-Label Pro) | Laudo pericial com marca própria e selo SHA-256 como produto vendável |
| Dra. Camila (DPO/Consultor GRC) — trabalho braçal no RIPD | Dor operacional do inventário manual + cegueira sobre Shadow AI | Ativação Rápida (Time-to-First-Audit ≥ 80% em 48h) | Varredura automática de Shadow AI + 122 controles estruturados |
| Eng. Rodrigo (Tech Lead/MLOps) — agentes em produção | Risco de guardrails furados e vazamento de PII por agentes autônomos | Retenção técnica (gate MCP de menor privilégio + prova de due diligence) | Console MCP com deny-by-default e Human-in-the-Loop |
| Dra. Fátima (Perita/Juiz) — validade probatória | Necessidade de prova pericial válida perante o CPC (Arts. 464+) | North Star: Laudos Periciais Válidos/mês (LPCV) | QR Code público de verificação + hash congelado no cofre OCI |

---

## 1.2 Personas e Matriz RBAC (Role-Based Access Control)

### Personas Operacionais e Administrativas

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   MAPA DE PERSONAS DO SISTEMA                                   │
├──────────────────────────────┬──────────────────────────────┬────────────────────────────────────┤
│ PERSONA                      │ PAPEL PRIMÁRIO               │ MOTIVAÇÃO CENTRAL                  │
├──────────────────────────────┼──────────────────────────────┼────────────────────────────────────┤
│ 1. Sócio de Banca (Decisor)  │ Administrador do Tenant      │ Monetizar novos honorários em      │
│    "Dr. Marcelo"             │ (White-Label Owner)          │ Direito Digital com marca própria. │
├──────────────────────────────┼──────────────────────────────┼────────────────────────────────────┤
│ 2. DPO / Consultor GRC       │ Auditor Técnico / Operador   │ Eliminar trabalho braçal no RIPD   │
│    "Dra. Camila"             │ de Conformidade              │ e mapear Shadow AI sem atrito.     │
├──────────────────────────────┼──────────────────────────────┼────────────────────────────────────┤
│ 3. Tech Lead / MLOps         │ Engenheiro Responsável pelo  │ Garantir que os agentes em produção│
│    "Eng. Rodrigo"            │ Ativo de IA                  │ não furem guardrails nem vazem PII.│
├──────────────────────────────┼──────────────────────────────┼────────────────────────────────────┤
│ 4. Auditor Externo / Juiz    │ Visualizador Temporário de   │ Verificar a autenticidade e a      │
│    "Dra. Fátima (Perita)"    │ Evidências (Viewer)          │ cadeia de custódia do laudo pericial│
└──────────────────────────────┴──────────────────────────────┴────────────────────────────────────┘

```

### Matriz Tabular de Permissões RBAC

| Funcionalidade / Ação Crítica | Super Admin (Brachattech) | Tenant Admin (Sócio da Banca) | Lead Auditor (DPO / Especialista) | Tech Contributor (Dev / TI) | Auditor Externo / Viewer |
| --- | --- | --- | --- | --- | --- |
| **Criar / Suspender Tenants** | **TOTAL** | NEGADO | NEGADO | NEGADO | NEGADO |
| **Configurar White-Label (Logo/Cores/DNS)** | LEITURA | **TOTAL** | NEGADO | NEGADO | NEGADO |
| **Gerenciar Usuários e Convites da Equipe** | NEGADO | **TOTAL** | LEITURA | NEGADO | NEGADO |
| **Cadastrar Ativo de IA / Repositório / RAG** | LEITURA | **TOTAL** | **TOTAL** | **TOTAL** | LEITURA |
| **Preencher Questionário dos 122 Controles** | LEITURA | **TOTAL** | **TOTAL** | EDIÇÃO PARCIAL | LEITURA |
| **Executar Testes de Viés e Injeção de Prompt** | NEGADO | **TOTAL** | **TOTAL** | **TOTAL** | LEITURA |
| **Disparar Compilação do Laudo Pericial** | NEGADO | **TOTAL** | **TOTAL** | NEGADO | NEGADO |
| **Assinar Digitalmente o Laudo (RT)** | **TOTAL** | **TOTAL** | NEGADO | NEGADO | NEGADO |
| **Consultar Manifestos Criptográficos SHA-256** | LEITURA | LEITURA | LEITURA | LEITURA | LEITURA |
| **Acessar Módulo Academy e Emitir Badges** | LEITURA | **TOTAL** | **TOTAL** | **TOTAL** | NEGADO |
| **Alterar Plano e Dados de Cobrança (Billing)** | LEITURA | **TOTAL** | NEGADO | NEGADO | NEGADO |

---

## 1.3 Épicos e Histórias de Usuário do MVP

---

### ÉPICO 1: Autenticação, Multi-tenancy e Configuração White-Label

#### História de Usuário 1.1: Provisionamento de Tenant Isolado

> **Como** Sócio de uma Banca de Advocacia Digital,
> **Quero** cadastrar minha banca na plataforma e configurar meu subdomínio corporativo próprio,
> **Para** fornecer aos meus clientes uma experiência exclusiva sob a minha marca, garantindo segregação total de dados.

* **Critérios de Aceite (BDD/Gherkin):**
* **Cenário 1: Provisionamento bem-sucedido com subdomínio**
* **Dado que** sou um novo cliente aprovado e insiro a razão social, CNPJ e o slug desejado `paolaavila`,
* **Quando** o sistema processa a requisição de criação,
* **Então** deve criar o registro na tabela `Tenants`, configurar a política de Row-Level Security no PostgreSQL, provisionar o roteamento para `paolaavila.ezragov.com.br` e disparar o e-mail de ativação de MFA.


* **Cenário 2: Tentativa de slug duplicado**
* **Dado que** o slug `paolaavila` já existe na base de dados,
* **Quando** outro usuário tenta registrar o mesmo identificador,
* **Então** o sistema deve retornar erro HTTP 409 (Conflict) informando que o endereço já está em uso e sugerir alternativas.




* **Casos de Borda e Tratamento de Falhas:**
* *Falha na propagação do DNS/SSL:* O sistema deve manter o tenant acessível via identificador único de fallback (`app.ezragov.com.br/tenant_id`) enquanto a emissão automática do certificado Let's Encrypt para o domínio personalizado é concluída em segundo plano com até 3 tentativas com backoff exponencial.



---

### ÉPICO 2: Ingestão de Ativos de IA e Varredura dos 122 Controles AGCP

#### História de Usuário 2.1: Diagnóstico de Risco e Enquadramento no PL 2338/2023

> **Como** DPO ou Auditor de Governança de IA,
> **Quero** cadastrar um pipeline de IA (LLM, base vetorial e prompts de sistema) e submetê-lo aos 122 controles do AGCP v2.0.8,
> **Para** saber exatamente se o sistema possui práticas vedadas (Art. 13) ou se enquadra em Alto Risco (Art. 17).

* **Critérios de Aceite (BDD/Gherkin):**
* **Cenário 1: Identificação de Sistema de Alto Risco**
* **Dado que** cadastro um sistema cuja finalidade declarada é "Análise de Perfil de Crédito para Concessão de Financiamento",
* **Quando** o motor de regras cruza os dados com o Art. 17, inciso II do PL 2338/2023,
* **Então** o sistema deve classificar compulsoriamente o ativo como **ALTO RISCO**, ativar o checklist rigoroso dos níveis L1 a L4 e bloquear a emissão de laudo positivo até que todos os testes de viés (Art. 19) e supervisão humana (Art. 21) sejam comprovados.


* **Cenário 2: Detecção de Prática Vedada (Veto Absoluto)**
* **Dado que** o questionário aponta o uso de pontuação social (*social scoring*) para restrição de acesso a serviços públicos,
* **Quando** o motor de compliance avalia a regra de negócio,
* **Então** o sistema deve emitir alerta vermelho impeditivo baseado no Art. 13 do PL 2338/2023 e no Art. 5º do EU AI Act, travando a emissão de laudo de conformidade e gerando notificação de risco legal imediato.




* **Casos de Borda e Tratamento de Falhas:**
* *Upload de arquivos de configuração corrompidos ou maliciosos:* Se o usuário fizer upload de arquivos YAML/JSON contendo scripts injetados ou formatação inválida, o parser deve isolar o arquivo em sandbox segura, rejeitar o processamento com HTTP 422 (Unprocessable Entity) e registrar o evento na trilha de auditoria.



---

### ÉPICO 3: Cadeia de Custódia Criptográfica SHA-256 e Emissão do Laudo 1-Clique

#### História de Usuário 3.1: Compilação Pericial e Registro Imutável

> **Como** Auditor Técnico ou Sócio da Banca,
> **Quero** clicar em "Compilar Laudo Pericial" e gerar o documento oficial de 20 páginas em PDF com selo SHA-256,
> **Para** entregar ao cliente uma prova técnica pronta para instruir processos judiciais (Arts. 464+ do CPC) e blindar a diretoria contra o Art. 27 do PL 2338/2023.

* **Critérios de Aceite (BDD/Gherkin):**
* **Cenário 1: Emissão de Laudo com Hash Válido em menos de 10 segundos**
* **Dado que** todas as checagens mínimas dos 122 controles foram preenchidas e salvas,
* **Quando** clico em "Compilar Laudo Pericial",
* **Então** o motor ReportLab deve compilar o PDF de 20 páginas personalizado com as cores e logotipo da banca parceira, calcular o hash SHA-256 de todas as evidências, gerar o `validation_manifest.json`, gravar o arquivo no cofre WORM da OCI e disponibilizar o download em menos de 10 segundos.


* **Cenário 2: Verificação de Integridade Pública via QR Code**
* **Dado que** qualquer pessoa (ex.: juiz ou auditor externo) aponta a câmera do celular para o QR Code impresso no laudo,
* **Quando** a página pública de validação for carregada,
* **Então** ela deve exibir a confirmação de autenticidade, o carimbo de tempo indelével, os dados da banca emissora e o hash correspondente congelado na OCI.




* **Casos de Borda e Tratamento de Falhas:**
* *Queda momentânea de rede durante o upload para o Object Storage:* Se o envio do laudo assinado falhar, o worker Celery deve realizar até 5 tentativas automáticas utilizando chave de idempotência para evitar duplicidade de registros financeiros ou periciais.



---

### ÉPICO 4: Governança de Runtime e Agentes via Model Context Protocol (MCP)

#### História de Usuário 4.1: Barramento de Ferramentas com Menor Privilégio

> **Como** Tech Lead de Sistemas Agênticos,
> **Quero** configurar as permissões das ferramentas (*tools*) dos meus agentes de IA através do console da EZRA,
> **Para** impedir que um agente autônomo execute ações destrutivas ou acesse dados bancários sem autorização humana expressa.

* **Critérios de Aceite (BDD/Gherkin):**
* **Cenário 1: Bloqueio de ação financeira sem Human-in-the-Loop**
* **Dado que** o agente tenta acionar uma ferramenta do tipo `execute_wire_transfer` com valor superior a R$ 5.000,00,
* **Quando** a chamada passa pelo gateway MCP auditado pela EZRA,
* **Então** o sistema deve reter a execução, disparar uma notificação de aprovação obrigatória para o gestor humano e registrar a tentativa no Decision Ledger.


* **Cenário 2: Negação por padrão (deny-by-default) em barramento de ferramentas**
* **Dado que** um agente tenta acionar uma ferramenta não registrada no ACL de permissões do tenant,
* **Quando** a chamada passa pelo gateway MCP auditado pela EZRA,
* **Então** o sistema deve negar a execução por padrão, classificar o evento como `UNKNOWN_TOOL`, registrar no Decision Ledger e notificar o administrador com sugestão de criação de permissão explícita.


* **Cenário 3: Trilha de auditoria indelével de chamadas MCP**
* **Dado que** qualquer ferramenta é acionada por um agente autônomo,
* **Quando** o gateway MCP encerra a chamada,
* **Então** o sistema deve gravar no `Audit_Logs` o agente autor, o nome da ferramenta, o resultado (APROVADO / NEGADO / RETIDO) e o hash SHA-256 do payload, com retenção indelével conforme a política do cofre WORM.





---

### ÉPICO 5: Faturamento Recorrente e Gestão de Cotas

#### História de Usuário 5.1: Bloqueio Suave por Excesso de Ativos

> **Como** Administrador da Plataforma (Super Admin),
> **Quero** que os limites do plano contratado pelo tenant (ex.: 3 clientes ativos no Professional vs. 10 no White-Label Pro) sejam fiscalizados automaticamente,
> **Para** assegurar a correta monetização do software sem interrupções abruptas nos serviços essenciais.

* **Critérios de Aceite (BDD/Gherkin):**
* **Cenário 1: Atingimento da cota máxima do plano**
* **Dado que** uma banca no plano Professional atinge 3 projetos ativos simultâneos,
* **Quando** o usuário tenta criar o 4º projeto,
* **Então** a plataforma deve bloquear a criação, exibir uma modal explicativa de upgrade com cálculo proporcional (*prorata*) para o plano White-Label Pro e manter todos os laudos já gerados perfeitamente acessíveis.


* **Cenário 2: Período de tolerância (grace period) sem interrupção de serviço**
* **Dado que** um tenant ultrapassa a cota do plano atual,
* **Quando** o limite é excedido,
* **Então** o sistema deve manter os serviços essenciais (consulta de laudos e validação pública por QR Code) ativos por 7 dias corridos, exibindo banner de upgrade e bloqueando apenas a criação de novos ativos de IA.


* **Cenário 3: Upgrade pro-rata com retenção integral de evidências**
* **Dado que** um tenant do plano Professional conclui o upgrade para White-Label Pro,
* **Quando** a transação de faturamento é confirmada via webhook (Stripe / Pagar.me),
* **Então** o sistema deve recalculcular o valor proporcional (*prorata*) do ciclo vigente, liberar imediatamente a nova cota e manter todos os laudos e manifestos criptográficos anteriores acessíveis sem qualquer recompilação ou quebra de cadeia de custódia.





---

## 1.4 Open Questions, Gate Strategy e Assunções Críticas

*Contribuição: Maria Hill (PM) + Hawkeye (preview de Test Architecture). Resolve a punch list da validação de PRD.*

### Open Questions (dono + deadline)

| # | Pergunta em Aberto | Dono | Deadline | Impacto |
| --- | --- | --- | --- | --- |
| OQ-1 | Sanção e calendário de regulamentação do PL 2338/2023 (Art. 27) | CPO | 2026-10-15 | Enquadramento de responsabilidade (bloqueia mensagens de marketing pericial) |
| OQ-2 | Paridade de preço BRL vs OneTrust/Credo AI para posicionamento comercial | CPO / Sales | 2026-10-01 | Precificação dos planos Professional e White-Label Pro |
| OQ-3 | Aceite da ANPD sobre o padrão de laudo pericial e cadeia de custódia adotado | Jurídico | 2026-11-01 | Validade probatória formal do laudo |
| OQ-4 | Disponibilidade de instância dedicada OCI em Valinhos/SP para planos Enterprise | Infra | 2026-10-20 | Escopo do Tier Enterprise (Schema-per-tenant) |

### Gate Strategy (preview Hawkeye)

* **Modo Advisory** durante a execução: os 122 controles são preenchíveis com gaps não resolvidos, exibindo avisos por nível (L1–L4).
* **Modo Enforcing** na compilação do laudo: ativos classificados como **ALTO RISCO** (Art. 17) **não** permitem status `CERTIFIED` nem emissão de laudo positivo enquanto os controles obrigatórios (viés Art. 19, supervisão humana Art. 21) estiverem pendentes. A regra é aplicada no motor de compliance, não apenas na UI.

### Assunções Críticas com Plano de Verificação

| # | Assunção | Risco se Errada | Plano de Verificação | Dono | Prazo |
| --- | --- | --- | --- | --- | --- |
| A-1 | Disposição a pagar por laudo pericial (entrada R$ 1.890/mês) | >30% do escopo monetário inviabilizado | Beta pago com 20 bancas no primeiro trimestre; análise de conversão e churn | CPO | 2026-10-30 |
| A-2 | Adequação de latência e soberania da OCI Valinhos/SP | Violação de SLO p95 < 200 ms ou requisito de soberania | Spike técnico de 2 semanas com benchmark de latência e teste de resiliência | Infra / Tony | 2026-10-10 |
| A-3 | Viabilidade do Time-to-First-Audit < 48h para 122 controles | North Star dependente de ativação rápida | Piloto com 3 clientes; medição de tempo por etapa do questionário | PM (Maria Hill) | 2026-11-15 |

---

# PARTE 2: SYSTEM DESIGN & ARCHITECTURE DOCUMENT

---

## 2.1 Modelo Multi-tenancy e Isolamento de Dados

### Estratégia Adotada: Shared Database com Row-Level Security (RLS) Nativo

Para equilibrar **custo de infraestrutura, eficiência operacional e rigor de compliance**, a EZRA adota a estratégia de **Banco de Dados Compartilhado com Isolamento Estrito por Linha via PostgreSQL Row-Level Security (RLS)**, complementada por esquemas lógicos dedicados para dados altamente volumosos.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                    ISOLAMENTO DE DADOS MULTI-TENANT COM POSTGRESQL RLS                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ REQUISIÇÃO HTTP -> [Subdomain: banca-alfa.ezragov.com.br]                              │
│         │                                                                              │
│         ▼                                                                              │
│ [FastAPI Middleware] Extrai tenant_id do JWT validado e abre conexão com o Pool        │
│         │                                                                              │
│         ▼                                                                              │
│ [SQL Execution] SET LOCAL app.current_tenant_id = '018f23a1-b829-7921-9981-b2c3d4e5f6';│
│         │                                                                              │
│         ▼                                                                              │
│ [PostgreSQL Engine] Avalia a política RLS antes de retornar qualquer dado:             │
│         POLICY: USING (tenant_id = current_setting('app.current_tenant_id')::uuid)     │
│         │                                                                              │
│         ├── Acesso a dados do próprio tenant ........................ [AUTORIZADO]     │
│         └── Tentativa de leitura de outro tenant .................... [0 ROWS RETURNED]│
└────────────────────────────────────────────────────────────────────────────────────────┘

```

### Análise de Trade-Off Arquitetural

| Estratégia Avaliada | Custo de Nuvem | Complexidade Operacional | Risco de Vazamento | Decisão & Racional Técnico |
| --- | --- | --- | --- | --- |
| **Database-per-tenant** | Altíssimo | Crítica (centenas de migrações e pools) | Baixíssimo | **Descartada no MVP:** Inviabiliza economicamente os planos de entrada (R$ 1.890/mês). |
| **Schema-per-tenant** | Médio | Alta (DDL migrations complexas via Alembic) | Baixo | **Reservada para Tier 3:** Apenas para instâncias dedicadas de órgãos de governo ou bancos. |
| **Shared DB com RLS** *(Adotada)* | **Otimizado** | **Controlada (1 único banco gerenciado)** | **Quase Nulo com RLS** | **Aprovada:** O PostgreSQL aplica o isolamento no nível do kernel do banco de dados, prevenindo falhas no código Python. |

### Mecanismo de Prevenção contra Vazamento de Dados (Data Leakage Mitigation)

1. **Ativação Obrigatória de RLS em 100% das Tabelas de Negócio:** Nenhuma tabela corporativa é criada sem `ALTER TABLE nome_tabela ENABLE ROW LEVEL SECURITY;` e `FORCE ROW LEVEL SECURITY`.
2. **Defesa em Profundidade no Backend:** Todas as consultas no SQLAlchemy incluem explicitamente o filtro `WHERE tenant_id = :tenant_id`, atuando como segunda barreira caso o RLS seja contornado por um superusuário acidental.
3. **Impossibilidade de Execução Sem Contexto:** O middleware assíncrono do FastAPI intercepta toda requisição; se o cabeçalho de autenticação não contiver um `tenant_id` criptograficamente assinado pela chave privada da plataforma, a requisição é rejeitada com HTTP 401 antes de tocar no banco de dados.

---

## 2.2 Arquitetura de Alto Nível e Componentes

### Topologia do Sistema em Camadas

```
                                  [USUÁRIO / ADVOGADO / AUDITOR]
                                                │
                                                ▼ HTTPS / WSS (TLS 1.3)
                       ┌─────────────────────────────────────────────────┐
                       │  OCI API GATEWAY / CLOUD FLARE ENTERPRISE EDGE  │
                       │  • Terminação TLS 1.3 & Proteção Anti-DDoS      │
                       │  • Validação WAF (OWASP Top 10 API & LLM Rules) │
                       │  • Roteamento Dinâmico de Subdomínio CNAME      │
                       └────────────────────────┬────────────────────────┘
                                                │
                                                ▼ HTTP / REST & SSE
                       ┌─────────────────────────────────────────────────┐
                       │    CAMADA DE APLICAÇÃO FASTAPI (PYTHON 3.12)    │
                       │  • Middleware de Tenant & Extração de Sessão    │
                       │  • Validação Estrita de Schemas via Pydantic v2 │
                       │  • Rate Limiting Distribuído (Redis Token Bucket)│
                       └────────┬───────────────┼────────────────────────┘
                                │               │
                Leituras Rápidas│               │ Tarefas Pesadas (PDF / Varreduras)
                & Transações DB │               ▼
                                │      ┌─────────────────────────────────┐
                                │      │   REDIS CLUSTER 7.2 (BROKER)    │
                                │      │   • Filas de Mensageria Celery  │
                                │      │   • Cache de Permissões RBAC    │
                                │      └────────────────┬────────────────┘
                                │                       │
                                │                       ▼
                                │      ┌─────────────────────────────────┐
                                │      │   CELERY ASYNC WORKER POOL      │
                                │      │   • Worker 1: Discovery & Redes │
                                │      │   • Worker 2: ReportLab Engine  │
                                │      │   • Worker 3: Hasher SHA-256    │
                                │      └────────────────┬────────────────┘
                                │                       │
                                ▼                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  CAMADA DE DADOS E CUSTÓDIA SOBERANA (OCI)             │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────┐  │
│  │ POSTGRESQL 16 ENTERPRISE (OCI)  │  │ OCI OBJECT STORAGE (SPO)    │  │
│  │ • Políticas RLS Ativas          │  │ • Cofre de Imutabilidade    │  │
│  │ • Replicação Streaming Síncrona │  │   (WORM Lock por 5 anos)    │  │
│  │ • Extensão pgvector             │  │ • Armazenamento de PDFs e   │  │
│  │ • Índices B-Tree & GIN          │  │   manifestos assinados      │  │
│  └─────────────────────────────────┘  └─────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘

```

### Fluxo Detalhado da Requisição Principal: Compilação do Laudo Pericial

```
USUÁRIO            FASTAPI GATEWAY            WORKER (CELERY)       POSTGRESQL (RLS)       OCI OBJECT STORAGE
   │                      │                          │                     │                       │
   │── [POST] /compile ──>│                          │                     │                       │
   │                      │── Valida Cota & Token ──>│                     │                       │
   │                      │── Dispara Job Assíncrono>│                     │                       │
   │<── HTTP 202 Accepted │   (com Task ID único)    │                     │                       │
   │                      │                          │── Lê 122 Controles─>│                       │
   │                      │                          │<── Retorna Evidências                       │
   │                      │                          │                                             │
   │                      │                          │── Calcula Hashes SHA-256 de Prompts/Regras  │
   │                      │                          │── Gera validation_manifest.json             │
   │                      │                          │── Compila PDF 20 págs (ReportLab)           │
   │                      │                          │                                             │
   │                      │                          │────── Grava Manifesto & PDF no Cofre ──────>│
   │                      │                          │<───── Confirmação de Imutabilidade (ETag) ──│
   │                      │                          │                                             │
   │                      │                          │── Atualiza Status da Auditoria como CONCLUÍDO
   │                      │                          │   com URL de Download e Hash Master ───────>│
   │                      │                          │                                             │
   │<── [SSE/Poll] Status: CONCLUÍDO ────────────────│                                             │
   │    com Hash SHA-256 e Link Oficial              │                                             │

```

---

## 2.3 Modelo de Dados (ERD Tabular e Relacionamentos)

### 1. Tabela: `Tenants`

Armazena as organizações contratantes (bancas de advocacia, consultorias e empresas).

| Coluna | Tipo de Dado | Restrições / Chaves | Descrição e Regra de Negócio |
| --- | --- | --- | --- |
| `id` | `UUID` | `PRIMARY KEY` (v7 sequencial) | Identificador global único da organização. |
| `slug` | `VARCHAR(64)` | `UNIQUE, NOT NULL` | Identificador de URL para subdomínio (ex: `paolaavila`). |
| `legal_name` | `VARCHAR(255)` | `NOT NULL` | Razão Social completa da pessoa jurídica. |
| `trade_name` | `VARCHAR(255)` | `NOT NULL` | Nome Fantasia exibido na interface e nos laudos. |
| `cnpj` | `VARCHAR(18)` | `UNIQUE, NOT NULL` | CNPJ com validação de dígitos verificadores. |
| `white_label_config` | `JSONB` | `NOT NULL, DEFAULT '{}'` | Armazena: `{logo_url, primary_hex, custom_domain}`. |
| `status` | `VARCHAR(32)` | `NOT NULL, DEFAULT 'ACTIVE'` | Status operacional: `TRIAL`, `ACTIVE`, `SUSPENDED`. |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT clock_timestamp()` | Data e hora com fuso horário da criação do registro. |

*Índices Recomendados:* `CREATE UNIQUE INDEX idx_tenants_slug ON Tenants(slug);` | `CREATE INDEX idx_tenants_status ON Tenants(status);`

---

### 2. Tabela: `Users`

Registra os operadores e administradores vinculados a cada tenant.

| Coluna | Tipo de Dado | Restrições / Chaves | Descrição e Regra de Negócio |
| --- | --- | --- | --- |
| `id` | `UUID` | `PRIMARY KEY` | Identificador único do usuário. |
| `tenant_id` | `UUID` | `FOREIGN KEY (Tenants.id), NOT NULL` | Tenant ao qual o usuário pertence (Filtro do RLS). |
| `email` | `VARCHAR(255)` | `NOT NULL` | E-mail corporativo (único por tenant). |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` | Hash seguro gerado via Argon2id (custo calibrado). |
| `full_name` | `VARCHAR(128)` | `NOT NULL` | Nome completo do profissional. |
| `role` | `VARCHAR(32)` | `NOT NULL` | Papel RBAC: `TENANT_ADMIN`, `AUDITOR`, `TECH`, `VIEWER`. |
| `mfa_secret` | `VARCHAR(128)` | `NULLABLE` | Chave secreta criptografada para autenticação TOTP. |
| `is_active` | `BOOLEAN` | `NOT NULL, DEFAULT TRUE` | Controle de bloqueio de acesso individual. |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT clock_timestamp()` | Data de criação do usuário. |

*Índices Recomendados:* `CREATE UNIQUE INDEX idx_users_tenant_email ON Users(tenant_id, email);`

---

### 3. Tabela: `AI_Assets`

Cataloga os sistemas inteligentes, LLMs e pipelines auditados pelo tenant.

| Coluna | Tipo de Dado | Restrições / Chaves | Descrição e Regra de Negócio |
| --- | --- | --- | --- |
| `id` | `UUID` | `PRIMARY KEY` | Identificador único do sistema de IA. |
| `tenant_id` | `UUID` | `FOREIGN KEY (Tenants.id), NOT NULL` | Tenant proprietário do ativo. |
| `name` | `VARCHAR(128)` | `NOT NULL` | Nome comercial do ativo (ex.: `Chatbot Atendimento v2`). |
| `asset_type` | `VARCHAR(64)` | `NOT NULL` | `LLM_PROMPT`, `RAG_PIPELINE`, `AUTONOMOUS_AGENT`. |
| `model_provider` | `VARCHAR(64)` | `NOT NULL` | Provedor base: `OPENAI`, `ANTHROPIC`, `OCI_GENAI`, `LOCAL`. |
| `risk_level_pl2338` | `VARCHAR(32)` | `NOT NULL` | Classificação: `EXCESSIVO`, `ALTO_RISCO`, `LIMITADO`, `BAIXO`. |
| `has_sensitive_data` | `BOOLEAN` | `NOT NULL, DEFAULT FALSE` | Indica tráfego de dados do Art. 11 da LGPD (Saúde/Biometria). |
| `is_shadow_ai` | `BOOLEAN` | `NOT NULL, DEFAULT FALSE` | Flag de ativo detectado sem aprovação prévia da TI. |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT clock_timestamp()` | Data de catalogação. |

*Índices Recomendados:* `CREATE INDEX idx_ai_assets_tenant_risk ON AI_Assets(tenant_id, risk_level_pl2338);`

---

### 4. Tabela: `Compliance_Assessments`

Armazena a avaliação formal dos 122 controles do AGCP v2.0.8 para um ativo.

| Coluna | Tipo de Dado | Restrições / Chaves | Descrição e Regra de Negócio |
| --- | --- | --- | --- |
| `id` | `UUID` | `PRIMARY KEY` | Identificador único da auditoria. |
| `tenant_id` | `UUID` | `FOREIGN KEY (Tenants.id), NOT NULL` | Isolamento multi-tenant. |
| `asset_id` | `UUID` | `FOREIGN KEY (AI_Assets.id), NOT NULL` | Ativo auditado. |
| `agcp_score` | `NUMERIC(5,2)` | `NOT NULL` | Pontuação final calculada de 0.00 a 100.00. |
| `controls_payload` | `JSONB` | `NOT NULL` | Respostas individuais dos 122 controles (L1 a L4). |
| `gaps_critical` | `INTEGER` | `NOT NULL, DEFAULT 0` | Quantidade de não-conformidades de alto risco. |
| `status` | `VARCHAR(32)` | `NOT NULL` | `IN_PROGRESS`, `SUBMITTED`, `CERTIFIED`, `REJECTED`. |
| `evaluated_by` | `UUID` | `FOREIGN KEY (Users.id), NOT NULL` | Usuário auditor responsável técnico. |
| `updated_at` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT clock_timestamp()` | Última modificação. |

*Índices Recomendados:* `CREATE INDEX idx_assessments_asset ON Compliance_Assessments(tenant_id, asset_id);`

---

### 5. Tabela: `Forensic_Manifests`

Garante a integridade probatória e o carimbo imutável SHA-256 do Laudo Pericial.

| Coluna | Tipo de Dado | Restrições / Chaves | Descrição e Regra de Negócio |
| --- | --- | --- | --- |
| `id` | `UUID` | `PRIMARY KEY` | Identificador do protocolo pericial. |
| `tenant_id` | `UUID` | `FOREIGN KEY (Tenants.id), NOT NULL` | Isolamento multi-tenant. |
| `assessment_id` | `UUID` | `FOREIGN KEY (Compliance_Assessments.id)` | Avaliação vinculada ao laudo. |
| `protocol_code` | `VARCHAR(64)` | `UNIQUE, NOT NULL` | Código amigável (ex: `EZRA-2026-BR-0917-8841`). |
| `master_hash_sha256` | `CHAR(64)` | `NOT NULL` | Hash SHA-256 do `validation_manifest.json`. |
| `pdf_storage_url` | `TEXT` | `NOT NULL` | Caminho seguro no bucket WORM da OCI. |
| `manifest_json` | `JSONB` | `NOT NULL` | Conteúdo integral de todos os hashes de evidências. |
| `sealed_at` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT clock_timestamp()` | Carimbo oficial de congelamento temporal da evidência. |

*Índices Recomendados:* `CREATE UNIQUE INDEX idx_manifests_protocol ON Forensic_Manifests(protocol_code);` | `CREATE INDEX idx_manifests_hash ON Forensic_Manifests(master_hash_sha256);`

---

### 6. Tabela: `Audit_Logs`

Trilha de auditoria indelével de todas as ações de segurança e administrativas da plataforma.

| Coluna | Tipo de Dado | Restrições / Chaves | Descrição e Regra de Negócio |
| --- | --- | --- | --- |
| `id` | `BIGSERIAL` | `PRIMARY KEY` | Identificador sequencial. |
| `tenant_id` | `UUID` | `NOT NULL` | Tenant onde ocorreu o evento. |
| `user_id` | `UUID` | `NULLABLE` | Usuário autor da ação (ou `SYSTEM`). |
| `action` | `VARCHAR(64)` | `NOT NULL` | Ex.: `USER_LOGIN`, `COMPILE_REPORT`, `UPDATE_POLICY`. |
| `ip_address` | `INET` | `NOT NULL` | Endereço IP de origem da requisição. |
| `user_agent` | `TEXT` | `NOT NULL` | Identificação do navegador/cliente HTTP. |
| `payload_hash` | `CHAR(64)` | `NOT NULL` | Checksum SHA-256 do payload enviado para prevenir fraudes. |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT clock_timestamp()` | Registro temporal exato. |

*Índices Recomendados:* `CREATE INDEX idx_audit_logs_tenant_time ON Audit_Logs(tenant_id, created_at DESC);`

---

## 2.4 Segurança, Governança e Compliance

### Modelo de Autenticação e Sessão

* **JWT Criptografado (JWE / RS256):** Autenticação *stateless* com Access Token assinado por chave assimétrica RSA-4096 (validade estrita de 15 minutos) e Refresh Token rotativo (armazenado no banco com expiração em 7 dias e invalidação por reuso).
* **MFA Compulsório (RFC 6238 TOTP):** Ativação obrigatória para todos os administradores e auditores. Sem a inserção do código de 6 dígitos, o token gerado possui escopo restrito (`mfa:pending`).
* **Suporte a SSO Corporativo (SAML 2.0 e OpenID Connect):** Disponível para clientes Enterprise, permitindo integração direta com Okta, Microsoft Entra ID (antigo Azure AD) e Google Workspace.

### Estrutura do Registro de Auditoria (Audit Trail)

Todo evento crítico gera um registro canônico em formato JSON:

```json
{
  "event_id": "8b9e0231-5f21-4d1a-8c11-9a2c3d4e5f60",
  "timestamp": "2026-09-17T15:40:12.891Z",
  "tenant_id": "018f23a1-b829-7921-9981-b2c3d4e5f67a",
  "actor": {
    "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "marcelo@paolaavila.adv.br",
    "role": "TENANT_ADMIN"
  },
  "action": "COMPILE_PERICIAL_REPORT",
  "resource": {
    "type": "AI_ASSET",
    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "name": "Pipeline CredTech v2.4"
  },
  "network": {
    "ip": "200.180.45.12",
    "country": "BR",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
  },
  "integrity": {
    "input_payload_sha256": "4f8b2c1794da87bc9e053f19e48d37492c10a48b52f9e7104d826a79e4bf0122",
    "manifest_ref": "EZRA-2026-BR-0917-8841"
  }
}

```

### Criptografia e Conformidade com a LGPD

1. **Em Repouso (At-Rest):** Dados no PostgreSQL criptografados via LUKS/AES-256 e backups automáticos criptografados com chaves gerenciadas pelo OCI Vault (KMS FIPS 140-2 Level 3).
2. **Em Trânsito (In-Transit):** Comunicação 100% blindada por TLS 1.3 com suites de cifras modernas (HSTS ativo com max-age de 1 ano e pré-carregamento).
3. **Privacidade e Descarte (LGPD):**
* **Soft Delete:** Registros marcados como deletados recebem carimbo `deleted_at` e deixam de ser listados nas consultas comuns.
* **Direito ao Esquecimento / Expurgamento:** Procedimento assíncrono executado por rotina dedicada que sobrescreve dados pessoais com hashes irreversíveis (pseudonimização irreversível) conforme autoriza o Art. 16 da LGPD para fins de cumprimento de obrigação legal.



---

## 2.5 Resiliência, Rate Limiting e Observabilidade

### Políticas de Rate Limiting (Token Bucket via Redis)

Para proteger o cluster contra abusos e ataques de negação de serviço:

* **Nível 1 (Por IP - Proteção de Borda):** Máximo de 120 requisições por minuto para endpoints públicos; 10 tentativas por minuto para rotas de autenticação (`/login`, `/mfa`).
* **Nível 2 (Por Tenant - Proteção de Cota do Plano):**
* *Plano Professional:* 60 requisições/minuto na API; máximo de 10 compilações de laudos/dia.
* *Plano White-Label Pro:* 300 requisições/minuto na API; compilações ilimitadas com fila de prioridade alta.
* *Plano Enterprise Corp:* 1.200 requisições/minuto; instâncias dedicadas de workers.



### Padrões de Resiliência

1. **Circuit Breaker (Disjuntor de Falhas):** Aplicado em todas as integrações externas (APIs de LLMs, gateways de faturamento e OCI Object Storage). Se a taxa de falhas exceder 40% em uma janela de 30 segundos, o disjuntor abre imediatamente, retornando respostas degradadas (*graceful degradation*) e evitando exaustão de conexões.
2. **Retries com Exponential Backoff e Jitter:** Chamadas assíncronas com falha são reexecutadas em $t = 2^n \times 1000\text{ ms} \pm \text{random}(100, 500\text{ ms})$, evitando o fenômeno de "rebanho enfurecido" (*thundering herd*).
3. **Dead Letter Queue (DLQ):** Mensagens que falharem após 5 tentativas consecutivas são transferidas para uma fila morta no Redis (`dlq:failed_jobs`), disparando alerta imediato para o time de suporte de engenharia.

### Métricas, Observabilidade e SLOs

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          TABELA DE SLOs DA EZRA PLATFORM                               │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ INDICADOR DE NÍVEL (SLI)   │ OBJETIVO FORMAL (SLO)       │ MÉTODO DE MEDIÇÃO           │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Disponibilidade da API     │ 99.9% de uptime mensal      │ Probes externas a cada 30s  │
│ Latência de Endpoints CRUD │ p95 < 200 ms                │ Telemetria OTel / Prometheus│
│ Compilação do Laudo PDF    │ p90 < 10 segundos           │ Duração do Job no Celery    │
│ Taxa de Erro 5xx           │ < 0.05% do tráfego total    │ Nginx Ingress / FastAPI Logs│
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘

```

* **Rastreamento Distribuído (Distributed Tracing):** Toda requisição recebe um cabeçalho canônico `X-Trace-Id` propagado desde o Next.js, passando pelo FastAPI, filas do Celery e queries do PostgreSQL, permitindo reconstruir o fluxo exato de qualquer incidente de produção em menos de 60 segundos.

---

# SÍNTESE EXECUTIVA DE ENGENHARIA & HOMOLOGAÇÃO

Este documento consolida as decisões arquiteturais da plataforma **BRACHATTECH | EZRA AI Governance Platform**. Todas as especificações técnicas detalhadas acima foram modeladas para assegurar escalabilidade horizontal, soberania de dados em solo brasileiro (OCI Valinhos/SP) e blindagem jurídica irrefutável para nossos clientes e bancas de advocacia parceiras.

---

## Validation log — 2026-09-17

**Status:** validated

**Processo:** `/wize-validate-prd` (Wize Development Kit, Fase 2 — Planejamento)

**Signatários**

- Maria Hill (PM) — concerns: resolvidas nesta revisão (ACs dos Épicos 4 e 5 complementados; Open Questions com dono/deadline; assunções críticas com plano de verificação; gate strategy registrada).
- Pepper Potts (Analyst) — concern resolvida: Trigger Map (WDS Saga) adicionada na seção 1.1.1, ancorando as 4 métricas às personas.
- Mantis (UX) — sem concerns registradas nesta validação; fase de UX inicia-se após a solução técnica.
- Nick Fury (Solution Strategy) — sem contradições com o System Design (Parte 2); NFRs confirmados.
- Hawkeye (Test Architect) — preview incluído: gate strategy advisory/enforcing explicitada; testes de viés (Art. 19) e supervisão humana (Art. 21) bloqueiam `CERTIFIED` para ALTO RISCO.

**Notas**

- OQ-1 (PL 2338/2023) e OQ-3 (aceite ANPD) são os itens com maior impacto no roadmap comercial; acompanhamento atribuído a CPO e Jurídico.
- A validação confirma o documento como `status: validated`, pronto para entrar em Solutioning (Fury → Tony).