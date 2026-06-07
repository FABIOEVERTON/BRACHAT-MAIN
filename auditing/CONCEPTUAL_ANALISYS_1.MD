BRACHÁT — Análise Conceitual do Ecossistema para Entrevistas & Certificações
Foco: conceito · propósito · arquitetura · integração · entrevista · certificação

ÍNDICE DE FERRAMENTAS E TECNOLOGIAS
FERRAMENTA 1
OpenCode (Go Runtime)
O que é
Runtime de agentes AI que executa prompts estruturados como programas, com persistência de estado, dispatch por horário, e bridges de comunicação.

Problema que resolve
LLMs isolados não mantêm estado, não seguem rotinas, não coordenam múltiplos agentes, e não se conectam a canais de comunicação reais (Telegram, WhatsApp).

Como funciona
O OpenCode lê um arquivo de configuração (opencode.json) que aponta para instruções (.opencode/instructions/memory.md). Ao iniciar, carrega contexto de state.json, executa protocolos de sessão (ler caches, verificar horário, fazer dispatch) e delega para agentes especializados conforme um schedule pré-definido.

Analogia
É como um sistema operacional para agentes: tem boot sequence (startup protocol), processos (agentes), memória (cache.json + state.json), kernel (orquestrador), e I/O (bridges Telegram/WhatsApp).

Entrada
Mensagens do usuário (via Telegram, WhatsApp, terminal)
Arquivos de configuração (AGENT.md, state.json, cache.json)
Horário atual (para dispatch)
Saída
Respostas ao usuário
Atualizações de cache (cache.json)
Materiais de estudo (summaries em writings_studies/)
Propostas, posts, lembretes
Quando usar
Automação de rotinas pessoais com múltiplos agentes coordenados
Sistemas que precisam de persistência de estado entre sessões
Orquestração de agentes com regras rígidas de governança
Quando NÃO usar
Tarefas únicas e simples (overkill)
Sistemas que precisam de latência sub-segundo (bridges adicionam overhead)
Quando não há necessidade de multi-agente
Relação com outras ferramentas
Composio MCP → conecta agentes a LinkedIn, ClickUp
Telegram API → bridge de comunicação (EZRA + Nice)
WhatsApp Baileys → bridge alternativa
Ollama → fallback de LLM local (Windows VM)
launchd → mantém bridges 24/7
Como aparece em entrevistas
"Explique como você projetaria um sistema multi-agente com coordenação."
"Como manter estado persistente entre sessões de LLM?"
"Como implementar governança em sistemas autônomos de IA?"
Resposta curta de entrevista
"Projetei um runtime multi-agente com dispatch baseado em horário, estado persistente via JSON, governança com ledger append-only, e bridges para Telegram/WhatsApp. O orquestrador central opera em temperatura zero para determinismo, delegando para agentes especializados com regras rígidas de isolamento de domínio."

O que memorizar
OpenCode = runtime Go que executa agentes via prompts estruturados
Boot sequence: date → state.json → cache.json → dispatch
Bridges: Telegram (polling direto), WhatsApp (Baileys), launchd 24/7
Estado: state.json (canônico), cache.json (por agente)
Importância para Data Engineer: 4/10
Importância para Machine Learning Engineer: 5/10
Importância para AI Engineer: 10/10
FERRAMENTA 2
Padrão Harness (Agent Architecture Pattern)
O que é
Framework arquitetural obrigatório de 5 módulos que define a estrutura de CADA agente no ecossistema BRACHÁT.

Problema que resolve
Agentes AI sem estrutura padronizada são imprevisíveis, difíceis de auditar, e impossíveis de coordenar. O Harness garante uniformidade, observabilidade e governança.

Como funciona
Todo agente DEVE implementar 5 seções:

🧠 Núcleo Central → papel, missão, modelo, temperatura
⚙️ Skills → procedimentos operacionais + heurísticas de decisão
🧩 Memória → 4 camadas (working, episodic, semantic, personal)
🔗 Protocolos → comunicação agent-agent e agent-tools
⚖️ Regulação → constraints, approval loops, observability, compression
Analogia
É como a ISO 9001 para agentes de IA: um padrão de qualidade que todo agente deve seguir, garantindo que cada um tenha papel claro, memória estruturada, comunicação definida, e controles de qualidade.

Entrada
Template de harness (shared/general_harness/harness.md)
Requisitos do domínio do agente
Saída
AGENT.md completo com os 5 módulos preenchidos
Quando usar
SEMPRE que criar um novo agente no ecossistema
Ao auditar agentes existentes (verificar completude)
Quando NÃO usar
Agentes descartáveis de uso único (não justifica o overhead)
Relação com outras ferramentas
AGCP → protocolo de governança que complementa o Harness
QILIS → sistema de qualidade que audita materiais dos agentes
AUDITORIA.md → checklist semanal que verifica conformidade Harness
Aísio → diretor que fiscaliza aderência ao Harness
Como aparece em entrevistas
"Como você estruturaria um agente de IA para produção?"
"Quais controles de governança você implementaria em sistemas multi-agente?"
"Como garantir observabilidade em agentes autônomos?"
Resposta curta de entrevista
"Uso um padrão de 5 módulos: núcleo (papel + temperatura), skills (procedimentos + heurísticas), memória (4 camadas: working, episodic, semantic, personal), protocolos (comunicação inter-agente e com ferramentas), e regulação (constraints, approval loops, observabilidade, compressão). Isso garante agentes auditáveis, previsíveis e coordenáveis."

