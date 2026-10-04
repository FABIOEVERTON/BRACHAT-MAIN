# BrachaTec — Registro de Decisões Arquiteturais e de Design (ADR)

Este documento centraliza todas as decisões rígidas tomadas para a plataforma BrachaTec, garantindo que nenhum sub-agente ou desenvolvedor fuja do escopo ou perca o contexto das premissas de negócios e design estabelecidas.

## 1. Arquitetura do Sistema (Shared-Nothing)
- **Decisão:** A plataforma opera em um modelo **Shared-Nothing** (Arquitetura Desacoplada e Individualizada).
- **Justificativa:** O modelo *White-label* exige isolamento total de dados e zero latência compartilhada. Não existe pasta `/shared` para código em tempo de execução.
- **Estrutura:** Cada ramo (`gov_ai`, `gov_muni`, `rig_tech`) possui seu próprio frontend (Next.js) e backend (Python/FastAPI) com infraestruturas isoladas.

## 2. Design System & Identidade Visual (Site Oficial)
- **Referência:** Baseado no `DESIGN.md` (Integrated Biosciences), mas adaptado para o perfil SaaS de alta conversão.
- **Cores Oficiais:**
  - Background (Tinta Abissal / Rich Black): `#0a0e17`
  - Acento Principal (Bioluminescent Lime / Cyan): `#3ecfbe`
- **Tipografia:** `Inter` (Sans) e `JetBrains Mono` (Logs/Tags).
- **Estética:** Fundo escuro profundo, linhas de rede neural em WebGL (Cadeia Criptográfica SHA-256), *glassmorphism* nos cards flutuantes, sem poluição visual.

## 3. Padrão de Nomenclatura dos Produtos
Os produtos devem ser sempre referenciados como marcas registradas, utilizando o prefixo **BT**, que herda a cor exata do "B" e "T" da logo oficial (Ciano):
- **BT Gov AI**
- **BT Muni**
- **BT Rig**
*(Regra estrita: Esses nomes não devem ser traduzidos para Inglês ou Espanhol).*

## 4. Diferenciais de Venda (Copywriting Exigido)
Sempre que um produto for descrito, o seu "Killer Feature" deve estar explícito:
- **BT Gov AI:** Foco na atuação em **Runtime** (interceptação e bloqueio no milissegundo da decisão do algoritmo) e não apenas mapeamento passivo.
- **BT Muni:** Foco no monitoramento ativo do CAUC e no rastreamento de **emendas parlamentares** para garantir captação de recursos.
- **BT Rig:** Foco em dossiês instantâneos com Inteligência Artificial para antecipar impactos tributários e regulatórios.
- **O Motor Central:** SHA-256 (Cadeia probatória) e WORM (Cofre forense) hospedados na AWS sa-east-1.

## 5. UI / Navegação (Landing Page)
- **Scroll e Âncoras:** Links do menu devem rolar a página parando com uma margem de `40vh` (meio exato da tela) para focar a leitura do executivo.
- **Isolamento da Academy:** O link "Academy" é o único que não rola a página atual, direcionando imediatamente para `academy/index.html`, isolando o funil de compra de software do funil educacional.

## 6. Painel de Controle Master (NOC Global)
- **Decisão:** O Backoffice central da BrachaTec atuará como um Network Operations Center (NOC) visual, hospedado no diretório isolado `master_admin/index.html`.
- **Justificativa:** Refletir visualmente e tecnicamente a arquitetura Shared-Nothing, garantindo que o Hub monitore clusters independentes.
- **Estrutura:** Deve obrigatoriamente exibir a separação física da infraestrutura: Instâncias de Banco de Dados, Nodos Computacionais (EKS) e Cofres Glacier para cada um dos ramos (BT Gov AI, BT Muni, BT Rig) separadamente.

## 7. Gateway de Pagamento e Faturamento (Escala Global)
- **Gateway Oficial:** **Stripe** será o motor financeiro oficial da plataforma.
- **Justificativa:** Atender clientes globalmente (Dólar/Euro via cartão internacional) e clientes no Brasil (incluindo prefeituras) via PIX e Boleto nativos.
- **Emissão de Notas Fiscais (NFS-e):** Como o Stripe não gera NFS-e brasileira nativamente, a arquitetura exige a integração de um serviço auxiliar via Webhook (ex: eNotas ou Focus NFe) disparado automaticamente assim que o Stripe confirmar a liquidação (PIX, Boleto ou Cartão).