O que memorizar
5 módulos: Núcleo, Skills, Memória, Protocolos, Regulação
Memória tem 4 camadas: Working, Episodic, Semantic, Personal
Skills = Operational Procedure + Decision Heuristics
Regulação inclui: Normative Constraints, Evaluator, Approval Loop, Observability, Compression
Importância para Data Engineer: 3/10
Importância para Machine Learning Engineer: 5/10
Importância para AI Engineer: 10/10
FERRAMENTA 3
Orquestrador (Dispatch Engine)
O que é
Agente central de coordenação que opera em temperatura zero (determinístico puro), fazendo dispatch de agentes especializados baseado no horário do dia.

Problema que resolve
Sem coordenação central, múltiplos agentes competem por atenção, executam fora de contexto, e perdem coerência com a rotina do usuário.

Como funciona
Executa date → descobre horário
Lê state.json → contexto do usuário
Lê todos cache.json → o que foi feito ontem
Consulta tabela de dispatch → qual agente ativar agora
Carrega AGENT.md do agente do horário
Reporta: "Ontem: [X]. Pendente: [Y]. Agora: [horário] → [atividade]"
Analogia
É como um controlador de tráfego aéreo: não voa os aviões (agentes), mas diz qual avião decola em qual horário, evitando colisões e garantindo a sequência correta.

Entrada
Horário atual (date)
Estado do sistema (state.json)
Histórico de cada agente (cache.json)
Tabela de dispatch (dispatch-schedule.md)
Saída
Dispatch do agente correto
Relatório de status ao usuário
Máximo 5 linhas de output
Quando usar
SEMPRE como ponto de entrada do sistema
Para coordenar rotinas com múltiplos agentes especializados
Quando NÃO usar
Tarefas ad-hoc que não seguem schedule
Quando há apenas 1 agente no sistema
Relação com outras ferramentas
Coordena todos os 12 daily agents + 4 diretores + Nice
Lê dispatch-schedule.md para saber a atividade do momento
Lê official_schedule.md para saber o tópico de estudo do dia
Aísio pode bloquear ações — o único que supera o orquestrador (além do usuário)
Como aparece em entrevistas
"Como implementar orquestração em sistemas multi-agente?"
"Qual a diferença entre orquestração e coreografia em microserviços?"
"Como garantir determinismo em um sistema de IA?"
Resposta curta de entrevista
"O orquestrador opera em temperatura zero para máximo determinismo. Ele não raciocina — apenas faz dispatch baseado em horário e estado. Cada agente tem seu domínio isolado, e a comunicação é via cache.json, nunca direta. Isso garante previsibilidade, auditabilidade e zero drift."

O que memorizar
Temperatura 0 = determinístico, sem reasoning, só dispatch
Boot: date → state.json → cache.json → dispatch-schedule
12 daily + 4 diretores + Nice = 17 agentes coordenados
Máximo 5 linhas de output, chunks de 100 tokens
Cross-domain PROIBIDO sem permissão
Importância para Data Engineer: 4/10
Importância para Machine Learning Engineer: 5/10
Importância para AI Engineer: 10/10
FERRAMENTA 4
AGCP (Agent Governance & Compliance Protocol)
O que é
Protocolo formal de governança que define hierarquia de autoridade, approval gates, regras de isolamento e escalation paths para todos os agentes.

Problema que resolve
Agentes autônomos sem governança podem tomar decisões prejudiciais: gastar dinheiro sem autorização, acessar domínios proibidos, ou executar ações irreversíveis.

Como funciona
Define uma hierarquia de 5 níveis:

Usuário (autoridade máxima)
Aísio (fiscaliza TUDO)
Orquestrador (coordena, NÃO governa)
Diretores (domínio específico)
Daily agents (execução, sem autoridade)
Toda ação passa por approval gates com thresholds definidos (financeiro >R$500, publicação sempre, cross-domain sempre).

Analogia
É como a constituição de um país: define quem tem poder sobre o quê, quais ações precisam de aprovação do "congresso" (usuário), e como resolver conflitos entre "órgãos" (agentes).

Entrada
Ações propostas por agentes
Regras definidas no AGCP
Saída
APPROVED / BLOCKED
Registro no governance-ledger.jsonl
Quando usar
Em QUALQUER sistema multi-agente que toma ações no mundo real
Quando agentes lidam com dados financeiros, pessoais ou publicações
Quando NÃO usar
Sistemas de agente único sem ações no mundo real
Prototipagem rápida (adicionar depois)
Relação com outras ferramentas
Aísio → implementa e fiscaliza o AGCP
governance-ledger.jsonl → log append-only de todas as ações
QILIS → complementa com qualidade de ensino
REGRAS.md → "constituição" base
Como aparece em entrevistas
"Como implementar governança responsável em AI Agents?"
"O que é Human-in-the-Loop e quando usar?"
"Como garantir compliance em sistemas autônomos?"
Resposta curta de entrevista
"Implementei governança com hierarquia de 5 níveis, approval gates para ações financeiras e publicações, commit-bound authorization com ledger append-only, isolamento de domínio entre agentes, e um agente auditor (Aísio) que fiscaliza conformidade a cada sessão. Human-in-the-loop é obrigatório para ações acima de thresholds financeiros e qualquer publicação."

O que memorizar
5 níveis: Usuário > Aísio > Orquestrador > Diretores > Daily
Approval gates: >R$500 (financeiro), sempre (publicação), sempre (cross-domain)
Commit-Bound Authorization: toda ação → registro no ledger
Isolamento: Nice (só doméstico), Jéssica (memória isolada), daily agents (sem cross-domain)
Importância para Data Engineer: 5/10
Importância para Machine Learning Engineer: 6/10
Importância para AI Engineer: 10/10
FERRAMENTA 5
QILIS (Quality, Intelligence & Learning Inspection System)
O que é
Sistema de inspeção de qualidade focado em ensino e aprendizado, com métricas específicas para agentes tutores e de execução.

Problema que resolve
Materiais de estudo produzidos por IA podem ser genéricos, longos demais, difíceis de memorizar, ou avançar sem confirmar aprendizado real.

Como funciona
Define métricas por tipo de agente:

Ensino: Clareza, Memorabilidade (mnemônicos), Praticidade (exemplos), Checkpoint, MVI (<200 linhas), Spaced Repetition
Execução: Conversão, Personalização, ATS compliance, Approval gates
Gilmário atua como quality gate: revisa materiais antes de persistir.

Analogia
É como o controle de qualidade numa fábrica de conteúdo educacional: cada "produto" (material de estudo) passa por inspeção antes de ser "entregue" (salvo permanentemente).

Entrada
Materiais produzidos pelos agentes tutores
Métricas de execução dos agentes produtores
Saída
PASS/FAIL por métrica
Relatório semanal QILIS (tabela: agente | material | métricas | status)
Quando usar
Em sistemas educacionais com IA
Para garantir qualidade consistente de materiais de aprendizado
Quando NÃO usar
Sistemas que não envolvem ensino/aprendizado
Relação com outras ferramentas
Gilmário → quality gate que implementa QILIS
AGCP → governança geral (QILIS foca em qualidade de ensino)
Spaced Repetition → integrado ao agente de inglês (24h → 3d → 7d → 30d → 90d)
MVI → princípio de arquivos <200 linhas (Minimum Viable Information)
Como aparece em entrevistas
"Como garantir qualidade de output em LLMs?"
"O que é spaced repetition e como automatizar?"
"Como implementar avaliação contínua em sistemas de IA?"
Resposta curta de entrevista
"Implementei um sistema de inspeção de qualidade com métricas específicas: clareza, memorabilidade via mnemônicos, exemplos práticos obrigatórios, checkpoints que impedem avanço sem confirmação, e spaced repetition automatizado em ciclos de 24h, 3d, 7d, 30d e 90d. Um agente quality gate revisa materiais antes da persistência."

O que memorizar
Métricas de ensino: Clareza + Memorabilidade + Praticidade + Checkpoint + MVI
Ciclo spaced repetition: 24h → 3d → 7d → 30d → 90d
MVI = <200 linhas por arquivo
Gilmário = quality gate
Importância para Data Engineer: 3/10
Importância para Machine Learning Engineer: 5/10
Importância para AI Engineer: 8/10
FERRAMENTA 6
Sistema de Memória em 4 Camadas
O que é
Arquitetura de memória com 4 camadas distintas (Working, Episodic, Semantic, Personal) que simula memória humana para agentes de IA.

Problema que resolve
LLMs não têm memória nativa entre sessões. Sem arquitetura de memória, cada interação é "amnésica" — o agente perde todo contexto.

Como funciona
Working Context (Volátil): carregado na sessão, descartado depois. Fontes: state.json, cache.json, official_schedule.md
Episodic Experience (Persistente): daily_log em cache.json por data. Cada agente registra o que fez.
Semantic Knowledge (Persistente): resumos de estudo em writings_studies/, governance docs, skills-cache
Personal Memory (Persistente): perfil do usuário em state.json, contatos, background
Analogia
Como a memória humana: Working = RAM (curto prazo), Episodic = diário pessoal, Semantic = enciclopédia internalizada, Personal = memória autobiográfica.

Entrada
Eventos da sessão (working)
Resultados de tarefas (episodic)
Conhecimento adquirido (semantic)
Perfil do usuário (personal)
Saída
Contexto relevante para cada agente em cada sessão
Quando usar
Em QUALQUER sistema de agentes que precisa manter contexto entre sessões
Sistemas educacionais com progressão
Quando NÃO usar
Chatbots stateless simples
Relação com outras ferramentas
state.json → fonte canônica de Personal Memory
cache.json → Episodic Experience por agente
writings_studies/ → Semantic Knowledge persistente
Orquestrador → lê TODAS as camadas no boot
Aísio → audita integridade das memórias
Como aparece em entrevistas
"Como implementar memória de longo prazo em LLMs?"
"Qual a diferença entre RAG e memória persistente?"
"Como estruturar estado em sistemas multi-agente?"
Resposta curta de entrevista
"Implementei memória em 4 camadas inspirada na cognição humana: Working (volátil, carregada por sessão), Episodic (logs persistentes por data), Semantic (base de conhecimento persistente), e Personal (perfil do usuário). Cada camada tem regras de acesso por agente, e o orquestrador consolida tudo no review noturno."