## 8. Arquitetura de Microsserviços e Nomenclatura dos 8 Produtos
- **Decisão:** A plataforma oficializa o escopo em **3 Ramos Principais**, abrigando **8 Produtos (Microsserviços) 100% independentes**. Cada um dos 8 produtos terá seu próprio servidor e próprio banco de dados isolado.
- **Justificativa:** A hiper-modularidade permite vender o pacote completo do "Ramo" no checkout, mas dá liberdade técnica e comercial para vender qualquer microsserviço isoladamente no futuro.
- **Mapeamento Oficial dos 8 Microsserviços:**

  **RAMO 1: BT Gov AI**
  1. **BTScan:** Microsserviço de mapeamento passivo e diagnóstico de Shadow AI.
  2. **BTMonitor:** Microsserviço de Controlador CPT (Runtime) para interceptação ativa e bloqueio.

  **RAMO 2: BT Muni**
  3. **BTCapta:** Microsserviço de rastreamento e captação de emendas parlamentares.
  4. **BTGestor:** Microsserviço de gestão, prestação de contas, auditoria (CAUC, SIAFI e Transferegov) e atuação corretiva. Inclui os sub-módulos **BTAssist** (Checklists e formulários), **Análise de Prestação de Contas IA** (validação cruzada de notas fiscais, extratos e medições de obras antes do envio para não reprovar convênios) e o **Gerador de Defesa (Advogado IA)** (que elabora automaticamente defesas prévias para o TCE baseadas em jurisprudência e no cofre WORM).
  5. **BTLicita:** Microsserviço de auditoria em tempo real de licitações (Lei 14.133).

  **RAMO 3: BT Rig**
  6. **BTLex:** Microsserviço de scraping massivo (Câmara, Senado, Diários Oficiais).
  7. **BTAlerta:** Microsserviço de notificações Push/Email sobre impactos tributários.
  8. **BTProva:** Microsserviço gerador de dossiês jurídicos automatizados.

- **Estrutura de Fechamento:** O cliente assina o "Ramo" (Macrosserviço) pelo Master Admin, que orquestra e libera o acesso aos microsserviços subjacentes adquiridos.

## 9. Visão de Produto: Plataforma de Resolução e Atuação 360º (Não-Notificadora)
- **Decisão:** A plataforma BrachaTec (especialmente o BT Muni e BT Rig) é estritamente proibida de atuar como um "mero notificador de problemas". O sistema é um motor de **Resolução Ativa e Prevenção 360º**.
- **Regras de Atuação (O Padrão Ouro):**
  1. **Monitoramento Preventivo (Anti-Queda):** Robôs (RPA) rodam 24/7 nos portais governamentais (SIAFI, Transferegov, CAUC) para prever o vencimento de certidões e atuar *antes* da queda da documentação, garantindo que o município nunca seja bloqueado de receber repasses.
  2. **Análise de Conformidade 360º:** Editais e contratos são ingeridos pela IA e cruzados linha por linha com a legislação vigente (ex: Lei 14.133), apontando falhas e gerando as retificações necessárias de forma automática.
  3. **Preparação Documental e Defesa (TCU/TCE):** A plataforma não apenas aponta o erro, mas utiliza a base de dados em tempo real e jurisprudência para redigir preventivamente a documentação de defesa para os órgãos de controle.
  4. **Acompanhamento de Convênios:** Rastreabilidade fim-a-fim da prestação de contas dos convênios firmados.
- **Justificativa:** O verdadeiro valor do B2B de alto ticket não é dizer ao prefeito que ele tem um problema, é dizer a ele que o problema existiu, mas o sistema já gerou o ofício de resolução e a defesa jurídica automática.

## 10. Evoluções Críticas de Escopo (Anti-Churn e Venda em Lote)
Com base em simulações de Inteligência de Enxame (MiroFish) focadas no mercado real (ex: Municípios do Maranhão), a arquitetura incorpora duas exigências inegociáveis para garantir a adoção e barrar o churn:

1. **Evolução do BTGestor para BTAssist:**
   - **O Problema:** Municípios pequenos sem equipe técnica não conseguem agir em cima de um alerta de bloqueio.
   - **A Solução (BTAssist):** Todo alerta de restrição no CAUC/SIAFI gerado pelo BTGestor deve ser acompanhado de um "Checklist Guiado", gerando automaticamente os formulários e ofícios em PDF no formato exigido pela Receita/Órgão. A plataforma passa de um monitor para um solucionador braçal.

2. **Venda em Bloco (BT GovFed - Arquitetura de Consórcio):**
   - **O Problema:** Federações (ex: FAMEM) ou Consórcios Públicos compram licenças em lote, mas os prefeitos rejeitam a adoção por medo de perderem a soberania dos dados ou darem munição (liability) para opositores políticos que comandam a Federação.
   - **A Solução (BT GovFed):** Implementação obrigatória de *Master-Tenant Architecture* com consentimento granular. A Federação paga o boleto unificado e vê apenas a "taxa de adesão" no seu dashboard (quantos municípios ativaram). Os laudos WORM, dados financeiros e de licitação (BTLicita) de cada município ficam trancados criptograficamente apenas para o CPF/CNPJ do próprio prefeito. O consentimento e a trilha de isolamento de dados são gravados via hash SHA-256 no Cofre.