O que memorizar
4 camadas: Working (volátil) | Episodic (cache.json) | Semantic (studies/) | Personal (state.json)
CHECK → EXECUTA → CONFIRM → LOG (ciclo de cache)
Orquestrador lê TUDO, daily agents lêem SÓ o seu cache
Aísio só escreve no ledger, nunca em caches de outros
Importância para Data Engineer: 5/10
Importância para Machine Learning Engineer: 7/10
Importância para AI Engineer: 10/10
FERRAMENTA 7
Composio MCP (Multi-Channel Platform Integration)
O que é
Plataforma de integração que conecta agentes de IA a ferramentas externas (LinkedIn, ClickUp, Telegram) via Model Context Protocol (MCP).

Problema que resolve
Agentes de IA precisam interagir com plataformas reais (postar no LinkedIn, criar tasks no ClickUp, enviar mensagens) mas não têm acesso nativo a essas APIs.

Como funciona
O Composio atua como middleware MCP: o agente faz chamadas padronizadas, e o Composio traduz para a API específica de cada plataforma (OAuth, REST, GraphQL).

Analogia
É como um adaptador universal de tomadas: o agente sempre fala o mesmo "idioma" (MCP), e o Composio traduz para o "idioma" de cada plataforma (LinkedIn API, ClickUp API, etc.).

Entrada
Chamadas MCP padronizadas do agente
Credenciais OAuth pré-configuradas
Saída
Ações executadas nas plataformas (posts, tasks, conexões)
Dados retornados (vagas, perfis, métricas)
Quando usar
Para conectar agentes a SaaS externos
Quando precisar de múltiplas integrações com uma API unificada
Quando NÃO usar
Integrações simples com uma única API (use direto)
Quando a plataforma não é suportada pelo Composio
Relação com outras ferramentas
LinkedIn → auto-connect, posts, profile optimization (via portfolio + job-hunter)
ClickUp → CRM pipeline de job hunting (via job-hunter + josue)
Telegram → bridge separada (não usa Composio)
WhatsApp → bridge separada (Baileys)
Como aparece em entrevistas
"O que é Model Context Protocol (MCP)?"
"Como integrar agentes de IA com ferramentas externas?"
"Qual a diferença entre API direta e middleware de integração?"
Resposta curta de entrevista
"MCP é um protocolo padronizado para conectar LLMs a ferramentas externas. Uso o Composio como middleware MCP que traduz chamadas padronizadas para APIs específicas de cada plataforma — LinkedIn, ClickUp, etc. — com gestão automática de OAuth e rate limiting."

O que memorizar
MCP = Model Context Protocol (padrão de ferramentas para LLMs)
Composio = middleware que conecta a LinkedIn, ClickUp, etc.
OAuth e credenciais gerenciados pelo Composio, não pelo agente
Bridges de Telegram/WhatsApp são separadas (não MCP)
Importância para Data Engineer: 4/10
Importância para Machine Learning Engineer: 5/10
Importância para AI Engineer: 9/10
FERRAMENTA 8
Telegram Bridge (EZRA + Nice)
O que é
Ponte bidirecional entre Telegram e o sistema de agentes, usando polling direto da API do Telegram. Duas instâncias: EZRA (para Fábio) e Nice (para Dona Lu).

Problema que resolve
O usuário precisa interagir com o sistema de agentes pelo celular, a qualquer hora, sem abrir terminal ou computador.

Como funciona
Script Python faz polling contínuo da Telegram API
Recebe mensagem → encaminha para OpenCode processar
Recebe resposta → envia de volta pelo Telegram
EZRA inclui suporte a voz (Whisper tiny no Apple MPS)
Mantido 24/7 via launchd (macOS)
Analogia
É como um secretário pessoal ao telefone 24h: você manda mensagem, ele consulta o "escritório" (sistema de agentes) e responde.

Entrada
Mensagens de texto via Telegram
Áudio via Telegram (EZRA — transcreve com Whisper)
Saída
Respostas em texto via Telegram
Quando usar
Interface mobile para sistemas de agentes
Comunicação assíncrona (não precisa estar no computador)
Quando NÃO usar
Tarefas que precisam de output visual complexo (gráficos, código longo)
Quando latência <1s é crítica
Relação com outras ferramentas
OpenCode → backend que processa as mensagens
launchd → serviço macOS que mantém bridges 24/7
Whisper → transcrição de áudio (EZRA)
Nice bot → instância separada para Dona Lu (domínio doméstico isolado)
Como aparece em entrevistas
"Como implementar interface conversacional para sistemas de IA?"
"O que é webhook vs polling em bots?"
"Como manter serviços sempre ativos em macOS?"
Resposta curta de entrevista
"Implementei bridges Telegram com polling direto da API, sem subprocessos. Duas instâncias isoladas: uma profissional e uma doméstica, com separação de domínio. Suporte a voz via Whisper no Apple MPS para transcrição local. launchd garante uptime 24/7."

O que memorizar
Polling direto (não webhook) → mais controle, sem servidor público
Duas instâncias: EZRA (profissional) + Nice (doméstica)
Whisper tiny no MPS → transcrição de áudio local
launchd com KeepAlive=true + RunAtLoad=true
Importância para Data Engineer: 2/10
Importância para Machine Learning Engineer: 3/10
Importância para AI Engineer: 7/10
FERRAMENTA 9
Hierarquia de LLM (Temperature Engineering)
O que é
Sistema de configuração de temperatura e nível de reasoning para cada camada de agentes, garantindo comportamento previsível ou criativo conforme o propósito.

Problema que resolve
Usar o mesmo modelo e temperatura para todos os agentes causa outputs imprevisíveis em tarefas que precisam de determinismo, ou outputs robóticos em tarefas que precisam de criatividade.

Como funciona
Camada	T°	Reasoning	Uso
Orquestrador	0	Mínimo (só dispatch)	Coordenação
Gerentes (tutores)	0.2-0.3	Moderado	Ensino, criação
Produtores	0	ZERO	Job hunting, freela
Analogia
É como contratar funcionários diferentes para tarefas diferentes: o gerente de fábrica (orquestrador) segue regras rígidas, os professores (gerentes) são criativos dentro de limites, os operadores de linha (produtores) repetem processos exatos.

Entrada
Tipo de tarefa do agente
Domínio (ensino vs execução vs coordenação)
Saída
Configuração de modelo + temperatura por agente
Quando usar
Em QUALQUER sistema multi-agente
Quando diferentes agentes precisam de diferentes níveis de criatividade/determinismo
Quando NÃO usar
Sistema com um único agente
Quando todos os agentes fazem a mesma coisa
Relação com outras ferramentas
Orquestrador → T°0, modelo rápido (dispatch)
Tutores → T°0.2-0.3, modelo médio (ensino)
Produtores → T°0, qualquer modelo (execução determinística)
Como aparece em entrevistas
"Como escolher a temperatura ideal para LLMs?"
"Qual a diferença entre agentes determinísticos e estocásticos?"
"Como configurar diferentes agentes para diferentes tarefas?"
Resposta curta de entrevista
"Uso temperatura como controle de criatividade: 0 para agentes de coordenação e execução determinística, 0.2-0.3 para agentes tutores que precisam de adaptação didática. A regra é: quanto mais consequência real a ação tem, menor a temperatura."

O que memorizar
T°0 = determinístico (dispatch, execução, finanças)
T°0.2-0.3 = criatividade controlada (ensino, branding)
Regra: mais consequência → menor temperatura
Produtores NUNCA têm reasoning agents
Importância para Data Engineer: 4/10
Importância para Machine Learning Engineer: 8/10
Importância para AI Engineer: 10/10
FERRAMENTA 10
MVI (Minimum Viable Information)
O que é
Princípio arquitetural que limita TODOS os arquivos do sistema a máximo 200 linhas, forçando concisão e eficiência.

Problema que resolve
Documentos extensos desperdiçam tokens de contexto do LLM, são difíceis de manter, e criam ruído informacional.