## 11. BT Strategy: O Hub Profissional de Consultoria e Representação (Efeito Insidec)
- **Decisão:** Em vez de um simples botão de "SOS Jurídico", a plataforma terá um módulo oficial integrado chamado **BT Strategy** (ou Hub de Serviços Estratégicos). Ele consolida a capacidade de tecnologia da BrachaTec com o *know-how* humano de consultorias de Brasília (parceiros, advogados, contadores).
- **Escopo de Serviços (Oferecidos via Parceiros na Plataforma):**
  1. **Representação Técnica e Articulação Institucional em Brasília:** Para destravar recursos e emendas presencialmente nos ministérios.
  2. **Auditoria Administrativa, Financeira e Tributária:** Quando a plataforma (BT Muni) rastrear um rombo orçamentário crônico, ela recomenda e precifica a intervenção humana da equipe parceira.
  3. **Assessoria Profunda em Licitações e Contratos:** Para casos em que a IA diagnosticou um alto risco de TCU e o município precisa terceirizar a confecção de um edital de alta complexidade.
  4. **Cursos, Treinamentos e Palestras:** A plataforma identifica se os servidores de um município (ou DPOs de uma empresa) estão cometendo muitos erros, e aciona a venda de treinamentos especializados (Academy).
- **Mecânica Profissional:** O dashboard do cliente terá uma vitrine corporativa de "Serviços Especializados". O município solicita o orçamento, a IA empacota o diagnóstico (com hashes WORM e escopo do problema), e repassa como um "Briefing de Alto Nível" para os parceiros (advogados/consultores) da BrachaTec cotarem e assumirem a execução física/jurídica.
- **Justificativa:** Transforma a plataforma em um ecossistema definitivo ("One-Stop-Shop"). O que a tecnologia não pode assinar (por exigir OAB, CRC ou presença física em Brasília), a rede de parceiros homologados BrachaTec resolve, gerando comissionamento/receita cruzada para a plataforma com um posicionamento corporativo premium.

## 12. Regras de Atuação Dinâmica do BT Muni (Onboarding e Execução)
Para garantir o "AHA Moment" (percepção de valor imediata) e eliminar atritos processuais para a prefeitura, o Ramo 2 (BT Muni) operará com as seguintes mecânicas obrigatórias:
1. **O Choque de Realidade no Onboarding (A "Geral" de Instalação):**
   - No milésimo de segundo em que a prefeitura conecta suas credenciais (SIAFI/CAUC) na plataforma pela primeira vez, o BTGestor executa uma **Auditoria de Raio-X Inicial**.
   - Ele varre todo o passado recente e o status atual, entregando um relatório de impacto na tela: *"Você tem 3 convênios prestes a estourar o prazo no Transferegov, 2 certidões bloqueadas e R$ 400 mil em risco de devolução."* O cliente vê o valor do software no Dia 1.
2. **Auto-Preenchimento de Prestação de Contas:**
   - O módulo de prestação de contas do BTGestor não atua apenas como um validador final. Ele atua como um **"Preparador Antecipado"**.
   - O sistema puxa os metadados do Transferegov e do SIAFI, estrutura os relatórios obrigatórios e já deixa a Prestação de Contas estruturada, aguardando apenas o upload das notas/fotos e o clique de confirmação do usuário. A máquina faz o trabalho braçal da contabilidade pública.

## 13. Modelo Híbrido de Escala (Absorção do Mercado de Consultorias Tradicionais)
- **Decisão:** A plataforma BrachaTec atua como a digitalização completa de uma "Consultoria Estratégica de Brasília" (Cobrindo 100% do escopo de escritórios tradicionais, como gestão de recursos, licitações, lobby, auditoria e capacitação).
- **Mecânica de Absorção (A Divisão Inteligente):**
  A operação é dividida em duas camadas para garantir escala infinita e margem de lucro máxima:
  1. **A Camada SaaS (O Trabalho Braçal - Feito pela IA):** Tudo o que for rastreamento de emendas (BTCapta), prestação de contas, monitoramento 24/7 (SIAFI/CAUC) e leitura de editais (BTLicita) é feito por robôs. Isso permite que a BrachaTec atenda centenas de municípios simultaneamente sem inchar a folha de pagamento de consultores humanos.
  2. **A Camada BT Strategy (O Trabalho Premium - Feito por Parceiros):** Tudo o que exigir articulação física em Brasília, assinatura de advogado/contador (OAB/CRC), lobby técnico ou treinamento presencial/eventos, é diagnosticado pela IA e repassado como um *Briefing de Alto Nível* para a rede de parceiros homologados da BrachaTec.
- **Justificativa Comercial:** Consultorias físicas não escalam porque dependem de horas humanas para analisar papéis. O BT Muni analisa os papéis em segundos e só repassa aos parceiros o momento de cobrar os honorários premium. É o fim do modelo artesanal de consultoria pública.