Como funciona
Todo arquivo: <200 linhas
Prompts de agente: <60 linhas
Respostas padrão: <5 linhas
Código em blocos: <30 linhas
Chunks de output: 100 tokens
Analogia
É como o princípio YAGNI (You Ain't Gonna Need It) aplicado a documentação: se não cabe em 200 linhas, divida em partes menores.

Entrada
Qualquer conteúdo produzido no sistema
Saída
Conteúdo comprimido, focado e eficiente
Quando usar
Em sistemas de IA com limite de contexto
Para manter documentação enxuta
Quando NÃO usar
Documentos legais que precisam de completude
Código complexo que não pode ser dividido
Relação com outras ferramentas
QILIS → verifica compliance com MVI
Aísio → alerta quando arquivo excede 200 linhas
Todos os agentes → produzem output dentro dos limites MVI
Como aparece em entrevistas
"Como otimizar uso de tokens em sistemas LLM?"
"Qual a diferença entre compressão de contexto e summarização?"
Resposta curta de entrevista
"MVI garante que nenhum arquivo excede 200 linhas, prompts ficam abaixo de 60 linhas, e respostas padrão em 5 linhas. Isso otimiza contexto window do LLM, reduz custo, e força clareza na comunicação."

O que memorizar
Arquivo: <200 linhas | Prompt: <60 linhas | Resposta: <5 linhas
Código: <30 linhas por bloco | Output: 100 tokens por chunk
Se ultrapassar → dividir em partes menores
Aísio fiscaliza compliance
Importância para Data Engineer: 3/10
Importância para Machine Learning Engineer: 6/10
Importância para AI Engineer: 9/10
FERRAMENTA 11
state.json (Single Source of Truth)
O que é
Arquivo JSON canônico que centraliza TODA a informação do sistema: perfil do usuário, rotina diária, pipeline de job hunting, cronograma de estudos, princípios estratégicos.

Problema que resolve
Informações espalhadas em múltiplos arquivos causam inconsistência, duplicação, e decisões baseadas em dados desatualizados.

Como funciona
Único arquivo (~13KB) carregado por TODOS os agentes no início da sessão
Contém: user profile, daily_routine, study_schedule, job_hunting_system, portfolio_vivo, linkedin_engine, implementation_phases, strategic_principles
Agentes lêem state.json mas NÃO escrevem nele (só o usuário ou orquestrador)
Analogia
É como o banco de dados master em microserviços: todos os serviços consultam, mas tem regras rígidas de quem pode escrever.

Entrada
Decisões do usuário e do orquestrador
Saída
Contexto unificado para todos os agentes
Quando usar
Em QUALQUER sistema multi-agente que precisa de estado compartilhado
Quando NÃO usar
Quando agentes não precisam de contexto compartilhado
Relação com outras ferramentas
Todos os agentes → lêem state.json no CHECK
cache.json → memória local de cada agente (complementar)
metadata.json → aponta para state.json como fonte
Como aparece em entrevistas
"Como implementar single source of truth em sistemas distribuídos?"
"Como compartilhar estado entre microserviços/agentes?"
Resposta curta de entrevista
"Uso um JSON canônico central como single source of truth. Todos os agentes lêem, mas apenas o orquestrador e o usuário escrevem. Cada agente tem cache local para memória episódica, mas decisões são sempre baseadas no state centralizado."

O que memorizar
state.json = single source of truth (~13KB)
Todos lêem, poucos escrevem
cache.json = complementar, local, por agente
Seções: user, daily_routine, study_schedule, job_hunting, portfolio
Importância para Data Engineer: 6/10
Importância para Machine Learning Engineer: 5/10
Importância para AI Engineer: 9/10
FERRAMENTA 12
Spaced Repetition System (SRS)
O que é
Sistema de revisão espaçada integrado ao agente de inglês, com ciclos de 24h, 3d, 7d, 30d e 90d para fixação de vocabulário.

Problema que resolve
Vocabulário aprendido sem revisão é esquecido em poucos dias (curva de esquecimento de Ebbinghaus).

Como funciona
Vocábulo novo → agendar revisão em 24h
Se acertou → próxima revisão em 3d
Se acertou → 7d → 30d → 90d
Se errou 2x → reset + exemplo extra
Deck ativo mantido em cache.json do inglês
Analogia
É como o Anki automatizado: o agente é o professor que lembra de cobrar revisão no momento certo.

Entrada
Vocabulário novo aprendido
Resultados de revisão (acerto/erro)
Saída
Agendamento de revisão no cache.json
Exercícios de revisão no momento certo
Quando usar
Aprendizado de vocabulário, conceitos, fórmulas
Qualquer conteúdo que precisa de memorização de longo prazo
Quando NÃO usar
Conteúdo que precisa de compreensão, não memorização
Relação com outras ferramentas
Agente de inglês → implementa SRS no vocabulário
QILIS → audita se revisões estão sendo agendadas
cache.json → armazena deck ativo com datas de revisão
REGRAS.md → define obrigatoriedade de SRS para inglês
Como aparece em entrevistas
"O que é spaced repetition e como funciona?"
"Como implementar curva de esquecimento em software?"
Resposta curta de entrevista
"Implementei spaced repetition automatizado com ciclos de 24h, 3d, 7d, 30d e 90d. O agente rastreia cada item no deck, prioriza revisões pendentes sobre conteúdo novo, e aumenta o intervalo quando o aluno acerta. Erros consecutivos fazem reset com material complementar."

O que memorizar
Ciclo: 24h → 3d → 7d → 30d → 90d
Revisão pendente > conteúdo novo (prioridade)
Erro 2x → reset + exemplo extra
Baseado na curva de Ebbinghaus
Importância para Data Engineer: 2/10
Importância para Machine Learning Engineer: 3/10
Importância para AI Engineer: 6/10
FERRAMENTA 13
launchd (macOS Service Management)
O que é
Sistema nativo do macOS para gerenciar serviços persistentes (daemons e agents) que devem rodar continuamente em background.

Problema que resolve
Scripts Python (bridges) precisam rodar 24/7 sem intervenção humana, reiniciando automaticamente em caso de crash.

Como funciona
Plists (XML) definem serviços em ~/Library/LaunchAgents/
KeepAlive=true → reinicia se morrer
RunAtLoad=true → inicia ao login
Serviços BRACHÁT: com.brachat.opencode, com.brachat.nice, com.brachat.antigravity, com.brachat.clickup
Analogia
É como o systemd do Linux mas para macOS: gerencia serviços em background, garante que estejam sempre rodando.

Entrada
Plist com configuração do serviço
Script a ser executado
Saída
Serviço rodando 24/7 em background
Restart automático em caso de falha
Quando usar
Serviços que precisam rodar continuamente em macOS
Bridges de comunicação, sync, monitoring
Quando NÃO usar
Tarefas one-shot (use cron ou at)
Linux (use systemd)
Relação com outras ferramentas
Telegram bridges → mantidas vivas pelo launchd
WhatsApp bridge → mantida pelo launchd
ClickUp sync → mantido pelo launchd
Como aparece em entrevistas
"Como manter serviços em background no macOS?"
"Qual a diferença entre launchd e cron?"
"Como implementar self-healing em serviços?"
Resposta curta de entrevista
"launchd é o init system do macOS, equivalente ao systemd no Linux. Uso com KeepAlive para restart automático e RunAtLoad para iniciar ao boot. Ideal para bridges de comunicação que precisam de uptime 24/7."

O que memorizar
launchd = init system do macOS (equivalente systemd no Linux)
KeepAlive + RunAtLoad = 24/7 com auto-restart
Plists em ~/Library/LaunchAgents/
4 serviços BRACHÁT: opencode, nice, antigravity, clickup
Importância para Data Engineer: 3/10
Importância para Machine Learning Engineer: 2/10
Importância para AI Engineer: 6/10
FERRAMENTA 14
Whisper (OpenAI Speech-to-Text)
O que é
Modelo de transcrição de áudio para texto da OpenAI, rodando localmente no modelo tiny com aceleração Apple MPS.

Problema que resolve
O usuário quer interagir com o sistema por voz (via Telegram), mas o agente precisa de texto para processar.

Como funciona
Áudio recebido no Telegram → salvo localmente
Whisper tiny roda localmente no Apple MPS (GPU)
Transcreve áudio → texto
Texto segue para o pipeline normal do agente
Analogia
É como um intérprete que traduz voz para texto em tempo real, rodando no próprio computador (sem enviar para nuvem).

Entrada
Arquivo de áudio (via Telegram)
Saída
Texto transcrito
Quando usar
Interface de voz para agentes
Transcrição local sem dependência de API externa
Quando NÃO usar
Quando precisar de transcrição de alta qualidade (use modelo maior)
Para idiomas menos comuns (tiny é limitado)
Relação com outras ferramentas
EZRA bridge → usa Whisper para transcrever áudios do Telegram
Apple MPS → aceleração GPU para inferência local
Como aparece em entrevistas
"O que é Whisper e como funciona?"
"Qual a diferença entre rodar modelos na edge vs cloud?"
"Como implementar speech-to-text local?"
Resposta curta de entrevista
"Whisper é o modelo de speech-to-text da OpenAI. Uso o modelo tiny rodando localmente no Apple MPS para transcrição em tempo real de áudios do Telegram, sem latência de rede e sem custo de API."

O que memorizar
Whisper = speech-to-text da OpenAI
tiny = modelo menor, roda local
Apple MPS = Metal Performance Shaders (GPU acceleration)
Edge inference = sem custo de API, sem latência de rede
Importância para Data Engineer: 2/10
Importância para Machine Learning Engineer: 7/10
Importância para AI Engineer: 7/10
FERRAMENTA 15
governance-ledger.jsonl (Append-Only Audit Log)
O que é
Log de auditoria em formato JSONL (JSON Lines) onde TODA ação do sistema é registrada de forma append-only (nunca deleta, nunca edita).

Problema que resolve
Sem log de auditoria, é impossível verificar quem fez o quê, quando, e se teve aprovação.

Como funciona
Formato: {"timestamp", "agent", "action", "approved_by", "status"}
Somente Aísio escreve no ledger
Append-only: NUNCA deletar entradas
Auditado a cada sessão por Aísio
Analogia
É como o blockchain de governança: registro imutável de todas as ações para auditoria posterior.

Entrada
Ações executadas por qualquer agente
Saída
Registro permanente para auditoria
Quando usar
Em QUALQUER sistema que precisa de accountability
Compliance, governança, auditoria
Quando NÃO usar
Sistemas sem necessidade de auditoria
Relação com outras ferramentas
Aísio → único que escreve e audita o ledger
AGCP → define formato e regras do ledger
AUDITORIA.md → checklist semanal que usa dados do ledger
Como aparece em entrevistas
"Como implementar auditoria em sistemas de IA?"
"O que é append-only log e por que é importante?"
"Como garantir accountability em agentes autônomos?"
Resposta curta de entrevista
"Uso um JSONL append-only como ledger de governança. Toda ação é registrada com timestamp, agente, ação, e aprovador. Nunca se deleta entradas. Um agente auditor dedicado verifica conformidade a cada sessão."

O que memorizar
JSONL = uma entry JSON por linha
Append-only = nunca editar, nunca deletar
Campos: timestamp, agent, action, approved_by, status
Aísio = único que escreve e audita
Importância para Data Engineer: 6/10
Importância para Machine Learning Engineer: 4/10
Importância para AI Engineer: 8/10
MAPA MENTAL GERAL — COMO TUDO SE CONECTA

                        ┌─────────────────┐
                        │   USUÁRIO        │
                        │   (Fábio)        │
                        └───────┬─────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐ ┌────────┐ ┌──────────┐
              │ Telegram  │ │Terminal│ │WhatsApp  │
              │ (EZRA)    │ │        │ │(Baileys) │
              └─────┬─────┘ └───┬────┘ └────┬─────┘
                    │           │            │
                    ▼           ▼            ▼
              ┌─────────────────────────────────┐
              │         OPENCODE RUNTIME         │
              │   (boot: date → state → cache)   │
              └───────────────┬─────────────────┘
                              │
                              ▼
              ┌─────────────────────────────────┐
              │        ORQUESTRADOR (T°0)        │
              │   dispatch-schedule + state.json  │
              │   "Ontem: [X]. Agora: [Y]."      │
              └─────┬──────────┬──────────┬──────┘
                    │          │          │
          ┌────────┘   ┌──────┘    ┌─────┘
          ▼            ▼           ▼
    ┌───────────┐ ┌─────────┐ ┌───────────┐
    │ DIRETORES │ │ DAILY   │ │GOVERNANÇA │
    │ (4+Nice)  │ │AGENTS   │ │ (Aísio)   │
    └─────┬─────┘ │ (12)    │ └─────┬─────┘
          │       └────┬────┘       │
          │            │            │
          ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌──────────────┐
    │ Josué   │  │Ensino:  │  │ AGCP + QILIS │
    │(Comerc.)│  │cert,ing,│  │ governance-  │
    │ Gilmário│  │python,  │  │ ledger.jsonl │
    │(Branding│  │ml,torah,│  └──────────────┘
    │ Jéssica │  │filos,pmp│
    │(Jurídico│  │google-sk│
    │ Nice    │  ├─────────┤
    │(Domést.)│  │Execução:│
    └─────────┘  │job-hunt │
                 │freelance│
                 │portfolio│
                 └────┬────┘
                      │
                      ▼
              ┌───────────────┐
              │   MEMÓRIA     │
              ├───────────────┤
              │ state.json    │ ← Personal + Working
              │ cache.json    │ ← Episodic
              │ writings_     │ ← Semantic
              │  studies/     │
              │ governance-   │ ← Audit
              │  ledger.jsonl │
              └───────────────┘
Fluxo de Dados Principal:

Mensagem (Telegram/WhatsApp/Terminal)
  ↓
OpenCode Runtime (boot sequence)
  ↓
Orquestrador (T°0 dispatch)
  ↓
Daily Agent (T°0-0.3 execução)
  ↓
CHECK cache.json → EXECUTA tarefa → CONFIRM com user → LOG cache.json
  ↓
Aísio audita → governance-ledger.jsonl
  ↓
Gilmário revisa qualidade (se ensino) → writings_studies/
Fluxo de Interação entre Agentes:

job-hunter → [leads qualificados] → josue (pipeline comercial)
freelancer → [propostas] → josue + jessica (análise contratual)
certificacoes/python/ml → [materiais] → gilmario (quality gate) → writings_studies/
portfolio → [drafts] → gilmario (revisão) → usuario (publicação)
nice → [lembretes] → telegram (Dona Lu) [ISOLADA de trabalho]
jessica → [pareceres] → usuário [MEMÓRIA ISOLADA]
aisio → [auditorias] → governance-ledger.jsonl [BLOQUEIA qualquer agente]
RESUMO EXECUTIVO
Ferramentas REALMENTE importantes para entrevistas
Ferramenta	Área	Por quê
Padrão Harness (5 módulos)	AI Engineering	Framework de agentes auditáveis e governáveis
Orquestrador (dispatch)	AI Engineering	Coordenação multi-agente com determinismo
AGCP (governança)	AI Engineering + Compliance	Human-in-the-loop, approval gates, audit trail
Sistema de Memória 4 camadas	AI/ML Engineering	Solução real para persistência de LLMs
Temperature Engineering	ML Engineering	Controle de criatividade vs determinismo
MCP (Composio)	AI Engineering	Integração padronizada com ferramentas externas
MVI (compressão)	AI Engineering	Otimização de contexto e tokens
Ferramentas secundárias (complementam)
Ferramenta	Área
QILIS	Qualidade de ensino
Spaced Repetition	Educação + IA
Whisper (local)	Edge ML
governance-ledger.jsonl	Observabilidade
state.json (SSOT)	Arquitetura de dados
Ferramentas de apoio operacional (não caem em prova)
Ferramenta	Uso
launchd	Infra macOS
Telegram bridges	Comunicação
WhatsApp Baileys	Comunicação
Ollama (fallback)	LLM local
Os 20% de Conceitos que geram 80% do Valor para Entrevistas
Multi-Agent Orchestration: como coordenar múltiplos agentes especializados com dispatch determinístico e isolamento de domínio
AI Governance: approval gates, human-in-the-loop, commit-bound authorization, audit trail append-only
Memory Architecture: 4 camadas (Working/Episodic/Semantic/Personal) para resolver amnésia de LLMs
Temperature as Control Parameter: T°0 para determinismo, T°0.2-0.3 para criatividade controlada, regra de consequência
Agent Design Pattern (Harness): framework padronizado de 5 módulos para agentes auditáveis e reproduzíveis
MCP Integration: protocolo padronizado para conectar LLMs a ferramentas externas
Context Optimization (MVI): princípios de compressão para maximizar valor dentro da context window do LLM