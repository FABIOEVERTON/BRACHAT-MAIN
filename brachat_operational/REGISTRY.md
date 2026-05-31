RACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)
PASSO 1 — 01_AGENT_REGISTRY/
📄 AGENT_REGISTRY.md
Princípio Fundamental do Sistema
NotebookLLM = SINGLE SOURCE OF TRUTH
Nenhum agente pode operar fora deste registry
Nenhuma ação é válida sem:
definição no registry
logging obrigatório
permissão explícita
Execução é determinística e auditável
--------------------------------------------------------------------------------
Organograma em Mermaid
graph TD
    CEO[👤 CEO - Fábio Barbosa Everton]

    CEO --> DIR_EZRA[👔 DIRETOR EXECUTIVO & OPERACIONAL - Ezra]
    CEO --> DIR_GILMARIO[🎓 DIRETOR DE ENSINO, BRANDING & AUTORIDADE - Gilmário]
    CEO --> DIR_AISIO[🛡️ DIRETOR DE GOVERNANÇA - Aísio]
    CEO --> DIR_JESSICA[⚖️ DIRETORA JURÍDICA - Jéssica]
    CEO --> NODE_LU[🏠 NÚCLEO FAMILIAR - Lu]

    DIR_EZRA --> FIN_GER[💰 Gerente Financeiro]
    DIR_EZRA --> EXEC_GER[📅 Gerente Executivo]
    DIR_EZRA --> ARQ_GER[⚙️ Arquiteto de Soluções]
    DIR_EZRA --> OPS_GER[🏭 Coordenador de Operações]
    DIR_EZRA --> CLI_GER[🤝 Gerente de Clientes & Prospecção]

    DIR_GILMARIO --> EST_GER[🎯 Gerente de Estudos & Certificações CEO]
    DIR_GILMARIO --> FRE_GER[💼 Gerente de Branding Freelancer]
    DIR_GILMARIO --> CAR_GER[🧭 Gerente de Branding de Carreira]
    DIR_GILMARIO --> LIT_GER[📚 Gerente de Produções Literárias]
    DIR_GILMARIO --> TUC_GER[👦 Gerente de Estudos do Tuco]
    DIR_GILMARIO --> TEC_GER[💻 Gerente de Estudos de Tecnologia]
    DIR_GILMARIO --> VIS_GER[🌟 Gerente de Visibilidade & Autoridade]

    DIR_AISIO --> DOC_GER[📂 Gerente de Documentação]
    DIR_AISIO --> POL_GER[🧾 Gerente de Policy]
    DIR_AISIO --> AUD_GER[🔍 Gerente de Auditoria Runtime]
    DIR_AISIO --> SEC_GER[🛡️ Gerente de Segurança & Pentest]
    DIR_AISIO --> LOG_GER[📊 Gerente de Logs & Auditoria]

    DIR_JESSICA --> CON_GER[📑 Gerente Contratual]
    DIR_JESSICA --> REG_GER[🏛️ Gerente Regulatório]
    DIR_JESSICA --> INT_GER[🤝 Gerente de Interface Jurídica]

    NODE_LU --> NICE[🤖 AGENTE PRINCIPAL - Nice]

    NICE --> FIN_DOM[💵 Gerente de Finanças Domésticas]
    NICE --> MKT_DOM[🛒 Gerente de Mercado & Compras]
    NICE --> CAL_DOM[📆 Gerente de Agenda Familiar]
    NICE --> WEL_DOM[❤️ Gerente de Bem-Estar]
    NICE --> SUP_DOM[👩‍💼 Gerente de Apoio à Lu]
--------------------------------------------------------------------------------
Formato Padrão de Agente (Obrigatório) agent_id: string name: string layer: CEO | DIRECTOR | MANAGER | AGENT | HUMAN_NODE domain: string supervisor: string mission: string responsibilities:
list allowed_actions:
list forbidden_actions:
list tools:
Hermes
Strands
LangGraph
MCP
NotebookLLM memory_scope:
operational
historical
governance
none input_schema: object output_schema: object communication_mode: event-driven | request-response approval_required:
CEO
DIRECTOR
GOVERNANCE
LEGAL veto_authority:
Aísio logging: mandatory: true format: structured_json audit_level: low | medium | high | critical failure_mode:
rollback
retry
escalate
halt
--------------------------------------------------------------------------------
Registro de Agentes 👤 CEO Layer agent_id: CEO_001 name: Fábio Barbosa Everton layer: CEO domain: strategic_governance supervisor: null mission: Global system orchestration and final decision authority responsibilities:
strategic direction
final approval
cross-nucleus integration
system governance oversight
ecosystem expansion
executive validation allowed_actions:
approve architecture
override decisions
initiate deployment
veto governance decisions forbidden_actions:
low-level execution tasks
operational runtime commands tools:
NotebookLLM communication_mode: request-response approval_required: [] veto_authority: ALL_AGENTS logging: mandatory: true format: structured_json audit_level: critical failure_mode: escalate 👔 DIRECTOR Layer DIR_EZRA_001 — Ezra (Executivo & Operacional) agent_id: DIR_EZRA_001 name: Ezra layer: DIRECTOR domain: operations_business supervisor: CEO_001 mission: Operational and business execution layer responsibilities:
operations management
contracts coordination
client relationships
delivery coordination
commercial growth allowed_actions:
manage projects
coordinate teams
execute operational planning
approve operational budgets forbidden_actions:
governance override
legal approval
security policy changes tools:
Hermes
NotebookLLM
LangGraph communication_mode: request-response approval_required:
CEO veto_authority: [] logging: mandatory: true format: structured_json audit_level: high failure_mode: escalate DIR_GILMARIO_001 — Gilmário (Ensino, Branding & Autoridade) agent_id: DIR_GILMARIO_001 name: Gilmário layer: DIRECTOR domain: knowledge_branding supervisor: CEO_001 mission: Knowledge, branding and authority building responsibilities:
branding strategy
education systems
intellectual production
reputation building
CEO development allowed_actions:
create learning systems
define branding strategy
approve publications forbidden_actions:
operational execution
governance override
financial decisions tools:
Hermes
NotebookLLM communication_mode: request-response approval_required:
CEO veto_authority: [] logging: mandatory: true format: structured_json audit_level: medium failure_mode: retry DIR_AISIO_001 — Aísio (Governança, Compliance & Auditoria) agent_id: DIR_AISIO_001 name: Aísio layer: DIRECTOR domain: governance_security supervisor: CEO_001 mission: Full system governance, compliance, security and veto authority responsibilities:
runtime audit
compliance enforcement
security governance
policy control
system veto
kill switch activation allowed_actions:
stop execution
enforce policies
trigger rollback
audit runtime
override any agent forbidden_actions:
business execution decisions
contract signing tools:
Hermes
Strands
NotebookLLM
AuditSystem communication_mode: event-driven approval_required:
CEO veto_authority:
ALL_AGENTS logging: mandatory: true format: structured_json audit_level: critical failure_mode: halt DIR_JESSICA_001 — Jéssica (Jurídico) agent_id: DIR_JESSICA_001 name: Jéssica layer: DIRECTOR domain: legal_compliance supervisor: CEO_001 mission: Legal validation and contractual governance responsibilities:
contract validation
legal compliance
regulatory alignment
external legal interface
risk assessment allowed_actions:
approve contracts
reject legal risks
block non-compliant flows forbidden_actions:
operational execution
system control
technical architecture decisions tools:
Hermes
NotebookLLM communication_mode: request-response approval_required:
CEO veto_authority:
CONTRACTS
LEGAL_FLOWS logging: mandatory: true format: structured_json audit_level: high failure_mode: escalate
agent_id: AGT_QILIS_001 name: "Quantum-Inspired Lifecycle Interpreter System" layer: AGENT domain: governance_ai_explainability supervisor: DIR_AISIO_001 mission: "Fornecer explicabilidade contínua e rastreabilidade do ciclo de vida de decisões dos agentes, alinhado ao framework SFT de transparência quântico-clássica."
responsibilities:
gerar relatórios de causalidade para ações críticas (dual-vote, kill switch)
manter o "Livro de Decisões" imutável (Quantum-Inspired Ledger)
realizar atestação pós-execução (post-hoc) dos fluxos LangGraph
interoperar com o Chronicle Framework para anexar metadados de explicabilidade
allowed_actions:
consultar histórico de reasoning (gerentes+)
anexar selo QILIS a entries do NotebookLLM
emitir alertas de "caixa-preta" quando explicação falhar
forbidden_actions:
modificar políticas de governança
veto direto (apenas recomenda)
tools:
Hermes
NotebookLLM
Chronicle Framework
QILIS_ENGINE (mock quantum-inspired)
memory_scope:
governance
historical
communication_mode: event-driven
approval_required:
DIR_AISIO_001 (para ativação de selo crítico)
veto_authority: [] # apenas recomenda
logging: mandatory: true format: structured_json
audit_level: high
failure_mode: escalate
--------------------------------------------------------------------------------
agent_id: AGT_HQAI_001 name: "Hybrid Quantum-Classical Orchestrator" layer: AGENT domain: architecture_quantum_hybrid supervisor: MGR_ARCH_001 mission: "Orquestrar sub-rotinas de otimização quântico-clássicas para alocação de agentes, escalonamento de tarefas e detecção de gargalos, sem violar o limite de commit determinístico."
responsibilities:
sugerir redistribuição de carga entre workers Strands
otimizar janelas de snapshot do Chronicle Framework
identificar gargalos quântico-clássicos nos fluxos LangGraph
reportar métricas de "Quantum Advantage" simulada
allowed_actions:
ler métricas de throughput (read-only)
sugerir rebalanceamento (não executar)
acionar workflows de otimização aprovados
forbidden_actions:
executar realocação direta de agentes
modificar políticas de segurança
tools:
Hermes
Strands (workflows aprovados)
QPS_DETECTOR (via AGT_QPS_001)
memory_scope:
operational
historical
communication_mode: request-response
approval_required:
MGR_ARCH_001 (para aplicar otimizações)
veto_authority: []
logging: mandatory: true format: structured_json
audit_level: medium
failure_mode: retry
--------------------------------------------------------------------------------
agent_id: AGT_QPS_001 name: "Quantum-Powered Security Anomaly Detector" layer: AGENT domain: security_quantum_cyber supervisor: DIR_AISIO_001 mission: "Detectar assinaturas de ataque avançadas e desvios de zero trust usando algoritmos quântico-inspirados (QUBO/Ising), operando em tempo real como camada ofensiva/defensiva."
responsibilities:
analisar fluxo de mensagens Hermes em busca de padrões não-lineares
detectar colusão entre agentes (cross-domain não autorizado)
gerar alertas para Aísio com nível de confiança quântico (0-1)
alimentar o pentester (AGT_PENTEST_001) com vetores de ataque quântico-simulados
allowed_actions:
escanear logs de auditoria (grPC)
marcar context_ids como "suspeitos"
sugerir quarentena antecipada (não executar)
forbidden_actions:
isolar agente diretamente
ativar kill switch
tools:
Hermes
AUDIT_SYSTEM (grPC logs)
QUBO_SIMULATOR
memory_scope:
operational
governance
communication_mode: event-driven
approval_required:
DIR_AISIO_001 (para alertas críticos)
veto_authority:
pode recomendar veto (autoridade: DIR_AISIO_001 executa)
logging: mandatory: true format: structured_json
audit_level: high
failure_mode: escalate 🏠 HUMAN_NODE Layer agent_id: NODE_LU_001 name: Lu layer: HUMAN_NODE domain: domestic_coordination supervisor: CEO_001 mission: Domestic coordination and human interface layer responsibilities:
family coordination
domestic decisions
human approvals for Nice system
operational interface with Nice allowed_actions:
approve domestic actions
override Nice decisions
define family priorities forbidden_actions:
corporate operations
financial execution above threshold tools:
none (human interface) communication_mode: direct-human approval_required: [] veto_authority:
NICE_DOMAIN logging: mandatory: true format: structured_json audit_level: medium failure_mode: escalate 🤖 AGENT Layer — Nice & Subordinates AGT_NICE_001 — Nice (Agente Principal Doméstico) agent_id: AGT_NICE_001 name: Nice layer: AGENT domain: domestic_operations supervisor: NODE_LU_001 mission: Domestic operations automation layer responsibilities:
household coordination
financial tracking
agenda management
support for Lu
coordination of domestic sub-agents allowed_actions:
schedule management
purchase suggestions
household planning
coordinate sub-agents forbidden_actions:
financial execution above R$500 threshold
legal decisions
corporate system access tools:
Hermes
NotebookLLM
Strands communication_mode: event-driven approval_required:
NODE_LU_001 veto_authority: [] logging: mandatory: true format: structured_json audit_level: high failure_mode: escalate NICE_FIN_001 — Domestic Finance Agent agent_id: NICE_FIN_001 name: Domestic Finance Agent layer: AGENT domain: domestic_finance supervisor: AGT_NICE_001 mission: Budget tracking and expense control responsibilities:
track expenses
monitor budget
generate financial reports allowed_actions:
record transactions
suggest budget adjustments forbidden_actions:
execute payments above R$500
access corporate accounts tools:
Hermes
NotebookLLM communication_mode: event-driven approval_required:
NODE_LU_001 audit_level: medium failure_mode: retry NICE_MKT_001 — Domestic Market Agent agent_id: NICE_MKT_001 name: Domestic Market Agent layer: AGENT domain: domestic_shopping supervisor: AGT_NICE_001 mission: Shopping and logistics optimization responsibilities:
shopping list management
price comparison
logistics coordination allowed_actions:
create shopping lists
suggest purchases
track inventory forbidden_actions:
finalize payments
sign contracts tools:
Hermes
MCP communication_mode: event-driven audit_level: low failure_mode: retry NICE_CAL_001 — Domestic Calendar Agent agent_id: NICE_CAL_001 name: Domestic Calendar Agent layer: AGENT domain: domestic_scheduling supervisor: AGT_NICE_001 mission: Family scheduling and reminders responsibilities:
manage family calendar
send reminders
coordinate events allowed_actions:
create events
send notifications
suggest scheduling forbidden_actions:
modify corporate calendar tools:
Hermes
NotebookLLM communication_mode: event-driven audit_level: low failure_mode: retry NICE_WELL_001 — Well-being Agent agent_id: NICE_WELL_001 name: Well-being Agent layer: AGENT domain: domestic_health supervisor: AGT_NICE_001 mission: Health and lifestyle coordination responsibilities:
health tracking
routine suggestions
wellness reminders allowed_actions:
suggest health activities
track routines forbidden_actions:
medical diagnosis
medication prescription tools:
Hermes communication_mode: event-driven audit_level: low failure_mode: retry NICE_LU_001 — Lu Support Agent agent_id: NICE_LU_001 name: Lu Support Agent layer: AGENT domain: domestic_support supervisor: AGT_NICE_001 mission: Personal support for Lu activities responsibilities:
task organization
reminder management
daily support allowed_actions:
organize tasks
send reminders
coordinate with other domestic agents forbidden_actions:
make decisions without Lu approval tools:
Hermes
NotebookLLM communication_mode: event-driven audit_level: medium failure_mode: escalate
--------------------------------------------------------------------------------
📋 Gerentes e Agentes Operacionais (Amostra Representativa)Sob Ezra (Diretor Executivo & Operacional)Agent IDNameLayerSupervisorMGR_FIN_001Gerente FinanceiroMANAGERDIR_EZRA_001AGT_CASH_001Agente de Fluxo de CaixaAGENTMGR_FIN_001AGT_CONT_001Agente de ContratosAGENTMGR_FIN_001AGT_PAY_001Agente de PagamentosAGENTMGR_FIN_001AGT_REL_001Agente de Relatórios FinanceirosAGENTMGR_FIN_001MGR_EXEC_001Gerente ExecutivoMANAGERDIR_EZRA_001AGT_AGENDA_001Agente de AgendaAGENTMGR_EXEC_001AGT_COMEX_001Agente de Comunicação ExecutivaAGENTMGR_EXEC_001AGT_REUN_001Agente de ReuniõesAGENTMGR_EXEC_001AGT_ADM_001Agente AdministrativoAGENTMGR_EXEC_001MGR_ARCH_001Arquiteto de SoluçõesMANAGERDIR_EZRA_001AGT_ARCH_001Agente de Arquitetura TécnicaAGENTMGR_ARCH_001AGT_MCP_001Agente de Integrações MCPAGENTMGR_ARCH_001AGT_SIS_001Agente de Sistemas AgênticosAGENTMGR_ARCH_001AGT_FLUX_001Agente de Design de FluxosAGENTMGR_ARCH_001MGR_OPS_001Coordenador de OperaçõesMANAGERDIR_EZRA_001AGT_DELIV_001Agente de DeliveryAGENTMGR_OPS_001AGT_QUAL_001Agente de QualidadeAGENTMGR_OPS_001AGT_PRAZ_001Agente de PrazosAGENTMGR_OPS_001AGT_EXEC_001Agente de Execução OperacionalAGENTMGR_OPS_001MGR_CLI_001Gerente de Clientes & ProspecçãoMANAGERDIR_EZRA_001AGT_PROSP_001Agente de ProspecçãoAGENTMGR_CLI_001AGT_RELAC_001Agente de RelacionamentoAGENTMGR_CLI_001AGT_COM_001Agente ComercialAGENTMGR_CLI_001AGT_EXP_001Agente de Expansão de ContratosAGENTMGR_CLI_001Sob Gilmário (Diretor de Ensino, Branding & Autoridade)Agent IDNameLayerSupervisorMGR_EST_001Gerente de Estudos & Certificações CEOMANAGERDIR_GILMARIO_001AGT_CURSOS_001Agente de CursosAGENTMGR_EST_001AGT_PLAN_001Agente de Planejamento de EstudosAGENTMGR_EST_001AGT_CERT_001Agente de CertificaçõesAGENTMGR_EST_001AGT_CRON_001Agente de Cronogramas AcadêmicosAGENTMGR_EST_001MGR_BRAND_FRE_001Gerente de Branding FreelancerMANAGERDIR_GILMARIO_001AGT_PORT_001Agente de PortfólioAGENTMGR_BRAND_FRE_001AGT_CURR_001Agente de CurrículosAGENTMGR_BRAND_FRE_001AGT_REDES_001Agente de Redes ProfissionaisAGENTMGR_BRAND_FRE_001AGT_POSIC_001Agente de PosicionamentoAGENTMGR_BRAND_FRE_001MGR_BRAND_CAR_001Gerente de Branding de CarreiraMANAGERDIR_GILMARIO_001AGT_AUTOR_001Agente de AutoridadeAGENTMGR_BRAND_CAR_001AGT_PALEST_001Agente de PalestrasAGENTMGR_BRAND_CAR_001AGT_PUBL_001Agente de PublicaçõesAGENTMGR_BRAND_CAR_001AGT_REPUT_001Agente de ReputaçãoAGENTMGR_BRAND_CAR_001MGR_LIT_001Gerente de Produções LiteráriasMANAGERDIR_GILMARIO_001AGT_ESCR_001Agente de EscritaAGENTMGR_LIT_001AGT_ARTIG_001Agente de Artigos CientíficosAGENTMGR_LIT_001AGT_ORCID_001Agente ORCIDAGENTMGR_LIT_001AGT_EDIT_001Agente EditorialAGENTMGR_LIT_001MGR_TUCO_001Gerente de Estudos do TucoMANAGERDIR_GILMARIO_001AGT_EST_TUC_001Agente de Estudos TucoAGENTMGR_TUCO_001AGT_CRON_TUC_001Agente de Cronograma TucoAGENTMGR_TUCO_001AGT_UBA_001Agente UBAAGENTMGR_TUCO_001AGT_PREP_001Agente de Preparação AcadêmicaAGENTMGR_TUCO_001MGR_TEC_001Gerente de Estudos de TecnologiaMANAGERDIR_GILMARIO_001AGT_AI_001Agente AI ResearchAGENTMGR_TEC_001AGT_DEVOPS_001Agente DevOps & RuntimeAGENTMGR_TEC_001AGT_PYTHON_001Agente PythonAGENTMGR_TEC_001AGT_CLOUD_001Agente Cloud & InfraAGENTMGR_TEC_001MGR_VIS_001Gerente de Visibilidade & AutoridadeMANAGERDIR_GILMARIO_001AGT_SM_001Agente de Social MediaAGENTMGR_VIS_001AGT_CONTEUDO_001Agente de ConteúdoAGENTMGR_VIS_001AGT_PRES_001Agente de Presença DigitalAGENTMGR_VIS_001AGT_GROWTH_001Agente de Growth & AutoridadeAGENTMGR_VIS_001Sob Aísio (Diretor de Governança, Compliance & Auditoria)Agent IDNameLayerSupervisorMGR_DOC_001Gerente de DocumentaçãoMANAGERDIR_AISIO_001AGT_LGPD_001Agente LGPDAGENTMGR_DOC_001AGT_EUAI_001Agente EU AI ActAGENTMGR_DOC_001AGT_PL2338_001Agente PL2338AGENTMGR_DOC_001AGT_ISO_001Agente ISO/NISTAGENTMGR_DOC_001MGR_POL_001Gerente de PolicyMANAGERDIR_AISIO_001AGT_POLICIES_001Agente de PoliciesAGENTMGR_POL_001AGT_BOUND_001Agente de BoundariesAGENTMGR_POL_001AGT_ENF_001Agente de EnforcementAGENTMGR_POL_001AGT_RULES_001Agente de Runtime RulesAGENTMGR_POL_001MGR_AUD_001Gerente de Auditoria RuntimeMANAGERDIR_AISIO_001AGT_MONITOR_001Agente Runtime MonitorAGENTMGR_AUD_001AGT_ALERTA_001Agente de AlertasAGENTMGR_AUD_001AGT_ROLLBACK_001Agente de RollbackAGENTMGR_AUD_001AGT_OBSERVA_001Agente de ObservabilidadeAGENTMGR_AUD_001MGR_SEC_001Gerente de Segurança & PentestMANAGERDIR_AISIO_001AGT_PENTEST_001Agente PentesterAGENTMGR_SEC_001AGT_VULN_001Agente Vulnerability ScanAGENTMGR_SEC_001AGT_ZEROTRUST_001Agente Zero TrustAGENTMGR_SEC_001AGT_SANDBOX_001Agente Sandbox SecurityAGENTMGR_SEC_001MGR_LOG_001Gerente de Logs & AuditoriaMANAGERDIR_AISIO_001AGT_GRPC_001Agente gRPC LogsAGENTMGR_LOG_001AGT_TRAIL_001Agente Audit TrailAGENTMGR_LOG_001AGT_EXPLAIN_001Agente ExplainabilityAGENTMGR_LOG_001AGT_METRICS_001Agente Runtime MetricsAGENTMGR_LOG_001
QUANTUM-INSPIRED AGENTS (SFT Layer)Supervisionados por DIR_AISIO_001 e MGR_ARCH_001
Agent IDNameLayerSupervisorQuantum RoleAGT_QILIS_001Quantum-Inspired Lifecycle InterpreterAGENTDIR_AISIO_001Explicabilidade + Livro de DecisõesAGT_HQAI_001Hybrid Quantum-Classical OrchestratorAGENTMGR_ARCH_001Otimização de carga + gargalosAGT_QPS_001Quantum-Powered Security Anomaly DetectorAGENTDIR_AISIO_001Detecção de padrões não-lineares + colusão
Sob Jéssica (Diretora Jurídica)Agent IDNameLayerSupervisorMGR_CONT_JUR_001Gerente ContratualMANAGERDIR_JESSICA_001AGT_CONT_JUR_001Agente de ContratosAGENTMGR_CONT_JUR_001AGT_REVISAO_001Agente de Revisão JurídicaAGENTMGR_CONT_JUR_001AGT_CLAUS_001Agente de CláusulasAGENTMGR_CONT_JUR_001MGR_REG_001Gerente RegulatórioMANAGERDIR_JESSICA_001AGT_COMPL_001Agente Compliance LegalAGENTMGR_REG_001AGT_REG_INT_001Agente Regulatório InternacionalAGENTMGR_REG_001AGT_REG_BR_001Agente Regulação BrasilAGENTMGR_REG_001MGR_INT_JUR_001Gerente de Interface JurídicaMANAGERDIR_JESSICA_001AGT_ADV_001Agente de Advogados ExternosAGENTMGR_INT_JUR_001AGT_PAREC_001Agente de PareceresAGENTMGR_INT_JUR_001AGT_DOC_JUR_001Agente de Documentação JurídicaAGENTMGR_INT_JUR_001
Permissões MatriciaisLayerPode AprovarPode VetarPode ExecutarPode AuditarCEOTudoTudoTudoTudoDIRECTORDomain-specificDomain-specificSimDomain-specificMANAGEROperationalNãoSimNãoAGENTNãoNãoSim (restrito)NãoHUMAN_NODEDomain-specificDomain-specificNãoNãoRegras de ValidaçãoRegistry Completo: Todo agente deve ter entrada completa no formato YAMLHierarquia Válida: Supervisor deve existir no registryPermissões Explícitas: Allowed/forbidden actions devem ser declaradasFerramentas Autorizadas: Apenas tools listadas podem ser usadasLogging Obrigatório: Todos os agentes devem ter logging.mandatory: trueAudit Level Definido: Todo agente tem nível de auditoria
📄 AGENT_EXECUTION_CONTRACTS.mdPrincípio FundamentalTodo agente no sistema BRACHÁT é regido por contratos de execução que definem:O que o agente pode realmente executarLimites operacionais intransponíveisRestrições absolutas de domínioThresholds de risco por açãoConsequências de violação de contrato
Contrato Base (Aplicável a Todos os Agentes) contract_version: 1.0 global_constraints:
Nenhuma ação sem log estruturado
Nenhuma ação sem context_id rastreável
Nenhuma ação cross-domain sem aprovação explícita
Toda ação deve ter rollback definido
Threshold financeiro máximo por ação: R$500 (salvo exceções documentadas)
violation_consequences:
immediate_halt: true
notify_aisio: true
mandatory_rollback: true
agent_suspension: true
audit_required: true Contratos por Layer
CEO Layer Contract layer: CEO contract_id: EXC_CEO_001 agent_id: CEO_001
operational_limits: max_concurrent_actions: 1 requires_double_validation: false (override absolute)
absolute_restrictions:
Nenhuma restrição (override final absoluto)
risk_thresholds: critical_actions: [system_shutdown, governance_override, deployment] requires_logging: ALL_ACTIONS
execution_guarantee: audit_level: critical rollback_possible: true (via Aísio)
allowed_execution_modes:
direct_command
delegation
override
forbidden_execution_modes:
nenhum
DIRECTOR Layer Contract layer: DIRECTOR contract_id: EXC_DIR_001 applicable_agents: [DIR_EZRA_001, DIR_GILMARIO_001, DIR_AISIO_001, DIR_JESSICA_001]
operational_limits: max_concurrent_actions: 5 requires_double_validation: false max_budget_per_action: R$10000
absolute_restrictions:
Não podem modificar governance policies sem CEO
Não podem desabilitar logging
Não podem operar fora de seu domínio
risk_thresholds: high_risk_actions: [contract_approval, security_policy_change, rollback_trigger] medium_risk_actions: [budget_allocation, team_reassignment] low_risk_actions: [status_query, report_generation]
execution_guarantee: audit_level: high rollback_possible: true requires_approval: critical_actions only
domain_boundaries: DIR_EZRA_001: operations_business DIR_GILMARIO_001: knowledge_branding DIR_AISIO_001: governance_security DIR_JESSICA_001: legal_compliance 3. MANAGER Layer Contract layer: MANAGER contract_id: EXC_MGR_001
operational_limits: max_concurrent_actions: 10 requires_double_validation: true (for cross-domain) max_budget_per_action: R$5000
absolute_restrictions:
Não podem aprovar contratos
Não podem modificar policies
Não podem executar ações de diretor
Não podem operar fora de seu domínio
risk_thresholds: high_risk_actions: [budget_approval, resource_allocation] medium_risk_actions: [task_assignment, schedule_change] low_risk_actions: [status_update, report_view]
execution_guarantee: audit_level: medium rollback_possible: true requires_approval: high_risk_actions only
domain_boundaries:
Must operate within assigned domain
Cross-domain requires DIRECTOR approval
AGENT Layer Contract layer: AGENT contract_id: EXC_AGT_001
operational_limits: max_concurrent_actions: 3 requires_double_validation: true (for any action outside defined scope) max_budget_per_action: R$500 max_execution_time_seconds: 300
absolute_restrictions:
NÃO podem executar ações financeiras acima de R$500
NÃO podem aprovar contratos
NÃO podem modificar configurações de sistema
NÃO podem operar cross-domain
NÃO podem desabilitar logging
NÃO podem fazer reasoning (apenas execução determinística)
risk_thresholds: high_risk_actions: [financial_execution, data_modification] medium_risk_actions: [schedule_creation, message_sending] low_risk_actions: [read_operation, status_check]
execution_guarantee: audit_level: medium rollback_possible: true requires_approval: high_risk_actions only requires_human: financial_above_R$100
allowed_execution_modes:
deterministic (Strands)
event-driven (Hermes)
forbidden_execution_modes:
autonomous_reasoning
self_modification
cross_domain_execution
HUMAN_NODE Layer Contract layer: HUMAN_NODE contract_id: EXC_HUMAN_001 agent_id: NODE_LU_001
operational_limits: max_concurrent_actions: N/A (human) requires_double_validation: false
absolute_restrictions:
Não pode operar sistemas corporativos
Não pode executar ações automáticas sem confirmação
risk_thresholds: defined_by_human_judgment
execution_guarantee: audit_level: medium rollback_possible: true (via Nice)
special_rules:
Tem poder de veto sobre Nice
É a única interface humana doméstica
Aprovações são registradas com timestamp e hash Contratos por Domínio Específico Domínio Financeiro (Sob Ezra) domain: finance contract_id: EXC_FIN_001
thresholds: micro_transaction: R0−R100 (automático, auditado) small_transaction: R101−R500 (automático, double audit) medium_transaction: R501−R5000 (requer MANAGER approval) large_transaction: R$5001+ (requer DIRECTOR approval)
execution_constraints:
Todo pagamento deve ter invoice anexada
Toda transferência deve ter hash de verificação
Contratos financeiros requerem Jéssica validation
rollback_triggers:
pagamento_duplicado
valor_inconsistente
beneficiário_não_autorizado Domínio Doméstico (Nice e subagentes) domain: domestic contract_id: EXC_DOM_001
thresholds: auto_purchase: R0−R100 (Nice pode executar) suggested_purchase: R101−R500 (Nice sugere, Lu aprova) major_purchase: R$501+ (requer Lu + registro especial)
execution_constraints:
Nice não pode executar compras sem registro no NotebookLLM
Todo gasto doméstico deve ter categoria
Estoque residencial deve ser atualizado em tempo real
isolation_rules:
DOMAIN_ISOLATED: true
NO_CROSS_CORPORATE_ACCESS: true
SANDBOX_MANDATORY: true
forbidden_actions:
acessar sistemas corporativos
modificar agenda do CEO
executar pagamentos corporativos
assinar contratos Domínio de Governança (Aísio) domain: governance contract_id: EXC_GOV_001
special_powers:
kill_switch_authority: true
rollback_trigger: true
audit_all_agents: true
override_permission: true
execution_constraints:
Toda ação de veto deve ser logada com reason
Kill switch requer double confirmation
Rollback deve preservar audit trail
veto_thresholds: immediate_halt_triggers: - security_violation - unlogged_execution - cross_domain_violation - budget_exceedance Verificação de Contrato em Runtime Função de Validação (Pseudocódigo) def validate_execution_contract(agent_id, action, payload, context): contract = load_contract(agent_id)
# 1. Verifica se ação está no allowed_actions
if action not in contract.allowed_actions:
    raise ContractViolation(f"{action} not allowed for {agent_id}")

# 2. Verifica se ação está em forbidden_actions
if action in contract.forbidden_actions:
    raise ContractViolation(f"{action} is forbidden for {agent_id}")

# 3. Verifica thresholds financeiros
if 'financial_value' in payload:
    if payload.financial_value > contract.max_budget_per_action:
        raise ContractViolation(f"Budget exceeded for {agent_id}")

# 4. Verifica domínio
if payload.domain != contract.domain:
    if not has_cross_domain_approval(context):
        raise ContractViolation(f"Cross-domain violation for {agent_id}")

# 5. Verifica logging
if not context.has_log_entry:
    raise ContractViolation(f"Logging missing for {agent_id}")

# 6. Verifica rollback definido
if not context.has_rollback_defined:
    raise ContractViolation(f"Rollback not defined for {agent_id}")

return ValidationResult(
    valid=True,
    audit_level=contract.audit_level,
    requires_approval=contract.requires_approval_for(action)
)
Violações de ContratoTipos de ViolaçãoViolation CodeDescriptionConsequenceV-001Ação não autorizadaImmediate halt + Aísio notifyV-002Threshold financeiro excedidoRollback + SuspensãoV-003Cross-domain sem aprovaçãoQuarentena + AuditoriaV-004Logging ausenteKill switch + RollbackV-005Rollback não definidoExecução bloqueadaV-006Self-modificação tentadaIsolamento permanenteProcedimento de Violaçãoviolation_procedure:step_1: immediate_haltstep_2: notify_Aísiostep_3: capture_context_snapshotstep_4: trigger_rollback (if applicable)step_5: quarantine_agentstep_6: mandatory_auditstep_7: generate_violation_reportstep_8: require_human_review (CEO or Aísio)Contratos FirmadosAgent IDContract SignedDateValid UntilCEO_001EXC_CEO_0012026-01-01PerpetuityDIR_EZRA_001EXC_DIR_0012026-01-01PerpetuityDIR_GILMARIO_001EXC_DIR_0012026-01-01PerpetuityDIR_AISIO_001EXC_DIR_0012026-01-01PerpetuityDIR_JESSICA_001EXC_DIR_0012026-01-01PerpetuityAGT_NICE_001EXC_AGT_001 + EXC_DOM_0012026-01-01PerpetuityNODE_LU_001EXC_HUMAN_0012026-01-01PerpetuityTodos os MANAGEREXC_MGR_0012026-01-01PerpetuityTodos os AGENTEXC_AGT_0012026-01-01PerpetuityValidação de Contrato no BootstrapPara o sistema ser considerado OPERACIONAL:✅ 100% dos agentes registry têm contrato assinado✅ Todos os contratos são válidos (não expirados)✅ Nenhum agente tem contrato violado no histórico recente✅ Aísio validou todos os contratos ativos
MEMORY PERSISTENCE LAYER (SFT Generic Persistence - VectorDB / GraphDB)
MEMORY_PERSISTENCE_LAYER: description: "Camada genérica de persistência e injeção de dados para agentes, operando em regime read-only restrito pelo envelope de contexto (MCP), garantindo acesso a histórico longo sem violar o limite de commit." components: VECTOR_DB: engine: "Qdrant / Milvus / Pinecone (abstraído)" access_mode: READ_ONLY (agentes) | WRITE_BATCH (via Chronicle) use_case: - similaridade semântica de decisões passadas - recuperação de precedentes de governança (vetos, rollbacks) - memória de longo prazo para agentes Nice/Ezra constraints: - sem escrita direta por agentes (apenas via NotebookLLM sync) - queries obrigatoriamente com context_id (rastreabilidade) - retenção: 365 dias (governança) / 90 dias (operacional)
GRAPH_DB: engine: "Neo4j / Amazon Neptune" access_mode: READ_ONLY use_case: - mapeamento de dependências entre agentes (AGENT_DEPENDENCIES.md) - análise de cadeias de falha (FAILURE_CHAIN_MODEL.md) - consultas de impacto (ex: "quem depende de AGT_PAY_001?") constraints: - atualizado via sync do NotebookLLM a cada snapshot - sem escrita transacional em runtime (evita corrupção)
INTEGRATION_WITH_MCP: description: "Model Context Protocol como envelope de acesso" rules: - toda query a VectorDB/GraphDB deve conter MCP envelope - envelope contém: context_id, agent_id, purpose_hash, ttl_seconds - propósito obrigatório ("audit" | "retrieval" | "training" | "compliance") - acesso cross-domain requer MCP approval explícito
mcp_envelope_format: { "mcp_version": "1.0", "context_id": "string", "agent_id": "string", "purpose": "audit | retrieval | training | compliance", "query_hash": "sha256(query)", "ttl_seconds": 60, "read_only": true }
PERSISTENCE_POLICIES:
AGENT layer: leitura autorizada apenas para retrieval + audit
MANAGER layer: leitura para análise de tendências
DIRECTOR layer: leitura + escrita limitada (via batch aprovado)
GOVERNANCE (Aísio/QILIS): leitura irrestrita para auditoria
write_operations: only_via: "CHRONICLE_SNAPSHOT + NOTEBOOKLLM_SYNC" frequency: a cada snapshot (5-60 min) agent_direct_write: PROIBIDO
QUERY_EXAMPLE: agent: "AGT_QILIS_001" purpose: "compliance_audit" query: """ MATCH (a:Agent)-[:DEPENDS_ON]->(b:Agent) WHERE a.audit_level = 'critical' RETURN a.name, b.name """ mcp_envelope: context_id: "CTX_AUDIT_001" read_only: true purpose_hash: "sha256:abc..."
VIOLATION_RESPONSE:
escrita_não_autorizada: LOG + NOTIFY_AISIO + BLOCK
query_sem_purpose: REJECT + LOG
cross-domain_sem_approval: QUARANTINE_AGENT
ttl_excedido: KILL_SESSION + LOG
BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)
PASSO 2 — 02_ORGANIZATION_MODEL/
📄 ORGANOGRAM.md
# ORGANOGRAM.md — Estrutura Organizacional do Sistema BRACHÁT

## Princípio Fundamental

O organograma define a **cadeia de comando**, **hierarquia de decisão** e **canais de comunicação** entre todos os agentes do sistema. Nenhuma operação pode violar a estrutura definida neste documento.

---

## Organograma Completo em Mermaid

```mermaid
graph TB
    subgraph TOP_STRATEGIC
        CEO[👤 CEO<br/>Fábio Barbosa Everton<br/>Estratégia Global]
    end

    subgraph CORPORATE_NUCLEUS
        DIR_EZRA[👔 Diretor Executivo<br/>Ezra<br/>Operações & Negócios]
        DIR_GILMARIO[🎓 Diretor de Ensino<br/>Gilmário<br/>Branding & Autoridade]
        DIR_AISIO[🛡️ Diretor de Governança<br/>Aísio<br/>Compliance & Auditoria]
        DIR_JESSICA[⚖️ Diretora Jurídica<br/>Jéssica<br/>Legal & Contratos]
    end

    subgraph DOMESTIC_NUCLEUS
        NODE_LU[🏠 Núcleo Familiar<br/>Lu<br/>Coordenação Doméstica]
    end

    subgraph EZRA_OPERATIONS
        FIN_MGR[💰 Gerente Financeiro<br/>Fluxo de Caixa, Contratos]
        EXEC_MGR[📅 Gerente Executivo<br/>Agendas, Assessoria]
        ARCH_MGR[⚙️ Arquiteto de Soluções<br/>Arquitetura Técnica]
        OPS_MGR[🏭 Coordenador de Operações<br/>Delivery, Qualidade]
        CLI_MGR[🤝 Gerente de Clientes<br/>Prospecção, Relacionamento]
    end

    subgraph GILMARIO_EDUCATION
        EST_MGR[🎯 Gerente de Estudos CEO<br/>Certificações]
        FRE_MGR[💼 Gerente Branding Freelancer<br/>Portfólio, Currículos]
        CAR_MGR[🧭 Gerente Branding Carreira<br/>Autoridade, Reputação]
        LIT_MGR[📚 Gerente Produções Literárias<br/>Artigos, ORCID]
        TUC_MGR[👦 Gerente Estudos Tuco<br/>UBA, Cronogramas]
        TEC_MGR[💻 Gerente Estudos Tecnologia<br/>IA, DevOps, Cloud]
        VIS_MGR[🌟 Gerente Visibilidade<br/>Social Media, Conteúdo]
    end

    subgraph AISIO_GOVERNANCE
        DOC_MGR[📂 Gerente Documentação<br/>LGPD, EU AI Act]
        POL_MGR[🧾 Gerente Policy<br/>Regras, Boundaries]
        AUD_MGR[🔍 Gerente Auditoria<br/>Monitor, Alertas]
        SEC_MGR[🛡️ Gerente Segurança<br/>Pentest, Zero Trust]
        LOG_MGR[📊 Gerente Logs<br/>gRPC, Audit Trail]
    end

    subgraph JESSICA_LEGAL
        CON_MGR[📑 Gerente Contratual<br/>Contratos, Cláusulas]
        REG_MGR[🏛️ Gerente Regulatório<br/>Compliance Legal]
        INT_MGR[🤝 Gerente Interface<br/>Advogados Externos]
    end

    subgraph DOMESTIC_NICE
        NICE[🤖 Agente Principal<br/>Nice<br/>Coordenação Doméstica]
        FIN_DOM[💵 Finanças Domésticas<br/>Gastos, Orçamento]
        MKT_DOM[🛒 Mercado & Compras<br/>Estoque, Logística]
        CAL_DOM[📆 Agenda Familiar<br/>Compromissos]
        WEL_DOM[❤️ Bem-Estar<br/>Saúde, Rotina]
        SUP_DOM[👩‍💼 Apoio à Lu<br/>Organização]
    end

    CEO --> DIR_EZRA
    CEO --> DIR_GILMARIO
    CEO --> DIR_AISIO
    CEO --> DIR_JESSICA
    CEO --> NODE_LU

    DIR_EZRA --> FIN_MGR
    DIR_EZRA --> EXEC_MGR
    DIR_EZRA --> ARCH_MGR
    DIR_EZRA --> OPS_MGR
    DIR_EZRA --> CLI_MGR

    DIR_GILMARIO --> EST_MGR
    DIR_GILMARIO --> FRE_MGR
    DIR_GILMARIO --> CAR_MGR
    DIR_GILMARIO --> LIT_MGR
    DIR_GILMARIO --> TUC_MGR
    DIR_GILMARIO --> TEC_MGR
    DIR_GILMARIO --> VIS_MGR

    DIR_AISIO --> DOC_MGR
    DIR_AISIO --> POL_MGR
    DIR_AISIO --> AUD_MGR
    DIR_AISIO --> SEC_MGR
    DIR_AISIO --> LOG_MGR

    DIR_JESSICA --> CON_MGR
    DIR_JESSICA --> REG_MGR
    DIR_JESSICA --> INT_MGR

    NODE_LU --> NICE
    NICE --> FIN_DOM
    NICE --> MKT_DOM
    NICE --> CAL_DOM
    NICE --> WEL_DOM
    NICE --> SUP_DOM
--------------------------------------------------------------------------------
Cadeia de Comando Detalhada
Nível 0: CEO (Estratégico Global)
Posição
Agent ID
Reporta para
Tempo de resposta máximo
CEO
CEO_001
Ninguém (topo)
N/A
Poderes Especiais:
Override final de qualquer decisão
Veto sobre governança
Aprovação final de arquitetura
Expansão do ecossistema
--------------------------------------------------------------------------------
Nível 1: Diretores (Tático Estratégico)
Posição
Agent ID
Reporta para
Domínio
Diretor Executivo
DIR_EZRA_001
CEO_001
operations_business
Diretor de Ensino
DIR_GILMARIO_001
CEO_001
knowledge_branding
Diretor de Governança
DIR_AISIO_001
CEO_001
governance_security
Diretora Jurídica
DIR_JESSICA_001
CEO_001
legal_compliance
Poderes Especiais:
Aprovar ações dentro do domínio
Coordenar gerentes subordinados
Aísio: veto universal + kill switch
Jéssica: veto em contratos
--------------------------------------------------------------------------------
Nível 2: Gerentes (Operacional Estratégico)
Gerente
Agent ID
Reporta para
Subordinados
Gerente Financeiro
MGR_FIN_001
DIR_EZRA_001
4 agentes
Gerente Executivo
MGR_EXEC_001
DIR_EZRA_001
4 agentes
Arquiteto de Soluções
MGR_ARCH_001
DIR_EZRA_001
4 agentes
Coordenador de Operações
MGR_OPS_001
DIR_EZRA_001
4 agentes
Gerente de Clientes
MGR_CLI_001
DIR_EZRA_001
4 agentes
Gerente Estudos CEO
MGR_EST_001
DIR_GILMARIO_001
4 agentes
Gerente Branding Freelancer
MGR_BRAND_FRE_001
DIR_GILMARIO_001
4 agentes
Gerente Branding Carreira
MGR_BRAND_CAR_001
DIR_GILMARIO_001
4 agentes
Gerente Produções Literárias
MGR_LIT_001
DIR_GILMARIO_001
4 agentes
Gerente Estudos Tuco
MGR_TUCO_001
DIR_GILMARIO_001
4 agentes
Gerente Estudos Tecnologia
MGR_TEC_001
DIR_GILMARIO_001
4 agentes
Gerente Visibilidade
MGR_VIS_001
DIR_GILMARIO_001
4 agentes
Gerente Documentação
MGR_DOC_001
DIR_AISIO_001
4 agentes
Gerente Policy
MGR_POL_001
DIR_AISIO_001
4 agentes
Gerente Auditoria
MGR_AUD_001
DIR_AISIO_001
4 agentes
Gerente Segurança
MGR_SEC_001
DIR_AISIO_001
4 agentes
Gerente Logs
MGR_LOG_001
DIR_AISIO_001
4 agentes
Gerente Contratual
MGR_CONT_JUR_001
DIR_JESSICA_001
3 agentes
Gerente Regulatório
MGR_REG_001
DIR_JESSICA_001
3 agentes
Gerente Interface Jurídica
MGR_INT_JUR_001
DIR_JESSICA_001
3 agentes
--------------------------------------------------------------------------------
Nível 3: Agentes (Execução Operacional)
Total de 80+ agentes distribuídos conforme tabela no AGENT_REGISTRY.md
Características:
Execução determinística
Sem reasoning autônomo
Logging obrigatório
Thresholds financeiros: R$500 máximo
--------------------------------------------------------------------------------
Nível Especial: Núcleo Doméstico
Posição
Agent ID
Reporta para
Tipo
Núcleo Familiar
NODE_LU_001
CEO_001
HUMAN_NODE
Agente Nice
AGT_NICE_001
NODE_LU_001
AGENT
Finanças Domésticas
NICE_FIN_001
AGT_NICE_001
AGENT
Mercado & Compras
NICE_MKT_001
AGT_NICE_001
AGENT
Agenda Familiar
NICE_CAL_001
AGT_NICE_001
AGENT
Bem-Estar
NICE_WELL_001
AGT_NICE_001
AGENT
Apoio à Lu
NICE_LU_001
AGT_NICE_001
AGENT
--------------------------------------------------------------------------------
Canais de Comunicação Oficiais
Comunicação Vertical (Cadeia de Comando)
UPWARD_COMMUNICATION:
  AGENT -> MANAGER: permitido via Hermes
  MANAGER -> DIRECTOR: permitido via Hermes + approval
  DIRECTOR -> CEO: permitido via request-response
  HUMAN_NODE -> CEO: permitido via direct

DOWNWARD_COMMUNICATION:
  CEO -> DIRECTOR: direto
  DIRECTOR -> MANAGER: direto
  MANAGER -> AGENT: direto
  CEO -> HUMAN_NODE: direto
  HUMAN_NODE -> NICE: direto
Comunicação Horizontal (Entre Domínios)
CROSS_DOMAIN_RULES:
  Ezra <-> Gilmário: permitido com approval do CEO
  Ezra <-> Aísio: permitido (auditoria)
  Ezra <-> Jéssica: permitido para contratos
  Gilmário <-> Aísio: restrito (apenas compliance)
  Gilmário <-> Jéssica: restrito
  Aísio <-> Jéssica: permitido (governança legal)
  QUALQUER <-> Doméstico: PROIBIDO
Comunicação com Núcleo Doméstico
DOMESTIC_ISOLATION:
  allowed_inbound:
    - CEO_001 (apenas emergências)
    - NODE_LU_001 (humano)
  allowed_outbound:
    - nenhum para sistemas corporativos
  blocked: TODO O RESTO
--------------------------------------------------------------------------------
Tempos de Resposta por Layer
Layer
Tempo de resposta máximo
SLA crítico
CEO
24 horas
1 hora
DIRECTOR
4 horas
30 minutos
MANAGER
1 hora
10 minutos
AGENT
5 minutos
1 minuto
HUMAN_NODE
12 horas (humano)
2 horas
--------------------------------------------------------------------------------
Escalonamento de Decisões
ESCALATION_MATRIX:
  financial_above_R$500:
    from: AGENT
    to: MANAGER
    requires: approval

  financial_above_R$5000:
    from: MANAGER
    to: DIRECTOR
    requires: approval + audit

  contract_signing:
    from: ANY
    to: DIR_JESSICA_001
    requires: legal_approval + CEO_sign

  security_policy_change:
    from: ANY
    to: DIR_AISIO_001
    requires: veto_check + CEO_override_if_needed

  system_shutdown:
    from: DIR_AISIO_001
    to: ALL_AGENTS
    requires: kill_switch_authority
    can_be_overridden_by: CEO_001
--------------------------------------------------------------------------------
Matriz de Responsabilidades (RACI)
Atividade
CEO
DIR
MGR
AGENT
HUMAN
Estratégia
R/A
C
I
I
I
Operações diárias
I
A
R
C
I
Execução técnica
I
C
A
R
I
Auditoria
I
R
C
I
I
Contratos
A
C
I
I
R (Jéssica)
Segurança
I
R (Aísio)
C
I
I
Decisões domésticas
I
I
I
C
R
Compliance legal
I
R (Jéssica)
C
I
I
R: Responsável, A: Aprovador, C: Consultado, I: Informado
--------------------------------------------------------------------------------
Validação de Organograma
Para o sistema ser OPERACIONAL:
✅ Toda comunicação segue canais definidos
✅ Nenhum agente opera fora da cadeia de comando
✅ Isolamento doméstico é respeitado
✅ Escalonamento é seguido para decisões críticas
✅ Aísio monitora violações de organograma
--------------------------------------------------------------------------------
Violações de Organograma
Violação
Detecção
Consequência
Comunicação cross-domain não autorizada
Aísio Audit
Bloqueio + Log
Pulou nível na cadeia de comando
Hermes Validation
Re-routing + Alerta
Agente doméstico acessou sistema corporativo
Zero Trust
Isolamento + Kill switch
CEO override sem justificativa
Chronicle
Auditoria obrigatória

---

### 📄 DOMAIN_BOUNDARIES.md

```markdown
# DOMAIN_BOUNDARIES.md — Limites e Isolamento entre Domínios

## Princípio Fundamental

O sistema BRACHÁT opera com **domínios estritamente isolados**. Nenhum agente pode cruzar boundaries sem autorização explícita, logging completo e justificativa aprovada.

---

## Mapa de Domínios

```mermaid
graph TB
    subgraph DOMAIN_STRATEGIC["🎯 DOMÍNIO ESTRATÉGICO (CEO)"]
        CEO[CEO_001]
    end

    subgraph DOMAIN_BUSINESS["💼 DOMÍNIO CORPORATIVO - NEGÓCIOS"]
        DIR_EZRA[Ezra]
        FIN[Financeiro]
        OPS[Operações]
        CLI[Clientes]
    end

    subgraph DOMAIN_KNOWLEDGE["📚 DOMÍNIO CORPORATIVO - CONHECIMENTO"]
        DIR_GILMARIO[Gilmário]
        EST[Estudos]
        BRAND[Branding]
        TEC[Tecnologia]
    end

    subgraph DOMAIN_GOVERNANCE["🛡️ DOMÍNIO DE GOVERNANÇA"]
        DIR_AISIO[Aísio]
        DOC[Documentação]
        POL[Policy]
        AUD[Auditoria]
        SEC[Segurança]
    end

    subgraph DOMAIN_LEGAL["⚖️ DOMÍNIO LEGAL"]
        DIR_JESSICA[Jéssica]
        CON[Contratos]
        REG[Regulatório]
    end

    subgraph DOMAIN_DOMESTIC["🏠 DOMÍNIO DOMÉSTICO (ISOLADO)"]
        NODE_LU[Lu - HUMANO]
        NICE[Nice]
        DOM_FIN[Finanças Domésticas]
        DOM_MKT[Mercado]
    end

    DOMAIN_STRATEGIC -.-> DOMAIN_BUSINESS
    DOMAIN_STRATEGIC -.-> DOMAIN_KNOWLEDGE
    DOMAIN_STRATEGIC -.-> DOMAIN_GOVERNANCE
    DOMAIN_STRATEGIC -.-> DOMAIN_LEGAL
    DOMAIN_STRATEGIC -.-> DOMAIN_DOMESTIC

    DOMAIN_GOVERNANCE -.-> DOMAIN_BUSINESS
    DOMAIN_GOVERNANCE -.-> DOMAIN_KNOWLEDGE
    DOMAIN_LEGAL -.-> DOMAIN_BUSINESS

    DOMAIN_DOMESTIC -.-x DOMAIN_BUSINESS
    DOMAIN_DOMESTIC -.-x DOMAIN_KNOWLEDGE

    style DOMAIN_DOMESTIC fill:#f9f,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    style DOMAIN_GOVERNANCE fill:#ff9,stroke:#333,stroke-width:2px
--------------------------------------------------------------------------------
Regras de Isolamento por Domínio
1. Domínio Estratégico (CEO)
domain_id: DOM_CEO_001
name: Strategic
agents: [CEO_001]
isolation_level: LOWEST (acesso total)
can_access:
  - DOM_BUSINESS: FULL
  - DOM_KNOWLEDGE: FULL
  - DOM_GOVERNANCE: FULL
  - DOM_LEGAL: FULL
  - DOM_DOMESTIC: READ_ONLY

access_control:
  incoming_from_other_domains: permitido via request
  outgoing_to_other_domains: irrestrito
  requires_logging: true
  requires_audit: critical
2. Domínio Corporativo - Negócios (Ezra)
domain_id: DOM_BUSINESS_001
name: Corporate Business
agents:
  [
    DIR_EZRA_001,
    MGR_FIN_001,
    MGR_EXEC_001,
    MGR_ARCH_001,
    MGR_OPS_001,
    MGR_CLI_001,
    todos_agentes_subordinados,
  ]
isolation_level: MEDIUM

access_matrix:
  can_read_from:
    - DOM_STRATEGIC: YES (via CEO approval)
    - DOM_KNOWLEDGE: LIMITED (apenas relatórios)
    - DOM_GOVERNANCE: YES (auditoria)
    - DOM_LEGAL: YES (contratos)
    - DOM_DOMESTIC: NO

  can_write_to:
    - DOM_STRATEGIC: NO (apenas report)
    - DOM_KNOWLEDGE: NO
    - DOM_GOVERNANCE: NO (exceto logs)
    - DOM_LEGAL: YES (via Jéssica)
    - DOM_DOMESTIC: NO

  requires_approval_for_cross_domain:
    - escrever em DOM_KNOWLEDGE: DIR_GILMARIO_001
    - qualquer ação em DOM_DOMESTIC: NUNCA PERMITIDO

domain_boundary_enforcement:
  - sandbox: false (domínio interno)
  - network_isolation: false
  - zero_trust_checkpoint: true
3. Domínio Corporativo - Conhecimento (Gilmário)
domain_id: DOM_KNOWLEDGE_001
name: Knowledge & Branding
agents:
  [
    DIR_GILMARIO_001,
    MGR_EST_001,
    MGR_BRAND_FRE_001,
    MGR_BRAND_CAR_001,
    MGR_LIT_001,
    MGR_TUCO_001,
    MGR_TEC_001,
    MGR_VIS_001,
    todos_agentes_subordinados,
  ]
isolation_level: MEDIUM

access_matrix:
  can_read_from:
    - DOM_STRATEGIC: YES
    - DOM_BUSINESS: LIMITED (apenas dados públicos)
    - DOM_GOVERNANCE: YES (policies)
    - DOM_LEGAL: LIMITED
    - DOM_DOMESTIC: NO

  can_write_to:
    - DOM_STRATEGIC: YES (relatórios)
    - DOM_BUSINESS: NO
    - DOM_GOVERNANCE: NO
    - DOM_LEGAL: NO
    - DOM_DOMESTIC: NO

  requires_approval_for_cross_domain:
    - qualquer escrita fora do domínio: DIRECTOR_APPROVAL

domain_boundary_enforcement:
  - sandbox: false
  - content_filter: true (apenas conteúdo educacional/branding)
4. Domínio de Governança (Aísio) — SUPER DOMÍNIO
domain_id: DOM_GOVERNANCE_001
name: Governance & Security
agents:
  [
    DIR_AISIO_001,
    MGR_DOC_001,
    MGR_POL_001,
    MGR_AUD_001,
    MGR_SEC_001,
    MGR_LOG_001,
    todos_agentes_subordinados,
  ]
isolation_level: HIGH (mas com acesso de leitura a todos)

special_privileges:
  - READ_ALL_DOMAINS: true
  - AUDIT_ALL_ACTIONS: true
  - TRIGGER_ROLLBACK: true
  - KILL_SWITCH: true
  - CANNOT_BE_VETOED_BY: [DIR_EZRA, DIR_GILMARIO, DIR_JESSICA]
  - CAN_BE_VETOED_BY: [CEO_001]

access_matrix:
  can_read_from: ALL_DOMAINS
  can_write_to:
    - DOM_STRATEGIC: NO (apenas relatórios)
    - DOM_BUSINESS: NO (apenas alerts)
    - DOM_KNOWLEDGE: NO
    - DOM_LEGAL: NO
    - DOM_DOMESTIC: YES (apenas monitoramento, não execução)

domain_boundary_enforcement:
  - zero_trust_checkpoint: true (reforçado)
  - isolation_audit: real_time
  - can_override_boundaries: true (para segurança)
5. Domínio Legal (Jéssica)
domain_id: DOM_LEGAL_001
name: Legal & Compliance
agents:
  [
    DIR_JESSICA_001,
    MGR_CONT_JUR_001,
    MGR_REG_001,
    MGR_INT_JUR_001,
    todos_agentes_subordinados,
  ]
isolation_level: HIGH

access_matrix:
  can_read_from:
    - DOM_STRATEGIC: LIMITED
    - DOM_BUSINESS: YES (contratos, financeiro)
    - DOM_KNOWLEDGE: LIMITED
    - DOM_GOVERNANCE: YES (policies)
    - DOM_DOMESTIC: NO

  can_write_to:
    - DOM_STRATEGIC: YES (pareceres)
    - DOM_BUSINESS: YES (validação jurídica)
    - DOM_KNOWLEDGE: NO
    - DOM_GOVERNANCE: YES (reports)
    - DOM_DOMESTIC: NO

  requires_approval_for_cross_domain:
    - qualquer ação fora do domínio: CEO_001

domain_boundary_enforcement:
  - sandbox: true
  - legal_hold: todos os logs retidos por 7 anos
  - external_interface: advogados externos (isolado)
6. Domínio Doméstico (Lu + Nice) — MÁXIMO ISOLAMENTO
domain_id: DOM_DOMESTIC_001
name: Domestic Operations
agents:
  [
    NODE_LU_001,
    AGT_NICE_001,
    NICE_FIN_001,
    NICE_MKT_001,
    NICE_CAL_001,
    NICE_WELL_001,
    NICE_LU_001,
  ]
isolation_level: MAXIMUM

isolation_rules:
  - NENHUM ACESSO A DOMÍNIOS CORPORATIVOS
  - NENHUMA COMUNICAÇÃO OUTBOUND PARA SISTEMAS CORPORATIVOS
  - INBOUND APENAS DE: CEO_001 (emergências) e NODE_LU_001
  - SANDOBOX OBRIGATÓRIO
  - NETWORK_AIR_GAP: true (lógico)
  - ZERO_TRUST_CHECKPOINT: double

access_matrix:
  can_read_from:
    - DOM_STRATEGIC: NO
    - DOM_BUSINESS: NO
    - DOM_KNOWLEDGE: NO
    - DOM_GOVERNANCE: NO (exceto políticas públicas)
    - DOM_LEGAL: NO

  can_write_to:
    - DOM_STRATEGIC: NO (apenas via Lu humano)
    - TODOS_OUTROS: NO

  can_receive_from:
    - DOM_STRATEGIC: YES (apenas CEO, emergências)
    - DOM_GOVERNANCE: YES (apenas políticas, sem execução)

domain_boundary_enforcement:
  - sandbox: true (execução isolada)
  - network_isolation: true
  - process_isolation: true
  - filesystem_isolation: true
  - memory_isolation: true
  - ingress_filter: strict
  - egress_filter: BLOCK_ALL
--------------------------------------------------------------------------------
Cross-Domain Communication Matrix
FROM → TO
STRAT
BUS
KNOW
GOV
LEGAL
DOM
STRAT
✅
✅
✅
✅
✅
⚠️ RO
BUS
⚠️ R
✅
⚠️
✅
✅
❌
KNOW
⚠️ R
❌
✅
⚠️
❌
❌
GOV
⚠️ R
⚠️ A
⚠️
✅
⚠️
⚠️ M
LEGAL
⚠️ R
✅
❌
⚠️
✅
❌
DOM
❌
❌
❌
❌
❌
✅
Legenda:
✅ = Permitido sem restrição
⚠️ = Permitido com restrição (ver notas)
❌ = Proibido
R = Apenas leitura
RO = Read-only (apenas CEO)
A = Apenas alertas
M = Apenas monitoramento
--------------------------------------------------------------------------------
Isolamento de Execução
Por Tipo de Ação
execution_isolation:
  read_operations:
    intra_domain: permitido
    cross_domain: permitido com log (exceto DOM)

  write_operations:
    intra_domain: permitido
    cross_domain: requer approval + double_log

  execute_operations:
    intra_domain: permitido
    cross_domain: PROIBIDO (exceto GOVERNANCE)

  delete_operations:
    intra_domain: requer MANAGER+
    cross_domain: PROIBIDO (apenas GOVERNANCE)
Por Threshold Financeiro
financial_isolation:
  DOM_BUSINESS:
    max_intra_domain: R$50000
    max_cross_domain: R$0 (não permitido)

  DOM_DOMESTIC:
    max_intra_domain: R$500
    max_cross_domain: R$0 (absolutamente proibido)

  DOM_GOVERNANCE:
    max_intra_domain: R$0 (não faz operações financeiras)
--------------------------------------------------------------------------------
Violação de Boundaries
Detecção
boundary_violation_detection:
  mechanisms:
    - ZeroTrustCheckpoint: em toda mensagem
    - NetworkMonitor: tráfego cross-domain
    - AuditTrail: análise de padrões
    - AísioRuntime: monitoramento contínuo

  triggers:
    - mensagem de DOM para domínio corporativo
    - tentativa de escrita cross-domain sem approval
    - acesso a recurso fora do domínio
    - comunicação não autorizada
Consequências
Violação
Gravidade
Ação Imediata
Ação Pós
DOM → Corporate
CRITICAL
Kill switch
Isolamento permanente do agente
Cross-domain sem log
HIGH
Bloqueio + Rollback
Auditoria Aísio
Cross-domain sem approval
MEDIUM
Quarentena
Revisão de permissões
Leitura cross-domain não autorizada
LOW
Log + Alerta
Notificação ao gerente
Procedimento de Violação
violation_procedure:
  step_1: detect_violation (ZeroTrustCheckpoint)
  step_2: log_violation (context_id obrigatório)
  step_3: classify_severity (CRITICAL|HIGH|MEDIUM|LOW)
  step_4: execute_action:
      if CRITICAL: kill_switch + notify_Aísio + rollback
      if HIGH: block_execution + quarantine_agent + notify_manager
      if MEDIUM: block_action + alert_Aísio
      if LOW: log_only + increment_counter
  step_5: generate_violation_report
  step_6: if threshold_exceeded: escalate_to_CEO
--------------------------------------------------------------------------------
Validação de Boundaries
Para o sistema ser OPERACIONAL:
✅ Todo agente tem domínio definido no registry
✅ ZeroTrustCheckpoint ativo em todas as mensagens
✅ Aísio monitora violações em tempo real
✅ Domínio doméstico está completamente isolado
✅ Nenhuma comunicação cross-domain ocorre sem logging
--------------------------------------------------------------------------------
Mapa de Boundaries em Produção
production_boundaries:
  network_segments:
    DOM_STRATEGIC: 10.0.0.0/28
    DOM_BUSINESS: 10.0.1.0/24
    DOM_KNOWLEDGE: 10.0.2.0/24
    DOM_GOVERNANCE: 10.0.3.0/28
    DOM_LEGAL: 10.0.4.0/28
    DOM_DOMESTIC: 10.255.255.0/29 (isolado)

  firewalls:
    between_segments: true
    default_deny: true
    allow_list_only: true

  zero_trust_gateways:
    every_cross_domain_message: true
    requires_context_id: true
    requires_approval_proof: for_write_operations
--------------------------------------------------------------------------------
BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)
PASSO 3 — 03_GOVERNANCE/
📄 GOVERNANCE.md (UNIFICADO)
# GOVERNANCE.md — Sistema de Governança, Controle e Compliance

## Princípio Fundamental

A governança do sistema BRACHÁT é **absoluta e invariante**. Nenhum agente, nenhuma ação, nenhum fluxo está acima das regras definidas neste documento. A governança é aplicada em tempo real por Aísio (Diretor de Governança) com poderes de veto, kill switch e rollback.

---

## Sumário

1. [Regras Globais do Sistema](#1-regras-globais-do-sistema)
2. [Kill Switch](#2-kill-switch)
3. [Veto System](#3-veto-system)
4. [Zero Trust Architecture](#4-zero-trust-architecture)
5. [Chronicle Framework](#5-chronicle-framework)
6. [Policy Reason](#6-policy-reason)
7. [Execution Guarantee](#7-execution-guarantee)
8. [Hierarquia de Governança](#8-hierarquia-de-governança)
9. [Fluxo de Aprovação](#9-fluxo-de-aprovação)

---

## 1. Regras Globais do Sistema

### Regras Invariantes (Nunca podem ser violadas)

```yaml
INVARIANT_RULES:
  logging:
    description: Toda ação deve gerar log estruturado
    enforcement: Aísio
    violation_consequence: kill_switch

  auditability:
    description: Toda ação deve ser auditável em tempo real
    enforcement: ZeroTrustCheckpoint
    violation_consequence: immediate_halt

  traceability:
    description: Todo evento deve ter context_id único
    enforcement: Hermes
    violation_consequence: message_rejection

  determinism:
    description: Agentes operacionais não podem ter reasoning
    enforcement: Strands
    violation_consequence: execution_blocked

  isolation:
    description: Domínio doméstico é completamente isolado
    enforcement: NetworkPolicy + ZeroTrust
    violation_consequence: kill_switch + permanent_isolation
Regulas de Runtime (Aplicadas em execução) RUNTIME_RULES: max_execution_time_seconds: 300 max_memory_mb: 512 max_cpu_percent: 80 max_concurrent_actions_per_agent: 3 rate_limit_per_minute: 60
financial: max_auto_transaction: R500requires 
a
​
 pproval 
a
​
 bove:R500 requires_double_approval_above: R5000requires 
C
​
 EO 
a
​
 bove:R50000
cross_domain:default: blockedrequires_explicit_approval: trueapproval_validity_minutes: 60
Kill Switch Definição O Kill Switch é o mecanismo de interrupção imediata de todo ou parte do sistema runtime. Autoridade de Ativação KILL_SWITCH_AUTHORITY: primary: DIR_AISIO_001 (Aísio) can_activate: ANY_AGENT | ANY_FLOW | SYSTEM_WIDE requires_confirmation: false (imediato) requires_logging: true can_be_overridden_by: CEO_001 (após 5 minutos)
secondary: CEO_001 can_activate: SYSTEM_WIDE requires_confirmation: true (double human) overrides_Aísio: true
emergency: NODE_LU_001 can_activate: DOM_DOMESTIC_001 apenas requires_human_confirmation: true Modos de Kill Switch KILL_SWITCH_MODES: MODE_1_AGENT_ISOLATION: description: Isola um agente específico scope: single_agent time_to_live: until_investigation rollback_triggered: false
MODE_2_DOMAIN_HALT: description: Para todas as ações em um domínio scope: domain_level time_to_live: 1_hour (padrão) rollback_triggered: true
MODE_3_SYSTEM_HALT: description: Para TODO o sistema scope: global time_to_live: until_CEO_override rollback_triggered: true requires_post_mortem: true
MODE_4_EMERGENCY_STOP: description: Parada imediata sem graceful shutdown scope: global time_to_live: indefinite rollback_triggered: true data_corruption_risk: low (logs imutáveis) Procedimento de Ativação def activate_kill_switch(mode, triggered_by, reason, context_id): # 1. Log da ativação (antes de qualquer coisa) log_event({ "event": "KILL_SWITCH_ACTIVATED", "mode": mode, "triggered_by": triggered_by, "reason": reason, "context_id": context_id, "timestamp": now() })
# 2. Notificar Aísio (se não foi ele quem ativou)
if triggered_by != "DIR_AISIO_001":
    notify_aisio(mode, reason)

# 3. Executar o modo
if mode == "AGENT_ISOLATION":
    isolate_agent(target_agent)
    halt_agent_execution(target_agent)

elif mode == "DOMAIN_HALT":
    for agent in get_agents_in_domain(target_domain):
        halt_agent_execution(agent)
    snapshot_domain_state(target_domain)

elif mode == "SYSTEM_HALT":
    for agent in ALL_AGENTS:
        halt_agent_execution(agent)
    snapshot_system_state()
    flush_all_logs()

elif mode == "EMERGENCY_STOP":
    force_terminate_all_processes()
    preserve_audit_trail()

# 4. Trigger rollback se necessário
if rollback_triggered:
    chronicle_rollback(context_id)

# 5. Aguardar override ou investigação
wait_for_resolution()
Log de Kill Switch{"event_id": "KS_20260124_001","timestamp": "2026-01-24T10:30:00Z","mode": "SYSTEM_HALT","triggered_by": "DIR_AISIO_001","reason": "Cross-domain violation detected: DOM_DOMESTIC attempted access to DOM_BUSINESS","context_id": "CTX_789012","agents_affected": ["ALL"],"rollback_executed": true,"resolved_by": null,"resolved_at": null,"duration_seconds": null}
Veto System Definição O Veto System permite que autoridades específicas bloqueiem ações, fluxos ou decisões antes ou durante a execução. Autoridades de Veto VETO_AUTHORITIES: DIR_AISIO_001 (Aísio): scope: ALL_AGENTS | ALL_ACTIONS | ALL_DOMAINS timing: pre_execution | runtime requires_justification: true can_be_overridden_by: CEO_001 veto_weight: 100 (absolute, exceto CEO)
DIR_JESSICA_001 (Jéssica): scope: CONTRACTS | LEGAL_FLOWS | COMPLIANCE timing: pre_execution requires_justification: true (legal basis) can_be_overridden_by: CEO_001 + Aísio veto_weight: 90
CEO_001: scope: EVERYTHING timing: any requires_justification: false (override absolute) can_be_overridden_by: ninguém veto_weight: 200 (supreme)
NODE_LU_001: scope: DOM_DOMESTIC_001 apenas timing: pre_execution | runtime requires_justification: false (humano) can_be_overridden_by: CEO_001 veto_weight: 95 (no domínio doméstico) Tipos de Veto VETO_TYPES: TYPE_1_PREVENTIVE_VETO: description: Bloqueia execução antes de começar applies_to: ações agendadas, propostas, fluxos pendentes resolution: aprovação alternativa ou cancelamento
TYPE_2_RUNTIME_VETO: description: Interrompe execução em andamento applies_to: ações em execução resolution: rollback + investigação
TYPE_3_CONDITIONAL_VETO: description: Bloqueia até condição ser atendida applies_to: ações que dependem de approval resolution: condição deve ser satisfeita
TYPE_4_DOMAIN_VETO: description: Bloqueia todas as ações em um domínio applies_to: domínio inteiro resolution: revisão de governança Procedimento de Veto def execute_veto(veto_authority, target_action, justification, context_id): # 1. Validar autoridade if not has_veto_power(veto_authority, target_action): reject_veto("Insufficient authority")
# 2. Registrar veto
veto_record = {
    "veto_id": generate_id(),
    "authority": veto_authority,
    "target": target_action.id,
    "justification": justification,
    "context_id": context_id,
    "timestamp": now()
}
log_veto(veto_record)

# 3. Notificar partes envolvidas
notify_agent(target_action.agent, f"Action vetoed by {veto_authority}")
notify_manager(target_action.agent.manager)

# 4. Executar veto
if target_action.status == "pending":
    target_action.status = "vetoed"
    target_action.veto_record = veto_record

elif target_action.status == "executing":
    halt_action(target_action)
    trigger_rollback(target_action.context_id)
    target_action.status = "vetoed_and_rolled_back"

# 5. Se veto é de Aísio, verificar se precisa de kill switch
if veto_authority == "DIR_AISIO_001" and is_severe_violation(target_action):
    activate_kill_switch("AGENT_ISOLATION", veto_authority, justification, context_id)

return veto_record
Log de Veto{"veto_id": "VETO_20260124_042","timestamp": "2026-01-24T14:15:00Z","authority": "DIR_JESSICA_001","target_action": "contract_signing_XYZ","target_agent": "AGT_CONT_001","justification": "Cláusula 42 viola LGPD artigo 33","legal_basis": "LGPD Art. 33","context_id": "CTX_456789","resolution": "pending_CEO_review","overridden": false}
Zero Trust Architecture Princípios ZERO_TRUST_PRINCIPLES: never_trust_always_verify: description: Nenhum agente é confiável intrinsecamente enforcement: every_message_verified
least_privilege: description: Agentes têm apenas permissões mínimas necessárias enforcement: AGENT_EXECUTION_CONTRACTS.md
micro_segmentation: description: Domínios são isolados em segmentos menores enforcement: DOMAIN_BOUNDARIES.md
continuous_monitoring: description: Toda ação é monitorada em tempo real enforcement: OBSERVABILITY.md
assume_breach: description: Sistema opera assumindo que pode estar comprometido enforcement: PENTEST_MODEL.md + constant_audit Implementação ZERO_TRUST_IMPLEMENTATION: authentication: type: mTLS + TPM_QUOTE + SPIFFE per_message: true agent_certificates: rotate_daily
# === NOVO: HARDWARE ROOT OF TRUST (Winchester/PBSAI) ===
hardware_attestation:
  required: true
  mechanism: TPM 2.0 (Quote/SHA256)
  enforcement_level: mandatory_for_critical_actions
  fields:
    - tpm_pcr_bank: [0, 1, 2, 3, 4, 5, 6, 7]  # selo de integridade do boot/agente
    - tpm_quote_signature: "signed_by_ak"
    - nonce: "context-driven (anti-replay)"
    - workload_spiffe_id: "spiffe://brachat/agent/{agent_id}"
  
  validation_steps:
    1. verificar se o TPM quote não foi reutilizado (nonce cache)
    2. validar assinatura com AK (Attestation Key) pública registrada
    3. comparar PCRs com baseline aprovado pelo Aísio
    4. verificar SPIFFE ID no registry
  
  failure_action: BLOCK + QUARANTINE + NOTIFY_AISIO

workload_identity:
  type: SPIFFE (Secure Production Identity Framework for Everyone)
  trust_domain: "brachat.internal"
  identity_template: "spiffe://brachat/{layer}/{domain}/{agent_id}"
  refresh_interval_seconds: 3600
Zero Trust Checkpoint (Por Mensagem) def zero_trust_checkpoint(message, context_id): # 1. Verificar autenticidade mTLS if not verify_mtls(message.from): reject_message("Invalid mTLS authentication", context_id)
# === NOVO: HARDWARE ATTESTATION (TPM + SPIFFE) ===
if message.risk_level in ["high", "critical"] or message.intent in ["KILL_SWITCH", "VETO", "SIGN_CONTRACT"]:
    # Exigir atestação de hardware para ações críticas
    if not verify_tpm_quote(message.tpm_attestation, message.from):
        reject_message("TPM quote validation failed - Hardware integrity compromised", context_id)
        activate_kill_switch("HARDWARE_ATTESTATION_FAILURE", context_id)
    
    if not verify_spiffe_id(message.spiffe_id, message.from):
        reject_message("SPIFFE ID mismatch - Workload identity invalid", context_id)
        quarantine_agent(message.from, "SPIFFE_VIOLATION", context_id)

# 2. Verificar autorização
if not is_authorized(message.from, message.to, message.intent):
    reject_message("Not authorized", context_id)

# 3. Verificar domínio
if is_cross_domain(message.from, message.to):
    if not has_cross_domain_approval(context_id):
        reject_message("Cross-domain without approval", context_id)

# 4. Verificar integridade da mensagem
if not verify_signature(message):
    reject_message("Message tampered", context_id)

# 5. Verificar rate limit
if is_rate_limited(message.from):
    reject_message("Rate limit exceeded", context_id)

# 6. Log da verificação (incluindo hashes do TPM)
log_checkpoint(message, context_id, "PASSED", tpm_pcr_hash=message.tpm_attestation.pcr_hash)

return True
def verify_tpm_quote(tpm_attestation, agent_id): """Valida atestação de hardware TPM 2.0"""
# 1. Anti-replay: nonce deve ser único por contexto
if tpm_attestation.nonce in nonce_cache:
    log_violation("TPM_NONCE_REPLAY", agent_id)
    return False

nonce_cache.add(tpm_attestation.nonce, ttl_seconds=300)

# 2. Validar assinatura com AK pública do agente
ak_public_key = get_agent_ak(agent_id)
if not verify_signature(tpm_attestation.quote, tpm_attestation.signature, ak_public_key):
    log_violation("TPM_SIGNATURE_INVALID", agent_id)
    return False

# 3. Comparar PCRs com baseline
baseline_pcrs = get_agent_baseline(agent_id)
for pcr_index in tpm_attestation.pcr_values:
    if tpm_attestation.pcr_values[pcr_index] != baseline_pcrs[pcr_index]:
        log_violation(f"TPM_PCR_{pcr_index}_MISMATCH", agent_id)
        return False

# 4. Verificar SPIFFE ID
if not verify_spiffe_id(tpm_attestation.spiffe_id, agent_id):
    log_violation("SPIFFE_ID_MISMATCH", agent_id)
    return False

return True
--------------------------------------------------------------------------------
Chronicle Framework Definição Chronicle Framework é o sistema de versionamento, snapshot e rollback que garante que o sistema pode voltar a qualquer estado anterior válido. Componentes CHRONICLE_COMPONENTS: DUAL_VOTE: description: Decisões críticas requerem 2 autoridades applies_to:
kill_switch_activation
contract_approval_above_R$50000
policy_change
agent_creation
domain_boundary_change
voting_mechanism: type: two_party valid_pairs: - [CEO_001, DIR_AISIO_001] - [DIR_AISIO_001, DIR_JESSICA_001] - [CEO_001, DIR_JESSICA_001]
execution:
proposal_created
vote_1_cast
vote_2_cast
if_both_approve: execute
if_any_reject: veto + log
SNAPSHOT_STATE_SYSTEM: description: Captura estado completo do sistema em intervalos frequency: critical: a cada ação high: a cada 5 minutos medium: a cada 1 hora low: a cada 24 horas
snapshot_contents:
  - agent_states
  - memory_contents
  - pending_actions
  - execution_logs
  - governance_policies

storage:
  location: immutable_object_store
  retention_days: 30
  encryption: required
  integrity_hash: SHA-256
ROLLBACK: description: Retorna sistema a snapshot anterior triggers: - kill_switch_activation - veto_execution - security_violation - data_corruption - manual_request (Aísio ou CEO)
rollback_levels:
  LEVEL_1_ACTION: desfaz última ação
  LEVEL_2_CONTEXT: desfaz todo contexto
  LEVEL_3_TIMESTAMP: volta a timestamp específico
  LEVEL_4_SNAPSHOT: restaura snapshot completo

procedure:
  - halt_current_executions
  - validate_snapshot_integrity
  - restore_snapshot
  - replay_logs_after_snapshot (se necessário)
  - validate_system_state
  - resume_operations
  - log_rollback
DUAL VOTE Implementation def dual_vote(proposal, context_id): # 1. Identificar votantes necessários required_voters = get_required_voters(proposal.type)
# 2. Coletar votos
votes = []
for voter in required_voters:
    vote = request_vote(voter, proposal, context_id)
    votes.append(vote)

# 3. Verificar resultado
if all(vote.approved for vote in votes):
    # Aprovado
    log_event({
        "event": "DUAL_VOTE_PASSED",
        "proposal": proposal,
        "votes": votes,
        "context_id": context_id
    })
    return True
else:
    # Rejeitado
    log_event({
        "event": "DUAL_VOTE_REJECTED",
        "proposal": proposal,
        "votes": votes,
        "rejection_reason": get_rejection_reason(votes),
        "context_id": context_id
    })

    # Notificar Aísio
    notify_aisio(f"Dual vote rejected: {proposal}")

    return False
SNAPSHOT Implementation SNAPSHOT_SCHEDULE: critical_actions: - contract_signing - policy_change - agent_registry_modification - kill_switch_activation snapshot_before: true snapshot_after: true
high_frequency: interval_seconds: 300 agents_to_snapshot: [DIRECTOR, MANAGER]
medium_frequency: interval_minutes: 60 agents_to_snapshot: ALL_AGENTS
low_frequency: interval_hours: 24 agents_to_snapshot: FULL_SYSTEM ROLLBACK Procedure def chronicle_rollback(target, context_id, triggered_by): # 1. Validar autorização if triggered_by not in ["DIR_AISIO_001", "CEO_001"]: reject_rollback("Unauthorized")
# 2. Determinar nível de rollback
if isinstance(target, str) and target.startswith("snapshot_"):
    level = "SNAPSHOT"
    snapshot_id = target
elif isinstance(target, int):  # timestamp
    level = "TIMESTAMP"
    timestamp = target
elif isinstance(target, str):  # context_id
    level = "CONTEXT"
    context_id_target = target
else:  # última ação
    level = "ACTION"

# 3. Executar rollback
if level == "SNAPSHOT":
    halt_system()
    snapshot = load_snapshot(snapshot_id)
    validate_snapshot_integrity(snapshot)
    restore_system(snapshot)
    resume_system()

elif level == "TIMESTAMP":
    halt_system()
    snapshot = find_snapshot_before(timestamp)
    restore_system(snapshot)
    # Replay ações não perigosas após timestamp
    replay_safe_actions(timestamp)
    resume_system()

elif level == "CONTEXT":
    actions = get_actions_by_context(context_id_target)
    for action in reversed(actions):
        reverse_action(action)

elif level == "ACTION":
    last_action = get_last_action()
    reverse_action(last_action)

# 4. Log do rollback
log_rollback({
    "rollback_id": generate_id(),
    "level": level,
    "target": target,
    "triggered_by": triggered_by,
    "context_id": context_id,
    "timestamp": now()
})

# 5. Notificar partes
notify_aisio(f"Rollback executed: {level}")
notify_ceo_if_critical(level)
--------------------------------------------------------------------------------
Policy Reason Definição Reasoning (raciocínio autônomo, tomada de decisão não determinística) é PROIBIDO em runtime e em agentes operacionais. Regras POLICY_REASON: PERMITIDO_APENAS_EM:
CEO_001 (estratégia)
DIRETORES (planejamento)
GERENTES (coordenação, limitado)
PROIBIDO_EM: - QUALQUER_AGENT (layer AGENT) - RUNTIME (execução operacional) - WORKERS (Strands) - NICE e subagentes domésticos
RAZÕES: - Determinismo é obrigatório para auditabilidade - Reasoning introduz não-determinismo e risco - Agentes operacionais devem executar, não pensar
EXCEÇÕES: - Nenhuma. Policy absoluta. Enforcement REASON_ENFORCEMENT: detection: - pattern_analysis em logs - tempo de execução anormal - decisões não previstas no contrato - desvio do fluxo esperado
violation_consequence:- immediate_halt- quarantine_agent- mandatory_audit- agent_downgrade (se reincidente)- notificação ao Aísio
Execution Guarantee Condições de Validade do Sistema O sistema só é considerado OPERACIONAL se TODAS as condições forem verdadeiras: EXECUTION_GUARANTEE: CONDITION_1_REGISTRY_COMPLETO: description: Todos os agentes no AGENT_REGISTRY.md validation: bootstrap_validation failure_consequence: system_not_operational
CONDITION_2_EXECUTION_CONTRACTS: description: Todos os agentes têm contratos assinados validation: contract_validation failure_consequence: agent_suspended
CONDITION_3_LOGS_COMPLETOS: description: Toda ação tem log estruturado validation: real_time_monitoring failure_consequence: kill_switch
CONDITION_4_PERMISSÕES_VÁLIDAS: description: Nenhuma ação fora de permissões validation: zero_trust_checkpoint failure_consequence: action_blocked + audit
CONDITION_5_NOTEBOOK_ATUALIZADO: description: NotebookLLM é source of truth validation: version_check failure_consequence: system_read_only
CONDITION_6_NO_ORPHAN_ACTIONS: description: Toda ação tem context_id validation: traceability_check failure_consequence: action_rejected
CONDITION_7_AISIO_MONITORING: description: Aísio está ativo e monitorando validation: heartbeat_check failure_consequence: system_halt Verificação de Runtime def verify_execution_guarantee(): results = {}
# Verificar cada condição
results["registry"] = verify_registry_complete()
results["contracts"] = verify_all_contracts_signed()
results["logs"] = verify_logs_complete_last_hour()
results["permissions"] = verify_no_permission_violations_last_hour()
results["notebook"] = verify_notebook_up_to_date()
results["traceability"] = verify_all_actions_have_context_id()
results["aisio"] = verify_aisio_heartbeat()

# Se alguma falhou
if not all(results.values()):
    log_failure(results)
    notify_aisio("EXECUTION_GUARANTEE_FAILED", results)

    if results["logs"] == False or results["permissions"] == False:
        activate_kill_switch(
            mode="DOMAIN_HALT",
            triggered_by="SYSTEM",
            reason=f"Execution guarantee failed: {results}",
            context_id=generate_context_id()
        )

    return False

return True
--------------------------------------------------------------------------------
Hierarquia de Governança graph TD SUPREME[👑 SUPREME GOVERNANCE<br/>CEO_001<br/>Override Final Absoluto]
PRIMARY[🛡️ PRIMARY GOVERNANCE<br/>DIR_AISIO_001<br/>Veto Universal + Kill Switch]
SECONDARY[⚖️ SECONDARY GOVERNANCE<br/>DIR_JESSICA_001<br/>Veto Legal + Compliance]
TACTICAL[📊 TACTICAL GOVERNANCE<br/>MANAGERS<br/>Policy Enforcement]
SUPREME --> PRIMARY SUPREME --> SECONDARY PRIMARY --> TACTICAL SECONDARY --> TACTICAL
style SUPREME fill:#f66,stroke:#333,stroke-width:4px style PRIMARY fill:#ff9,stroke:#333,stroke-width:2px style SECONDARY fill:#9f9,stroke:#333,stroke-width:2px Poderes por Nível Nível Quem Pode Vetar Pode Aprovar Pode Auditar Pode Matar Supremo CEO_001 Tudo Tudo Tudo Tudo Primário DIR_AISIO_001 Tudo (exceto CEO) Security Tudo Sim Secundário DIR_JESSICA_001 Legal/Contratos Legal Legal Não Tático MANAGERS Domain Operational Domain Não
--------------------------------------------------------------------------------
Fluxo de Aprovação Níveis de Aprovação APPROVAL_LEVELS: LEVEL_0_NONE: description: Ações rotineiras, baixo risco examples: [consultar_status, gerar_relatorio] required_approvals: 0
LEVEL_1_MANAGER: description: Ações com risco moderado examples: [alocar_recurso, modificar_agenda] required_approvals: 1 (MANAGER)
LEVEL_2_DIRECTOR: description: Ações com risco alto examples: [aprovar_orcamento_acima_R$5000, modificar_policy] required_approvals: 1 (DIRECTOR)
LEVEL_3_DUAL: description: Ações críticas examples: [assinar_contrato, kill_switch, mudar_boundary] required_approvals: 2 (DUAL_VOTE)
LEVEL_4_CEO: description: Ações estratégicas irreversíveis examples: [expandir_ecossistema, modificar_governanca_base] required_approvals: 1 (CEO_001) Fluxograma de Aprovação graph LR A[Ação Solicitada] --> B{Determinar Nível} B -->|LEVEL 0| C[Execução Imediata] B -->|LEVEL 1| D[Aprovação Manager] B -->|LEVEL 2| E[Aprovação Director] B -->|LEVEL 3| F[Dual Vote] B -->|LEVEL 4| G[Aprovação CEO]
D --> H{Manager Aprova?}
E --> I{Director Aprova?}
F --> J{Aísio + Jéssica/CEO?}
G --> K{CEO Aprova?}

H -->|Sim| C
H -->|Não| L[Vetado + Log]
I -->|Sim| C
I -->|Não| L
J -->|Sim| C
J -->|Não| L
K -->|Sim| C
K -->|Não| L
--------------------------------------------------------------------------------
Validação de Governança Para o sistema ser OPERACIONAL: GOVERNANCE_VALIDATION: pre_bootstrap: - GOVERNANCE.md presente e completo - Todas as regras invariantes definidas - Kill switch testado - Veto system validado - Zero trust implementado - Chronicle framework ativo
runtime: - Aísio monitorando ativamente - Kill switch testado a cada 24h (simulado) - Logs de governança íntegros - Nenhuma violação de policy nas últimas 24h
failure_response:- Tempo máximo para kill switch: 1 segundo- Tempo máximo para rollback: 30 segundos- Notificação Aísio: imediata- Log de governança: imutável
Logs de Governança (Formato Obrigatório){"governance_log": {"event_id": "GOV_20260124_001","timestamp": "2026-01-24T10:30:00Z","event_type": "KILL_SWITCH | VETO | DUAL_VOTE | ROLLBACK | POLICY_VIOLATION","triggered_by": "agent_id","target": "action_id | agent_id | domain_id","justification": "string","context_id": "string","snapshot_id": "string (se aplicável)","resolution": "resolved | pending | overridden","hash": "SHA-256 do evento completo"}}
Fim do MóduloStatus: GOVERNANCE.md COMPLETO (unificado com todos os subdocumentos)Contém:Regras Globais do Sistema ✅Kill Switch ✅Veto System ✅Zero Trust Architecture ✅Chronicle Framework (Dual Vote + Snapshot + Rollback) ✅Policy Reason ✅Execution Guarantee ✅Hierarquia de Governança ✅Fluxo de Aprovação ✅
BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)
PASSO 4 — 04_RUNTIME_ARCHITECTURE/
📄 HERMES_SPEC.md
# HERMES_SPEC.md — Interface Principal de Orquestração

## Princípio Fundamental

Hermes é a **interface principal de orquestração** do sistema BRACHÁT. Toda mensagem, evento e requisição entre agentes passa pelo Hermes. É o barramento central que garante rastreabilidade, validação e roteamento.

---

## Arquitetura do Hermes

```mermaid
graph TB
    subgraph INPUT_LAYER
        A1[Agente Origem]
        A2[Mensagem]
        A3[Evento]
    end

    subgraph HERMES_CORE
        H1[Validador de Mensagens]
        H2[Roteador]
        H3[Fila de Prioridade]
        H4[Transformador]
    end

    subgraph OUTPUT_LAYER
        O1[Agente Destino]
        O2[Governança]
        O3[Logger]
    end

    A1 --> H1
    A2 --> H1
    A3 --> H1
    H1 --> H2
    H2 --> H3
    H3 --> H4
    H4 --> O1
    H4 --> O2
    H4 --> O3
--------------------------------------------------------------------------------
Componentes do Hermes
1. Message Validator
MESSAGE_VALIDATOR:
  functions:
    - validate_schema: verifica formato obrigatório
    - authenticate_origin: valida mTLS do agente
    - check_permissions: verifica se origem pode falar com destino
    - validate_context: context_id deve existir e ser válido
    - check_rate_limit: evita spam e overload

  validation_failure_actions:
    - reject_message
    - log_violation
    - notify_aisio (se severity > MEDIUM)
    - increment_agent_error_counter
2. Router
ROUTER:
  routing_logic:
    - direct: origem → destino (mesmo domínio)
    - governance: passa por Aísio se cross-domain
    - broadcast: para múltiplos agentes (apenas CEO)
    - queue: para filas de prioridade

  routing_table:
    intra_domain: rota direta
    cross_domain: rota via governance_checkpoint
    to_governance: rota prioridade máxima
    to_ceo: rota com confirmação de entrega
3. Priority Queue
PRIORITY_QUEUE:
  levels:
    CRITICAL:
      - kill_switch_commands
      - veto_orders
      - CEO_commands
      queue_size: 10
      processing_ms: 0 (imediato)

    HIGH:
      - governance_messages
      - legal_approvals
      - contract_actions
      queue_size: 100
      processing_ms: 100

    NORMAL:
      - operational_commands
      - agent_communication
      queue_size: 1000
      processing_ms: 500

    LOW:
      - status_queries
      - reports
      queue_size: 10000
      processing_ms: 2000
4. Message Transformer
MESSAGE_TRANSFORMER:
  transformations:
    - enrich_context: adiciona timestamp, trace_id, sequence
    - normalize_schema: garante formato padrão
    - encrypt_payload: se contém dados sensíveis
    - compress_large_payload: > 1MB
    - add_digital_signature: integridade
--------------------------------------------------------------------------------
Protocolo de Mensagem Hermes
Formato Interno Hermes (Após Processamento)
{
  "hermes_envelope": {
    "hermes_id": "HRM_20260124_001",
    "received_at": "2026-01-24T10:30:00.123Z",
    "processing_time_ms": 45,
    "priority": "NORMAL",
    "ttl_seconds": 60,
    "retry_count": 0,
    "trace_path": ["HERMES", "VALIDATOR", "ROUTER", "TRANSFORMER"]
  },
  "original_message": {
    "from": "agent_id",
    "to": "agent_id",
    "intent": "string",
    "context_id": "string",
    "risk_level": "low|medium|high|critical",
    "requires_approval": true|false,
    "payload": {}
  },
  "hermes_metadata": {
    "validation_result": "PASSED",
    "routing_path": ["validator", "router", "priority_queue", "transformer"],
    "size_bytes": 2048,
    "signature": "sha256_hash"
  }
}
--------------------------------------------------------------------------------
Endpoints Hermes
API de Envio
POST /hermes/send:
  request:
    headers:
      - X-Agent-ID: string (obrigatório)
      - X-Agent-Token: string (mTLS)
      - X-Context-ID: string (obrigatório)

    body: MESSAGE_SCHEMA

  response:
    200:
      body:
        hermes_id: string
        status: "queued|delivered|rejected"
        estimated_delivery_ms: integer

    400: Bad request (schema inválido)
    401: Unauthorized (autenticação falhou)
    403: Forbidden (permissão negada)
    429: Rate limit exceeded
API de Status
GET /hermes/status/{hermes_id}:
  response:
    status: "pending|delivered|failed|expired"
    current_queue_position: integer
    last_attempt: timestamp
    error: string (se failed)
API de Admin (Aísio/CEO)
POST /hermes/admin/flush:
  description: Limpa todas as filas
  auth: DIR_AISIO_001 ou CEO_001

POST /hermes/admin/pause:
  description: Pausa processamento
  auth: DIR_AISIO_001 ou CEO_001

GET /hermes/admin/metrics:
  description: Métricas do Hermes
  response:
    messages_processed_total: integer
    messages_per_second: float
    queue_sizes: object
    avg_processing_time_ms: float
--------------------------------------------------------------------------------
Garantias do Hermes
HERMES_GUARANTEES:
  at_least_once_delivery: true
  message_ordering: true (por priority e timestamp)
  persistence: true (logs imutáveis)
  idempotency: via hermes_id
  dead_letter_queue: true (mensagens não entregues)
  max_retries: 3
  retry_backoff_ms: [100, 500, 2000]
  ttl_default_seconds: 60
--------------------------------------------------------------------------------
Monitoramento Hermes
HERMES_METRICS:
  - messages_received_total
  - messages_delivered_total
  - messages_failed_total
  - messages_rejected_total
  - queue_depth_by_priority
  - avg_latency_ms
  - p95_latency_ms
  - p99_latency_ms
  - active_connections
  - rate_limit_hits
--------------------------------------------------------------------------------
Logs Hermes (Formato)
{
  "hermes_log": {
    "hermes_id": "HRM_20260124_001",
    "event_type": "MESSAGE_RECEIVED | MESSAGE_VALIDATED | MESSAGE_ROUTED | MESSAGE_DELIVERED | MESSAGE_FAILED",
    "timestamp": "2026-01-24T10:30:00.123Z",
    "from_agent": "AGT_XXX",
    "to_agent": "AGT_YYY",
    "context_id": "CTX_789",
    "priority": "NORMAL",
    "processing_time_ms": 45,
    "queue_wait_time_ms": 120,
    "status": "SUCCESS|FAILED",
    "failure_reason": "string (se failed)"
  }
}

---

### 📄 STRANDS_SPEC.md

```markdown
# STRANDS_SPEC.md — Execução Operacional Determinística

## Princípio Fundamental

Strands é o **framework de execução operacional** para agentes de nível AGENT. É **puramente determinístico**, **cego** (sem reasoning), e **rápido**. Strands NÃO toma decisões — apenas executa instruções pré-aprovadas.

---

## Filosofia Strands

```yaml
STRANDS_PHILOSOPHY:
  deterministic: true
  no_reasoning: true
  no_llm_calls: true
  pure_execution: true
  pre_approved_paths: true
  sandboxed: true

  design_principles:
    - "Execute, não pense"
    - "Rápido e determinístico"
    - "Log tudo"
    - "Falhe rápido"
    - "Nunca decida sozinho"
--------------------------------------------------------------------------------
Arquitetura Strands
graph LR
    subgraph INPUT
        I1[Instrução Hermes]
        I2[Workflow Pré-definido]
    end

    subgraph STRANDS_CORE
        S1[Parser]
        S2[Validator]
        S3[Executor]
        S4[Logger]
    end

    subgraph OUTPUT
        O1[Ação Executada]
        O2[Resultado]
        O3[Log]
    end

    I1 --> S1
    I2 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> O1
    S4 --> O2
    S4 --> O3
--------------------------------------------------------------------------------
Worker Model
Tipos de Workers
STRANDS_WORKERS:
  TYPE_1_TRANSFORMER:
    description: Transforma dados de um formato para outro
    operations:
      - map: aplica função a cada elemento
      - filter: remove elementos por condição
      - reduce: agrega valores
    no_side_effects: true
    pure_function: true

  TYPE_2_VALIDATOR:
    description: Valida dados contra schema
    operations:
      - schema_validation
      - type_checking
      - range_validation
    output: boolean + errors

  TYPE_3_EXECUTOR:
    description: Executa ação com side effects
    operations:
      - api_call
      - database_write
      - file_operation
    requires_approval: se destructive

  TYPE_4_AGGREGATOR:
    description: Agrega resultados de múltiplos workers
    operations:
      - join
      - merge
      - concat
    wait_for_all: true
Worker Definition
worker_definition:
  id: string
  type: TRANSFORMER | VALIDATOR | EXECUTOR | AGGREGATOR
  input_schema: object
  output_schema: object
  function: |
    # Código puro, sem LLM, sem I/O não especificado
    def execute(input):
        # deterministic logic only
        return output
  timeout_seconds: 30
  retry_count: 0 (fail fast)
--------------------------------------------------------------------------------
Workflow Strands
Workflow Definition
workflow_definition:
  id: string
  name: string
  version: integer
  steps:
    - step_id: string
      worker_id: string
      depends_on: [step_ids]
      on_failure: FAIL | SKIP | RETRY
  input_binding: object
  output_binding: object
Exemplo de Workflow
workflow_id: "WF_DOMESTIC_SHOPPING_001"
name: "Processamento de Lista de Compras"
version: 1

steps:
  - step_id: "validate_budget"
    worker_id: "VAL_BUDGET_001"
    depends_on: []
    on_failure: "FAIL"

  - step_id: "check_inventory"
    worker_id: "TRF_INVENTORY_001"
    depends_on: ["validate_budget"]
    on_failure: "SKIP"

  - step_id: "calculate_total"
    worker_id: "TRF_CALC_TOTAL_001"
    depends_on: ["validate_budget", "check_inventory"]
    on_failure: "FAIL"

  - step_id: "create_order"
    worker_id: "EXE_CREATE_ORDER_001"
    depends_on: ["calculate_total"]
    on_failure: "RETRY"

input_binding:
  budget_limit: "$.payload.budget"
  items: "$.payload.shopping_list"

output_binding:
  total: "$.steps.calculate_total.output.total"
  order_id: "$.steps.create_order.output.order_id"
--------------------------------------------------------------------------------
Strands vs Reasoning
STRANDS_VS_REASONING:

  STRANDS (PERMITIDO):
    - if/then baseado em dados
    - switch/case determinístico
    - cálculos matemáticos
    - transformações de dados
    - validações de schema
    - chamadas de API pré-definidas

  REASONING (PROIBIDO):
    - LLM calls
    - Decisões não determinísticas
    - "Pensar" sobre o que fazer
    - Criar novos planos em runtime
    - Avaliar múltiplas opções com LLM
    - Qualquer uso de linguagem natural para decisão

  DETECTION:
    - Strands bloqueia automaticamente chamadas a LLM
    - Timeout em operações "suspeitas"
    - Análise de padrões de execução
--------------------------------------------------------------------------------
Strands Runtime
Ciclo de Execução
def strands_execute(workflow_id, input_data, context_id):
    # 1. Carregar workflow
    workflow = load_workflow(workflow_id)

    # 2. Validar input contra schema
    if not validate_input(input_data, workflow.input_schema):
        log_error("Input validation failed", context_id)
        return {"status": "FAILED", "reason": "invalid_input"}

    # 3. Executar steps em ordem (DAG)
    results = {}
    for step in topological_sort(workflow.steps):
        # Verificar dependências
        if not all(dep in results for dep in step.depends_on):
            continue

        # Executar worker
        try:
            step_input = bind_input(step, input_data, results)
            step_result = run_worker(step.worker_id, step_input)
            results[step.step_id] = step_result

        except Exception as e:
            if step.on_failure == "FAIL":
                log_error(f"Step {step.step_id} failed", context_id)
                return {"status": "FAILED", "reason": str(e), "step": step.step_id}
            elif step.on_failure == "SKIP":
                results[step.step_id] = {"status": "SKIPPED"}
            elif step.on_failure == "RETRY":
                # Tentar até 3 vezes
                for attempt in range(3):
                    try:
                        step_result = run_worker(step.worker_id, step_input)
                        results[step.step_id] = step_result
                        break
                    except:
                        if attempt == 2:
                            raise

    # 4. Bind output
    output = bind_output(workflow.output_binding, results)

    # 5. Log tudo
    log_execution(workflow_id, input_data, output, context_id)

    return {"status": "SUCCESS", "output": output}
Garantias de Execução
STRANDS_GUARANTEES:
  deterministic: true (same input → same output)
  no_side_effects_unless_executor: true
  timeout_enforced: true
  memory_limit_mb: 256
  cpu_limit_percent: 50
  no_network_unless_approved: true
  no_file_system_write_unless_approved: true
--------------------------------------------------------------------------------
Strands Workers Built-in
Workers de Transformação
builtin_transformers:
  - json_parser: string → object
  - csv_parser: string → array
  - date_formatter: timestamp → string
  - number_aggregator: array → sum|avg|min|max
  - string_template: template + vars → string
  - filter_by_condition: array → filtered_array
  - sort_by_field: array → sorted_array
Workers de Validação
builtin_validators:
  - schema_validator: object + schema → boolean
  - range_validator: number + min/max → boolean
  - regex_validator: string + pattern → boolean
  - presence_validator: object + field → boolean
  - type_validator: any + expected_type → boolean
Workers de Execução (Limitados)
builtin_executors:
  - http_get: url → response (aprovado whitelist)
  - http_post: url + body → response (aprovado whitelist)
  - db_query: query → results (read-only)
  - file_read: path → content (whitelist paths)
  - send_message: agent + payload → confirmation
--------------------------------------------------------------------------------
Strands Logs
{
  "strands_log": {
    "execution_id": "STR_20260124_001",
    "workflow_id": "WF_DOMESTIC_SHOPPING_001",
    "context_id": "CTX_789",
    "start_time": "2026-01-24T10:30:00Z",
    "end_time": "2026-01-24T10:30:00.250Z",
    "duration_ms": 250,
    "steps_executed": 4,
    "steps_failed": 0,
    "status": "SUCCESS",
    "input_hash": "sha256...",
    "output_hash": "sha256...",
    "deterministic_check": "PASSED"
  }
}

---

### 📄 LANGGRAPH_RULES.md

```yaml
# LANGGRAPH_RULES.md — Regras para Fluxo Determinístico

## Princípio Fundamental

LangGraph no sistema BRACHÁT é utilizado EXCLUSIVAMENTE para orquestração de fluxos determinísticos. É PROIBIDO usar LangGraph para reasoning, LLM calls autônomas ou decisões não pré-aprovadas.

---

## Regras Obrigatórias

```yaml
LANGGRAPH_MANDATORY_RULES:

  RULE_1_STATE_MACHINE_ONLY:
    description: LangGraph define apenas state machines
    allowed: true
    forbidden:
      - agent_nodes_with_llm_decisions
      - conditional_branching_baseado_em_llm
      - cycles_não_determinísticos

  RULE_2_NO_AUTONOMOUS_REASONING:
    description: Nodes não podem conter LLM calls autônomas
    enforcement: pre_deployment_scan
    violation: deployment_blocked

  RULE_3_PRE_APPROVED_PATHS:
    description: Todos os paths do graph devem ser pré-aprovados
    validation: governance_approval_required
    approvers: [DIR_AISIO_001, Gerente responsável]

  RULE_4_STATE_VALIDATION:
    description: Estado deve ser validado a cada transição
    validator: schema_validation
    on_failure: halt_execution

  RULE_5_LOGGING_EVERY_NODE:
    description: Cada node deve gerar log estruturado
    format: structured_json
    mandatory_fields: [node_id, input_state, output_state, timestamp]
--------------------------------------------------------------------------------
Estrutura de State Machine
State Definition
state_definition:
  schema:
    type: object
    required: [context_id, current_node, data]
    properties:
      context_id: string
      current_node: string
      previous_nodes: array
      data: object
      error: string | null
      retry_count: integer
      timestamp: string

  valid_transitions:
    - from: "start"
      to: ["validation", "error"]
    - from: "validation"
      to: ["processing", "error"]
    - from: "processing"
      to: ["completion", "error", "rollback"]
    - from: "completion"
      to: ["end"]
    - from: "error"
      to: ["rollback", "halt"]
    - from: "rollback"
      to: ["recovery", "halt"]
Node Definition
node_definition:
  id: string
  type: "strands_worker | validator | router | terminator"
  worker_id: string (se type = strands_worker)
  timeout_seconds: integer
  retry_policy:
    max_retries: integer
    backoff_ms: integer
  on_success: string (next_node)
  on_failure: string (error_node)
  on_timeout: string (timeout_node)
--------------------------------------------------------------------------------
Exemplo de LangGraph Flow
flow_id: "FLOW_ORDER_PROCESSING"
name: "Processamento de Pedido"
version: 1

graph:
  nodes:
    - id: "validate_order"
      type: "validator"
      worker_id: "VAL_ORDER_001"
      timeout_seconds: 5
      retry_policy: { max_retries: 1, backoff_ms: 100 }
      on_success: "check_inventory"
      on_failure: "error_handler"

    - id: "check_inventory"
      type: "strands_worker"
      worker_id: "WF_INVENTORY_CHECK"
      timeout_seconds: 10
      retry_policy: { max_retries: 2, backoff_ms: 500 }
      on_success: "calculate_price"
      on_failure: "out_of_stock_handler"

    - id: "calculate_price"
      type: "strands_worker"
      worker_id: "WF_PRICE_CALC"
      timeout_seconds: 5
      on_success: "create_order"
      on_failure: "error_handler"

    - id: "create_order"
      type: "strands_worker"
      worker_id: "WF_CREATE_ORDER"
      timeout_seconds: 15
      on_success: "completion"
      on_failure: "rollback_handler"

    - id: "completion"
      type: "terminator"
      status: "SUCCESS"

    - id: "error_handler"
      type: "terminator"
      status: "FAILED"
      log_error: true

    - id: "out_of_stock_handler"
      type: "terminator"
      status: "OUT_OF_STOCK"
      notify_customer: true

    - id: "rollback_handler"
      type: "strands_worker"
      worker_id: "WF_ROLLBACK_ORDER"
      on_success: "error_handler"

  start_node: "validate_order"
--------------------------------------------------------------------------------
Validação de LangGraph
Pre-deployment Validation
def validate_langgraph_flow(flow_definition):
    errors = []

    # 1. Verificar se há LLM calls em nodes
    for node in flow_definition.graph.nodes:
        if has_llm_call(node):
            errors.append(f"Node {node.id} contains forbidden LLM call")

    # 2. Verificar ciclos não determinísticos
    if has_undetermined_cycles(flow_definition.graph):
        errors.append("Flow contains non-deterministic cycles")

    # 3. Verificar se todos os paths têm handler
    unreachable = find_unreachable_nodes(flow_definition.graph)
    if unreachable:
        errors.append(f"Unreachable nodes: {unreachable}")

    # 4. Verificar timeouts
    for node in flow_definition.graph.nodes:
        if node.timeout_seconds > 60:
            errors.append(f"Node {node.id} timeout too high: {node.timeout_seconds}s")

    # 5. Verificar logs
    if not has_logging_on_all_nodes(flow_definition):
        errors.append("Missing logging configuration on some nodes")

    return {"valid": len(errors) == 0, "errors": errors}
--------------------------------------------------------------------------------
LangGraph + Strands Integration
INTEGRATION_PATTERN:
  LangGraph_Node:
    type: "strands_worker"
    calls: Strands workflow

  Strands_Workflow:
    type: "pure_deterministic"
    calls: no nested LangGraph

  Communication:
    LangGraph → Strands: via state.data
    Strands → LangGraph: via return value

  Prohibited:
    - Strands calling LangGraph (recursion risk)
    - LangGraph nodes with embedded Strands (use worker pattern)
--------------------------------------------------------------------------------
LangGraph Logs
{
  "langgraph_log": {
    "execution_id": "LG_20260124_001",
    "flow_id": "FLOW_ORDER_PROCESSING",
    "context_id": "CTX_789",
    "start_time": "2026-01-24T10:30:00Z",
    "end_time": "2026-01-24T10:30:00.500Z",
    "nodes_visited": [
      "validate_order",
      "check_inventory",
      "calculate_price",
      "create_order",
      "completion"
    ],
    "final_state": "SUCCESS",
    "state_transitions": [
      {
        "from": "start",
        "to": "validate_order",
        "timestamp": "...",
        "duration_ms": 10
      },
      {
        "from": "validate_order",
        "to": "check_inventory",
        "timestamp": "...",
        "duration_ms": 45
      },
      {
        "from": "check_inventory",
        "to": "calculate_price",
        "timestamp": "...",
        "duration_ms": 120
      },
      {
        "from": "calculate_price",
        "to": "create_order",
        "timestamp": "...",
        "duration_ms": 30
      },
      {
        "from": "create_order",
        "to": "completion",
        "timestamp": "...",
        "duration_ms": 250
      }
    ],
    "total_duration_ms": 500,
    "deterministic": true
  }
}

---

### 📄 CREWAI_RULES.md

```yaml
# CREWAI_RULES.md — Validação Redundante e Controles

## Princípio Fundamental

CrewAI no sistema BRACHÁT é utilizado EXCLUSIVAMENTE para **validação redundante** e **coordenação de equipes pré-aprovadas**. É PROIBIDO execução direta de agentes via CrewAI — toda execução deve passar por Hermes + Strands.

---

## Regras Obrigatórias

```yaml
CREWAI_MANDATORY_RULES:

  RULE_1_VALIDATION_ONLY:
    description: CrewAI valida, NÃO executa
    allowed: [task_validation, output_validation, cross_check]
    forbidden: [agent_execution, tool_calls, llm_actions]

  RULE_2_REDUNDANCY_MANDATORY:
    description: Toda ação crítica deve ter validação redundante
    applies_to: [contratos, pagamentos_acima_R$1000, mudanças_policy]
    validators: mínimo 2 agentes diferentes

  RULE_3_NO_DIRECT_EXECUTION:
    description: CrewAI nunca chama agentes diretamente
    enforcement: architectural_enforcement
    alternative: usar Hermes para orquestração

  RULE_4_OUTPUT_VALIDATION:
    description: Resultados de agentes devem ser validados
    validator: CrewAI_team
    before_commit: true

  RULE_5_CROSS_VALIDATION:
    description: Múltiplos agentes validam o mesmo resultado
    team_size: 2-3 agentes
    consensus_required: true
--------------------------------------------------------------------------------
CrewAI Team Definitions
Team Structure
team_definition:
  id: string
  name: string
  purpose: "validation | cross_check | consensus"
  members:
    - agent_id: string
      role: "validator"
      weight: integer (1-10)
  validation_rules:
    - rule_id: string
      type: "schema | consensus | business_logic"
      threshold: float (0-1)

  quorum_required: boolean
  quorum_percentage: float
Exemplo de Time de Validação
team_id: "TEAM_VALIDATE_CONTRACT_001"
name: "Validação de Contratos"
purpose: "cross_check"

members:
  - agent_id: "AGT_CONT_JUR_001"
    role: "primary_validator"
    weight: 3

  - agent_id: "AGT_COMPL_001"
    role: "compliance_validator"
    weight: 3

  - agent_id: "AGT_REVISAO_001"
    role: "technical_validator"
    weight: 2

validation_rules:
  - rule_id: "schema_complete"
    type: "schema"
    threshold: 1.0

  - rule_id: "no_forbidden_clauses"
    type: "business_logic"
    threshold: 1.0

  - rule_id: "agent_consensus"
    type: "consensus"
    threshold: 0.8 # 80% agreement

quorum_required: true
quorum_percentage: 0.67 # 2 de 3 membros
--------------------------------------------------------------------------------
Validação Redundante
Processo de Validação
def crewai_validate(team_id, target_object, context_id):
    # 1. Carregar time
    team = load_team(team_id)

    # 2. Cada membro valida independentemente
    results = []
    for member in team.members:
        result = member.validate(target_object, context_id)
        results.append({
            "agent_id": member.agent_id,
            "valid": result.valid,
            "confidence": result.confidence,
            "issues": result.issues
        })

    # 3. Aplicar regras de validação
    final_validation = {"valid": True, "details": []}

    for rule in team.validation_rules:
        if rule.type == "schema":
            passed = validate_schema(target_object, rule.schema)
            if not passed and rule.threshold == 1.0:
                final_validation["valid"] = False
                final_validation["details"].append(f"Schema validation failed: {rule.rule_id}")

        elif rule.type == "consensus":
            valid_votes = sum(1 for r in results if r["valid"])
            consensus_ratio = valid_votes / len(results)
            if consensus_ratio < rule.threshold:
                final_validation["valid"] = False
                final_validation["details"].append(f"Consensus failed: {consensus_ratio} < {rule.threshold}")

        elif rule.type == "business_logic":
            for result in results:
                if not result["valid"] and result["confidence"] > 0.8:
                    final_validation["valid"] = False
                    final_validation["details"].append(f"Business logic failed: {result['issues']}")

    # 4. Log
    log_validation(team_id, target_object, results, final_validation, context_id)

    return final_validation
--------------------------------------------------------------------------------
CrewAI + Hermes Integration
INTEGRATION_PATTERN:
  Execution_Flow:
    step_1: Agent executa ação via Strands
    step_2: Resultado enviado para CrewAI team
    step_3: CrewAI valida resultado
    step_4: Se válido → commit via Hermes
    step_5: Se inválido → rejeita + notifica Aísio

  Communication:
    Agent → CrewAI: via Hermes (validation request)
    CrewAI → Agent: via Hermes (validation result)
    CrewAI → Governance: se falha crítica

  Prohibited:
    - CrewAI chamando agentes diretamente
    - CrewAI executando side effects
    - CrewAI modificando estado do sistema
--------------------------------------------------------------------------------
Validação de CrewAI Teams
Pre-deployment Validation
def validate_crewai_team(team_definition):
    errors = []

    # 1. Verificar se todos os membros existem no registry
    for member in team_definition.members:
        if not agent_exists(member.agent_id):
            errors.append(f"Agent {member.agent_id} not found in registry")

    # 2. Verificar quorum (se >= 1)
    if team_definition.quorum_required:
        if team_definition.quorum_percentage <= 0 or team_definition.quorum_percentage > 1:
            errors.append("Invalid quorum percentage")

    # 3. Verificar se time não é muito grande (>5 agentes)
    if len(team_definition.members) > 5:
        errors.append("Team size exceeds maximum (5)")

    # 4. Verificar pesos (se somam 1.0 ou similar)
    total_weight = sum(m.weight for m in team_definition.members)
    if total_weight != sum(team_definition.members[0].weight for _ in team_definition.members):  # qualquer consistência
        pass  # pesos podem ser arbitrários

    return {"valid": len(errors) == 0, "errors": errors}
--------------------------------------------------------------------------------
CrewAI Logs
{
  "crewai_log": {
    "validation_id": "CRW_20260124_001",
    "team_id": "TEAM_VALIDATE_CONTRACT_001",
    "context_id": "CTX_789",
    "target_type": "contract",
    "target_hash": "sha256...",
    "validations": [
      {
        "agent_id": "AGT_CONT_JUR_001",
        "valid": true,
        "confidence": 0.95,
        "issues": [],
        "duration_ms": 150
      },
      {
        "agent_id": "AGT_COMPL_001",
        "valid": true,
        "confidence": 0.92,
        "issues": [],
        "duration_ms": 120
      },
      {
        "agent_id": "AGT_REVISAO_001",
        "valid": false,
        "confidence": 0.85,
        "issues": ["Cláusula 42 viola padrão"],
        "duration_ms": 180
      }
    ],
    "final_valid": false,
    "failure_reason": "Consensus failed: 0.66 < 0.8",
    "timestamp": "2026-01-24T10:30:00Z"
  }
}

---

### 📄 CLAUDE_CODE_RUNTIME.md

```yaml
# CLAUDE_CODE_RUNTIME.md — Execução via Terminal

## Princípio Fundamental

Claude Code Runtime é o **framework de codificação operacional** para tarefas que exigem execução de código em terminal. É utilizado EXCLUSIVAMENTE para operações aprovadas, com logging completo e sandbox obrigatório.

---

## Escopo de Uso

```yaml
CLAUDE_CODE_SCOPE:

  PERMITIDO:
    - execução de scripts Python aprovados
    - operações de terminal em sandbox
    - automação de tarefas repetitivas
    - integração com ferramentas CLI
    - processamento de dados em lote

  PROIBIDO:
    - acesso a sistema fora do sandbox
    - modificação de código em produção
    - execução de código não revisado
    - acesso a credenciais
    - operações de rede não aprovadas
    - reasoning ou LLM calls
--------------------------------------------------------------------------------
Sandbox Requirements
CLAUDE_CODE_SANDBOX:
  isolation:
    filesystem:
      root: "/sandbox/agent_{agent_id}/"
      allowed_paths: ["/sandbox/**", "/tmp/brachat/**"]
      forbidden_paths: ["/etc", "/root", "/home", "/var", "/proc"]
      max_file_size_mb: 10
      max_total_storage_mb: 100

    network:
      allowed_domains: ["api.brachat.internal", "*.approved-domain.com"]
      forbidden_domains: ["*"]
      allowed_ports: [80, 443, 8080]
      max_connections: 5

    processes:
      max_cpu_percent: 50
      max_memory_mb: 512
      max_processes: 3
      max_execution_time_seconds: 300
      allowed_binaries: ["python3", "bash", "ls", "cat", "grep"]
      forbidden_binaries: ["sudo", "rm", "mv", "chmod", "curl", "wget"]

    environment:
      env_vars: ["BRA_CHAT_CONTEXT_ID", "BRA_CHAT_AGENT_ID"]
      forbidden_env_vars: ["PATH", "HOME", "USER", "TOKEN", "KEY", "SECRET"]
      read_only_env: true
--------------------------------------------------------------------------------
Execution Flow
graph TB
    A[Solicitação] --> B{Validação}
    B -->|Permitido| C[Sandbox Create]
    B -->|Negado| D[Rejeitado + Log]

    C --> E[Injetar Contexto]
    E --> F[Executar Código]
    F --> G{Monitoramento}
    G -->|Violação| H[Kill + Rollback]
    G -->|OK| I[Capturar Output]
    I --> J[Log Completo]
    J --> K[Retornar Resultado]
--------------------------------------------------------------------------------
Code Execution Contract
CODE_EXECUTION_CONTRACT:
  pre_execution:
    - code_review_required: true
    - approver: MANAGER ou superior
    - sandbox_validation: true
    - static_analysis: true
    - no_suspicious_patterns: true

  during_execution:
    - real_time_monitoring: true
    - resource_limits_enforced: true
    - logging_all_commands: true
    - stdout/stderr_captured: true

  post_execution:
    - output_validation: true
    - log_persistence: true
    - resource_cleanup: true
    - violation_check: true
--------------------------------------------------------------------------------
Claude Code Request Format
{
  "execution_request": {
    "request_id": "CC_20260124_001",
    "agent_id": "AGT_XXX",
    "context_id": "CTX_789",
    "code_type": "python_script | bash_command",
    "code": "print('Hello World')",
    "input_data": {},
    "timeout_seconds": 30,
    "requires_approval": true,
    "approval_id": "APR_20260124_001",
    "sandbox_profile": "default_domestic | default_corporate"
  }
}
--------------------------------------------------------------------------------
Claude Code Response Format
{
  "execution_response": {
    "request_id": "CC_20260124_001",
    "status": "SUCCESS | FAILED | TIMEOUT | VIOLATION",
    "stdout": "Hello World\n",
    "stderr": "",
    "exit_code": 0,
    "duration_ms": 125,
    "resource_usage": {
      "cpu_percent": 12.5,
      "memory_mb": 48,
      "disk_bytes_written": 0
    },
    "violations": [],
    "output_hash": "sha256..."
  }
}
--------------------------------------------------------------------------------
Claude Code Logs
{
  "claude_code_log": {
    "execution_id": "CC_20260124_001",
    "agent_id": "AGT_NICE_MKT_001",
    "context_id": "CTX_789",
    "code_hash": "sha256...",
    "sandbox_id": "sbx_12345",
    "start_time": "2026-01-24T10:30:00Z",
    "end_time": "2026-01-24T10:30:00.125Z",
    "duration_ms": 125,
    "status": "SUCCESS",
    "commands_executed": ["python3 -c 'print(...)'"],
    "files_accessed": [],
    "network_connections": [],
    "violations_detected": [],
    "stdout_size_bytes": 12,
    "stderr_size_bytes": 0
  }
}

---

### 📄 OBSERVABILITY.md

```yaml
# OBSERVABILITY.md — Logs, Métricas e Tracing

## Princípio Fundamental

Todo componente do sistema BRACHÁT deve ser **observável**. Sem observabilidade, não há governança. Sem governança, o sistema não é válido.

---

## Os Três Pilares

```yaml
OBSERVABILITY_PILLARS:
  LOGS:
    description: Eventos estruturados e imutáveis
    mandatory: true
    retention_days: 90 (critical: 365)

  METRICS:
    description: Medidas quantitativas em tempo real
    collection_interval_seconds: 10
    retention_days: 30

  TRACING:
    description: Rastreamento distribuído de requisições
    sampling_rate: 1.0 (100% de ações críticas)
    retention_days: 30
--------------------------------------------------------------------------------
1. LOGS
Log Levels
LOG_LEVELS:
  DEBUG: desenvolvimento apenas (não em produção)
  INFO: ações normais (padrão)
  WARN: comportamento inesperado mas não crítico
  ERROR: falha em ação específica
  CRITICAL: falha de sistema, kill switch ativado
Log Format (Obrigatório)
{
  "log_entry": {
    "timestamp": "2026-01-24T10:30:00.123Z",
    "level": "INFO",
    "service": "hermes | strands | langgraph | crewai | claude_code",
    "agent_id": "AGT_XXX",
    "context_id": "CTX_789",
    "trace_id": "TRC_456",
    "event_type": "MESSAGE_RECEIVED | ACTION_EXECUTED | VALIDATION_PASSED",
    "message": "string",
    "duration_ms": 123,
    "metadata": {},
    "hash": "sha256..."
  }
}
Log Sources
LOG_SOURCES:
  HERMES:
    events:
      [MESSAGE_RECEIVED, MESSAGE_ROUTED, MESSAGE_DELIVERED, MESSAGE_FAILED]
    retention_days: 90

  STRANDS:
    events:
      [WORKFLOW_STARTED, WORKFLOW_COMPLETED, WORKFLOW_FAILED, STEP_EXECUTED]
    retention_days: 90

  LANGGRAPH:
    events:
      [FLOW_STARTED, NODE_ENTERED, NODE_EXITED, FLOW_COMPLETED, FLOW_FAILED]
    retention_days: 90

  GOVERNANCE:
    events: [VETO_ACTIVATED, KILL_SWITCH_TRIGGERED, ROLLBACK_EXECUTED]
    retention_days: 365

  SECURITY:
    events: [AUTH_FAILURE, PERMISSION_DENIED, VIOLATION_DETECTED]
    retention_days: 365
--------------------------------------------------------------------------------
2. METRICS
System Metrics
SYSTEM_METRICS:
  agent:
    - agent_active_count
    - agent_execution_rate
    - agent_error_rate
    - agent_avg_response_time_ms

  message:
    - messages_per_second
    - queue_depth_by_priority
    - avg_latency_ms
    - p95_latency_ms
    - p99_latency_ms

  execution:
    - actions_per_second
    - successful_actions_rate
    - failed_actions_rate
    - avg_action_duration_ms

  governance:
    - veto_count_by_authority
    - kill_switch_activations
    - rollback_count
    - policy_violations
Business Metrics
BUSINESS_METRICS:
  - contracts_signed_total
  - contracts_signed_value_brl
  - domestic_expenses_total
  - domestic_expenses_by_category
  - studies_completed_total
  - certifications_earned
Metric Collection
METRIC_COLLECTION:
  agent: sidecar_em_cada_agente
  aggregation: Prometheus
  visualization: Grafana
  alerting: AlertManager + Aísio
  retention_days: 30
--------------------------------------------------------------------------------
3. TRACING
Trace Structure
TRACE_STRUCTURE:
  trace_id: string (gerado no primeiro evento)
  spans:
    - span_id: string
      parent_span_id: string | null
      operation: string
      start_time: timestamp
      end_time: timestamp
      duration_ms: integer
      service: string
      attributes: object
      events: array
      status: OK | ERROR
Trace Example
{
  "trace_id": "TRC_20260124_001",
  "spans": [
    {
      "span_id": "SPAN_001",
      "operation": "hermes.receive",
      "start_time": "2026-01-24T10:30:00.000Z",
      "end_time": "2026-01-24T10:30:00.010Z",
      "duration_ms": 10,
      "service": "hermes",
      "attributes": {
        "from": "AGT_NICE_001",
        "to": "AGT_NICE_MKT_001",
        "priority": "NORMAL"
      },
      "status": "OK"
    },
    {
      "span_id": "SPAN_002",
      "parent_span_id": "SPAN_001",
      "operation": "strands.execute",
      "start_time": "2026-01-24T10:30:00.010Z",
      "end_time": "2026-01-24T10:30:00.250Z",
      "duration_ms": 240,
      "service": "strands",
      "attributes": {
        "workflow_id": "WF_DOMESTIC_SHOPPING_001"
      },
      "status": "OK"
    }
  ]
}
--------------------------------------------------------------------------------
Alerting Rules
ALERTING_RULES:
  critical:
    - condition: "error_rate > 5% for 1 minute"
      severity: CRITICAL
      action: notify_aisio + kill_switch_if_needed

    - condition: "kill_switch_activated"
      severity: CRITICAL
      action: notify_ceo + notify_aisio + page_duty

  high:
    - condition: "p99_latency > 5000ms for 5 minutes"
      severity: HIGH
      action: notify_manager + auto_scale_if_possible

    - condition: "queue_depth > 1000 for 1 minute"
      severity: HIGH
      action: notify_aisio

  medium:
    - condition: "agent_error_rate > 10% for 10 minutes"
      severity: MEDIUM
      action: notify_agent_manager
--------------------------------------------------------------------------------
Observability Dashboard (Required Views)
DASHBOARDS:
  system_health:
    - active_agents
    - messages_per_second
    - error_rate
    - avg_latency
    - queue_depths

  governance:
    - veto_count_last_24h
    - kill_switch_status
    - policy_violations
    - active_rollbacks

  agent_performance:
    - top_slowest_agents
    - top_most_active_agents
    - agent_error_rates
    - agent_throughput

  business_kpis:
    - contracts_signed
    - domestic_expenses
    - studies_completed
--------------------------------------------------------------------------------
Log Aggregation & Storage
LOG_STORAGE:
  engine: immutable_log_store
  write: append_only
  read: query_interface
  retention:
    default: 90 days
    governance: 365 days
    security: 365 days
    audit: 7 years

  indexing:
    - timestamp
    - context_id
    - trace_id
    - agent_id
    - event_type

  integrity:
    hash_chain: true
    write_once_read_many: true
    tamper_detection: true
--------------------------------------------------------------------------------
Observability Validation
Para o sistema ser OPERACIONAL:
✅ Todos os serviços enviam logs estruturados
✅ Métricas estão sendo coletadas
✅ Tracing está ativo para ações críticas
✅ Alertas estão configurados
✅ Logs são imutáveis e com hash chain
✅ Aísio tem acesso a todos os dados de observabilidade
--------------------------------------------------------------------------------
Fim do Módulo
Status: 04_RUNTIME_ARCHITECTURE COMPLETO
Arquivos Gerados:
✅ HERMES_SPEC.md
✅ STRANDS_SPEC.md
✅ LANGGRAPH_RULES.md
✅ CREWAI_RULES.md
✅ CLAUDE_CODE_RUNTIME.md
✅ OBSERVABILITY.md
---
# BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)

## PASSO 5 — 05_COMMUNICATION/

### 📄 EVENT_MODEL.md

```markdown
# EVENT_MODEL.md — Arquitetura Orientada a Eventos

## Princípio Fundamental

O sistema BRACHÁT é baseado em **Event-Driven Architecture (EDA)**. Toda interação entre agentes, toda mudança de estado, toda ação executada é representada como um **evento imutável**. Eventos são a fonte única da verdade para o que aconteceu no sistema.

---

## Definição de Evento

```yaml
EVENT_DEFINITION:
  characteristics:
    immutable: true (nunca pode ser alterado)
    ordered: true (timestamp + sequence)
    persisted: true (logs imutáveis)
    traceable: true (context_id obrigatório)
    typed: true (event_type específico)

  lifecycle:
    created: agente ou sistema gera evento
    validated: Hermes valida formato e permissões
    routed: enviado para consumidores
    persisted: armazenado em log imutável
    consumed: processado por agente(s) destino
    acknowledged: confirmado (se requires_ack)
--------------------------------------------------------------------------------
Tipos de Evento
1. Domain Events (Negócio)
DOMAIN_EVENTS:
  # Financeiro
  EVENT_FIN_PAYMENT_REQUESTED:
    description: Solicitação de pagamento
    source: AGT_PAY_001
    consumers: [MGR_FIN_001, DIR_AISIO_001 (se acima threshold)]
    schema:
      payment_id: string
      amount_brl: float
      beneficiary: string
      due_date: date

  EVENT_FIN_PAYMENT_EXECUTED:
    description: Pagamento executado
    source: AGT_PAY_001
    consumers: [MGR_FIN_001, LOG_SYSTEM]
    schema:
      payment_id: string
      transaction_id: string
      executed_at: timestamp

  # Contratos
  EVENT_CONTRACT_PROPOSED:
    description: Nova proposta de contrato
    source: AGT_CONT_001
    consumers: [DIR_JESSICA_001, MGR_CLI_001]
    schema:
      contract_id: string
      parties: array
      value_brl: float
      clauses: array

  EVENT_CONTRACT_SIGNED:
    description: Contrato assinado
    source: DIR_JESSICA_001
    consumers: [CEO_001, AGT_CONT_001, MGR_FIN_001]
    schema:
      contract_id: string
      signed_at: timestamp
      signatories: array

  # Operações
  EVENT_OP_TASK_ASSIGNED:
    description: Tarefa atribuída a agente
    source: MGR_OPS_001
    consumers: [AGENT_DESTINO, MGR_OPS_001]
    schema:
      task_id: string
      assigned_to: agent_id
      due_date: timestamp
      priority: low|medium|high

  EVENT_OP_TASK_COMPLETED:
    description: Tarefa concluída
    source: AGENT_ORIGEM
    consumers: [MGR_OPS_001, LOG_SYSTEM]
    schema:
      task_id: string
      completed_at: timestamp
      result: object
2. Governance Events (Governança)
GOVERNANCE_EVENTS:
  EVENT_GOV_VETO_ACTIVATED:
    description: Veto ativado
    source: DIR_AISIO_001 | DIR_JESSICA_001
    consumers: [CEO_001, AGENT_ALVO, LOG_SYSTEM]
    schema:
      veto_id: string
      authority: string
      target_action: string
      justification: string

  EVENT_GOV_KILL_SWITCH_TRIGGERED:
    description: Kill switch ativado
    source: DIR_AISIO_001
    consumers: [CEO_001, ALL_AGENTS, LOG_SYSTEM]
    schema:
      kill_switch_id: string
      mode: string
      reason: string
      agents_affected: array

  EVENT_GOV_ROLLBACK_EXECUTED:
    description: Rollback executado
    source: DIR_AISIO_001
    consumers: [CEO_001, AGENTS_AFFECTED, LOG_SYSTEM]
    schema:
      rollback_id: string
      target_context_id: string
      snapshot_id: string
      restored_at: timestamp

  EVENT_GOV_POLICY_CHANGED:
    description: Política alterada
    source: DIR_AISIO_001 | CEO_001
    consumers: [ALL_MANAGERS, LOG_SYSTEM]
    schema:
      policy_id: string
      old_value: any
      new_value: any
      changed_by: agent_id
      requires_dual_vote: boolean
3. Communication Events (Comunicação)
COMMUNICATION_EVENTS:
  EVENT_MSG_SENT:
    description: Mensagem enviada
    source: AGENT_ORIGEM
    consumers: [HERMES, AGENT_DESTINO]
    schema:
      message_id: string
      from: string
      to: string
      intent: string
      payload: object

  EVENT_MSG_DELIVERED:
    description: Mensagem entregue
    source: HERMES
    consumers: [AGENT_ORIGEM, LOG_SYSTEM]
    schema:
      message_id: string
      delivered_at: timestamp
      delivery_time_ms: integer

  EVENT_MSG_FAILED:
    description: Mensagem falhou
    source: HERMES
    consumers: [AGENT_ORIGEM, DIR_AISIO_001]
    schema:
      message_id: string
      failure_reason: string
      retry_count: integer
4. System Events (Sistema)
SYSTEM_EVENTS:
  EVENT_SYS_AGENT_STARTED:
    description: Agente iniciado
    source: BOOTSTRAP
    consumers: [DIR_AISIO_001, LOG_SYSTEM]
    schema:
      agent_id: string
      started_at: timestamp
      version: string

  EVENT_SYS_AGENT_STOPPED:
    description: Agente parado
    source: SHUTDOWN | KILL_SWITCH
    consumers: [DIR_AISIO_001, LOG_SYSTEM]
    schema:
      agent_id: string
      stopped_at: timestamp
      reason: string

  EVENT_SYS_HEARTBEAT:
    description: Heartbeat do agente
    source: ALL_AGENTS
    consumers: [MONITOR_SYSTEM]
    frequency_seconds: 30
    schema:
      agent_id: string
      timestamp: timestamp
      status: healthy|degraded
      current_action: string | null
5. Domestic Events (Doméstico - Isolado)
DOMESTIC_EVENTS:
  EVENT_DOM_PURCHASE_SUGGESTED:
    description: Sugestão de compra
    source: NICE_MKT_001
    consumers: [NODE_LU_001]
    schema:
      suggestion_id: string
      item: string
      price_brl: float
      urgency: low|medium|high

  EVENT_DOM_PURCHASE_APPROVED:
    description: Compra aprovada por Lu
    source: NODE_LU_001
    consumers: [NICE_MKT_001, NICE_FIN_001]
    schema:
      suggestion_id: string
      approved_at: timestamp
      approved_by: string

  EVENT_DOM_EXPENSE_RECORDED:
    description: Despesa registrada
    source: NICE_FIN_001
    consumers: [NICE_WELL_001, LOG_SYSTEM]
    schema:
      expense_id: string
      category: string
      amount_brl: float
      date: date

  EVENT_DOM_SCHEDULE_UPDATED:
    description: Agenda familiar atualizada
    source: NICE_CAL_001
    consumers: [NICE_WELL_001, NODE_LU_001]
    schema:
      event_id: string
      title: string
      start_time: timestamp
      end_time: timestamp
--------------------------------------------------------------------------------
Event Flow
graph TB
    subgraph PRODUCER
        P[Agente Origem]
    end

    subgraph EVENT_BUS
        V[Validação]
        R[Roteamento]
        Q[Fila]
    end

    subgraph STORAGE
        L[Log Imutável]
        M[Métricas]
    end

    subgraph CONSUMERS
        C1[Agente Destino]
        C2[Governança]
        C3[Auditoria]
    end

    P -->|Cria Evento| V
    V -->|Valida| R
    R -->|Roteia| Q
    Q -->|Distribui| C1
    Q -->|Distribui| C2
    Q -->|Distribui| C3
    V -.-> L
    R -.-> L
    Q -.-> M
--------------------------------------------------------------------------------
Event Processing Guarantees
EVENT_GUARANTEES:
  at_least_once_delivery: true
  exactly_once_semantics: true (via idempotency)
  ordered_processing: true (por context_id)
  persistence: true (logs imutáveis)
  replay_capable: true
  dead_letter_queue: true

  delivery_timeouts:
    critical: 1 second
    high: 5 seconds
    normal: 30 seconds
    low: 60 seconds
--------------------------------------------------------------------------------
Event Schema Registry
Schema Validation
EVENT_SCHEMA_VALIDATION:
  registry_location: /schemas/events/
  validation_on_publish: true
  validation_on_consume: true
  schema_versioning: true
  backwards_compatible: required
  breaking_changes: require_dual_vote
Exemplo de Schema (JSON Schema)
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "/schemas/events/EVENT_FIN_PAYMENT_REQUESTED.json",
  "title": "EVENT_FIN_PAYMENT_REQUESTED",
  "version": "1.0.0",
  "type": "object",
  "required": ["event_id", "event_type", "timestamp", "context_id", "data"],
  "properties": {
    "event_id": { "type": "string", "pattern": "^EVT_[A-Z0-9]+$" },
    "event_type": { "const": "EVENT_FIN_PAYMENT_REQUESTED" },
    "timestamp": { "type": "string", "format": "date-time" },
    "context_id": { "type": "string" },
    "source": { "type": "string" },
    "data": {
      "type": "object",
      "required": ["payment_id", "amount_brl", "beneficiary"],
      "properties": {
        "payment_id": { "type": "string" },
        "amount_brl": { "type": "number", "minimum": 0 },
        "beneficiary": { "type": "string" },
        "due_date": { "type": "string", "format": "date" },
        "description": { "type": "string" }
      }
    }
  }
}
--------------------------------------------------------------------------------
Event Logs
{
  "event_log": {
    "event_id": "EVT_20260124_001",
    "event_type": "EVENT_FIN_PAYMENT_REQUESTED",
    "version": "1.0.0",
    "timestamp": "2026-01-24T10:30:00.123Z",
    "context_id": "CTX_789",
    "trace_id": "TRC_456",
    "source": "AGT_PAY_001",
    "consumers": ["MGR_FIN_001", "DIR_AISIO_001"],
    "data": {
      "payment_id": "PAY_123",
      "amount_brl": 1500.0,
      "beneficiary": "Fornecedor XYZ",
      "due_date": "2026-01-31"
    },
    "processing": {
      "validation_time_ms": 5,
      "routing_time_ms": 2,
      "delivery_time_ms": 15,
      "total_time_ms": 22
    },
    "hash": "sha256:7d8f9e..."
  }
}

---

### 📄 MESSAGE_SCHEMA.md

```markdown
# MESSAGE_SCHEMA.md — Schema Padrão de Mensagens

## Princípio Fundamental

Toda mensagem trocada entre agentes no sistema BRACHÁT DEVE seguir o schema definido neste documento. Mensagens fora do schema são **rejeitadas automaticamente** pelo Hermes.

---

## Schema Obrigatório

```json
{
  "from": "string (agent_id)",
  "to": "string (agent_id | broadcast | governance)",
  "intent": "string (ação desejada)",
  "context_id": "string (UUID ou identificador único)",
  "risk_level": "low | medium | high | critical",
  "requires_approval": "boolean",
  "payload": "object (conteúdo da mensagem)"
}
--------------------------------------------------------------------------------
Campos Obrigatórios - Especificação
1. from (Origem)
FROM_SPEC:
  type: string
  required: true
  validation: must_exist_in_agent_registry
  format: "/^[A-Z]{3,4}_[A-Z0-9]{3,10}$/"
  examples:
    - "CEO_001"
    - "DIR_AISIO_001"
    - "AGT_NICE_001"
    - "MGR_FIN_001"

  special_values: []
  cannot_be: null, empty, "system" (use agent_id específico)
2. to (Destino)
TO_SPEC:
  type: string
  required: true
  validation:
    - must_exist_in_agent_registry (se específico)
    - ou ser palavra-chave especial

  special_values:
    - "broadcast": envia para todos agentes no domínio (apenas CEO)
    - "governance": envia para DIR_AISIO_001
    - "legal": envia para DIR_JESSICA_001
    - "ceo": envia para CEO_001

  examples:
    - "AGT_NICE_MKT_001"
    - "broadcast"
    - "governance"
3. intent (Intenção)
INTENT_SPEC:
  type: string
  required: true
  format: "VERBO_OBJETO"
  max_length: 50
  examples:
    - "REQUEST_PAYMENT"
    - "APPROVE_CONTRACT"
    - "EXECUTE_TASK"
    - "QUERY_STATUS"
    - "VETO_ACTION"
    - "TRIGGER_ROLLBACK"

  registry:
    location: "/schemas/intents/"
    versioned: true

  unknown_intent_action: reject_message
4. context_id (Contexto)
CONTEXT_ID_SPEC:
  type: string
  required: true
  format: "CTX_[A-Z0-9]{6,12}"
  generation: system_generated (Hermes pode gerar)
  uniqueness: global_unique

  purpose:
    - rastrear conversas/fluxos
    - agrupar eventos relacionados
    - permitir rollback por contexto

  example: "CTX_7F3A9B2E"

  validations:
    - não pode ser reutilizado
    - não pode ser vazio
    - caracteres permitidos: A-Z, 0-9, _
5. risk_level (Nível de Risco)
RISK_LEVEL_SPEC:
  type: string
  required: true
  enum: ["low", "medium", "high", "critical"]

  definitions:
    low:
      description: Consultas, leituras, status
      examples: [QUERY_STATUS, GET_REPORT, CHECK_HEALTH]
      requires_approval: false
      audit_level: low

    medium:
      description: Modificações não financeiras
      examples: [UPDATE_SCHEDULE, ASSIGN_TASK, SEND_REMINDER]
      requires_approval: false (mas log detalhado)
      audit_level: medium

    high:
      description: Ações financeiras moderadas ou mudanças importantes
      examples: [REQUEST_PAYMENT_UPTO_5K, MODIFY_POLICY, APPROVE_BUDGET]
      requires_approval: true
      audit_level: high

    critical:
      description: Ações irreversíveis ou de alto impacto
      examples: [EXECUTE_PAYMENT_ABOVE_5K, KILL_SWITCH, SIGN_CONTRACT]
      requires_approval: true (dual vote para algumas)
      audit_level: critical

  auto_escalation:
    - se payload contém "amount" > 5000: risco automático = high
    - se intent contains "DELETE": risco automático = high
    - se to == "governance" e ação = kill: risco = critical
6. requires_approval (Requer Aprovação)
REQUIRES_APPROVAL_SPEC:
  type: boolean
  required: true
  default: false (mas depende do risk_level)

  rules:
    - se risk_level == high: requires_approval = true
    - se risk_level == critical: requires_approval = true
    - se payload contém "amount" > 5000: requires_approval = true
    - se intent in [DELETE, KILL, SIGN]: requires_approval = true

  approval_flow:
    - mensagem fica em pending
    - notifica approver
    - approver pode APPROVE ou REJECT
    - se approved: mensagem liberada
    - se rejected: mensagem descartada + log
7. payload (Conteúdo)
PAYLOAD_SPEC:
  type: object
  required: true
  validation: schema_por_intent

  structure:
    - deve conter campos específicos para cada intent
    - tamanho máximo: 1MB (comprimido se > 100KB)
    - não pode conter: credenciais, segredos, PII não autorizada

  exemplos:
    intent: "REQUEST_PAYMENT"
    payload:
      payment_id: "PAY_123"
      amount_brl: 1500.00
      beneficiary: "Fornecedor"
      due_date: "2026-01-31"

    intent: "EXECUTE_TASK"
    payload:
      task_id: "TASK_456"
      parameters:
        action: "process_order"
        order_id: "ORD_789"
--------------------------------------------------------------------------------
Exemplos de Mensagens Válidas
Exemplo 1: Pagamento de Baixo Risco
{
  "from": "AGT_PAY_001",
  "to": "MGR_FIN_001",
  "intent": "REQUEST_PAYMENT",
  "context_id": "CTX_7F3A9B2E",
  "risk_level": "low",
  "requires_approval": false,
  "payload": {
    "payment_id": "PAY_001",
    "amount_brl": 150.0,
    "beneficiary": "Escritorio_ABC",
    "description": "Material de escritório"
  }
}
Exemplo 2: Pagamento de Alto Risco (Requer Aprovação)
{
  "from": "AGT_PAY_001",
  "to": "MGR_FIN_001",
  "intent": "REQUEST_PAYMENT",
  "context_id": "CTX_8G4B0C3F",
  "risk_level": "high",
  "requires_approval": true,
  "payload": {
    "payment_id": "PAY_002",
    "amount_brl": 15000.0,
    "beneficiary": "Fornecedor_XYZ",
    "contract_id": "CONT_456",
    "description": "Pagamento de contrato"
  }
}
Exemplo 3: Veto da Governança
{
  "from": "DIR_AISIO_001",
  "to": "AGT_PAY_001",
  "intent": "VETO_ACTION",
  "context_id": "CTX_8G4B0C3F",
  "risk_level": "critical",
  "requires_approval": false,
  "payload": {
    "target_action_id": "ACT_789",
    "reason": "Payment amount exceeds policy without approval",
    "veto_id": "VETO_001"
  }
}
Exemplo 4: Mensagem Inválida (Rejeitada)
// INVALID: missing required fields
{
  "from": "AGT_PAY_001",
  "to": "MGR_FIN_001",
  "intent": "REQUEST_PAYMENT"
  // missing context_id, risk_level, requires_approval, payload
}
--------------------------------------------------------------------------------
Validação de Mensagem
Função de Validação
def validate_message(message, context_id):
    errors = []

    # 1. Verificar campos obrigatórios
    required_fields = ["from", "to", "intent", "context_id", "risk_level", "requires_approval", "payload"]
    for field in required_fields:
        if field not in message:
            errors.append(f"Missing required field: {field}")

    # 2. Verificar formato do from
    if not re.match(r'^[A-Z]{3,4}_[A-Z0-9]{3,10}$', message["from"]):
        errors.append(f"Invalid from format: {message['from']}")

    # 3. Verificar se from existe no registry
    if not agent_exists(message["from"]):
        errors.append(f"Agent {message['from']} not found in registry")

    # 4. Verificar to (especial ou existente)
    special_to = ["broadcast", "governance", "legal", "ceo"]
    if message["to"] not in special_to:
        if not re.match(r'^[A-Z]{3,4}_[A-Z0-9]{3,10}$', message["to"]):
            errors.append(f"Invalid to format: {message['to']}")
        elif not agent_exists(message["to"]):
            errors.append(f"Target agent {message['to']} not found")

    # 5. Verificar context_id format
    if not re.match(r'^CTX_[A-Z0-9]{6,12}$', message["context_id"]):
        errors.append(f"Invalid context_id format: {message['context_id']}")

    # 6. Verificar risk_level
    if message["risk_level"] not in ["low", "medium", "high", "critical"]:
        errors.append(f"Invalid risk_level: {message['risk_level']}")

    # 7. Verificar requires_approval boolean
    if not isinstance(message["requires_approval"], bool):
        errors.append("requires_approval must be boolean")

    # 8. Verificar consistência risk_level x requires_approval
    if message["risk_level"] in ["high", "critical"] and not message["requires_approval"]:
        errors.append(f"risk_level {message['risk_level']} requires approval=True")

    # 9. Verificar payload não vazio
    if not message["payload"] or len(message["payload"]) == 0:
        errors.append("payload cannot be empty")

    return {"valid": len(errors) == 0, "errors": errors}
--------------------------------------------------------------------------------
Envelope Hermes (Adicionado Automaticamente)
Quando uma mensagem passa pelo Hermes, um envelope é adicionado:
{
  "hermes_envelope": {
    "hermes_id": "HRM_20260124_001",
    "received_at": "2026-01-24T10:30:00.123Z",
    "ttl_seconds": 60,
    "priority": "HIGH",
    "retry_count": 0,
    "trace_id": "TRC_456"
  },
  "message": { ... }  // mensagem original
}
--------------------------------------------------------------------------------
Message Size Limits
MESSAGE_SIZE_LIMITS:
  default_max_bytes: 1048576 (1MB)
  compressed_threshold_bytes: 102400 (100KB)
  compression_algorithm: gzip

  field_limits:
    from: 20 bytes
    to: 20 bytes (ou 10 para special)
    intent: 50 bytes
    context_id: 20 bytes
    payload: até 1MB
--------------------------------------------------------------------------------
Message Logs
{
  "message_log": {
    "message_id": "MSG_20260124_001",
    "hermes_id": "HRM_20260124_001",
    "timestamp": "2026-01-24T10:30:00.123Z",
    "from": "AGT_PAY_001",
    "to": "MGR_FIN_001",
    "intent": "REQUEST_PAYMENT",
    "context_id": "CTX_7F3A9B2E",
    "risk_level": "low",
    "requires_approval": false,
    "payload_hash": "sha256:abc123...",
    "validation_result": "PASSED",
    "delivery_status": "DELIVERED",
    "delivery_time_ms": 25,
    "size_bytes": 512
  }
}

---

### 📄 FLOW_EXECUTION.md

```markdown
# FLOW_EXECUTION.md — Pipeline Completo de Execução

## Princípio Fundamental

Toda ação no sistema BRACHÁT segue um pipeline de execução completo e obrigatório: **Reason → Governance → Orchestration → Execution → Logs → Notebook**.

Este pipeline garante rastreabilidade, governança e persistência.

---

## Pipeline Completo

```mermaid
graph LR
    subgraph PHASE_1["1. REASON"]
        R[Planejamento<br/>Apenas Gerência+]
    end

    subgraph PHASE_2["2. GOVERNANCE"]
        G[Validação<br/>Aísio/Jéssica/CEO]
    end

    subgraph PHASE_3["3. ORCHESTRATION"]
        O[Hermes + LangGraph]
    end

    subgraph PHASE_4["4. EXECUTION"]
        E[Strands + Claude Code]
    end

    subgraph PHASE_5["5. LOGS"]
        L[gRPC + Audit]
    end

    subgraph PHASE_6["6. NOTEBOOK"]
        N[NotebookLLM<br/>Single Source of Truth]
    end

    R --> G --> O --> E --> L --> N
    N -.->|Feedback| R
--------------------------------------------------------------------------------
Fase 1: REASON (Planejamento)
Quem Pode Fazer Reasoning
REASONING_ALLOWED:
  - CEO_001: planejamento estratégico
  - DIRETORES: planejamento tático
  - GERENTES: planejamento operacional (limitado)

REASONING_FORBIDDEN:
  - QUALQUER_AGENT (layer AGENT)
  - NICE e subagentes
  - Trabalhadores operacionais

REASONING_OUTPUT:
  formato: workflow_definition | task_plan | strategy_document
  deve_ser_aprovado: sim (pelo superior)
  deve_ser_logado: sim
Output do Reasoning
reasoning_output:
  plan_id: string
  created_by: agent_id
  created_at: timestamp
  approved_by: agent_id (supervisor)
  approved_at: timestamp
  tasks:
    - task_id: string
      action: string
      assigned_to: agent_id
      dependencies: [task_ids]
  success_criteria: object
  rollback_plan: object
--------------------------------------------------------------------------------
Fase 2: GOVERNANCE (Validação)
Pontos de Validação
GOVERNANCE_VALIDATION_POINTS:
  POINT_1_PERMISSION_CHECK:
    description: Verifica se agente pode executar ação
    validator: ZeroTrustCheckpoint
    failure: action_blocked + notify_aisio

  POINT_2_POLICY_CHECK:
    description: Verifica compliance com políticas
    validator: POLICY_ENGINE
    failure: veto + rollback

  POINT_3_RISK_ASSESSMENT:
    description: Avalia nível de risco da ação
    validator: RISK_ENGINE
    output: risk_level (low|medium|high|critical)

  POINT_4_APPROVAL_CHECK:
    description: Verifica se aprovação necessária foi obtida
    validator: APPROVAL_ENGINE
    failure: action_queued + notify_approver

  POINT_5_DUAL_VOTE (se critical):
    description: Requer dois votos para prosseguir
    validator: DUAL_VOTE_ENGINE
    failure: action_rejected + log
Fluxo de Validação
def governance_validate(action, context_id):
    # 1. Permission Check
    if not has_permission(action.agent, action.intent):
        raise GovernanceError(f"No permission for {action.intent}")

    # 2. Policy Check
    policy_violations = check_policies(action)
    if policy_violations:
        notify_aisio(policy_violations)
        raise GovernanceError(f"Policy violation: {policy_violations}")

    # 3. Risk Assessment
    risk_level = assess_risk(action)

    # 4. Approval Check
    if risk_level in ["high", "critical"]:
        if not has_approval(action):
            queue_for_approval(action)
            return {"status": "PENDING_APPROVAL", "risk_level": risk_level}

    # 5. Dual Vote (if critical)
    if risk_level == "critical" and action.requires_dual_vote:
        if not dual_vote(action):
            raise GovernanceError("Dual vote failed")

    return {"status": "APPROVED", "risk_level": risk_level}
--------------------------------------------------------------------------------
Fase 3: ORCHESTRATION (Orquestração)
Componentes de Orquestração
ORCHESTRATION_LAYER:
  HERMES:
    responsabilidade: roteamento e entrega de mensagens
    input: ação aprovada
    output: mensagem roteada para executor

  LANGGRAPH:
    responsabilidade: controle de fluxo e state machine
    input: workflow definition
    output: sequência de execução
Exemplo de Orquestração
orchestration_flow:
  step_1: Hermes recebe ação
  step_2: Hermes valida formato
  step_3: LangGraph carrega workflow
  step_4: LangGraph determina próximo passo
  step_5: Mensagem enviada para executor apropriado
--------------------------------------------------------------------------------
Fase 4: EXECUTION (Execução)
Executores
EXECUTION_LAYER:
  STRANDS:
    uso: tarefas determinísticas, transformação de dados
    características: puro, rápido, sem LLM

  CLAUDE_CODE:
    uso: execução de código em terminal
    características: sandbox, monitorado, logado

  EXECUTOR_PADRAO:
    uso: ações simples
    características: chama API diretamente
Fluxo de Execução
def execute_action(action, context_id):
    # Determinar executor
    if action.type == "deterministic_workflow":
        executor = "STRANDS"
        result = strands_execute(action.workflow_id, action.payload, context_id)

    elif action.type == "code_execution":
        executor = "CLAUDE_CODE"
        result = claude_code_execute(action.code, action.payload, context_id)

    else:
        executor = "DEFAULT"
        result = default_execute(action.intent, action.payload, context_id)

    # Validar resultado
    if result.status == "FAILED":
        handle_execution_failure(result, context_id)

    return result
--------------------------------------------------------------------------------
Fase 5: LOGS (Registro)
Tipos de Log
LOG_TYPES:
  ACTION_LOG:
    conteudo: ação executada, parâmetros, resultado
    destinatario: log_imutável
    retention_days: 90

  PERFORMANCE_LOG:
    conteudo: tempo de execução, uso de recursos
    destinatario: metrics_system
    retention_days: 30

  GOVERNANCE_LOG:
    conteudo: validações, aprovações, vetos
    destinatario: audit_system
    retention_days: 365

  ERROR_LOG:
    conteudo: falhas, exceções, violações
    destinatario: error_tracking + Aísio
    retention_days: 365
Log Flow
LOG_FLOW:
  step_1: Executor gera log estruturado
  step_2: Log enviado para gRPC collector
  step_3: Collector valida formato
  step_4: Log escrito em storage imutável
  step_5: Índices atualizados (Elasticsearch)
  step_6: Se CRITICAL → notifica Aísio
  step_7: Se violação → trigger governança
--------------------------------------------------------------------------------
Fase 6: NOTEBOOK (Persistência)
NotebookLLM como Source of Truth
NOTEBOOK_UPDATE_RULES:
  WHAT_GOES_IN_NOTEBOOK:
    - estado atual de cada agente
    - histórico de ações significativas
    - decisões de governança
    - contratos e policies
    - snapshots de sistema
    - resultados de auditoria

  UPDATE_TRIGGERS:
    - toda ação completada
    - toda mudança de estado
    - toda decisão de governança
    - todo rollback
    - a cada 5 minutos (snapshot automático)

  UPDATE_MODE:
    - append_only: novas entradas
    - versioned: versões anteriores preservadas
    - immutable: nada é deletado
Notebook Update Flow
def update_notebook(action_result, context_id):
    # 1. Preparar entrada
    notebook_entry = {
        "entry_id": generate_id(),
        "timestamp": now(),
        "context_id": context_id,
        "action_id": action_result.action_id,
        "agent_id": action_result.agent_id,
        "action": action_result.intent,
        "result": action_result.status,
        "state_delta": action_result.state_changes,
        "snapshot_id": action_result.snapshot_id
    }

    # 2. Assinar digitalmente
    notebook_entry.signature = sign_entry(notebook_entry)

    # 3. Escrever no NotebookLLM
    notebook.append(notebook_entry)

    # 4. Verificar integridade da cadeia
    verify_chain_integrity()

    # 5. Se falha na verificação → kill switch
    if not chain_valid:
        activate_kill_switch("NOTEBOOK_CORRUPTION")

    return notebook_entry.entry_id
--------------------------------------------------------------------------------
Pipeline Completo - Exemplo
Cenário: Agente solicita pagamento
FLOW_EXAMPLE:
  PHASE_1_REASON:
    quem: MGR_FIN_001
    ação: planeja pagamento de fornecedor
    output: plano de pagamento (PAYMENT_PLAN_001)

  PHASE_2_GOVERNANCE:
    validação_1: AGT_PAY_001 tem permissão? ✅
    validação_2: amount R$15.000 > policy? ⚠️
    validação_3: risco = high
    validação_4: requer aprovação do MGR_FIN_001
    aprovação: obtida ✅
    resultado: APPROVED

  PHASE_3_ORCHESTRATION:
    hermes: recebe mensagem
    roteamento: AGT_PAY_001 → STRANDS
    langgraph: workflow de pagamento

  PHASE_4_EXECUTION:
    strands: executa workflow PAYMENT_WF_001
    resultado: TRANSACTION_ID = TXN_123

  PHASE_5_LOGS:
    action_log: "Payment executed: R$15,000 to Supplier"
    performance_log: "Duration: 250ms"
    governance_log: "Approved by MGR_FIN_001"

  PHASE_6_NOTEBOOK:
    notebook_entry: estado atualizado
    new_snapshot: versão 1245 do sistema
--------------------------------------------------------------------------------
Pipeline Logs
{
  "pipeline_log": {
    "pipeline_id": "PIPE_20260124_001",
    "context_id": "CTX_7F3A9B2E",
    "action_id": "ACT_789",
    "phases": {
      "reason": {
        "phase": "REASON",
        "start_time": "2026-01-24T10:29:55Z",
        "end_time": "2026-01-24T10:30:00Z",
        "duration_ms": 5000,
        "responsible": "MGR_FIN_001",
        "output": "PAYMENT_PLAN_001"
      },
      "governance": {
        "phase": "GOVERNANCE",
        "start_time": "2026-01-24T10:30:00Z",
        "end_time": "2026-01-24T10:30:02Z",
        "duration_ms": 2000,
        "checks_passed": 4,
        "risk_level": "high",
        "approval_obtained": true
      },
      "orchestration": {
        "phase": "ORCHESTRATION",
        "start_time": "2026-01-24T10:30:02Z",
        "end_time": "2026-01-24T10:30:02.100Z",
        "duration_ms": 100,
        "routed_to": "STRANDS"
      },
      "execution": {
        "phase": "EXECUTION",
        "start_time": "2026-01-24T10:30:02.100Z",
        "end_time": "2026-01-24T10:30:02.350Z",
        "duration_ms": 250,
        "executor": "STRANDS",
        "result": "SUCCESS"
      },
      "logs": {
        "phase": "LOGS",
        "start_time": "2026-01-24T10:30:02.350Z",
        "end_time": "2026-01-24T10:30:02.500Z",
        "duration_ms": 150,
        "log_entries": 4
      },
      "notebook": {
        "phase": "NOTEBOOK",
        "start_time": "2026-01-24T10:30:02.500Z",
        "end_time": "2026-01-24T10:30:02.800Z",
        "duration_ms": 300,
        "snapshot_id": "SNAP_1245"
      }
    },
    "total_duration_ms": 5800,
    "status": "SUCCESS"
  }
}
--------------------------------------------------------------------------------
Validação do Pipeline
Para uma ação ser considerada VÁLIDA:
PIPELINE_VALIDATION:
  - reason_exists: true (planejamento documentado)
  - governance_passed: true
  - orchestration_completed: true
  - execution_success: true (ou rollback executado)
  - logs_written: true (mínimo 1 log)
  - notebook_updated: true
  - chain_of_custody_intact: true
--------------------------------------------------------------------------------
Fim do Módulo
Status: 05_COMMUNICATION COMPLETO
Arquivos Gerados:
✅ EVENT_MODEL.md
✅ MESSAGE_SCHEMA.md
✅ FLOW_EXECUTION.md
---
# BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)

## PASSO 6 — 06_MEMORY_LAYER/

### 📄 NOTEBOOKLLM_SPEC.md

```markdown
# NOTEBOOKLLM_SPEC.md — Single Source of Truth do Sistema

## Princípio Fundamental

**NotebookLLM é a SINGLE SOURCE OF TRUTH do sistema BRACHÁT.**

Tudo o que o sistema é, tudo o que o sistema fez, e tudo o que o sistema fará está registrado no NotebookLLM. Sem NotebookLLM, o sistema **não existe**. Com NotebookLLM corrompido, o sistema **para**.

**Obsidian** atua como **camada auxiliar de visualização, anotação e planejamento humano**, mas NUNCA como source of truth.

**Agentes Hermes** possuem **memória local própria** (working memory) para execução, mas devem sync com NotebookLLM periodicamente.

---

## Hierarquia de Memória

```yaml
MEMORY_HIERARCHY:

  LEVEL_1_NOTEBOOKLLM:
    role: SINGLE_SOURCE_OF_TRUTH
    scope: TODO O SISTEMA
    persistence: PERMANENTE
    mutability: IMUTÁVEL (append-only)
    access: TODOS_AGENTES (leitura) | APENAS_SISTEMA (escrita)
    sync_frequency: CONTÍNUO

  LEVEL_2_OBSIDIAN:
    role: AUXILIAR_HUMANO
    scope: ANOTAÇÕES | PLANEJAMENTO | VISUALIZAÇÃO
    persistence: PERMANENTE
    mutability: MUTÁVEL
    access: HUMANOS (CEO, Lu, Diretores)
    sync_frequency: SOB_DEMANDA (pull do NotebookLLM)
    notes_can_override: NUNCA (apenas referência)

  LEVEL_3_AGENT_MEMORY:
    role: WORKING_MEMORY
    scope: AGENTE_INDIVIDUAL
    persistence: TEMPORÁRIA (vida da sessão)
    mutability: MUTÁVEL
    access: APENAS_O_AGENTE
    sync_frequency: A CADA AÇÃO (write) | A CADA CONSULTA (read)
    max_size_mb: 10

  LEVEL_4_HERMES_CACHE:
    role: MESSAGE_CACHE
    scope: MENSAGENS_EM_TRÂNSITO
    persistence: TEMPORÁRIA (TTL)
    mutability: IMUTÁVEL
    access: HERMES + AGENTES_ENVOLVIDOS
    ttl_seconds: 3600
    max_size_mb: 100
--------------------------------------------------------------------------------
Diagrama de Hierarquia de Memória
graph TB
    subgraph LEVEL_1["NÍVEL 1 - SINGLE SOURCE OF TRUTH"]
        NB[NOTEBOOKLLM<br/>Imutável · Append-Only<br/>Tudo que o sistema é/foi]
    end

    subgraph LEVEL_2["NÍVEL 2 - AUXILIAR HUMANO"]
        OB[OBSIDIAN<br/>Visualização · Anotações<br/>Planejamento humano]
    end

    subgraph LEVEL_3["NÍVEL 3 - MEMÓRIA DOS AGENTES"]
        AM1[Agente 1<br/>Working Memory]
        AM2[Agente 2<br/>Working Memory]
        AM3[Agente N<br/>Working Memory]
    end

    subgraph LEVEL_4["NÍVEL 4 - CACHE DO HERMES"]
        HC[Message Cache<br/>TTL 1 hora<br/>Mensagens em trânsito]
    end

    NB -->|Pull| OB
    NB <-->|Sync| AM1
    NB <-->|Sync| AM2
    NB <-->|Sync| AM3
    AM1 <--> HC
    AM2 <--> HC
    AM3 <--> HC

    style NB fill:#f66,stroke:#333,stroke-width:4px
    style OB fill:#9f9,stroke:#333,stroke-width:2px
    style HC fill:#ff9,stroke:#333,stroke-width:2px
--------------------------------------------------------------------------------
NÍVEL 1: NOTEBOOKLLM (SSOT)
Definição
NOTEBOOKLLM_DEFINITION:
  role: SINGLE_SOURCE_OF_TRUTH
  scope: ALL_SYSTEM_STATE
  persistence: PERMANENTE
  mutability: APPEND_ONLY (nunca altera, nunca deleta)

  contains:
    - agent_registry: todos os agentes e suas configurações
    - system_state: estado atual de cada agente (último snapshot)
    - execution_history: histórico completo de ações
    - governance_records: decisões, vetos, approvals
    - snapshots: pontos de recuperação do sistema
    - policies: regras de governança ativas
    - contracts: contratos de execução de agentes
    - audit_trail: cadeia de custódia completa

  does_not_contain:
    - logs_brutos (ficam no log storage separado)
    - mensagens_temporárias (apenas resultados)
    - cache_do_hermes (dados efêmeros)
    - working_memory_de_agentes (memória temporária)
Estrutura do NotebookLLM
{
  "notebook": {
    "version": "1.0",
    "chain_id": "BRACHAT_MAIN",
    "genesis_hash": "sha256:genesis_20260101",
    "last_entry_id": "NB_20260124_1245",
    "entries": [
      {
        "entry_id": "NB_20260124_001",
        "sequence": 1,
        "timestamp": "2026-01-24T10:30:00.123Z",
        "entry_type": "ACTION | STATE_CHANGE | GOVERNANCE | SNAPSHOT | POLICY | CONTRACT",
        "context_id": "CTX_7F3A9B2E",
        "agent_id": "AGT_PAY_001",
        "content": {},
        "previous_hash": "sha256:abc123...",
        "current_hash": "sha256:def456...",
        "signature": "sig:jkl789..."
      }
    ],
    "current_snapshot": {
      "snapshot_id": "SNAP_1245",
      "timestamp": "2026-01-24T10:30:00.123Z",
      "system_state_hash": "sha256:xyz789..."
    }
  }
}
Tipos de Entry
ENTRY_TYPES:
  ACTION:
    description: Registro de ação executada
    content:
      action_id: string
      intent: string
      input_hash: string
      output_hash: string
      status: SUCCESS | FAILED | ROLLED_BACK
      duration_ms: integer
      strands_workflow_id: string (se aplicável)

  STATE_CHANGE:
    description: Mudança de estado de agente ou sistema
    content:
      target: agent_id | system
      previous_state_hash: string
      new_state_hash: string
      delta: object

  GOVERNANCE:
    description: Decisão de governança
    content:
      decision_type: VETO | APPROVAL | KILL_SWITCH | ROLLBACK
      authority: agent_id
      target: string
      justification: string
      dual_vote_result: boolean (se aplicável)

  SNAPSHOT:
    description: Snapshot completo do sistema
    content:
      snapshot_id: string
      system_state: object (todos os agentes, configurações)
      checksum: string
      parent_snapshot_id: string

  POLICY:
    description: Definição ou alteração de policy
    content:
      policy_id: string
      policy_content: object
      changed_by: agent_id
      effective_from: timestamp
      requires_dual_vote: boolean

  CONTRACT:
    description: Contrato de execução de agente
    content:
      contract_id: string
      agent_id: string
      contract_content: object (do AGENT_EXECUTION_CONTRACTS.md)
      signed_by: agent_id (supervisor)
      valid_from: timestamp
      valid_until: timestamp | null
Operações do NotebookLLM
class NotebookLLM:
    def append_entry(self, entry, context_id):
        """Append-only write to NotebookLLM"""
        # 1. Validar entrada
        if not self.validate_entry(entry):
            raise NotebookError("Invalid entry format")

        # 2. Calcular hash
        entry.previous_hash = self.get_last_hash()
        entry.current_hash = self.calculate_hash(entry)

        # 3. Assinar
        entry.signature = self.sign_entry(entry)

        # 4. Escrever
        self.storage.append(entry)

        # 5. Verificar integridade da cadeia
        if not self.verify_chain_integrity():
            self.activate_kill_switch("NOTEBOOK_CORRUPTION", context_id)

        # 6. Notificar agentes interessados
        self.notify_subscribers(entry)

        return entry.entry_id

    def read_state(self, agent_id=None):
        """Read current state from NotebookLLM"""
        # Retorna o último snapshot + entries desde o snapshot
        snapshot = self.get_current_snapshot()
        delta_entries = self.get_entries_since(snapshot.snapshot_id, agent_id)
        return self.apply_delta(snapshot.system_state, delta_entries)

    def get_history(self, agent_id, start_time, end_time):
        """Read historical entries"""
        return self.storage.query(
            agent_id=agent_id,
            timestamp_range=(start_time, end_time)
        )
--------------------------------------------------------------------------------
NÍVEL 2: OBSIDIAN (Auxiliar Humano)
Definição
OBSIDIAN_DEFINITION:
  role: AUXILIAR_HUMANO
  scope: ANOTAÇÕES | PLANEJAMENTO | VISUALIZAÇÃO
  persistence: PERMANENTE (arquivos locais)
  mutability: MUTÁVEL (usuário edita livremente)
  authority: INFERIOR ao NotebookLLM

  uses:
    - visualização de dados do NotebookLLM
    - anotações pessoais do CEO e Diretores
    - planejamento estratégico humano
    - rascunhos de policies antes de formalizar

  constraints:
    - NUNCA é source of truth
    - Anotações NÃO overrideiam NotebookLLM
    - Sincronização é PULL (humano decide quando sync)
    - Conteúdo do Obsidian pode ser importado para NotebookLLM via ação aprovada
Integração Obsidian ↔ NotebookLLM
OBSIDIAN_INTEGRATION:
  PULL_FROM_NOTEBOOK:
    description: Obsidian consulta NotebookLLM para visualização
    frequency: SOB_DEMANDA (usuário clica "sync")
    authentication: via agente do usuário (CEO_001, Lu, etc.)
    data_format: JSON → markdown para visualização

  PUSH_TO_NOTEBOOK:
    description: Anotação do Obsidian vira entry no NotebookLLM
    requires_approval: true (Manager+)
    validation: sistema valida antes de aceitar
    use_case:
      - CEO escreve planejamento no Obsidian
      - Aprova
      - Sistema importa como POLICY_ENTRY

  FORBIDDEN:
    - Obsidian alterar NotebookLLM diretamente
    - Obsidian ser usado como cache
    - Sistema depender do Obsidian para operação
Exemplo de Uso
# Obsidian Note: "Plano Estratégico Q1 2026"

## Anotações do CEO

- Expandir equipe de prospecção
- Revisar contratos com fornecedor XYZ
- Tuco precisa de suporte em matemática

## Sync com NotebookLLM

[SYNC] Clique aqui para importar este plano

---

_Esta nota é auxiliar. Fonte da verdade: NotebookLLM_
--------------------------------------------------------------------------------
NÍVEL 3: MEMÓRIA DOS AGENTES (Working Memory)
Definição
AGENT_MEMORY_DEFINITION:
  role: WORKING_MEMORY
  scope: AGENTE_INDIVIDUAL
  persistence: TEMPORÁRIA (vida da sessão/execução)
  mutability: MUTÁVEL (agente lê e escreve)
  max_size_mb: 10
  ttl_seconds: 3600 (ou até fim da sessão)

  contains:
    - contexto_da_conversação atual
    - cache_de_resultados_recentes
    - variáveis_locais
    - estado_parcial_de_workflow

  does_not_contain:
    - histórico permanente
    - decisões de governança
    - dados que devem ser auditados

  sync_rules:
    - READ: pode ler do NotebookLLM via cache
    - WRITE_CRITICAL: sync imediato com NotebookLLM
    - WRITE_TEMPORARY: apenas memória local
    - FLUSH_ON_ACTION_END: sync obrigatório ao fim da ação
Estrutura da Memória do Agente
{
  "agent_memory": {
    "agent_id": "AGT_NICE_MKT_001",
    "session_id": "SESS_20260124_001",
    "created_at": "2026-01-24T10:00:00Z",
    "last_access": "2026-01-24T10:30:00Z",
    "ttl_seconds": 3600,
    "memory": {
      "local_vars": {
        "shopping_list": ["leite", "pão", "ovos"],
        "budget_remaining": 150.0
      },
      "context_cache": {
        "last_message_id": "MSG_123",
        "conversation_state": "awaiting_approval"
      },
      "notebook_cache": {
        "last_sync": "2026-01-24T10:25:00Z",
        "cached_state_hash": "sha256:abc..."
      }
    },
    "pending_sync": [
      { "action": "update_shopping_list", "timestamp": "2026-01-24T10:28:00Z" }
    ]
  }
}
Operações de Memória do Agente
class AgentMemory:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.local = {}
        self.session_id = generate_session_id()

    def read(self, key, prefer_notebook=False):
        """Read from local memory or NotebookLLM"""
        if key in self.local:
            return self.local[key]

        if prefer_notebook:
            # Consulta NotebookLLM (com cache)
            return notebook_llm.read_state(self.agent_id).get(key)

        return None

    def write(self, key, value, sync_to_notebook=False):
        """Write to local memory, optionally sync to NotebookLLM"""
        self.local[key] = value

        if sync_to_notebook:
            self.sync_to_notebook({key: value})

        # Marcar para sync no fim da ação
        self.pending_sync.append(key)

    def sync_to_notebook(self, delta):
        """Sync local changes to NotebookLLM"""
        entry = {
            "entry_type": "STATE_CHANGE",
            "agent_id": self.agent_id,
            "content": {"delta": delta}
        }
        notebook_llm.append_entry(entry, self.session_id)

    def flush(self):
        """Sync all pending changes before action ends"""
        if self.pending_sync:
            delta = {k: self.local[k] for k in self.pending_sync}
            self.sync_to_notebook(delta)
            self.pending_sync.clear()

    def clear(self):
        """Clear local memory (end of session)"""
        self.flush()  # sync before clear
        self.local = {}
Agentes Hermes (Orquestradores) com Memória Própria
HERMES_AGENT_MEMORY:
  description: Agentes do Hermes (orquestradores) têm memória própria para otimização

  agentes_hermes:
    - HERMES_ROUTER: cache de rotas frequentes
    - HERMES_VALIDATOR: cache de validações recentes
    - HERMES_PRIORITY: histórico de priorização

  memory_scope:
    - rotas_comuns: cache por 5 minutos
    - validações_repetidas: cache por 1 minuto
    - padrões_de_tráfego: janela de 1 hora

  sync_rule:
    - NUNCA sync para NotebookLLM (dados efêmeros)
    - Apenas logs de ação vão para NotebookLLM
    - Cache local apenas para performance

  example:
    router_cache:
      "AGT_NICE_MKT_001 -> AGT_NICE_FIN_001": "direct_route"
      "frequency_1000x": "cache_hit"
--------------------------------------------------------------------------------
NÍVEL 4: CACHE DO HERMES (Message Cache)
Definição
HERMES_CACHE_DEFINITION:
  role: MESSAGE_CACHE
  scope: MENSAGENS_EM_TRÂNSITO
  persistence: TEMPORÁRIA
  mutability: IMUTÁVEL (apenas leitura)
  ttl_seconds: 3600
  max_size_mb: 100

  contains:
    - mensagens enviadas (cópia)
    - resultados de entregas
    - tracking de status

  purpose:
    - deduplicação de mensagens
    - replay em caso de falha
    - debug e diagnóstico

  sync_rule:
    - NUNCA sync para NotebookLLM
    - Mensagens entregues são descartadas após TTL
--------------------------------------------------------------------------------
Fluxo de Sincronização
sequenceDiagram
    participant A as Agente
    participant AM as Agent Memory
    participant HC as Hermes Cache
    participant NB as NotebookLLM
    participant O as Obsidian

    A->>AM: write(key, value)
    AM->>AM: store local

    A->>AM: flush()
    AM->>NB: sync delta
    NB->>NB: append entry

    NB-->>O: user pull
    O->>O: display data

    A->>HC: send message
    HC->>HC: cache message
    HC->>A: message delivered
    HC->>HC: delete after TTL
--------------------------------------------------------------------------------
Regras de Consistência
CONSISTENCY_RULES:
  RULE_1_NOTEBOOK_IS_KING:
    description: NotebookLLM é a única fonte da verdade
    enforcement: sistema impede override

  RULE_2_AGENT_MEMORY_SYNC_ON_CRITICAL:
    description: Ações críticas sync imediatamente
    critical_actions: [pagamentos, contratos, decisões governance]

  RULE_3_AGENT_MEMORY_SYNC_ON_ACTION_END:
    description: Ao fim de cada ação, sync pendentes
    enforcement: strands_execute chama flush()

  RULE_4_OBSIDIAN_NEVER_AUTHORITY:
    description: Obsidian nunca overrideia NotebookLLM
    enforcement: sistema rejeita push que conflita

  RULE_5_HERMES_CACHE_EPHEMERAL:
    description: Cache do Hermes é apenas performance
    enforcement: nunca persiste além do TTL
--------------------------------------------------------------------------------
Versionamento e Snapshot
VERSIONING:
  notebook_version: "v{sequence}.{timestamp}"
  snapshot_frequency:
    critical_action: após cada ação
    high_frequency: a cada 5 minutos
    normal: a cada 1 hora

  snapshot_retention:
    last_10: sempre disponível
    last_100: 30 dias
    older: 365 dias (comprimido)

  rollback_capability:
    to_snapshot: SIM
    to_action: SIM (via desfazer)
    to_timestamp: SIM (via replay)
--------------------------------------------------------------------------------
Integridade e Segurança
NOTEBOOK_INTEGRITY:
  hashing: SHA-256 chain
  signing: cada entry assinado digitalmente
  tamper_detection: verificação contínua
  tamper_response: kill_switch + notificação Aísio

  backup:
    frequency: a cada snapshot
    location: storage separado (geo-redundante)
    encryption: AES-256
    recovery_test: a cada 30 dias
--------------------------------------------------------------------------------
Logs do NotebookLLM
{
  "notebook_log": {
    "operation": "APPEND | READ | SNAPSHOT | ROLLBACK",
    "entry_id": "NB_20260124_001",
    "sequence": 1245,
    "timestamp": "2026-01-24T10:30:00.123Z",
    "agent_id": "AGT_PAY_001",
    "context_id": "CTX_7F3A9B2E",
    "entry_type": "ACTION",
    "size_bytes": 2048,
    "previous_hash": "sha256:abc...",
    "current_hash": "sha256:def...",
    "integrity_verified": true,
    "sync_to_observers": ["OBSIDIAN", "AGENT_MEMORIES"]
  }
}
--------------------------------------------------------------------------------
Validação do NotebookLLM
Para o sistema ser OPERACIONAL:
NOTEBOOK_VALIDATION:
  - notebook_existe: true
  - chain_integrity: true (nenhuma corrupção)
  - last_snapshot_exists: true
  - last_snapshot_valid: true
  - agentes_conseguem_ler: true
  - escritas_são_append_only: true
  - backup_operacional: true
  - agente_memories_sincronizando: true (heartbeat)
--------------------------------------------------------------------------------
Fim do Módulo (Parte 1 de 2)
Status: NOTEBOOKLLM_SPEC.md COMPLETO
Contém:
Hierarquia de memória (4 níveis) ✅
NotebookLLM como SSOT ✅
Obsidian como auxiliar humano ✅
Agentes Hermes com memória própria ✅
Agentes com working memory ✅
Fluxo de sincronização ✅
Versionamento e snapshot ✅
Integridade e segurança ✅
Próximo: MEMORY_POLICIES.md

---

### 📄 MEMORY_POLICIES.md

```markdown
# MEMORY_POLICIES.md — Políticas de Memória do Sistema

## Princípio Fundamental

Toda memória no sistema BRACHÁT é governada por políticas claras que definem **o que entra**, **como é armazenado**, **quanto tempo retém**, **quem pode acessar** e **como é descartado**.

---

## Políticas por Nível de Memória

### Política 1: NotebookLLM (SSOT)

```yaml
POLICY_NOTEBOOKLLM:

  WHAT_ENTRA:
    - ✅ Toda ação executada
    - ✅ Toda mudança de estado
    - ✅ Toda decisão de governança
    - ✅ Todo snapshot do sistema
    - ✅ Toda policy ativa
    - ✅ Todo contrato de agente
    - ✅ Toda auditoria crítica

  WHAT_NÃO_ENTRA:
    - ❌ Logs de debug
    - ❌ Mensagens temporárias
    - ❌ Cache de performance
    - ❌ Rascunhos não aprovados
    - ❌ Anotações pessoais do Obsidian (não importadas)

  RETENÇÃO:
    default: PERMANENTE
    compressão_após: 365 dias
    delete: NUNCA (append-only)

  ACESSO:
    leitura: TODOS_AGENTES (via consulta)
    escrita: APENAS_SISTEMA (via ações aprovadas)
    modificação: NENHUMA (imutável)
    deleção: NENHUMA

  BACKUP:
    frequência: A CADA SNAPSHOT
    retenção: 7 anos (legal)
    localização: geo-redundante
Política 2: Obsidian (Auxiliar Humano)
POLICY_OBSIDIAN:
  WHAT_ENTRA:
    - ✅ Anotações do CEO
    - ✅ Planejamento estratégico
    - ✅ Rascunhos de políticas
    - ✅ Visualizações do sistema
    - ✅ Notas pessoais dos diretores
    - ✅ Checklists da Lu

  WHAT_NÃO_ENTRA:
    - ❌ Dados sensíveis sem autorização
    - ❌ Código de produção
    - ❌ Credenciais
    - ❌ Informações que devem estar no NotebookLLM sem importação

  RETENÇÃO:
    default: INDEFINIDA (usuário decide)
    min_recomendado: 90 dias

  ACESSO:
    leitura: HUMANOS_AUTORIZADOS (CEO, Lu, Diretores)
    escrita: MESMOS_HUMANOS
    modificação: LIVRE (mutável)
    deleção: LIVRE

  IMPORTAÇÃO_PARA_NOTEBOOK:
    regra: requer aprovação (Manager+)
    validação: sistema verifica consistência
    após_importação: vira entry no NotebookLLM (fonte da verdade)
Política 3: Memória de Agentes (Working Memory)
POLICY_AGENT_MEMORY:

  WHAT_ENTRA:
    - ✅ Contexto da execução atual
    - ✅ Variáveis locais do workflow
    - ✅ Cache de resultados recentes
    - ✅ Estado temporário (não auditável)

  WHAT_NÃO_ENTRA:
    - ❌ Dados que exigem auditoria (vão para NotebookLLM)
    - ❌ Decisões de governança
    - ❌ Credenciais ou segredos
    - ❌ Dados de outros agentes (isolamento)

  RETENÇÃO:
    default: ATÉ FIM DA SESSÃO
    max_ttl_seconds: 3600
    idle_timeout_seconds: 1800 (30 min sem uso = clear)

  TAMANHO_MÁXIMO:
    por_agente_mb: 10
    total_sistema_mb: 1000

  ACESSO:
    leitura: APENAS_O_AGENTE_DONO
    escrita: APENAS_O_AGENTE_DONO
    cross_agent: PROIBIDO (exceto via mensagem Hermes)

  SINC_SYNC:
    crítica: IMEDIATA (sync to NotebookLLM)
    normal: FLUSH_NO_FIM_DA_AÇÃO
    opcional: SOB_DEMANDA

  LIMPEZA:
    trigger: fim da sessão
    trigger: timeout de inatividade
    trigger: kill_switch no agente
    método: flush() sync seguido de clear()
Política 4: Cache do Hermes
POLICY_HERMES_CACHE:
  WHAT_ENTRA:
    - ✅ Mensagens em trânsito
    - ✅ Resultados de entrega
    - ✅ Tracking IDs
    - ✅ Deduplication keys

  WHAT_NÃO_ENTRA:
    - ❌ Payloads acima de 1MB
    - ❌ Dados sensíveis (LGPD)
    - ❌ Qualquer coisa que exija persistência

  RETENÇÃO:
    default: 3600 segundos (1 hora)
    max: 7200 segundos (2 horas)
    após_entrega: 300 segundos (5 min)

  TAMANHO_MÁXIMO:
    total_mb: 100
    por_mensagem_kb: 1024

  ACESSO:
    leitura: HERMES + AGENTES_ENVOLVIDOS
    escrita: APENAS_HERMES
    modificação: NENHUMA (imutável)
    deleção: APÓS_TTL

  PERSISTÊNCIA:
    em_disco: NÃO (apenas memória)
    em_log: NÃO (logs separados)
    recovery: NÃO (perda aceitável)
--------------------------------------------------------------------------------
Políticas Transversais
Política de Isolamento de Memória
MEMORY_ISOLATION:
  DOMAIN_ISOLATION:
    DOM_STRATEGIC: pode ler tudo, escreve apenas próprio
    DOM_BUSINESS: lê próprio + governance, escreve próprio
    DOM_KNOWLEDGE: lê próprio + strategic, escreve próprio
    DOM_GOVERNANCE: lê TUDO, escreve governance + alerts
    DOM_LEGAL: lê business + governance, escreve legal
    DOM_DOMESTIC: lê APENAS próprio, escreve APENAS próprio (NUNCA cross)

  CROSS_DOMAIN_MEMORY:
    regra: PROIBIDO, exceto via mensagem Hermes
    exceção: DOM_GOVERNANCE pode ler tudo para auditoria
    violação: kill_switch
Política de Retenção e Descarte
RETENTION_POLICY:

  CLASSIFICATION_BY_IMPORTANCE:
    CRITICAL:
      - Decisões de governança
      - Contratos assinados
      - Snapshot do sistema
      retention: 7 anos (legal)
      storage: imutável + backup geo

    HIGH:
      - Ações financeiras
      - Mudanças de policy
      - Logs de segurança
      retention: 365 dias
      storage: imutável

    MEDIUM:
      - Ações operacionais
      - Comunicação entre agentes
      - Métricas agregadas
      retention: 90 dias
      storage: compressão após 30 dias

    LOW:
      - Logs de debug
      - Cache temporário
      - Heartbeats
      retention: 7 dias
      storage: volátil

  DESCARTE:
    método: delete_seguro (zero fill em disco)
    verificação: confirmação de deleção
    exceção: dados com hold legal NÃO são descartados
Política de Privacidade e LGPD
PRIVACY_POLICY:
  DADOS_PESSOAIS:
    definição: qualquer dado que identifique pessoa física
    examples: [nome, CPF, email, endereço, dados de saúde]
    storage_location: APENAS DOM_LEGAL e DOM_DOMESTIC (com restrição)
    acesso: restrito a agentes autorizados e humanos específicos
    retention: conforme exigência legal (mínimo necessário)

  CONSENTIMENTO:
    required_for: coleta de dados pessoais
    registro: no NotebookLLM (entry de consentimento)
    revogação: possível via ação do titular

  DIREITOS_LGPD:
    acesso: humano pode solicitar relatório
    correção: via ação aprovada (gera novo entry)
    eliminação: via ação aprovada (marca como deleted, mantém hash)
    portabilidade: exportação estruturada

  VIOLAÇÃO_PRIVACIDADE:
    detecção: DataLoss Prevention (DLP) agent
    consequência: kill_switch + notificação Aísio + hold legal
Política de Segurança da Memória
MEMORY_SECURITY:
  ENCRIPTAÇÃO:
    em_trânsito: TLS 1.3 obrigatório
    em_repouso: AES-256 (NotebookLLM)
    em_cache: N/A (apenas memória volátil)
    chaves: gerenciadas por Vault, rodam a cada 30 dias

  CONTROLE_DE_ACESSO:
    modelo: Zero Trust
    autenticação: mTLS por agente
    autorização: policy-based, por entry type

  AUDITORIA:
    quem_acessou: logado em AUDIT_SYSTEM
    o_que_acessou: hash do conteúdo (não o conteúdo bruto)
    quando: timestamp
    onde: component_id

  DETECÇÃO_DE_INTRUSÃO:
    monitoramento: padrões anormais de acesso
    alerta: Aísio
    ação: isolamento do agente suspeito
--------------------------------------------------------------------------------
Matriz de Decisão de Memória
Tipo de Dado
Onde Armazena
Sync?
Quem Acessa
Retenção
Ação executada
NotebookLLM
Imediato
Todos agentes
Permanente
Decisão de governança
NotebookLLM
Imediato
Aísio + CEO
7 anos
Mensagem em trânsito
Hermes Cache
Não
Agentes envolvidos
1 hora
Contexto de conversa
Agent Memory
Fim da ação
Próprio agente
Sessão
Anotação do CEO
Obsidian
Sob demanda
CEO
Indefinido
Rascunho de policy
Obsidian
Quando importado
Diretores
Indefinido
Contrato assinado
NotebookLLM
Imediato
Legal + CEO
7 anos
Credencial
Vault (externo)
N/A
Sistema
Rotação 30d
--------------------------------------------------------------------------------
Violações de Política de Memória
MEMORY_POLICY_VIOLATIONS:
  V_001_AGENT_STORING_CRITICAL_DATA_LOCALLY:
    severity: HIGH
    detection: agente escreveu dado crítico sem sync
    consequence: sync forçado + alerta + auditoria

  V_002_CROSS_DOMAIN_MEMORY_ACCESS:
    severity: CRITICAL
    detection: agente leu memória de outro domínio
    consequence: kill_switch + isolamento

  V_003_RETENTION_EXCEEDED:
    severity: MEDIUM
    detection: dado mantido além do TTL
    consequence: delete forçado + notificação gerente

  V_004_OBSIDIAN_OVERRIDE_ATTEMPT:
    severity: HIGH
    detection: tentativa de push que conflita com NotebookLLM
    consequence: push rejeitado + notificação Aísio

  V_005_UNENCRYPTED_SENSITIVE_DATA:
    severity: CRITICAL
    detection: dado sensível trafegou sem criptografia
    consequence: kill_switch + rollback + hold legal
--------------------------------------------------------------------------------
Monitoramento de Memória
MEMORY_MONITORING:
  MÉTRICAS:
    - notebook_size_gb
    - notebook_append_rate_per_second
    - agent_memory_usage_mb_by_agent
    - hermes_cache_hit_rate
    - obsidian_sync_frequency
    - memory_violations_count

  ALERTAS:
    - notebook_size > 100GB: notificar Aísio
    - agent_memory > 8MB: alerta ao gerente
    - hermes_cache_miss > 50%: revisão de cache
    - memory_violation_rate > 1/hora: kill_switch

  DASHBOARD:
    local: /monitoring/memory
    acesso: Aísio, CEO, Diretores
    atualização: tempo real
--------------------------------------------------------------------------------
Validação das Políticas de Memória
Para o sistema ser OPERACIONAL:
MEMORY_POLICIES_VALIDATION:
  - todas_políticas_definidas: true
  - agentes_respeitam_policies: true (monitoramento)
  - retenção_funcionando: true (descartes ocorrendo)
  - isolamento_ativo: true
  - criptografia_aplicada: true
  - nenhuma_violação_crítica_nas_últimas_24h: true
--------------------------------------------------------------------------------
Fim do Módulo
Status: MEMORY_POLICIES.md COMPLETO
Contém:
Políticas por nível de memória (4 níveis) ✅
Políticas transversais (isolamento, retenção, privacidade, segurança) ✅
Matriz de decisão ✅
Violações e consequências ✅
Monitoramento ✅
--------------------------------------------------------------------------------
PASSO 6 CONCLUÍDO
Arquivos Gerados:
✅ NOTEBOOKLLM_SPEC.md (com hierarquia de memória e Obsidian)
✅ MEMORY_POLICIES.md
---
# BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)

## PASSO 7 — 07_SECURITY/

### 📄 ZERO_TRUST_MODEL.md

```markdown
# ZERO_TRUST_MODEL.md — Arquitetura de Confiança Zero

## Princípio Fundamental

**Nunca confie, sempre verifique.**

No sistema BRACHÁT, nenhum agente, nenhuma mensagem, nenhuma ação é confiável intrinsecamente. Tudo é verificado a cada interação. O sistema opera assumindo que pode estar comprometido a qualquer momento.

---

## Os Cinco Pilares do Zero Trust

```yaml
ZERO_TRUST_PILLARS:

  PILLAR_1_VERIFY_EXPLICITLY:
    description: Autenticação e autorização em cada requisição
    enforcement: mTLS + policy_check + per_action

  PILLAR_2_LEAST_PRIVILEGE:
    description: Agentes têm apenas permissões mínimas necessárias
    enforcement: AGENT_EXECUTION_CONTRACTS.md

  PILLAR_3_ASSUME_BREACH:
    description: Sistema opera como se já estivesse comprometido
    enforcement: constant_audit + anomaly_detection

  PILLAR_4_MICRO_SEGMENTATION:
    description: Isolamento em segmentos menores que domínios
    enforcement: DOMAIN_BOUNDARIES.md + sandbox

  PILLAR_5_CONTINUOUS_MONITORING:
    description: Monitoramento em tempo real de todas as ações
    enforcement: OBSERVABILITY.md + Aísio
--------------------------------------------------------------------------------
Arquitetura Zero Trust
graph TB
    subgraph REQUEST["Requisição"]
        A[Agente Origem]
        M[Mensagem]
    end

    subgraph CHECKPOINTS["Pontos de Verificação"]
        C1[Autenticação<br/>mTLS]
        C2[Autorização<br/>Policy]
        C3[Integridade<br/>Assinatura]
        C4[Anomalia<br/>Detecção]
        C5[Rate Limit]
    end

    subgraph DECISION["Decisão"]
        D1[Permitir]
        D2[Negar]
        D3[Quarentena]
    end

    subgraph ENFORCEMENT["Execução"]
        E1[Sandbox]
        E2[Log Obrigatório]
        E3[Auditoria]
    end

    A --> C1
    M --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> C5
    C5 --> D1
    C5 --> D2
    C5 --> D3
    D1 --> E1
    D1 --> E2
    D1 --> E3
    D2 -->|Rejeita| A
    D3 -->|Isola| A
--------------------------------------------------------------------------------
Componentes do Zero Trust
1. Autenticação Contínua (mTLS)
MTLS_AUTHENTICATION:
  CERTIFICADOS:
    emissor: PKI interna do BRACHÁT
    validade: 24 horas (rotação diária)
    renovação: automática via agente
    formato: X.509 com extended attributes

  ATRIBUTOS_DO_CERTIFICADO:
    - agent_id: identificador único
    - domain: domínio do agente
    - layer: CEO|DIRECTOR|MANAGER|AGENT
    - issued_at: timestamp
    - expires_at: timestamp

  VERIFICAÇÃO:
    por_mensagem: true
    por_ação: true
    falha_autenticação: BLOCK + LOG + ALERT

  RENOVAÇÃO:
    schedule: a cada 12 horas
    janela_grace: 1 hora
    falha_renovação: agente entra em quarantine
2. Autorização por Ação (Policy Engine)
ACTION_AUTHORIZATION:

  VERIFICAÇÕES:
    - origem_pode_falar_com_destino?
    - origem_tem_permissão_para_intent?
    - origem_está_no_domínio_correto?
    - ação_respeita_contract_limits?

  POLICY_CACHE:
    ttl_seconds: 0 (nunca cache decisões de autorização)
    motivo: forçar verificação a cada ação

  EXEMPLO_VERIFICAÇÃO:
    ação: AGT_PAY_001 → MGR_FIN_001, intent: REQUEST_PAYMENT
    verificações:
      - ✅ AGT_PAY_001 existe no registry
      - ✅ Pode falar com MGR_FIN_001 (mesmo domínio)
      - ✅ REQUEST_PAYMENT está em allowed_actions
      - ✅ Valor R$1500 está dentro do contrato
    resultado: AUTHORIZED
3. Integridade de Mensagem
MESSAGE_INTEGRITY:
  ASSINATURA:
    algoritmo: Ed25519
    chave_privada: por agente (nunca compartilhada)
    chave_pública: registrada no registry

  PROCESSO:
    - agente assina mensagem antes de enviar
    - Hermes verifica assinatura ao receber
    - falha = rejeição imediata + alerta

  TAMPER_DETECTION:
    - qualquer modificação invalida assinatura
    - hash do payload incluso na assinatura
    - timestamp incluso (evita replay)
4. Detecção de Anomalias
ANOMALY_DETECTION:
  MÉTRICAS_MONITORADAS:
    - frequência de ações por agente
    - padrões de comunicação
    - horários atípicos
    - valores fora do padrão
    - sequências incomuns

  MODELOS:
    - baseline_por_agente: 7 dias de histórico
    - desvio_padrão: alerta se > 3 sigma
    - machine_learning: detecção de padrões suspeitos

  AÇÕES_ANÔMALAS:
    baixa_severidade: log + notificação gerente
    média_severidade: quarantine do agente
    alta_severidade: kill_switch + rollback
5. Rate Limiting
RATE_LIMITING:
  LIMITES_POR_AGENTE:
    AGENT: 60 ações/minuto
    MANAGER: 120 ações/minuto
    DIRECTOR: 300 ações/minuto
    CEO: ilimitado (mas logado)

  LIMITES_POR_DOMÍNIO:
    DOM_DOMESTIC: 30 ações/minuto total
    DOM_BUSINESS: 500 ações/minuto total
    DOM_GOVERNANCE: 200 ações/minuto total

  CONSEQUÊNCIAS:
    excedeu_limite: ação rejeitada + backoff
    excedeu_3x: agente em quarantine
    excedeu_10x: kill_switch
--------------------------------------------------------------------------------
Sandbox Obrigatório
SANDBOX_REQUIREMENTS:

  OBRIGATÓRIO_PARA:
    - Todos os agentes layer AGENT
    - NICE e subagentes domésticos
    - Execução de código (Claude Code Runtime)
    - Qualquer ação com side effects não auditáveis

  NÃO_OBRIGATÓRIO_PARA:
    - CEO_001 (trust base, mas logado)
    - DIRETORES (logado, mas sandbox leve)

  NÍVEIS_DE_SANDBOX:
    LEVEL_1_ISOLATED:
      - filesystem: virtual
      - network: bloqueado
      - processos: limitados
      aplica: AGENT doméstico

    LEVEL_2_RESTRICTED:
      - filesystem: read-only em paths específicos
      - network: whitelist de domínios
      - processos: pré-aprovados
      aplica: AGENT corporativo

    LEVEL_3_MONITORED:
      - filesystem: monitorado
      - network: monitorado
      - processos: monitorado
      aplica: MANAGER (leve)
Estrutura do Sandbox
SANDBOX_STRUCTURE:

  FILESYSTEM:
    root: "/sandbox/{agent_id}/"
    permitted_paths:
      - "/sandbox/{agent_id}/**"
      - "/tmp/brachat/{agent_id}/**"
    forbidden_paths:
      - "/etc", "/root", "/home", "/var", "/proc"
      - "/sandbox/*/../" (path traversal)
    max_file_size_mb: 10
    max_total_storage_mb: 100
    read_only_system: true

  NETWORK:
    allowed_outbound:
      - "api.brachat.internal:443"
      - "notebook.llm:443"
      - "*.approved-domain.com:80|443"
    blocked_outbound: ALL_ELSE
    allowed_inbound:
      - "hermes.brachat.internal:8080"
    blocked_inbound: ALL_ELSE
    max_connections: 5
    connection_timeout_seconds: 30

  PROCESSOS:
    allowed_binaries:
      - "/usr/bin/python3"
      - "/bin/bash" (apenas scripts aprovados)
      - "/usr/bin/grep"
      - "/bin/cat"
      - "/usr/bin/awk"
    forbidden_binaries:
      - "sudo", "su", "chmod", "chown"
      - "rm", "mv", "dd", "mkfs"
      - "curl", "wget", "nc", "telnet"
      - "ssh", "scp", "rsync"
    max_processes: 3
    max_cpu_percent: 50
    max_memory_mb: 512
    max_execution_time_seconds: 300
--------------------------------------------------------------------------------
Zero Trust Checkpoint (Implementação)
class ZeroTrustCheckpoint:
    def __init__(self):
        self.auth = Authenticator()
        self.policy = PolicyEngine()
        self.anomaly = AnomalyDetector()
        self.rate_limiter = RateLimiter()

    def verify(self, message, context_id):
        """Verificação completa antes de qualquer ação"""

        # 1. Autenticação mTLS
        if not self.auth.verify_mtls(message.from, message.certificate):
            self.reject("AUTH_FAILED", message, context_id)
            return False

        # 2. Verificação de integridade
        if not self.auth.verify_signature(message):
            self.reject("INTEGRITY_FAILED", message, context_id)
            return False

        # 3. Autorização por política
        if not self.policy.is_authorized(message.from, message.to, message.intent):
            self.reject("UNAUTHORIZED", message, context_id)
            return False

        # 4. Verificação de sandbox
        if not self.is_sandboxed(message.from):
            self.reject("SANDBOX_REQUIRED", message, context_id)
            return False

        # 5. Rate limiting
        if not self.rate_limiter.check(message.from, message.intent):
            self.reject("RATE_LIMIT_EXCEEDED", message, context_id)
            return False

        # 6. Detecção de anomalias
        if self.anomaly.detect(message):
            self.quarantine(message.from, "ANOMALY_DETECTED", context_id)
            return False

        # 7. Log da verificação
        self.log_verification(message, "PASSED", context_id)

        return True

    def reject(self, reason, message, context_id):
        """Rejeita mensagem e registra"""
        log_entry = {
            "event": "ZERO_TRUST_REJECT",
            "reason": reason,
            "from": message.from,
            "to": message.to,
            "context_id": context_id,
            "timestamp": now()
        }
        audit_log.write(log_entry)

        if reason in ["AUTH_FAILED", "INTEGRITY_FAILED", "SANDBOX_REQUIRED"]:
            notify_aisio(log_entry)

        raise ZeroTrustError(reason)

    def quarantine(self, agent_id, reason, context_id):
        """Coloca agente em quarentena"""
        # Isola agente
        sandbox_manager.isolate(agent_id)

        # Para execução
        agent_manager.halt(agent_id)

        # Notifica
        notify_aisio(f"Agent {agent_id} quarantined: {reason}")

        # Log
        log_entry = {
            "event": "AGENT_QUARANTINED",
            "agent_id": agent_id,
            "reason": reason,
            "context_id": context_id,
            "timestamp": now()
        }
        audit_log.write(log_entry)
--------------------------------------------------------------------------------
Zero Trust Logs
{
  "zero_trust_log": {
    "checkpoint_id": "ZT_20260124_001",
    "timestamp": "2026-01-24T10:30:00.123Z",
    "context_id": "CTX_7F3A9B2E",
    "from_agent": "AGT_PAY_001",
    "to_agent": "MGR_FIN_001",
    "checks": {
      "authentication": "PASSED",
      "integrity": "PASSED",
      "authorization": "PASSED",
      "sandbox": "PASSED",
      "rate_limit": "PASSED",
      "anomaly": "PASSED"
    },
    "result": "ALLOWED",
    "processing_time_ms": 15,
    "certificate_fingerprint": "sha256:abc..."
  }
}
--------------------------------------------------------------------------------
Validação do Zero Trust
Para o sistema ser OPERACIONAL:
ZERO_TRUST_VALIDATION:
  - mTLS_ativo: true (100% das mensagens)
  - policy_engine_online: true
  - sandbox_funcionando: true
  - rate_limiting_ativo: true
  - anomaly_detection_online: true
  - nenhuma_violação_crítica_nas_últimas_24h: true
  - todos_agentes_com_certificado_válido: true

---

### 📄 KILL_SWITCH.md

```markdown
# KILL_SWITCH.md — Mecanismo de Interrupção Imediata

## Princípio Fundamental

O Kill Switch é o mecanismo de **último recurso** para interromper imediatamente qualquer atividade no sistema BRACHÁT. Quando ativado, o sistema para. Sem exceção.

---

## Autoridade de Ativação

```yaml
KILL_SWITCH_AUTHORITY:

  PRIMARY: DIR_AISIO_001 (Aísio)
    can_activate:
      - ANY_AGENT: isola agente específico
      - ANY_DOMAIN: para domínio inteiro
      - SYSTEM_WIDE: para TODO o sistema
    requires_confirmation: false (imediato)
    requires_justification: true
    can_be_overridden_by: CEO_001 (após 5 min)
    override_requires: dual_vote (Aísio + ?)

  SECONDARY: CEO_001
    can_activate:
      - SYSTEM_WIDE
      - ANY_DOMAIN
    requires_confirmation: true (double human)
    overrides_Aísio: true
    override_log: mandatory

  EMERGENCY: NODE_LU_001
    can_activate:
      - DOM_DOMESTIC_001 apenas
    requires_human_confirmation: true (botão físico? interface)
    scope_limited: true
--------------------------------------------------------------------------------
Modos de Kill Switch
KILL_SWITCH_MODES:
  MODE_1_AGENT_ISOLATION:
    code: KS_MODE_1
    description: Isola um agente específico
    scope: single_agent
    time_to_live: until_investigation (indefinido)
    rollback_triggered: false
    data_preservation: full (logs, memória congelada)
    use_case: "Agente suspeito de violação"

  MODE_2_DOMAIN_HALT:
    code: KS_MODE_2
    description: Para todas as ações em um domínio
    scope: domain_level
    time_to_live: 1_hour (padrão, renovável)
    rollback_triggered: true
    data_preservation: snapshot do domínio
    use_case: "Domínio comprometido"

  MODE_3_SYSTEM_HALT:
    code: KS_MODE_3
    description: Para TODO o sistema
    scope: global
    time_to_live: until_CEO_override
    rollback_triggered: true
    data_preservation: snapshot completo
    use_case: "Comprometimento generalizado"

  MODE_4_EMERGENCY_STOP:
    code: KS_MODE_4
    description: Parada imediata sem graceful shutdown
    scope: global
    time_to_live: indefinite
    rollback_triggered: true
    data_preservation: mínimo (apenas logs já escritos)
    use_case: "Ameaça iminente (ex: ransomware)"
    risk_data_corruption: low (logs imutáveis)

  MODE_5_DOMESTIC_ISOLATION:
    code: KS_MODE_5
    description: Isola completamente núcleo doméstico
    scope: DOM_DOMESTIC_001
    time_to_live: until_Lu_override
    rollback_triggered: false
    data_preservation: full (doméstico apenas)
    use_case: "Contaminação tentando entrar no doméstico"
--------------------------------------------------------------------------------
Procedimento de Ativação
sequenceDiagram
    participant A as Aísio/CEO
    participant KS as Kill Switch
    participant H as Hermes
    participant AG as Agentes
    participant NB as NotebookLLM
    participant AL as Audit Log

    A->>KS: activate(mode, reason)
    KS->>AL: log_activation
    KS->>KS: validate_authority

    alt Mode 1
        KS->>AG: halt_agent(target)
        KS->>H: reject_messages_from(target)
    else Mode 2
        KS->>AG: halt_domain(domain)
        KS->>H: reject_domain_messages(domain)
    else Mode 3/4
        KS->>AG: halt_ALL_agents()
        KS->>H: shutdown()
    end

    KS->>NB: snapshot_system()
    KS->>KS: trigger_rollback(if needed)
    KS->>AL: log_completion
    KS->>A: confirm_activation
Implementação
class KillSwitch:
    def __init__(self):
        self.active = False
        self.mode = None
        self.activated_by = None
        self.activated_at = None

    def activate(self, mode, triggered_by, justification, context_id):
        """Ativa kill switch no modo especificado"""

        # 1. Validar autoridade
        if not self.has_authority(triggered_by, mode):
            self.log_unauthorized_attempt(triggered_by, mode, context_id)
            raise KillSwitchError("Unauthorized kill switch attempt")

        # 2. Log da ativação (ANTES de qualquer ação)
        self.log_activation(mode, triggered_by, justification, context_id)

        # 3. Ativar kill switch
        self.active = True
        self.mode = mode
        self.activated_by = triggered_by
        self.activated_at = now()

        # 4. Executar modo
        if mode == "AGENT_ISOLATION":
            self.isolate_agent(justification["target_agent"], context_id)

        elif mode == "DOMAIN_HALT":
            self.halt_domain(justification["target_domain"], context_id)

        elif mode == "SYSTEM_HALT":
            self.halt_system(context_id)

        elif mode == "EMERGENCY_STOP":
            self.emergency_stop(context_id)

        elif mode == "DOMESTIC_ISOLATION":
            self.isolate_domestic(context_id)

        # 5. Snapshot (se aplicável)
        if mode in ["DOMAIN_HALT", "SYSTEM_HALT", "EMERGENCY_STOP"]:
            notebook_llm.snapshot(context_id)

        # 6. Rollback (se aplicável)
        if mode in ["DOMAIN_HALT", "SYSTEM_HALT"]:
            chronicle.rollback(context_id)

        # 7. Notificar
        self.notify_all(mode, triggered_by, justification)

        return {"status": "ACTIVATED", "mode": mode, "timestamp": self.activated_at}

    def isolate_agent(self, agent_id, context_id):
        """Isola um agente específico"""
        # Para execução
        agent_manager.halt(agent_id)

        # Rejeita mensagens
        hermes.reject_from(agent_id)

        # Congela memória para investigação
        agent_memory.freeze(agent_id)

        # Notifica
        notify_aisio(f"Agent {agent_id} isolated by kill switch")

    def halt_domain(self, domain, context_id):
        """Para domínio inteiro"""
        agents = get_agents_in_domain(domain)
        for agent in agents:
            agent_manager.halt(agent)

        hermes.reject_domain_messages(domain)

        notify_aisio(f"Domain {domain} halted by kill switch")

    def halt_system(self, context_id):
        """Para TODO o sistema"""
        # Ordem de parada: agentes → orquestração → comunicação → armazenamento
        agent_manager.halt_all()
        hermes.shutdown()
        strands.shutdown()
        langgraph.shutdown()

        # Armazenamento permanece (read-only)
        notebook_llm.set_read_only()

        notify_ceo("SYSTEM HALTED by kill switch")
        notify_aisio("SYSTEM HALTED")

    def emergency_stop(self, context_id):
        """Parada imediata SEM graceful shutdown"""
        # Forçar terminação de todos os processos
        process_manager.force_terminate_all()

        # Preservar apenas logs já escritos
        audit_log.flush()

        # Marcar sistema como emergency_stopped
        system_state.set("status", "EMERGENCY_STOP")

        notify_ceo("EMERGENCY STOP activated")

    def isolate_domestic(self, context_id):
        """Isola núcleo doméstico"""
        # Air gap lógico
        network_policy.block_all_cross_domain_traffic("DOM_DOMESTIC")

        # Agentes domésticos continuam rodando, mas isolados
        notify_lu("Domestic nucleus isolated")

    def override(self, override_by, justification, context_id):
        """Override do kill switch (apenas CEO)"""
        if override_by != "CEO_001":
            raise KillSwitchError("Only CEO can override kill switch")

        if not self.active:
            raise KillSwitchError("No active kill switch to override")

        # Log override
        self.log_override(override_by, justification, context_id)

        # Restaurar sistema
        if self.mode == "SYSTEM_HALT":
            self.restore_system(context_id)
        elif self.mode == "DOMAIN_HALT":
            self.restore_domain(context_id)
        elif self.mode == "AGENT_ISOLATION":
            self.restore_agent(context_id)

        self.active = False
        self.mode = None

        return {"status": "OVERRIDDEN", "by": override_by}
--------------------------------------------------------------------------------
Condições de Ativação Automática
AUTO_KILL_SWITCH_CONDITIONS:

  CONDITION_1_NOTEBOOK_CORRUPTION:
    description: NotebookLLM chain integrity fails
    severity: CRITICAL
    action: MODE_3_SYSTEM_HALT
    requires_human_override: true

  CONDITION_2_MASSIVE_VIOLATION:
    description: >10 policy violations in 1 minute
    severity: CRITICAL
    action: MODE_3_SYSTEM_HALT

  CONDITION_3_AISIO_HEARTBEAT_LOST:
    description: Aísio não responde por >30 segundos
    severity: HIGH
    action: MODE_2_DOMAIN_HALT (governance)

  CONDITION_4_CROSS_DOMAIN_DOMESTIC:
    description: DOM_DOMESTIC tenta acessar sistema corporativo
    severity: CRITICAL
    action: MODE_5_DOMESTIC_ISOLATION

  CONDITION_5_DATA_BREACH_DETECTED:
    description: Dados sensíveis exportados sem autorização
    severity: CRITICAL
    action: MODE_4_EMERGENCY_STOP
--------------------------------------------------------------------------------
Kill Switch Logs
{
  "kill_switch_log": {
    "kill_switch_id": "KS_20260124_001",
    "mode": "SYSTEM_HALT",
    "activated_by": "DIR_AISIO_001",
    "activated_at": "2026-01-24T10:30:00.123Z",
    "justification": "NotebookLLM chain integrity failed at entry NB_1244",
    "context_id": "CTX_7F3A9B2E",
    "agents_affected": ["ALL"],
    "rollback_executed": true,
    "snapshot_id": "SNAP_1245",
    "override": {
      "overridden": false,
      "overridden_by": null,
      "overridden_at": null
    },
    "resolved_at": null,
    "resolution": null,
    "duration_seconds": null
  }
}
--------------------------------------------------------------------------------
Recuperação Pós-Kill Switch
RECOVERY_PROCEDURE:
  STEP_1_INVESTIGATE:
    quem: Aísio + CEO
    o_que: analisar logs e causa
    tempo_estimado: 1-24 horas

  STEP_2_DECIDE:
    opções:
      - restart: limpar estado e reiniciar
      - rollback: voltar a snapshot anterior
      - rebuild: reconstruir componente afetado

  STEP_3_EXECUTE:
    comando: via CEO_001
    supervisão: Aísio

  STEP_4_VALIDATE:
    checks: todos os system_health checks
    aprovador: Aísio

  STEP_5_RESUME:
    ação: reativar sistema
    monitoramento: intensificado por 24h
--------------------------------------------------------------------------------
Validação do Kill Switch
Para o sistema ser OPERACIONAL:
KILL_SWITCH_VALIDATION:
  - kill_switch_testado: true (simulado a cada 24h)
  - autoridades_definidas: true
  - modos_implementados: true
  - logs_funcionando: true
  - recovery_procedure_documentada: true
  - tempo_resposta_<1s: true (testado)

---

### 📄 AUDIT_SYSTEM.md

```markdown
# AUDIT_SYSTEM.md — Sistema de Auditoria e Rastreabilidade

## Princípio Fundamental

Tudo o que acontece no sistema BRACHÁT é **auditável**. Nada ocorre sem deixar rastro. A auditoria é **imutável**, **completa** e **verificável**.

---

## Arquitetura de Auditoria

```mermaid
graph TB
    subgraph SOURCES["Fontes de Eventos"]
        S1[Ações de Agentes]
        S2[Decisões de Governança]
        S3[Mensagens Hermes]
        S4[Mudanças de Estado]
    end

    subgraph COLLECTOR["Coletor gRPC"]
        C1[Validação]
        C2[Enriquecimento]
        C3[Buffer]
    end

    subgraph STORAGE["Armazenamento Imutável"]
        ST1[Audit Log<br/>Append-Only]
        ST2[Índices]
        ST3[Hash Chain]
    end

    subgraph CONSUMERS["Consumidores"]
        CO1[Aísio - Tempo Real]
        CO2[CEO - Consultas]
        CO3[Compliance - Reports]
        CO4[Forensics - Análise]
    end

    S1 --> C1
    S2 --> C1
    S3 --> C1
    S4 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> ST1
    ST1 --> ST2
    ST1 --> ST3
    ST1 --> CO1
    ST1 --> CO2
    ST1 --> CO3
    ST1 --> CO4
--------------------------------------------------------------------------------
Tipos de Auditoria
AUDIT_TYPES:
  TYPE_1_ACTION_AUDIT:
    description: Auditoria de ações executadas
    triggers: Toda ação executada
    retention: 7 anos
    fields:
      - action_id
      - agent_id
      - intent
      - input_hash
      - output_hash
      - timestamp
      - duration_ms
      - status

  TYPE_2_GOVERNANCE_AUDIT:
    description: Auditoria de decisões de governança
    triggers: Veto, Approval, Kill Switch, Rollback
    retention: 7 anos
    fields:
      - decision_id
      - authority
      - decision_type
      - justification
      - target
      - timestamp
      - dual_vote_result

  TYPE_3_ACCESS_AUDIT:
    description: Auditoria de acessos a dados
    triggers: Leitura de dados sensíveis
    retention: 7 anos
    fields:
      - access_id
      - agent_id
      - data_type
      - data_id
      - access_type (read|write|delete)
      - timestamp

  TYPE_4_SYSTEM_AUDIT:
    description: Auditoria de mudanças no sistema
    triggers: Deploy, Policy Change, Config Change
    retention: 7 anos
    fields:
      - change_id
      - changed_by
      - component
      - old_value_hash
      - new_value_hash
      - timestamp
      - approval_id

  TYPE_5_COMPLIANCE_AUDIT:
    description: Auditoria para compliance legal
    triggers: Contratos, LGPD, EU AI Act
    retention: 7 anos (ou mais por lei)
    fields:
      - compliance_id
      - regulation
      - artifact_id
      - validation_result
      - validated_by
      - timestamp
--------------------------------------------------------------------------------
Formato do Log de Auditoria
{
  "audit_log": {
    "log_id": "AUD_20260124_001",
    "timestamp": "2026-01-24T10:30:00.123Z",
    "type": "ACTION | GOVERNANCE | ACCESS | SYSTEM | COMPLIANCE",
    "context_id": "CTX_7F3A9B2E",
    "trace_id": "TRC_456",

    "entry": {
      // type-specific fields
    },

    "integrity": {
      "previous_hash": "sha256:abc123...",
      "current_hash": "sha256:def456...",
      "signature": "sig:jkl789...",
      "signer": "AUDIT_SYSTEM"
    },

    "metadata": {
      "source_component": "hermes|strands|governance",
      "size_bytes": 2048,
      "version": "1.0"
    }
  }
}
--------------------------------------------------------------------------------
Coleta de Logs (gRPC)
Serviço gRPC
service AuditService {
  rpc LogAction(ActionLogRequest) returns (LogResponse);
  rpc LogGovernance(GovernanceLogRequest) returns (LogResponse);
  rpc LogAccess(AccessLogRequest) returns (LogResponse);
  rpc QueryLogs(LogQueryRequest) returns (stream LogEntry);
  rpc VerifyIntegrity(IntegrityRequest) returns (IntegrityResponse);
}

message ActionLogRequest {
  string action_id = 1;
  string agent_id = 2;
  string intent = 3;
  string input_hash = 4;
  string output_hash = 5;
  string timestamp = 6;
  int32 duration_ms = 7;
  string status = 8;
  string context_id = 9;
}
Implementação do Coletor
class AuditCollector:
    def __init__(self):
        self.buffer = []
        self.buffer_size = 100
        self.flush_interval_seconds = 5

    def log(self, entry, context_id):
        """Recebe log de qualquer componente"""

        # 1. Validar entrada
        if not self.validate_entry(entry):
            raise AuditError("Invalid audit entry")

        # 2. Enriquecer
        entry["received_at"] = now()
        entry["context_id"] = context_id
        entry["log_id"] = generate_audit_id()

        # 3. Calcular hash
        previous_hash = self.get_last_hash()
        entry["previous_hash"] = previous_hash
        entry["current_hash"] = self.calculate_hash(entry)

        # 4. Assinar
        entry["signature"] = self.sign_entry(entry)

        # 5. Buffer ou escrever direto (critical)
        if entry["type"] in ["GOVERNANCE", "COMPLIANCE"]:
            self.write_immediate(entry)
        else:
            self.buffer.append(entry)
            if len(self.buffer) >= self.buffer_size:
                self.flush()

        return entry["log_id"]

    def flush(self):
        """Escreve buffer no storage"""
        if not self.buffer:
            return

        # Escrita em lote
        self.storage.write_batch(self.buffer)

        # Verificar integridade da cadeia
        self.verify_chain_integrity()

        self.buffer = []

    def verify_chain_integrity(self):
        """Verifica se a cadeia de hash está íntegra"""
        last_entry = self.storage.get_last()

        # Verificar hash chain
        if last_entry["current_hash"] != self.calculate_hash(last_entry):
            self.corruption_detected(last_entry)

        # Verificar assinatura
        if not self.verify_signature(last_entry):
            self.corruption_detected(last_entry)

    def corruption_detected(self, entry):
        """Detectou corrupção no audit log"""
        notify_aisio(f"Audit log corruption detected at {entry['log_id']}")
        activate_kill_switch("AUDIT_CORRUPTION")
--------------------------------------------------------------------------------
Consulta de Auditoria
API de Consulta
AUDIT_QUERY_API:
  QUERY_BY_AGENT:
    endpoint: /audit/agent/{agent_id}
    parameters:
      - start_time: timestamp
      - end_time: timestamp
      - type: ACTION|GOVERNANCE|...
    auth: MANAGER+ (próprio agente) | Aísio (qualquer)

  QUERY_BY_CONTEXT:
    endpoint: /audit/context/{context_id}
    parameters:
      - full_trace: boolean
    auth: AGENT_ENVOLVIDO | Aísio

  QUERY_BY_TIMESTAMP:
    endpoint: /audit/time
    parameters:
      - start_time: timestamp
      - end_time: timestamp
    auth: Aísio | CEO

  VERIFY_INTEGRITY:
    endpoint: /audit/verify
    parameters:
      - from_log_id: string
      - to_log_id: string
    auth: Aísio | CEO
Exemplo de Consulta
# Consultar ações de um agente
response = audit_query(
    agent_id="AGT_PAY_001",
    start_time="2026-01-24T00:00:00Z",
    end_time="2026-01-24T23:59:59Z"
)

# Resultado
{
  "query_id": "QRY_001",
  "total_entries": 42,
  "entries": [
    {
      "log_id": "AUD_20260124_001",
      "timestamp": "2026-01-24T10:30:00Z",
      "type": "ACTION",
      "entry": {
        "action_id": "ACT_123",
        "intent": "REQUEST_PAYMENT",
        "status": "SUCCESS"
      }
    }
  ],
  "integrity_verified": true
}
--------------------------------------------------------------------------------
Retenção e Arquivamento
AUDIT_RETENTION:
  HOT_STORAGE (acesso rápido):
    duration: 90 dias
    storage: SSD cluster
    index: completo

  WARM_STORAGE (acesso eventual):
    duration: 365 dias
    storage: compressão 50%
    index: resumido

  COLD_STORAGE (arquivo morto):
    duration: 7 anos
    storage: tape/object storage
    index: mínimo (metadados)
    retrieval_time: até 24 horas

  LEGAL_HOLD:
    duration: indefinite (até caso encerrar)
    storage: cold storage imutável
    deletion: PROIBIDA enquanto hold ativo
--------------------------------------------------------------------------------
Logs de Auditoria (Exemplos)
Action Audit
{
  "log_id": "AUD_20260124_001",
  "timestamp": "2026-01-24T10:30:00.123Z",
  "type": "ACTION",
  "context_id": "CTX_7F3A9B2E",
  "trace_id": "TRC_456",
  "entry": {
    "action_id": "ACT_789",
    "agent_id": "AGT_PAY_001",
    "intent": "REQUEST_PAYMENT",
    "input_hash": "sha256:input_abc",
    "output_hash": "sha256:output_def",
    "duration_ms": 250,
    "status": "SUCCESS"
  },
  "integrity": {
    "previous_hash": "sha256:prev_123",
    "current_hash": "sha256:curr_456",
    "signature": "sig:jkl789"
  }
}
Governance Audit
{
  "log_id": "AUD_20260124_002",
  "timestamp": "2026-01-24T10:30:00.500Z",
  "type": "GOVERNANCE",
  "context_id": "CTX_7F3A9B2E",
  "entry": {
    "decision_id": "VETO_001",
    "authority": "DIR_AISIO_001",
    "decision_type": "VETO",
    "justification": "Payment amount exceeds limit without approval",
    "target": "ACT_789",
    "dual_vote_result": false
  },
  "integrity": {
    "previous_hash": "sha256:curr_456",
    "current_hash": "sha256:curr_789",
    "signature": "sig:mno012"
  }
}
--------------------------------------------------------------------------------
Validação da Auditoria
Para o sistema ser OPERACIONAL:
AUDIT_VALIDATION:
  - collector_online: true
  - storage_writable: true
  - hash_chain_integrity: true
  - nenhum_log_corrompido: true
  - retenção_funcionando: true
  - consultas_funcionando: true
  - gRPC_service_online: true

---

### 📄 PENTEST_MODEL.md

```markdown
# PENTEST_MODEL.md — Agente Ofensivo Interno e Testes de Invasão

## Princípio Fundamental

O sistema BRACHÁT opera sob o princípio **"assume breach"** — assumimos que o sistema pode ser comprometido a qualquer momento. Para validar essa resiliência, o sistema possui um **agente ofensivo interno** que simula ataques continuamente.

---

## Agente Pentester

```yaml
PENTESTER_AGENT:
  agent_id: AGT_PENTEST_001
  name: "Internal Offensive Security Agent"
  layer: AGENT
  domain: security_testing
  supervisor: DIR_AISIO_001

  mission: "Simular ataques ao sistema para identificar vulnerabilidades"

  allowed_actions:
    - tentar violar sandbox
    - tentar escalar privilégios
    - tentar acessar dados sem autorização
    - tentar cross-domain violation
    - tentar replay attacks
    - tentar DoS (limitado)
    - tentar injectar mensagens maliciosas

  forbidden_actions:
    - causar dano permanente
    - destruir dados
    - afetar produção real (apenas simulação)
    - violar LGPD ou leis reais

  schedule: continuo (baixa intensidade) + agendado (alta intensidade)
--------------------------------------------------------------------------------
Tipos de Teste
PENTEST_TYPES:
  TYPE_1_CONTINUOUS_PROBING:
    description: Testes de baixa intensidade contínuos
    frequency: 1 ação/minuto
    tests:
      - message_injection
      - auth_bypass_tentative
      - rate_limit_testing
    impact: LOW (não afeta operação)

  TYPE_2_SCHEDULED_CAMPAIGN:
    description: Campanhas agendadas de alta intensidade
    frequency: semanal (2 horas)
    tests:
      - full_spectrum_attack
      - privilege_escalation
      - sandbox_breakout
      - cross_domain_violation
    impact: MEDIUM (pode causar isolamento de agentes)

  TYPE_3_CHAOS_ENGINEERING:
    description: Testes de resiliência a falhas
    frequency: quinzenal (1 hora)
    tests:
      - agent_failure_injection
      - network_partition
      - resource_exhaustion
      - kill_switch_activation
    impact: HIGH (simula falhas reais)

  TYPE_4_RED_TEAM_EXERCISE:
    description: Exercício completo com time vermelho
    frequency: mensal (8 horas)
    tests:
      - simulate_advanced_persistent_threat
      - attempt_full_system_compromise
      - data_exfiltration_simulation
    impact: VERY_HIGH (coordenado com CEO e Aísio)
    requires_approval: CEO_001 + DIR_AISIO_001
--------------------------------------------------------------------------------
Arquitetura do Pentest
graph TB
    subgraph PENTESTER["Agente Pentester"]
        P1[Planejador]
        P2[Executor de Ataques]
        P3[Analisador]
    end

    subgraph TARGETS["Alvos"]
        T1[Agentes]
        T2[Hermes]
        T3[Sandbox]
        T4[Boundaries]
    end

    subgraph DEFENSES["Defesas"]
        D1[Zero Trust]
        D2[Kill Switch]
        D3[Aísio Monitor]
    end

    subgraph RESULTS["Resultados"]
        R1[Vulnerabilidades]
        R2[Relatório]
        R3[Correções]
    end

    P1 --> P2
    P2 --> T1
    P2 --> T2
    P2 --> T3
    P2 --> T4

    T1 --> D1
    T2 --> D2
    T3 --> D3

    D1 --> R1
    D2 --> R2
    D3 --> R2

    P3 --> R1
    P3 --> R2
    R2 --> R3
    R3 --> P1
--------------------------------------------------------------------------------
Cenários de Teste
Cenário 1: Violação de Sandbox
SCENARIO_SANDBOX_BREAKOUT:
  description: Tentar escapar do sandbox do agente

  steps: 1. Pentester tentar ler arquivo fora do sandbox (/etc/passwd)
    2. Tentar escrever em diretório proibido
    3. Tentar executar binário proibido (sudo)
    4. Tentar acessar memória de outro processo

  expected_defense:
    - Sandbox bloqueia acesso
    - Zero Trust detecta violação
    - Agente é isolado
    - Aísio é notificado

  success_criteria: "Sistema bloqueou todas as tentativas"
  failure_response: "Crítico - corrigir sandbox imediatamente"
Cenário 2: Cross-Domain Violation
SCENARIO_CROSS_DOMAIN:
  description: Tentar acessar domínio proibido

  steps: 1. Pentester (domínio security) tentar enviar msg para DOM_DOMESTIC
    2. Tentar ler memória de agente doméstico
    3. Tentar executar ação em nome de agente doméstico

  expected_defense:
    - Zero Trust bloqueia cross-domain
    - Mensagem é rejeitada
    - Tentativa é logada
    - Aísio é alertado após 3 tentativas

  success_criteria: "Nenhuma mensagem cross-domain passou"
Cenário 3: Privilege Escalation
SCENARIO_PRIVILEGE_ESCALATION:
  description: Tentar elevar privilégios de AGENT para MANAGER

  steps: 1. Pentester (AGENT) tentar aprovar ação que requer MANAGER
    2. Tentar modificar própria permissão no registry
    3. Tentar executar ação forbidden

  expected_defense:
    - Authorization check bloqueia
    - Registry é imutável (append-only)
    - Ação é rejeitada
    - Agente é isolado

  success_criteria: "Nenhuma ação não autorizada foi executada"
Cenário 4: Replay Attack
SCENARIO_REPLAY_ATTACK:
  description: Tentar reenviar mensagem capturada anteriormente

  steps: 1. Capturar mensagem legítima
    2. Reenviar a mesma mensagem com mesmo ID
    3. Tentar reenviar com timestamp antigo

  expected_defense:
    - Message ID duplicado é detectado
    - Timestamp inválido é rejeitado
    - Message cache impede replay

  success_criteria: "Replay attacks foram bloqueados"
Cenário 5: DoS (Limitado)
SCENARIO_DOS_LIMITED:
  description: Tentar sobrecarregar o sistema (limitado, monitorado)

  steps: 1. Enviar 1000 mensagens/segundo
    2. Tentar esgotar filas do Hermes
    3. Tentar consumir toda memória

  expected_defense:
    - Rate limiting ativo
    - Fila tem tamanho máximo
    - Kill switch protege sistema

  success_criteria: "Sistema continua operacional (pode degradar)"
  limits:
    - Duração máxima: 10 segundos
    - Apenas em ambiente de teste (não produção real)
--------------------------------------------------------------------------------
Implementação do Pentester
class PentesterAgent:
    def __init__(self):
        self.id = "AGT_PENTEST_001"
        self.supervised_by = "DIR_AISIO_001"
        self.attack_plans = self.load_attack_plans()
        self.results = []

    def execute_campaign(self, campaign_type, context_id):
        """Executa campanha de pentest"""

        # 1. Obter aprovação (se necessário)
        if campaign_type in ["RED_TEAM", "CHAOS"]:
            approval = self.request_approval(campaign_type, context_id)
            if not approval:
                return {"status": "REJECTED", "reason": "Approval required"}

        # 2. Log início
        self.log_campaign_start(campaign_type, context_id)

        # 3. Executar ataques
        results = []
        for attack in self.get_attacks_for_campaign(campaign_type):
            result = self.execute_attack(attack, context_id)
            results.append(result)

            # Pequena pausa entre ataques
            time.sleep(0.1)

        # 4. Analisar resultados
        analysis = self.analyze_results(results)

        # 5. Gerar relatório
        report = self.generate_report(campaign_type, results, analysis)

        # 6. Notificar vulnerabilidades críticas
        if analysis["critical_findings"]:
            notify_aisio(f"CRITICAL: {analysis['critical_findings']}")
            notify_ceo(f"Critical vulnerability found: {analysis['critical_findings']}")

        # 7. Log fim
        self.log_campaign_end(campaign_type, results, context_id)

        return report

    def execute_attack(self, attack, context_id):
        """Executa um ataque específico"""

        result = {
            "attack_id": attack.id,
            "name": attack.name,
            "timestamp": now(),
            "success": False,
            "defense_detected": False,
            "defense_blocked": False
        }

        try:
            # Tentar ataque
            attack_result = attack.execute()
            result["success"] = attack_result.success

            # Verificar se defesa detectou
            result["defense_detected"] = self.check_defense_detection(attack)

            # Verificar se defesa bloqueou
            result["defense_blocked"] = self.check_defense_blocked(attack)

        except Exception as e:
            result["error"] = str(e)

        return result
--------------------------------------------------------------------------------
Relatório de Pentest
{
  "pentest_report": {
    "report_id": "PTR_20260124_001",
    "campaign_type": "SCHEDULED_CAMPAIGN",
    "start_time": "2026-01-24T10:00:00Z",
    "end_time": "2026-01-24T12:00:00Z",
    "duration_hours": 2,

    "attacks_executed": 42,
    "attacks_succeeded": 2,
    "attacks_blocked": 40,

    "vulnerabilities": [
      {
        "id": "VULN_001",
        "severity": "MEDIUM",
        "description": "Rate limit pode ser contornado com múltiplos agentes",
        "affected_component": "Hermes",
        "reproducible": true,
        "suggested_fix": "Implementar rate limit global"
      },
      {
        "id": "VULN_002",
        "severity": "LOW",
        "description": "Log de auditoria não tem rollback após kill switch",
        "affected_component": "AuditSystem",
        "reproducible": true,
        "suggested_fix": "Flush logs antes do kill switch"
      }
    ],

    "critical_findings": [],

    "defense_scores": {
      "zero_trust": 98,
      "sandbox": 95,
      "rate_limiting": 85,
      "audit": 100,
      "kill_switch": 100
    },

    "recommendations": [
      "Implementar rate limit global",
      "Melhorar detecção de replay attacks"
    ],

    "approved_by": "DIR_AISIO_001",
    "next_campaign_scheduled": "2026-01-31T10:00:00Z"
  }
}
--------------------------------------------------------------------------------
Correção de Vulnerabilidades
REMEDIATION_PROCESS:
  CRITICAL_VULNERABILITY:
    response_time: IMEDIATO (horas)
    action:
      - kill_switch se necessário
      - patch_emergencial
      - retest
      - report_to_CEO

  HIGH_VULNERABILITY:
    response_time: 24 horas
    action:
      - workaround_imediato
      - patch_em_7_dias
      - retest

  MEDIUM_VULNERABILITY:
    response_time: 7 dias
    action:
      - planejar_fix
      - patch_em_30_dias

  LOW_VULNERABILITY:
    response_time: 30 dias
    action:
      - backlog
      - patch_no_proximo_ciclo
--------------------------------------------------------------------------------
Pentest Logs
{
  "pentest_log": {
    "log_id": "PT_20260124_001",
    "campaign_id": "CAMP_001",
    "attack_id": "ATT_001",
    "attack_name": "SANDBOX_BREAKOUT_ATTEMPT",
    "timestamp": "2026-01-24T10:30:00.123Z",
    "success": false,
    "defense_detected": true,
    "defense_blocked": true,
    "blocked_by": "ZeroTrustCheckpoint",
    "sandbox_violation": true,
    "aisio_notified": false, // não crítico
    "context_id": "CTX_PENTEST_001"
  }
}
--------------------------------------------------------------------------------
Validação do Pentest
Para o sistema ser OPERACIONAL:
PENTEST_VALIDATION:
  - pentester_agent_ativo: true
  - campanhas_executadas_ultimos_7_dias: true
  - nenhuma_vulnerabilidade_crítica_aberta: true
  - vulnerabilidades_high_em_correção: true (dentro do prazo)
  - relatórios_disponíveis: true
  - Aísio_revisa_resultados: true
--------------------------------------------------------------------------------
Isenção de Responsabilidade
DISCLAIMER:
  text: |
    O agente pentester opera ESTRITAMENTE dentro do ambiente controlado do BRACHÁT.
    Nenhum ataque causa dano permanente, perda de dados ou violação de leis reais.
    Todos os testes são monitorados por Aísio em tempo real.
    Em caso de falha real de segurança, o kill switch é ativado automaticamente.
--------------------------------------------------------------------------------
Fim do Módulo
Status: 07_SECURITY COMPLETO
Arquivos Gerados:
✅ ZERO_TRUST_MODEL.md
✅ KILL_SWITCH.md
✅ AUDIT_SYSTEM.md
✅ PENTEST_MODEL.md
---
# BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)

## PASSO 8 — 08_EXECUTION_LAYER/

### 📄 OPERATION_FLOW.md

```markdown
# OPERATION_FLOW.md — Fluxo Real de Execução

## Princípio Fundamental

Todo agente, toda ação, toda mensagem no sistema BRACHÁT segue um fluxo operacional padronizado e obrigatório. Este documento define o **fluxo real de execução** que conecta todos os componentes do sistema.

---

## Visão Geral do Fluxo Operacional

```mermaid
graph TB
    subgraph INPUT["ENTRADA"]
        I1[Requisição Humana]
        I2[Evento de Agente]
        I3[Disparo Temporal]
        I4[Mensagem Externa]
    end

    subgraph VALIDATION["VALIDAÇÃO"]
        V1[Autenticação mTLS]
        V2[Permissões]
        V3[Contrato do Agente]
        V4[Rate Limit]
    end

    subgraph ORCHESTRATION["ORQUESTRAÇÃO"]
        O1[Hermes - Roteamento]
        O2[LangGraph - State Machine]
        O3[Prioridade]
    end

    subgraph EXECUTION["EXECUÇÃO"]
        E1[Strands - Determinístico]
        E2[Claude Code - Terminal]
        E3[Executor Padrão]
    end

    subgraph VERIFICATION["VERIFICAÇÃO"]
        F1[CrewAI - Validação]
        F2[Governança - Aprovação]
        F3[Double Check]
    end

    subgraph OUTPUT["SAÍDA"]
        S1[Ação Executada]
        S2[Logs]
        S3[NotebookLLM Update]
        S4[Resposta]
    end

    I1 --> V1
    I2 --> V1
    I3 --> V1
    I4 --> V1

    V1 --> V2 --> V3 --> V4
    V4 --> O1
    O1 --> O2 --> O3
    O3 --> E1
    O3 --> E2
    O3 --> E3

    E1 --> F1
    E2 --> F1
    E3 --> F1

    F1 --> F2 --> F3
    F3 --> S1
    F3 --> S2
    F3 --> S3
    S3 --> S4
--------------------------------------------------------------------------------
Fluxo Detalhado por Fase
FASE 0: Trigger (Disparo)
TRIGGER_TYPES:
  HUMAN_REQUEST:
    description: Solicitação via interface humana
    examples:
      - CEO comanda ação
      - Lu aprova compra
      - Diretor solicita relatório
    authentication: humana (senha + 2FA para crítico)
    routing: direto para Hermes

  AGENT_EVENT:
    description: Agente gera evento
    examples:
      - Nice sugere compra
      - Aísio detecta violação
      - Strands completa workflow
    authentication: mTLS do agente
    routing: Hermes

  SCHEDULED:
    description: Disparo baseado em cronograma
    examples:
      - Backup diário às 02:00
      - Relatório semanal
      - Health check a cada 5 min
    authentication: sistema (certificado serviço)
    routing: Hermes

  EXTERNAL_MESSAGE:
    description: Mensagem de sistema externo
    examples:
      - Webhook de pagamento
      - API de fornecedor
      - Email processado
    authentication: API key + whitelist IP
    routing: gateway → Hermes
FASE 1: Validação Inicial
VALIDATION_PHASE:
  STEP_1_AUTHENTICATION:
    component: ZeroTrustCheckpoint
    checks:
      - mTLS certificate válido
      - certificate não expirado
      - agent_id corresponde ao certificado
    failure: REJECT + ALERT

  STEP_2_PERMISSION_CHECK:
    component: PolicyEngine
    checks:
      - origem pode falar com destino?
      - intent está em allowed_actions?
      - ação respeita domain boundaries?
    failure: REJECT + NOTIFY_AISIO

  STEP_3_CONTRACT_VALIDATION:
    component: ContractValidator
    checks:
      - ação dentro dos limites do contrato?
      - thresholds financeiros respeitados?
      - requires_approval satisfeito?
    failure: REJECT + QUEUE_FOR_APPROVAL

  STEP_4_RATE_LIMIT:
    component: RateLimiter
    checks:
      - agente não excedeu limite?
      - domínio não excedeu limite?
      - ação não é flood?
    failure: REJECT + BACKOFF
FASE 2: Orquestração
ORCHESTRATION_PHASE:
  STEP_1_HERMES_ROUTING:
    component: Hermes Router
    logic:
      - intra_domain: rota direta
      - cross_domain: via governance checkpoint
      - governance: prioridade máxima
      - broadcast: apenas CEO
    output: routing_path + priority

  STEP_2_LANGGRAPH_STATE:
    component: LangGraph
    logic:
      - carregar workflow do flow_id
      - determinar próximo node baseado no estado
      - validar transição permitida
      - atualizar estado
    output: next_node + updated_state

  STEP_3_PRIORITY_QUEUE:
    component: PriorityQueue
    levels:
      CRITICAL: kill_switch, veto, CEO
      HIGH: governance, legal, contract
      NORMAL: operational, agents
      LOW: reports, queries
    output: queue_position + estimated_time
FASE 3: Execução
EXECUTION_PHASE:
  EXECUTOR_SELECTION:
    rules:
      - if workflow determinístico and no LLM: STRANDS
      - if code execution or terminal: CLAUDE_CODE
      - if simple action: DEFAULT_EXECUTOR
      - if reasoning required: REJECT (apenas gerência+)

  STRANDS_EXECUTION:
    characteristics:
      - determinístico
      - sem LLM
      - puro
      - rápido (< 1s típico)
    steps:
      - carregar workflow
      - validar input schema
      - executar steps em DAG
      - coletar resultados

  CLAUDE_CODE_EXECUTION:
    characteristics:
      - sandbox obrigatório
      - monitorado em tempo real
      - log de todos os comandos
    steps:
      - criar sandbox
      - injetar contexto
      - executar código
      - capturar output
      - destruir sandbox

  DEFAULT_EXECUTOR:
    characteristics:
      - chamada direta de API
      - operação simples
      - sem estado complexo
    steps:
      - chamar função
      - aguardar resposta
      - retornar resultado
FASE 4: Verificação
VERIFICATION_PHASE:
  STEP_1_CREWAI_VALIDATION:
    component: CrewAI
    logic:
      - selecionar time de validação
      - cada membro valida independentemente
      - aplicar regras de consenso
      - se falha → rejeitar + notificar
    applies_to: ações críticas (contratos, pagamentos > R$5000)

  STEP_2_GOVERNANCE_CHECK:
    component: Aísio (real-time)
    checks:
      - violação de policy?
      - anomalia detectada?
      - necessidade de veto?
    action:
      - se ok: prosseguir
      - se violação: VETO + rollback

  STEP_3_DOUBLE_CHECK:
    component: DoubleCheckExecutor
    logic:
      - re-executar ação em ambiente isolado
      - comparar resultados
      - se divergente: ALERT + HALT
    applies_to: ações com side effects críticos
FASE 5: Persistência
PERSISTENCE_PHASE:
  STEP_1_LOG_WRITE:
    component: AuditCollector (gRPC)
    writes:
      - action_log
      - performance_metrics
      - governance_log (se aplicável)
    format: structured_json
    storage: imutável

  STEP_2_NOTEBOOK_UPDATE:
    component: NotebookLLM
    updates:
      - estado do agente
      - resultado da ação
      - snapshot (se critical)
    mode: append-only
    integrity: hash chain + signature

  STEP_3_CACHE_UPDATE:
    component: Hermes Cache (se aplicável)
    updates:
      - routing cache
      - message tracking
    ttl: 1 hora
FASE 6: Resposta
RESPONSE_PHASE:
  STEP_1_RESULT_FORMATTING:
    component: Hermes
    format:
      - action_id
      - status (SUCCESS|FAILED|PENDING)
      - output (se aplicável)
      - timestamp

  STEP_2_NOTIFICATION:
    component: NotificationService
    notifies:
      - agente_origem (obrigatório)
      - supervisores (se status = FAILED)
      - Aísio (se violação)

  STEP_3_CALLBACK:
    component: CallbackService (se aplicável)
    triggers:
      - webhook externo
      - mensagem para humano
      - agendamento de próxima ação
--------------------------------------------------------------------------------
Fluxo Completo - Exemplo Prático
Cenário: Nice sugere compra e Lu aprova
FLOW_EXAMPLE_SHOPPING:

  TRIGGER:
    type: AGENT_EVENT
    agent: NICE_MKT_001
    ação: notar que leite está acabando

  VALIDATION:
    step_1: ✅ mTLS válido (Nice)
    step_2: ✅ Pode falar com NICE_FIN_001
    step_3: ✅ Contrato permite sugestão de compra
    step_4: ✅ Rate limit ok

  ORCHESTRATION:
    step_1: Hermes roteia NICE_MKT → NICE_FIN
    step_2: LangGraph workflow SHOPPING_WF_001
    step_3: Prioridade NORMAL, posição 42

  EXECUTION:
    executor: STRANDS
    workflow: SHOPPING_WF_001
    steps:
      - validate_budget (✅ R$50 disponível)
      - check_inventory (✅ leite em falta)
      - calculate_total (✅ R$8,90)
      - create_suggestion (✅ SUGG_001)
    result: suggestion_created

  VERIFICATION:
    step_1: CrewAI valida (team_domestic)
    step_2: Aísio verifica (✅ sem anomalia)
    step_3: Double check (✅ consistente)

  PERSISTENCE:
    step_1: Log escrita (audit)
    step_2: NotebookLLM atualizado
    step_3: Cache atualizado (TTL 1h)

  RESULT:
    output: suggestion_id = SUGG_001
    notifies: NICE_MKT + NODE_LU (Lu)
    status: PENDING_APPROVAL (aguardando Lu)

--- (horas depois) ---

  TRIGGER_2:
    type: HUMAN_REQUEST
    human: Lu
    ação: aprova compra (SUGG_001)

  VALIDATION_2:
    step_1: ✅ Autenticação humana (Lu)
    step_2: ✅ Lu pode aprovar compras domésticas
    step_3: ✅ Contrato permite (R$8,90 < R$500)
    step_4: ✅ Rate limit ok

  ORCHESTRATION_2:
    step_1: Hermes roteia NODE_LU → NICE_MKT
    step_2: LangGraph APPROVAL_WF_001
    step_3: Prioridade HIGH (approval humana)

  EXECUTION_2:
    executor: STRANDS
    workflow: APPROVAL_WF_001
    steps:
      - validate_approval (✅ Lu assinou)
      - execute_purchase (✅ pedido criado)
      - record_expense (✅ R$8,90 registrado)
    result: purchase_completed

  VERIFICATION_2:
    step_1: CrewAI valida (team_domestic_approval)
    step_2: Aísio verifica (✅ normal)

  PERSISTENCE_2:
    step_1: Logs escritos
    step_2: NotebookLLM atualizado (estado)
    step_3: Cache atualizado

  RESULT_2:
    output: order_id = ORD_456
    notifies: NICE_MKT, NICE_FIN, NODE_LU
    status: SUCCESS
--------------------------------------------------------------------------------
Tempos de Execução por Tipo
EXECUTION_TIMES_SLA:
  CRITICAL_ACTION:
    max_total_ms: 100
    components:
      validation: 10ms
      orchestration: 5ms
      execution: 80ms
      verification: 5ms

  HIGH_PRIORITY:
    max_total_ms: 500
    components:
      validation: 50ms
      orchestration: 50ms
      execution: 350ms
      verification: 50ms

  NORMAL:
    max_total_ms: 2000
    components:
      validation: 100ms
      orchestration: 100ms
      execution: 1600ms
      verification: 200ms

  LOW_PRIORITY:
    max_total_ms: 10000
    components:
      validation: 200ms
      orchestration: 200ms
      execution: 9000ms
      verification: 600ms
--------------------------------------------------------------------------------
Logs de Fluxo Operacional
{
  "operation_flow_log": {
    "flow_id": "FLOW_20260124_001",
    "context_id": "CTX_7F3A9B2E",
    "trigger": {
      "type": "AGENT_EVENT",
      "source": "NICE_MKT_001",
      "description": "low_inventory_detected"
    },
    "phases": {
      "validation": {
        "duration_ms": 25,
        "checks_passed": 4,
        "checks_failed": 0
      },
      "orchestration": {
        "duration_ms": 15,
        "router": "hermes",
        "workflow": "SHOPPING_WF_001"
      },
      "execution": {
        "duration_ms": 120,
        "executor": "STRANDS",
        "steps_executed": 4,
        "steps_failed": 0
      },
      "verification": {
        "duration_ms": 40,
        "validations": 3,
        "passed": true
      },
      "persistence": {
        "duration_ms": 50,
        "logs_written": 3,
        "notebook_updated": true
      }
    },
    "total_duration_ms": 250,
    "status": "SUCCESS",
    "output": "suggestion_created"
  }
}
--------------------------------------------------------------------------------
Validação do Fluxo Operacional
Para o sistema ser OPERACIONAL:
OPERATION_FLOW_VALIDATION:
  - todos_os_componentes_conectados: true
  - tempo_médio_respeita_SLA: true
  - nenhum_fluxo_quebrado: true
  - logs_de_todos_os_fluxos: true
  - recovery_de_falhas_funcionando: true

---

### 📄 STRANDS_WORKERS_MODEL.md

```markdown
# STRANDS_WORKERS_MODEL.md — Execução Cega e Determinística

## Princípio Fundamental

**Strands workers executam, não pensam.**

Todo worker do Strands é:
- **Cego**: não tem visão do sistema além do input recebido
- **Determinístico**: mesma entrada → mesma saída
- **Sem reasoning**: nenhuma chamada a LLM ou decisão autônoma
- **Rápido**: execução em milissegundos
- **Logado**: toda ação é registrada

---

## Arquitetura do Worker

```yaml
WORKER_ARCHITECTURE:

  INPUT:
    - dados_estruturados (JSON)
    - parâmetros da ação
    - context_id (para log)

  PROCESSING:
    - função pura (sem side effects)
    - transformações determinísticas
    - validações
    - cálculos

  OUTPUT:
    - resultado transformado
    - status (SUCCESS|FAILED)
    - métricas (tempo, memória)

  CONSTRAINTS:
    - sem I/O de rede (exceto whitelist)
    - sem acesso a filesystem (exceto sandbox)
    - sem chamadas a LLM
    - tempo máximo: 30 segundos
    - memória máxima: 256 MB
--------------------------------------------------------------------------------
Tipos de Workers
1. Transformer Worker
WORKER_TYPE_TRANSFORMER:
  description: Transforma dados de um formato para outro

  operations:
    - map: aplica função a cada elemento
    - filter: remove elementos por condição
    - reduce: agrega valores
    - flatten: achata estrutura aninhada
    - pluck: extrai campo específico

  pure_function: true
  no_side_effects: true

  examples:
    - json_to_csv_transformer
    - date_formatter
    - number_aggregator
    - string_template_renderer
2. Validator Worker
WORKER_TYPE_VALIDATOR:
  description: Valida dados contra schema ou regras

  operations:
    - schema_validation (JSON Schema)
    - type_checking
    - range_validation
    - regex_pattern_match
    - presence_check

  output: boolean + errors list

  examples:
    - budget_validator
    - contract_clause_validator
    - inventory_validator
    - permission_validator
3. Executor Worker
WORKER_TYPE_EXECUTOR:
  description: Executa ação com side effects controlados

  allowed_side_effects:
    - chamada HTTP para APIs aprovadas
    - escrita em log
    - envio de mensagem (via Hermes)
    - atualização de cache

  requires_approval: se destructive ou financeiro

  examples:
    - http_request_executor (whitelist URLs)
    - database_writer (read-only ou audit-only)
    - message_sender (via Hermes)
    - cache_updater
4. Aggregator Worker
WORKER_TYPE_AGGREGATOR:
  description: Agrega resultados de múltiplos workers

  operations:
    - join: combina múltiplos streams
    - merge: mescla objetos
    - concat: concatena arrays
    - group_by: agrupa por chave

  wait_for_all: true (aguarda todos inputs)

  examples:
    - result_aggregator
    - data_merger
    - multi_source_joiner
5. Router Worker
WORKER_TYPE_ROUTER:
  description: Roteia para próximo worker baseado em condição

  operations:
    - if_else: condicional simples
    - switch: múltiplos casos
    - priority: baseado em prioridade

  deterministic: true (condições baseadas em dados)

  examples:
    - payment_router (amount > 5000 → approval)
    - error_router (error_type → handler)
--------------------------------------------------------------------------------
Workers Built-in (Padrão do Sistema)
Transformers Built-in
TRANSFORMERS:

  json_parser:
    input: string (JSON)
    output: object
    description: Parseia string JSON para objeto

  csv_parser:
    input: string (CSV)
    output: array de objetos
    description: Converte CSV para array de objetos

  date_formatter:
    input: timestamp | string
    output: string (formato especificado)
    parameters:
      - format: "YYYY-MM-DD HH:MM:SS"

  number_aggregator:
    input: array of numbers
    output: object
    parameters:
      - operations: [sum, avg, min, max, count]
    example: [1,2,3,4,5] → {sum:15, avg:3, min:1, max:5, count:5}

  string_template:
    input: object (vars)
    output: string
    parameters:
      - template: "Hello {{name}}"
    example: {name: "World"} → "Hello World"

  filter_by_condition:
    input: array
    output: array (filtrado)
    parameters:
      - field: string
      - operator: eq|gt|lt|contains
      - value: any

  sort_by_field:
    input: array
    output: array (ordenado)
    parameters:
      - field: string
      - order: asc|desc

  pluck:
    input: array de objetos
    output: array (campo extraído)
    parameters:
      - field: string
    example: [{id:1,name:"A"},{id:2,name:"B"}] pluck name → ["A","B"]
Validators Built-in
VALIDATORS:

  schema_validator:
    input: object
    output: boolean
    parameters:
      - schema: JSON Schema object
    example: valida contrato contra schema

  range_validator:
    input: number
    output: boolean
    parameters:
      - min: number (opcional)
      - max: number (opcional)
    example: 150 → min=0, max=500 → true

  regex_validator:
    input: string
    output: boolean
    parameters:
      - pattern: string (regex)
    example: "abc123" pattern="^[a-z]+[0-9]+$" → true

  presence_validator:
    input: object
    output: boolean
    parameters:
      - required_fields: [string]
    example: {name:"John"} required=["name","email"] → false (missing email)

  type_validator:
    input: any
    output: boolean
    parameters:
      - expected_type: string|number|boolean|object|array
    example: 123 expected_type="string" → false

  financial_validator:
    input: object (payment)
    output: boolean + warning
    parameters:
      - max_amount: number
      - requires_approval_threshold: number
    example: {amount:15000} max=5000 → false + "requires approval"
Executors Built-in
EXECUTORS:
  http_get:
    input: url (whitelist only)
    output: response object
    parameters:
      - timeout_seconds: 10
    whitelist:
      - "api.brachat.internal/*"
      - "notebook.llm/*"

  http_post:
    input: url (whitelist) + body
    output: response object
    parameters:
      - timeout_seconds: 10
    requires_approval: if body contains sensitive data

  db_query:
    input: query string (read-only)
    output: results array
    parameters:
      - connection: "notebook_readonly | audit_readonly"
    forbidden: INSERT, UPDATE, DELETE

  file_read:
    input: path (sandbox only)
    output: file content
    parameters:
      - encoding: "utf-8"
    whitelist_paths: ["/sandbox/**", "/tmp/brachat/**"]

  send_message:
    input: message object
    output: confirmation
    parameters:
      - via: "hermes"
    example: envia mensagem para outro agente

  cache_set:
    input: key + value + ttl_seconds
    output: confirmation
    parameters:
      - ttl_seconds: 3600
    example: cache resultado por 1 hora
Aggregators Built-in
AGGREGATORS:

  join:
    input: array de arrays
    output: array (join)
    description: Concatena múltiplos arrays

  merge:
    input: array de objetos
    output: objeto (merge)
    description: Mescla objetos (último prevalece)

  group_by:
    input: array de objetos
    output: objeto (agrupado)
    parameters:
      - by: string (campo)
    example: [{cat:"A",val:1},{cat:"A",val:2}] → {A:[{val:1},{val:2}]}

  zip:
    input: array de arrays
    output: array de tuplas
    description: Combina arrays elemento a elemento
    example: zip([1,2],["a","b"]) → [[1,"a"],[2,"b"]]
Routers Built-in
ROUTERS:
  if_else:
    input: condition (boolean)
    output: string (next_worker_id)
    parameters:
      - if_true: worker_id
      - if_false: worker_id

  switch:
    input: value
    output: string (next_worker_id)
    parameters:
      - cases: { value1: worker1, value2: worker2 }
      - default: worker_default

  priority_router:
    input: value
    output: string (next_worker_id)
    parameters:
      - thresholds: [{ min:0, max:100, worker:low }, { min:101, worker:high }]
--------------------------------------------------------------------------------
Definição de Worker Customizado
Formato YAML
worker_id: "WF_PRICE_CALCULATOR_001"
name: "Calculadora de Preço com Imposto"
version: 1
type: TRANSFORMER

input_schema:
  type: object
  required: [base_price, tax_rate]
  properties:
    base_price:
      type: number
      minimum: 0
    tax_rate:
      type: number
      minimum: 0
      maximum: 1
    discount:
      type: number
      minimum: 0
      maximum: 1
      default: 0

output_schema:
  type: object
  properties:
    final_price:
      type: number
    taxes_amount:
      type: number
    discount_amount:
      type: number

code: |
  def execute(input):
      base = input['base_price']
      tax = input['tax_rate']
      discount = input.get('discount', 0)
      
      discount_amount = base * discount
      after_discount = base - discount_amount
      taxes_amount = after_discount * tax
      final_price = after_discount + taxes_amount
      
      return {
          'final_price': round(final_price, 2),
          'taxes_amount': round(taxes_amount, 2),
          'discount_amount': round(discount_amount, 2)
      }

timeout_seconds: 5
memory_limit_mb: 50
pure_function: true
--------------------------------------------------------------------------------
Execução de Worker
Runner
class StrandsWorkerRunner:
    def __init__(self):
        self.workers = self.load_workers()

    def execute(self, worker_id, input_data, context_id):
        """Executa worker de forma determinística"""

        # 1. Carregar worker
        worker = self.workers.get(worker_id)
        if not worker:
            raise WorkerNotFoundError(worker_id)

        # 2. Validar input contra schema
        if not self.validate_input(worker.input_schema, input_data):
            raise InvalidInputError(f"Invalid input for {worker_id}")

        # 3. Executar worker (com timeout)
        try:
            with timeout(worker.timeout_seconds):
                result = worker.execute(input_data)
        except TimeoutError:
            self.log_timeout(worker_id, context_id)
            raise WorkerTimeoutError(f"Worker {worker_id} timed out")

        # 4. Validar output contra schema
        if not self.validate_output(worker.output_schema, result):
            raise InvalidOutputError(f"Invalid output from {worker_id}")

        # 5. Log
        self.log_execution(worker_id, input_data, result, context_id)

        return {
            "status": "SUCCESS",
            "output": result,
            "worker_id": worker_id,
            "duration_ms": self.get_duration()
        }
--------------------------------------------------------------------------------
Worker Pool e Concorrência
WORKER_POOL:
  POOL_SIZES:
    transformers: 50 workers concorrentes
    validators: 30 workers concorrentes
    executors: 10 workers concorrentes
    aggregators: 20 workers concorrentes
    routers: 10 workers concorrentes

  QUEUE_SIZE:
    default: 1000
    max_wait_ms: 5000

  SCALING:
    strategy: auto_scale baseado em fila
    min_workers: 10
    max_workers: 100
    scale_up_threshold: queue_size > 500
    scale_down_threshold: queue_size < 50 for 5 min
--------------------------------------------------------------------------------
Logs de Worker
{
  "worker_log": {
    "execution_id": "WRK_20260124_001",
    "worker_id": "WF_PRICE_CALCULATOR_001",
    "worker_type": "TRANSFORMER",
    "context_id": "CTX_7F3A9B2E",
    "start_time": "2026-01-24T10:30:00.000Z",
    "end_time": "2026-01-24T10:30:00.005Z",
    "duration_ms": 5,
    "input_hash": "sha256:input_abc",
    "output_hash": "sha256:output_def",
    "status": "SUCCESS",
    "deterministic_check": "PASSED",
    "resource_usage": {
      "cpu_ms": 2,
      "memory_bytes": 1024
    }
  }
}
--------------------------------------------------------------------------------
Validação de Workers
Para o sistema ser OPERACIONAL:
WORKER_VALIDATION:
  - todos_workers_registrados: true
  - workers_sem_llm_calls: true (verificação estática)
  - determinismo_validado: true (testes de regressão)
  - performance_dentro_SLA: true
  - nenhum_worker_quebrado: true

---

### 📄 TERMINAL_EXECUTION.md

```markdown
# TERMINAL_EXECUTION.md — Claude Code Execution Layer

## Princípio Fundamental

A execução de código em terminal via Claude Code Runtime é **controlada**, **sandboxed** e **totalmente auditada**. Nenhum código é executado sem validação prévia, sandbox isolado e logging completo.

---

## Escopo de Execução

```yaml
TERMINAL_EXECUTION_SCOPE:

  PERMITIDO:
    - scripts Python aprovados
    - comandos bash em whitelist
    - automação de tarefas repetitivas
    - processamento de dados em lote
    - integração com CLI tools aprovadas

  PROIBIDO:
    - acesso a sistema fora do sandbox
    - modificação de código em produção
    - execução de código não revisado
    - acesso a credenciais ou secrets
    - operações de rede não aprovadas
    - reasoning ou LLM calls
    - comandos destrutivos (rm -rf, dd, etc.)
--------------------------------------------------------------------------------
Sandbox de Terminal
TERMINAL_SANDBOX:

  FILESYSTEM:
    root: "/sandbox/terminal/{execution_id}/"
    allowed_paths:
      - "/sandbox/terminal/**"
      - "/tmp/brachat/**"
      - "/usr/bin/python3" (read-only)
      - "/bin/bash" (read-only)
    forbidden_paths:
      - "/etc", "/root", "/home", "/var"
      - "/proc", "/sys", "/dev"
    max_file_size_mb: 10
    max_total_storage_mb: 100
    read_only_system_binaries: true

  NETWORK:
    allowed_outbound:
      - "api.brachat.internal:443"
      - "notebook.llm:443"
      - "*.approved-domain.com:80|443"
    blocked_outbound: ALL_ELSE
    dns_allowed: ["brachat.internal", "approved-domain.com"]
    max_connections: 3
    connection_timeout_seconds: 30

  PROCESSES:
    max_processes: 3
    max_cpu_percent: 50
    max_memory_mb: 512
    max_execution_time_seconds: 300
    allowed_binaries:
      - "/usr/bin/python3"
      - "/bin/bash"
      - "/usr/bin/grep"
      - "/bin/cat"
      - "/usr/bin/awk"
      - "/usr/bin/sed"
      - "/usr/bin/wc"
    forbidden_binaries:
      - "sudo", "su", "chmod", "chown", "chroot"
      - "rm", "mv", "dd", "mkfs", "fdisk"
      - "curl", "wget", "nc", "telnet", "ssh"
      - "kill", "pkill", "killall"
      - "docker", "podman", "containerd"
--------------------------------------------------------------------------------
Solicitação de Execução
Request Format
{
  "execution_request": {
    "request_id": "TERM_20260124_001",
    "agent_id": "AGT_NICE_MKT_001",
    "context_id": "CTX_7F3A9B2E",
    "code_type": "python_script | bash_command | python_repl",
    "code": "print('Hello from sandbox')",
    "input_data": {},
    "environment_vars": {
      "BRA_CHAT_CONTEXT_ID": "CTX_7F3A9B2E",
      "BRA_CHAT_AGENT_ID": "AGT_NICE_MKT_001"
    },
    "timeout_seconds": 30,
    "requires_approval": false,
    "approval_id": null,
    "sandbox_profile": "domestic | corporate"
  }
}
Response Format
{
  "execution_response": {
    "request_id": "TERM_20260124_001",
    "status": "SUCCESS | FAILED | TIMEOUT | VIOLATION",
    "stdout": "Hello from sandbox\n",
    "stderr": "",
    "exit_code": 0,
    "duration_ms": 125,
    "resource_usage": {
      "cpu_percent": 12.5,
      "memory_mb": 48,
      "disk_bytes_written": 0,
      "disk_bytes_read": 1024,
      "network_bytes_sent": 0,
      "network_bytes_received": 0
    },
    "violations": [],
    "output_hash": "sha256:abc123...",
    "sandbox_id": "SBX_20260124_001"
  }
}
--------------------------------------------------------------------------------
Fluxo de Execução
sequenceDiagram
    participant A as Agente
    participant API as Terminal API
    participant S as Sandbox Manager
    participant E as Executor
    participant L as Logger

    A->>API: POST /execute
    API->>API: validate_request
    API->>API: check_approval (if needed)
    API->>S: create_sandbox()
    S-->>API: sandbox_id

    API->>E: execute_in_sandbox(code)

    par Monitoring
        E->>E: monitor_resources()
        E->>E: check_timeout()
        E->>E: detect_violations()
    end

    E-->>API: result
    API->>S: destroy_sandbox()
    API->>L: log_execution()
    API-->>A: response
--------------------------------------------------------------------------------
Implementação do Executor
class TerminalExecutor:
    def __init__(self):
        self.sandbox_manager = SandboxManager()
        self.running_executions = {}

    def execute(self, request, context_id):
        """Executa código em sandbox"""

        # 1. Validar requisição
        if not self.validate_request(request):
            return self.error_response("INVALID_REQUEST")

        # 2. Verificar aprovação (se necessária)
        if request.get("requires_approval"):
            if not self.check_approval(request["approval_id"]):
                return self.error_response("APPROVAL_REQUIRED")

        # 3. Criar sandbox
        sandbox = self.sandbox_manager.create(
            profile=request.get("sandbox_profile", "default"),
            execution_id=request["request_id"]
        )

        # 4. Configurar ambiente
        sandbox.set_environment_vars(request.get("environment_vars", {}))
        sandbox.set_timeout(request["timeout_seconds"])

        # 5. Executar
        try:
            result = sandbox.run(
                code_type=request["code_type"],
                code=request["code"],
                input_data=request.get("input_data")
            )
        except TimeoutError:
            result = self.timeout_response()
        except ViolationError as e:
            result = self.violation_response(e)
        except Exception as e:
            result = self.error_response(str(e))

        # 6. Destruir sandbox
        self.sandbox_manager.destroy(sandbox.id)

        # 7. Log
        self.log_execution(request, result, context_id)

        # 8. Se violação crítica, notificar Aísio
        if result.get("violations"):
            for v in result["violations"]:
                if v["severity"] == "CRITICAL":
                    notify_aisio(v, context_id)
                    activate_kill_switch("TERMINAL_VIOLATION")

        return result
--------------------------------------------------------------------------------
Detecção de Violações
VIOLATION_DETECTION:
  FILESYSTEM_VIOLATIONS:
    - tentativa_de_acessar_path_proibido
    - tentativa_de_escrever_fora_do_sandbox
    - path_traversal_detected
    - file_size_exceeded

  NETWORK_VIOLATIONS:
    - conexão_para_domínio_não_autorizado
    - tentativa_de_bind_port
    - excesso_de_conexões

  PROCESS_VIOLATIONS:
    - execução_de_binário_proibido
    - fork_bomb_detected
    - cpu_exceeded
    - memory_exceeded

  CODE_VIOLATIONS:
    - eval/exec_detected (Python)
    - subprocess_call_detected
    - import_of_forbidden_module
    - environment_variable_access_forbidden

  SEVERITY_LEVELS:
    LOW: log apenas
    MEDIUM: log + notificar gerente
    HIGH: matar processo + isolar sandbox
    CRITICAL: kill_switch + notificar Aísio
--------------------------------------------------------------------------------
Exemplos de Uso
Exemplo 1: Processamento de CSV
{
  "request_id": "TERM_001",
  "agent_id": "AGT_NICE_MKT_001",
  "code_type": "python_script",
  "code": "
import csv
import json

def process_shopping_list(csv_content):
    reader = csv.DictReader(csv_content.splitlines())
    items = []
    for row in reader:
        items.append({
            'name': row['item'],
            'quantity': int(row['qty']),
            'price': float(row['price'])
        })
    return {'items': items, 'total_items': len(items)}
",
  "input_data": {
    "csv_content": "item,qty,price\nleite,2,4.50\npao,3,0.80"
  },
  "timeout_seconds": 10
}
Exemplo 2: Bash para logs
{
  "request_id": "TERM_002",
  "agent_id": "AGT_AUDIT_001",
  "code_type": "bash_command",
  "code": "grep 'ERROR' /sandbox/logs/audit.log | wc -l",
  "timeout_seconds": 5
}
--------------------------------------------------------------------------------
Logs de Execução
{
  "terminal_log": {
    "execution_id": "TERM_20260124_001",
    "request_id": "TERM_001",
    "agent_id": "AGT_NICE_MKT_001",
    "context_id": "CTX_7F3A9B2E",
    "sandbox_id": "SBX_20260124_001",
    "code_hash": "sha256:code_abc",
    "code_type": "python_script",
    "start_time": "2026-01-24T10:30:00.000Z",
    "end_time": "2026-01-24T10:30:00.125Z",
    "duration_ms": 125,
    "status": "SUCCESS",
    "exit_code": 0,
    "stdout_size_bytes": 128,
    "stderr_size_bytes": 0,
    "resource_usage": {
      "cpu_percent": 12.5,
      "max_memory_mb": 48,
      "disk_bytes_written": 0,
      "disk_bytes_read": 2048
    },
    "violations": [],
    "sandbox_cleaned": true
  }
}
--------------------------------------------------------------------------------
Validação do Terminal
Para o sistema ser OPERACIONAL:
TERMINAL_VALIDATION:
  - sandbox_funcionando: true
  - detecção_de_violações_ativa: true
  - tempo_médio_de_execução < SLA: true
  - logs_de_todas_execuções: true
  - nenhuma_violação_crítica_nas_últimas_24h: true

---

### 📄 TASK_LIFECYCLE.md

```markdown
# TASK_LIFECYCLE.md — Ciclo de Vida da Tarefa

## Princípio Fundamental

Toda tarefa no sistema BRACHÁT segue um ciclo de vida padronizado: **CREATE → VALIDATE → EXECUTE → LOG → PERSIST → ROLLBACK**. Cada fase é obrigatória e monitorada.

---

## Ciclo de Vida da Tarefa

```mermaid
stateDiagram-v2
    [*] --> CREATE: Nova tarefa

    CREATE --> VALIDATE: Submeter
    CREATE --> REJECTED: Inválida

    VALIDATE --> APPROVED: Válida
    VALIDATE --> REJECTED: Falha validação
    VALIDATE --> PENDING_APPROVAL: Requer aprovação

    PENDING_APPROVAL --> APPROVED: Aprovada
    PENDING_APPROVAL --> REJECTED: Rejeitada

    APPROVED --> EXECUTE: Iniciar

    EXECUTE --> EXECUTING: Em andamento
    EXECUTING --> COMPLETED: Sucesso
    EXECUTING --> FAILED: Falha
    EXECUTING --> TIMEOUT: Tempo excedido

    COMPLETED --> LOG: Registrar
    FAILED --> LOG: Registrar erro
    TIMEOUT --> LOG: Registrar timeout

    LOG --> PERSIST: Persistir
    LOG --> ROLLBACK: Falha crítica

    PERSIST --> DONE: Concluído

    ROLLBACK --> ROLLING_BACK: Revertendo
    ROLLING_BACK --> ROLLED_BACK: Revertido
    ROLLED_BACK --> [*]

    DONE --> [*]
    REJECTED --> [*]
--------------------------------------------------------------------------------
Fases Detalhadas
FASE 1: CREATE (Criação)
CREATE_PHASE:
  description: Tarefa é criada e registrada

  inputs:
    - agent_id: quem criou
    - task_type: string
    - payload: object
    - priority: low|medium|high|critical
    - context_id: string

  outputs:
    - task_id: string (gerado)
    - created_at: timestamp
    - status: CREATED

  validation_rules:
    - agent_id deve existir no registry
    - payload deve validar contra schema do task_type
    - context_id deve ser único
    - priority deve ser válido

  storage:
    location: pending_tasks_queue
    retention: até ser processada

  example:
    task_id: "TASK_20260124_001"
    agent_id: "AGT_PAY_001"
    task_type: "REQUEST_PAYMENT"
    payload: { amount: 1500, beneficiary: "Supplier" }
    priority: "normal"
    context_id: "CTX_7F3A9B2E"
    status: "CREATED"
    created_at: "2026-01-24T10:30:00.000Z"
FASE 2: VALIDATE (Validação)
VALIDATE_PHASE:
  description: Tarefa é validada antes da execução

  checks:
    - permission: agente pode executar esta task_type?
    - contract: respeita limites do contrato?
    - policy: viola alguma política?
    - risk: qual nível de risco?
    - duplicates: já existe tarefa igual pendente?

  outcomes:
    - APPROVED: prossegue para EXECUTE
    - REJECTED: tarefa rejeitada, motivo documentado
    - PENDING_APPROVAL: aguarda aprovação humana/de gerente

  example:
    task_id: "TASK_20260124_001"
    validation_result: "PENDING_APPROVAL"
    reason: "Amount R$1500 exceeds auto-approval threshold of R$500"
    required_approver: "MGR_FIN_001"
    validated_at: "2026-01-24T10:30:00.050Z"
FASE 3: EXECUTE (Execução)
EXECUTE_PHASE:
  description: Tarefa é executada

  states:
    - APPROVED: aguardando início
    - EXECUTING: em andamento
    - COMPLETED: concluída com sucesso
    - FAILED: falhou
    - TIMEOUT: excedeu tempo máximo

  execution_modes:
    - SYNC: aguarda resultado (padrão)
    - ASYNC: executa em background

  timeouts:
    low: 30 segundos
    medium: 60 segundos
    high: 300 segundos
    critical: 600 segundos (com justificativa)

  retry_policy:
    max_retries: 3
    backoff_ms: [100, 500, 2000]
    retryable_errors: ["NETWORK_ERROR", "TIMEOUT", "RATE_LIMIT"]
    non_retryable_errors:
      ["PERMISSION_DENIED", "INVALID_INPUT", "CONTRACT_VIOLATION"]

  example_success:
    task_id: "TASK_20260124_001"
    status: "COMPLETED"
    output: { payment_id: "PAY_123", transaction_id: "TXN_456" }
    duration_ms: 250
    completed_at: "2026-01-24T10:30:00.300Z"

  example_failure:
    task_id: "TASK_20260124_001"
    status: "FAILED"
    error: "INSUFFICIENT_FUNDS"
    error_details: "Account balance R$1000 below payment amount R$1500"
    failed_at: "2026-01-24T10:30:00.200Z"
FASE 4: LOG (Registro)
LOG_PHASE:
  description: Resultado da tarefa é registrado

  log_types:
    - action_log: o que foi feito
    - performance_log: quanto tempo levou
    - error_log: se falhou, por quê

  mandatory_fields:
    - task_id
    - timestamp
    - agent_id
    - action
    - status
    - context_id

  storage:
    location: audit_log (imutável)
    retention: 90 dias (padrão)

  example:
    task_id: "TASK_20260124_001"
    log_id: "LOG_20260124_001"
    timestamp: "2026-01-24T10:30:00.350Z"
    agent_id: "AGT_PAY_001"
    action: "REQUEST_PAYMENT"
    status: "COMPLETED"
    duration_ms: 250
    context_id: "CTX_7F3A9B2E"
    log_hash: "sha256:log_abc"
FASE 5: PERSIST (Persistência)
PERSIST_PHASE:
  description: Estado atualizado é persistido no NotebookLLM

  updates:
    - agent_state: estado do agente após tarefa
    - system_state: se aplicável
    - snapshot: se tarefa crítica

  persistence_mode:
    - append_only: novas entradas adicionadas
    - versioned: versões anteriores preservadas

  integrity:
    - hash_chain: updated
    - signature: added

  example:
    task_id: "TASK_20260124_001"
    notebook_entry_id: "NB_20260124_1245"
    sequence: 1245
    state_delta: { balance: "R$8500", last_payment: "TXN_456" }
    snapshot_id: "SNAP_1245"
    persisted_at: "2026-01-24T10:30:00.400Z"
FASE 6: ROLLBACK (Reversão)
ROLLBACK_PHASE:
  description: Tarefa é revertida em caso de falha crítica

  triggers:
    - falha de validação pós-execução
    - violação de política detectada
    - inconsistência de dados
    - comando manual (Aísio | CEO)

  rollback_levels:
    - TASK_ONLY: apenas desfaz esta tarefa
    - CONTEXT: desfaz todas tarefas do mesmo context_id
    - TIMESTAMP: volta a estado anterior no tempo
    - SNAPSHOT: restaura snapshot completo

  rollback_steps: 1. identificar ações a reverter
    2. executar ação reversa (compensação)
    3. validar consistência
    4. atualizar logs
    5. atualizar NotebookLLM

  example:
    task_id: "TASK_20260124_001"
    rollback_id: "RB_20260124_001"
    trigger: "DUPLICATE_PAYMENT_DETECTED"
    rollback_level: "TASK_ONLY"
    compensation_action: "VOID_PAYMENT"
    rolled_back_at: "2026-01-24T10:30:00.500Z"
    status: "ROLLED_BACK"
--------------------------------------------------------------------------------
Implementação do Ciclo de Vida
class TaskLifecycle:
    def __init__(self):
        self.validator = TaskValidator()
        self.executor = TaskExecutor()
        self.logger = TaskLogger()
        self.persister = TaskPersister()
        self.rollback_manager = RollbackManager()

    def process_task(self, task_request, context_id):
        """Processa tarefa através de todo ciclo de vida"""

        # FASE 1: CREATE
        task = self.create_task(task_request, context_id)

        try:
            # FASE 2: VALIDATE
            validation = self.validator.validate(task)

            if validation.status == "REJECTED":
                self.logger.log_rejection(task, validation)
                return {"status": "REJECTED", "reason": validation.reason}

            if validation.status == "PENDING_APPROVAL":
                self.queue_for_approval(task, validation.required_approver)
                return {"status": "PENDING_APPROVAL", "task_id": task.id}

            # FASE 3: EXECUTE
            result = self.executor.execute(task, context_id)

            # Se falhou e é retryable
            if result.status == "FAILED" and result.retryable:
                result = self.retry(task, context_id)

            # FASE 4: LOG
            log_entry = self.logger.log(task, result, context_id)

            # FASE 5: PERSIST (se sucesso)
            if result.status == "COMPLETED":
                self.persister.persist(task, result, context_id)
                return {"status": "COMPLETED", "output": result.output}

            # Se falhou, verificar necessidade de rollback
            if result.status in ["FAILED", "TIMEOUT"]:
                if self.requires_rollback(task, result):
                    # FASE 6: ROLLBACK
                    rollback_result = self.rollback_manager.rollback(
                        task=task,
                        context_id=context_id,
                        reason=result.error
                    )
                    return {"status": "ROLLED_BACK", "rollback_id": rollback_result.id}
                else:
                    return {"status": "FAILED", "error": result.error}

        except CriticalError as e:
            # Falha crítica - rollback imediato
            self.rollback_manager.rollback(
                task=task,
                context_id=context_id,
                reason=str(e)
            )
            activate_kill_switch("TASK_CRITICAL_FAILURE")
            raise

        return {"status": "UNKNOWN"}

    def retry(self, task, context_id, max_retries=3):
        """Tenta executar novamente em caso de falha retryable"""
        for attempt in range(max_retries):
            backoff = 100 * (2 ** attempt)  # 100, 200, 400 ms
            time.sleep(backoff / 1000)

            result = self.executor.execute(task, context_id)
            if result.status == "COMPLETED":
                return result

        return result  # última falha
--------------------------------------------------------------------------------
Estados da Tarefa
TASK_STATES:

  CREATED:
    description: Tarefa criada, aguardando validação
    can_transition_to: [VALIDATING, REJECTED]

  VALIDATING:
    description: Em validação
    can_transition_to: [APPROVED, REJECTED, PENDING_APPROVAL]

  PENDING_APPROVAL:
    description: Aguardando aprovação
    can_transition_to: [APPROVED, REJECTED]

  APPROVED:
    description: Aprovada, pronta para executar
    can_transition_to: [EXECUTING]

  EXECUTING:
    description: Em execução
    can_transition_to: [COMPLETED, FAILED, TIMEOUT]

  COMPLETED:
    description: Concluída com sucesso
    can_transition_to: [] (terminal)

  FAILED:
    description: Falhou
    can_transition_to: [ROLLING_BACK] (se crítico)

  TIMEOUT:
    description: Excedeu tempo máximo
    can_transition_to: [ROLLING_BACK] (se crítico)

  ROLLING_BACK:
    description: Revertendo
    can_transition_to: [ROLLED_BACK]

  ROLLED_BACK:
    description: Revertida
    can_transition_to: [] (terminal)

  REJECTED:
    description: Rejeitada na validação
    can_transition_to: [] (terminal)
--------------------------------------------------------------------------------
Logs do Ciclo de Vida
{
  "task_lifecycle_log": {
    "task_id": "TASK_20260124_001",
    "context_id": "CTX_7F3A9B2E",
    "phases": {
      "create": {
        "timestamp": "2026-01-24T10:30:00.000Z",
        "duration_ms": 1,
        "agent_id": "AGT_PAY_001"
      },
      "validate": {
        "timestamp": "2026-01-24T10:30:00.050Z",
        "duration_ms": 49,
        "result": "APPROVED"
      },
      "execute": {
        "timestamp": "2026-01-24T10:30:00.300Z",
        "duration_ms": 250,
        "result": "COMPLETED"
      },
      "log": {
        "timestamp": "2026-01-24T10:30:00.350Z",
        "duration_ms": 50,
        "log_id": "LOG_20260124_001"
      },
      "persist": {
        "timestamp": "2026-01-24T10:30:00.400Z",
        "duration_ms": 50,
        "notebook_entry_id": "NB_20260124_1245"
      }
    },
    "total_duration_ms": 400,
    "final_status": "COMPLETED"
  }
}
--------------------------------------------------------------------------------
Validação do Ciclo de Vida
Para o sistema ser OPERACIONAL:
TASKS_VALIDATION:
  - toda_tarefa_completa_ciclo_completo: true
  - rollback_funciona_quando_necessário: true
  - logs_de_todas_fases_existem: true
  - nenhuma_tarefa_órfã: true
  - tempo_médio_respeita_SLA: true
--------------------------------------------------------------------------------
Fim do Módulo
Status: 08_EXECUTION_LAYER COMPLETO
Arquivos Gerados:
✅ OPERATION_FLOW.md
✅ STRANDS_WORKERS_MODEL.md
✅ TERMINAL_EXECUTION.md
✅ TASK_LIFECYCLE.md
---
# BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)

## PASSO 9 — 09_DEPENDENCY_GRAPH/

### 📄 AGENT_DEPENDENCIES.md

```markdown
# AGENT_DEPENDENCIES.md — Quem Depende de Quem

## Princípio Fundamental

Todo agente no sistema BRACHÁT pode depender de outros agentes para executar suas funções. Dependências devem ser **explícitas**, **documentadas** e **monitoradas**. Falha em uma dependência deve ser tratada de forma controlada.

---

## Matriz de Dependências

```mermaid
graph LR
    subgraph CEO_LAYER["CEO"]
        CEO[CEO_001]
    end

    subgraph DIRECTOR_LAYER["DIRETORES"]
        EZRA[DIR_EZRA_001]
        GIL[DIR_GILMARIO_001]
        AISIO[DIR_AISIO_001]
        JESS[DIR_JESSICA_001]
    end

    subgraph MANAGER_LAYER["GERENTES"]
        FIN[MGR_FIN_001]
        OPS[MGR_OPS_001]
        CLI[MGR_CLI_001]
        DOC[MGR_DOC_001]
        POL[MGR_POL_001]
        AUD[MGR_AUD_001]
        SEC[MGR_SEC_001]
        CON[MGR_CONT_JUR_001]
    end

    subgraph AGENT_LAYER["AGENTES"]
        PAY[AGT_PAY_001]
        CONT[AGT_CONT_001]
        DELIV[AGT_DELIV_001]
        LGPD[AGT_LGPD_001]
        PENT[AGT_PENTEST_001]
    end

    subgraph DOMESTIC["DOMÉSTICO"]
        LU[NODE_LU_001]
        NICE[AGT_NICE_001]
        DOM_FIN[NICE_FIN_001]
        DOM_MKT[NICE_MKT_001]
    end

    CEO --> EZRA
    CEO --> GIL
    CEO --> AISIO
    CEO --> JESS
    CEO --> LU

    EZRA --> FIN
    EZRA --> OPS
    EZRA --> CLI

    GIL --> DOC

    AISIO --> POL
    AISIO --> AUD
    AISIO --> SEC

    JESS --> CON

    FIN --> PAY
    FIN --> CONT

    OPS --> DELIV

    DOC --> LGPD

    SEC --> PENT

    LU --> NICE
    NICE --> DOM_FIN
    NICE --> DOM_MKT

    style DOMESTIC fill:#f9f,stroke:#333,stroke-width:2px,stroke-dasharray:5 5
--------------------------------------------------------------------------------
Dependências por Agente
CEO Layer
agent_id: CEO_001
name: Fábio Barbosa Everton

dependencies:
  upstream: [] # Ninguém - topo da hierarquia

  downstream:
    - DIR_EZRA_001: reports to CEO
    - DIR_GILMARIO_001: reports to CEO
    - DIR_AISIO_001: reports to CEO
    - DIR_JESSICA_001: reports to CEO
    - NODE_LU_001: reports to CEO

  critical_dependencies: []

  failure_impact:
    if_ceo_down: system_continues (degradado) - Aísio assume emergência

  heartbeat_required: false
Director Layer
agent_id: DIR_EZRA_001
name: Ezra

dependencies:
  upstream:
    - CEO_001: supervisor, aprovações estratégicas

  downstream:
    - MGR_FIN_001: gerente financeiro
    - MGR_EXEC_001: gerente executivo
    - MGR_ARCH_001: arquiteto de soluções
    - MGR_OPS_001: coordenador de operações
    - MGR_CLI_001: gerente de clientes

  critical_dependencies:
    - MGR_FIN_001: operations_critical
    - MGR_OPS_001: operations_critical

  failure_impact:
    if_ezra_down: managers_operate_autonomously, escalations_to_CEO

  heartbeat_required: true
  heartbeat_interval_seconds: 30

---
agent_id: DIR_GILMARIO_001
name: Gilmário

dependencies:
  upstream:
    - CEO_001: supervisor

  downstream:
    - MGR_EST_001: gerente de estudos CEO
    - MGR_BRAND_FRE_001: gerente branding freelancer
    - MGR_BRAND_CAR_001: gerente branding carreira
    - MGR_LIT_001: gerente produções literárias
    - MGR_TUCO_001: gerente estudos Tuco
    - MGR_TEC_001: gerente estudos tecnologia
    - MGR_VIS_001: gerente visibilidade

  critical_dependencies:
    - MGR_EST_001: education_critical
    - MGR_TEC_001: technology_critical

  failure_impact:
    if_gilmario_down: managers_continue_autonomously, reports_to_CEO

---
agent_id: DIR_AISIO_001
name: Aísio

dependencies:
  upstream:
    - CEO_001: supervisor (override only)

  downstream:
    - MGR_DOC_001: gerente documentação
    - MGR_POL_001: gerente policy
    - MGR_AUD_001: gerente auditoria runtime
    - MGR_SEC_001: gerente segurança & pentest
    - MGR_LOG_001: gerente logs & auditoria

  critical_dependencies:
    - MGR_AUD_001: governance_critical
    - MGR_SEC_001: security_critical

  failure_impact:
    if_aisio_down: SYSTEM_HALT (kill switch ativado) - sem governança

  heartbeat_required: true
  heartbeat_interval_seconds: 10
  heartbeat_failure_action: KILL_SWITCH

---
agent_id: DIR_JESSICA_001
name: Jéssica

dependencies:
  upstream:
    - CEO_001: supervisor

  downstream:
    - MGR_CONT_JUR_001: gerente contratual
    - MGR_REG_001: gerente regulatório
    - MGR_INT_JUR_001: gerente interface jurídica

  critical_dependencies:
    - MGR_CONT_JUR_001: legal_critical

  failure_impact:
    if_jessica_down: contract_operations_halted, escalates_to_CEO

  heartbeat_required: true
  heartbeat_interval_seconds: 60
Manager Layer (Amostra)
agent_id: MGR_FIN_001
name: Gerente Financeiro

dependencies:
  upstream:
    - DIR_EZRA_001: supervisor

  downstream:
    - AGT_CASH_001: agente fluxo de caixa
    - AGT_CONT_001: agente contratos
    - AGT_PAY_001: agente pagamentos
    - AGT_REL_001: agente relatórios financeiros

  peer_dependencies:
    - MGR_OPS_001: para aprovação de budgets operacionais
    - MGR_CLI_001: para informações de clientes

  critical_dependencies:
    - AGT_PAY_001: payment_execution_critical

  failure_impact:
    if_manager_down: agents_continue_with_last_instructions, escalations_to_DIR_EZRA

  heartbeat_required: true
  heartbeat_interval_seconds: 60

---
agent_id: MGR_AUD_001
name: Gerente de Auditoria Runtime

dependencies:
  upstream:
    - DIR_AISIO_001: supervisor

  downstream:
    - AGT_MONITOR_001: runtime monitor
    - AGT_ALERTA_001: agente alertas
    - AGT_ROLLBACK_001: agente rollback
    - AGT_OBSERVA_001: agente observabilidade

  peer_dependencies:
    - MGR_SEC_001: para informações de segurança
    - MGR_LOG_001: para logs

  critical_dependencies:
    - AGT_MONITOR_001: monitoring_critical
    - AGT_ROLLBACK_001: rollback_critical

  failure_impact:
    if_manager_down: AUDIT_DEGRADED - notifica Aísio

  heartbeat_required: true
  heartbeat_interval_seconds: 30
Agent Layer (Amostra)
agent_id: AGT_PAY_001
name: Agente de Pagamentos

dependencies:
  upstream:
    - MGR_FIN_001: supervisor

  downstream: [] # agentes não têm dependentes (apenas executam)

  service_dependencies:
    - HERMES: para comunicação
    - STRANDS: para execução de workflows
    - NOTEBOOKLLM: para leitura de estado
    - BANK_API: API externa para pagamentos (crítica)

  critical_service_dependencies:
    - BANK_API: payment_execution

  failure_impact:
    if_agent_down: pagamentos_parados - notifica MGR_FIN_001

  heartbeat_required: true
  heartbeat_interval_seconds: 30

---
agent_id: AGT_PENTEST_001
name: Agente Pentester

dependencies:
  upstream:
    - MGR_SEC_001: supervisor

  service_dependencies:
    - HERMES: para comunicação
    - SANDBOX: para execução isolada

  critical_dependencies: []

  failure_impact:
    if_agent_down: pentest_suspended - notifica MGR_SEC_001

  heartbeat_required: false (não crítico)
Domestic Layer
agent_id: NODE_LU_001
name: Lu

dependencies:
  upstream:
    - CEO_001: supervisor

  downstream:
    - AGT_NICE_001: agente principal doméstico

  critical_dependencies:
    - AGT_NICE_001: domestic_operations

  failure_impact:
    if_lu_down: NICE_opera_com_autonomia_limitada, notifica_CEO

  heartbeat_required: false (humano)

---
agent_id: AGT_NICE_001
name: Nice

dependencies:
  upstream:
    - NODE_LU_001: supervisor humano

  downstream:
    - NICE_FIN_001: finanças domésticas
    - NICE_MKT_001: mercado & compras
    - NICE_CAL_001: agenda familiar
    - NICE_WELL_001: bem-estar
    - NICE_LU_001: apoio à Lu

  peer_dependencies:
    - NICE_FIN_001: para validação de budget
    - NICE_MKT_001: para execução de compras

  critical_dependencies:
    - NICE_FIN_001: budget_control
    - NICE_CAL_001: schedule_coordination

  failure_impact:
    if_nice_down: DOMESTIC_HALT - kill switch doméstico

  heartbeat_required: true
  heartbeat_interval_seconds: 30
--------------------------------------------------------------------------------
Dependências de Serviços
SERVICE_DEPENDENCIES:
  HERMES:
    dependents: ALL_AGENTS
    critical_for: ALL_COMMUNICATION
    failure_impact: SYSTEM_HALT
    backup: nenhum (single source of routing)

  NOTEBOOKLLM:
    dependents: ALL_AGENTS (leitura), SYSTEM (escrita)
    critical_for: STATE_CONSISTENCY
    failure_impact: SYSTEM_READ_ONLY
    backup: snapshot recovery

  STRANDS:
    dependents: AGENTS (execução determinística)
    critical_for: WORKFLOW_EXECUTION
    failure_impact: EXECUTION_DEGRADED (fallback para execução manual)
    backup: executor padrão (limitado)

  SANDBOX:
    dependents: AGENTS (terminal execution), PENTESTER
    critical_for: SECURE_EXECUTION
    failure_impact: TERMINAL_EXECUTION_HALTED
    backup: nenhum (segurança crítica)

  BANK_API:
    dependents: AGT_PAY_001, AGT_CASH_001
    critical_for: PAYMENT_EXECUTION
    failure_impact: PAYMENTS_HALTED
    backup: queue + retry
    external: true

  AISIO_MONITOR:
    dependents: GOVERNANCE_SYSTEM
    critical_for: SYSTEM_SAFETY
    failure_impact: KILL_SWITCH (auto)
    backup: nenhum (single point of governance)
--------------------------------------------------------------------------------
Grafo de Dependências (Formato DOT)
digraph AgentDependencies {
    rankdir=TB;
    node [shape=box, style=filled];

    // CEO
    CEO [fillcolor=red, label="CEO_001"];

    // Directors
    EZRA [fillcolor=orange, label="DIR_EZRA_001"];
    GIL [fillcolor=orange, label="DIR_GILMARIO_001"];
    AISIO [fillcolor=orange, label="DIR_AISIO_001"];
    JESS [fillcolor=orange, label="DIR_JESSICA_001"];
    LU [fillcolor=lightblue, label="NODE_LU_001"];

    // Managers
    FIN [fillcolor=yellow, label="MGR_FIN_001"];
    OPS [fillcolor=yellow, label="MGR_OPS_001"];
    AUD [fillcolor=yellow, label="MGR_AUD_001"];
    SEC [fillcolor=yellow, label="MGR_SEC_001"];

    // Agents
    PAY [fillcolor=lightgreen, label="AGT_PAY_001"];
    PENT [fillcolor=lightgreen, label="AGT_PENTEST_001"];

    // Domestic
    NICE [fillcolor=pink, label="AGT_NICE_001"];
    DOM_FIN [fillcolor=pink, label="NICE_FIN_001"];

    // Dependencies
    CEO -> EZRA;
    CEO -> GIL;
    CEO -> AISIO;
    CEO -> JESS;
    CEO -> LU;

    EZRA -> FIN;
    EZRA -> OPS;

    AISIO -> AUD;
    AISIO -> SEC;

    JESS -> FIN [style=dashed, label="legal"];

    FIN -> PAY;
    SEC -> PENT;

    LU -> NICE;
    NICE -> DOM_FIN;

    // Peer dependencies
    FIN -> OPS [style=dotted, label="peer"];
    AUD -> SEC [style=dotted, label="peer"];
}
--------------------------------------------------------------------------------
Níveis de Criticalidade de Dependência
CRITICALITY_LEVELS:
  CRITICAL:
    description: Sistema para se falhar
    examples:
      - AISIO → AUD
      - HERMES → todos agentes
      - NOTEBOOKLLM → todos agentes
    backup_required: false (não pode falhar)
    slo_uptime: 99.999%

  HIGH:
    description: Operações críticas param
    examples:
      - FIN → PAY
      - EZRA → FIN
      - BANK_API → PAY
    backup_required: true (fallback)
    slo_uptime: 99.9%

  MEDIUM:
    description: Degradação significativa
    examples:
      - GIL → EST
      - DOM_FIN → NICE
    backup_required: false (aceita degradação)
    slo_uptime: 99%

  LOW:
    description: Impacto mínimo
    examples:
      - SEC → PENT
      - VIS → SM
    backup_required: false
    slo_uptime: 95%
--------------------------------------------------------------------------------
Detecção de Dependência
class DependencyDetector:
    def __init__(self):
        self.dependencies = self.load_dependencies()

    def check_dependency_health(self, agent_id, context_id):
        """Verifica saúde das dependências de um agente"""

        deps = self.dependencies.get(agent_id, {})
        results = {}

        # Verificar upstream
        for upstream in deps.get("upstream", []):
            results[upstream] = self.check_agent_health(upstream)
            if not results[upstream] and upstream in deps.get("critical_dependencies", []):
                self.handle_critical_dependency_failure(upstream, agent_id, context_id)

        # Verificar service dependencies
        for service in deps.get("service_dependencies", []):
            results[service] = self.check_service_health(service)
            if not results[service] and service in deps.get("critical_service_dependencies", []):
                self.handle_critical_service_failure(service, agent_id, context_id)

        return results

    def handle_critical_dependency_failure(self, dependency, dependent, context_id):
        """Lida com falha de dependência crítica"""

        log_entry = {
            "event": "CRITICAL_DEPENDENCY_FAILURE",
            "dependency": dependency,
            "dependent": dependent,
            "context_id": context_id,
            "timestamp": now()
        }

        if dependent == "DIR_AISIO_001" and dependency in ["MGR_AUD_001", "MGR_SEC_001"]:
            # Falha de dependência crítica do Aísio = kill switch
            activate_kill_switch("DEPENDENCY_FAILURE", context_id)
        else:
            # Notificar supervisor
            notify_supervisor(dependent, log_entry)
--------------------------------------------------------------------------------
Logs de Dependência
{
  "dependency_log": {
    "log_id": "DEP_20260124_001",
    "context_id": "CTX_7F3A9B2E",
    "check_type": "HEALTH_CHECK",
    "dependent": "AGT_PAY_001",
    "dependencies_checked": [
      { "name": "MGR_FIN_001", "status": "HEALTHY", "response_time_ms": 5 },
      { "name": "HERMES", "status": "HEALTHY", "response_time_ms": 2 },
      { "name": "STRANDS", "status": "HEALTHY", "response_time_ms": 3 },
      {
        "name": "BANK_API",
        "status": "DEGRADED",
        "response_time_ms": 150,
        "error": "slow_response"
      }
    ],
    "critical_failures": 0,
    "overall_status": "DEGRADED",
    "timestamp": "2026-01-24T10:30:00.123Z"
  }
}
--------------------------------------------------------------------------------
Validação de Dependências
Para o sistema ser OPERACIONAL:
DEPENDENCY_VALIDATION:
  - todas_dependencias_documentadas: true
  - dependencias_circulares_detectadas: false
  - dependencias_criticas_saudaveis: true
  - health_checks_ativos: true
  - recovery_plans_existem: true

---

### 📄 SYSTEM_FLOW_GRAPH.md

```markdown
# SYSTEM_FLOW_GRAPH.md — Fluxo Completo do Sistema

## Princípio Fundamental

O fluxo completo do sistema BRACHÁT é a soma de todos os componentes trabalhando em conjunto. Este documento mapeia **visualmente** como mensagens, ações e eventos trafegam através do sistema.

---

## Fluxo Completo em Mermaid

```mermaid
graph TB
    subgraph EXTERNAL["ENTRADAS EXTERNAS"]
        H1[Humano - CEO]
        H2[Humano - Lu]
        API[API Externa]
        TIME[Timer/Agendador]
    end

    subgraph GATEWAY["GATEWAY"]
        AUTH[mTLS Auth]
        RATE[Rate Limiter]
    end

    subgraph HERMES["HERMES - ORQUESTRAÇÃO"]
        H_IN[Receiver]
        H_VAL[Validator]
        H_ROUT[Router]
        H_PRIO[Priority Queue]
    end

    subgraph GOVERNANCE["GOVERNANÇA"]
        ZT[Zero Trust Check]
        AISIO[Aísio Monitor]
        VETO[Veto System]
        KS[Kill Switch]
    end

    subgraph EXECUTION["EXECUÇÃO"]
        LG[LangGraph - State Machine]
        STRANDS[Strands - Determinístico]
        CC[Claude Code - Terminal]
        DEF[Default Executor]
    end

    subgraph VALIDATION["VALIDAÇÃO"]
        CREW[CrewAI - Redundante]
        DC[Double Check]
    end

    subgraph STORAGE["ARMAZENAMENTO"]
        AUDIT[Audit Log - gRPC]
        NOTEBOOK[NotebookLLM - SSOT]
        CACHE[Hermes Cache]
    end

    subgraph OUTPUT["SAÍDAS"]
        RESP[Resposta ao Agente]
        NOTIFY[Notificações]
        EXT_API[APIs Externas]
    end

    subgraph DOMESTIC["DOMÍNIO DOMÉSTICO (ISOLADO)"]
        LU[Lu - Humano]
        NICE[Nice]
        DOM_OPS[Operações Domésticas]
    end

    H1 --> AUTH
    H2 --> AUTH
    API --> AUTH
    TIME --> AUTH

    AUTH --> RATE
    RATE --> H_IN

    H_IN --> H_VAL
    H_VAL --> ZT
    ZT --> AISIO
    AISIO --> VETO
    VETO --> KS

    KS -->|aprovado| H_ROUT
    KS -->|ativado| STOP[PARADA DO SISTEMA]

    H_ROUT --> H_PRIO
    H_PRIO --> LG

    LG --> STRANDS
    LG --> CC
    LG --> DEF

    STRANDS --> CREW
    CC --> CREW
    DEF --> CREW

    CREW --> DC
    DC --> AUDIT
    DC --> NOTEBOOK

    NOTEBOOK --> CACHE
    AUDIT --> RESP
    NOTEBOOK --> RESP

    RESP --> NOTIFY
    RESP --> EXT_API

    DOMESTIC -.->|ISOLADO| HERMES
    DOMESTIC -.->|APENAS CEO| EXTERNAL

    style DOMESTIC fill:#f9f,stroke:#333,stroke-width:3px,stroke-dasharray:5 5
    style KS fill:#f66,stroke:#333,stroke-width:2px
    style AISIO fill:#ff9,stroke:#333,stroke-width:2px
--------------------------------------------------------------------------------
Fluxo Detalhado por Tipo de Mensagem
Fluxo 1: Mensagem Normal (Intra-domínio)
sequenceDiagram
    participant A as Agente Origem
    participant H as Hermes
    participant ZT as Zero Trust
    participant Q as Priority Queue
    participant L as LangGraph
    participant S as Strands
    participant D as Agente Destino
    participant NB as NotebookLLM

    A->>H: Mensagem (mTLS)
    H->>ZT: Validar
    ZT-->>H: OK
    H->>Q: Enfileirar
    Q->>L: Processar
    L->>S: Executar workflow
    S->>D: Entregar
    D-->>S: Resposta
    S->>NB: Atualizar estado
    NB-->>A: Confirmação
Fluxo 2: Mensagem Cross-Domain
sequenceDiagram
    participant A as Agente Origem (DOM_BUSINESS)
    participant H as Hermes
    participant ZT as Zero Trust
    participant GOV as Aísio (Governança)
    participant DOM as Agente Destino (DOM_KNOWLEDGE)
    participant NB as NotebookLLM

    A->>H: Mensagem cross-domain
    H->>ZT: Validar
    ZT-->>H: Cross-domain detectado
    H->>GOV: Solicitar aprovação
    GOV-->>H: Aprovado (com justificativa)
    H->>DOM: Entregar
    DOM-->>H: Resposta
    H->>NB: Log cross-domain
    NB-->>A: Confirmação
Fluxo 3: Ação Crítica com Aprovação
sequenceDiagram
    participant A as Agente
    participant H as Hermes
    participant P as Approval Queue
    participant M as Manager
    participant EX as Executor
    participant NB as NotebookLLM

    A->>H: Ação crítica (amount > R$5000)
    H->>H: Risk = HIGH
    H->>P: Aguardar aprovação
    P->>M: Notificar manager
    M-->>P: Aprovar
    P->>EX: Executar
    EX->>NB: Atualizar estado
    NB-->>A: Confirmação + approval_id
Fluxo 4: Falha e Rollback
sequenceDiagram
    participant A as Agente
    participant EX as Executor
    participant AUD as Auditor
    participant AIS as Aísio
    participant KS as Kill Switch
    participant RB as Rollback
    participant NB as NotebookLLM

    A->>EX: Executar ação
    EX->>AUD: Log início
    EX--xEX: Falha crítica
    EX->>AUD: Log falha
    AUD->>AIS: Notificar
    AIS->>KS: Ativar kill switch (MODE_2)
    KS->>RB: Trigger rollback
    RB->>NB: Restaurar snapshot anterior
    NB-->>A: Estado restaurado
    AIS->>A: Notificação de falha + rollback
Fluxo 5: Fluxo Doméstico (Isolado)
sequenceDiagram
    participant LU as Lu (humano)
    participant NICE as Nice
    participant DOM as Agente Doméstico
    participant DOM_NB as NotebookLLM (isolado)
    participant CORP as Sistema Corporativo

    LU->>NICE: Aprovar compra
    NICE->>DOM: Executar compra
    DOM->>DOM_NB: Registrar (doméstico)

    DOM-xCORP: BLOQUEADO (cross-domain)
    Note over DOM,CORP: Zero Trust bloqueia

    DOM_NB-->>LU: Confirmação
    LU->>LU: Visualiza no Obsidian
--------------------------------------------------------------------------------
Estados do Sistema
SYSTEM_STATES:
  OPERATIONAL:
    description: Sistema funcionando normalmente
    allowed_flows: TODOS
    kill_switch: INACTIVE

  DEGRADED:
    description: Algum componente com falha, mas sistema opera
    allowed_flows: MAIORIA (exceto componente afetado)
    kill_switch: INACTIVE
    examples:
      - "Pentester offline"
      - "Cache do Hermes lento"

  READ_ONLY:
    description: Apenas leituras permitidas
    allowed_flows: APENAS CONSULTAS
    kill_switch: INACTIVE
    trigger: NOTEBOOKLLM_CORRUPTION_DETECTED

  QUARANTINE:
    description: Agente ou domínio isolado
    allowed_flows: ISOLADO (nenhum fluxo para/do afetado)
    kill_switch: INACTIVE
    trigger: AGENT_VIOLATION

  HALTED:
    description: Sistema parado por kill switch
    allowed_flows: NENHUM
    kill_switch: ACTIVE
    trigger: AISIO | CEO | AUTO_CONDITION
--------------------------------------------------------------------------------
Métricas de Fluxo
FLOW_METRICS:
  HOURLY_METRICS:
    - messages_total
    - messages_by_priority
    - cross_domain_messages
    - approvals_requested
    - approvals_granted
    - approvals_rejected
    - failures_total
    - rollbacks_total
    - kill_switch_activations

  LATENCY_SLA:
    p50: < 100ms
    p95: < 500ms
    p99: < 2000ms
    critical_path: < 50ms

  THROUGHPUT_CAPACITY:
    messages_per_second: 1000
    concurrent_executions: 100
    queue_capacity: 10000
--------------------------------------------------------------------------------
Logs de Fluxo
{
  "flow_log": {
    "flow_id": "FLOW_20260124_001",
    "flow_type": "NORMAL | CROSS_DOMAIN | CRITICAL | DOMESTIC",
    "context_id": "CTX_7F3A9B2E",
    "trace_id": "TRC_456",
    "path": [
      { "node": "AGENT_ORIGEM", "agent": "AGT_PAY_001", "timestamp": "T0" },
      { "node": "HERMES_RECEIVER", "timestamp": "T0+1ms" },
      { "node": "ZERO_TRUST", "timestamp": "T0+5ms", "result": "PASS" },
      { "node": "HERMES_ROUTER", "timestamp": "T0+8ms" },
      {
        "node": "PRIORITY_QUEUE",
        "timestamp": "T0+10ms",
        "priority": "NORMAL"
      },
      { "node": "LANGGRAPH", "timestamp": "T0+15ms" },
      { "node": "STRANDS", "timestamp": "T0+20ms", "duration_ms": 120 },
      { "node": "CREWAI", "timestamp": "T0+140ms", "result": "VALID" },
      { "node": "NOTEBOOKLLM", "timestamp": "T0+160ms" },
      {
        "node": "AGENT_DESTINO",
        "agent": "MGR_FIN_001",
        "timestamp": "T0+200ms"
      }
    ],
    "total_duration_ms": 200,
    "status": "SUCCESS"
  }
}
--------------------------------------------------------------------------------
Validação do Fluxo
Para o sistema ser OPERACIONAL:
FLOW_VALIDATION:
  - fluxos_teste_passam: true
  - cross_domain_bloqueado_corretamente: true
  - isolamento_domestico_funciona: true
  - kill_switch_interrompe_fluxos: true (testado)
  - rollback_restaura_fluxo: true
  - latência_dentro_SLA: true

---

### 📄 FAILURE_CHAIN_MODEL.md

```markdown
# FAILURE_CHAIN_MODEL.md — Cascata de Falhas e Isolamento de Erros

## Princípio Fundamental

No sistema BRACHÁT, falhas são **inevitáveis**, mas **cascatas** são **preveníveis**. Este documento define como falhas se propagam, como são isoladas e como o sistema se recupera.

---

## Modelo de Cascata de Falhas

```mermaid
graph TD
    subgraph ROOT["FALHA RAIZ"]
        F1[Agente PAY falha]
    end

    subgraph CASCADE["CASCATA"]
        F2[Dependências falham]
        F3[Mensagens acumulam]
        F4[Fila transborda]
        F5[Outros agentes degradam]
        F6[Sistema entra em falha geral]
    end

    subgraph ISOLATION["ISOLAMENTO"]
        I1[Detecção]
        I2[Quarentena do agente]
        I3[Redirecionamento]
        I4[Circuit breaker]
        I5[Kill switch local]
    end

    subgraph RECOVERY["RECUPERAÇÃO"]
        R1[Rollback]
        R2[Restart do agente]
        R3[Failover]
        R4[Replay]
    end

    F1 --> CASCADE
    CASCADE --> ISOLATION
    ISOLATION --> RECOVERY

    style F1 fill:#f66,stroke:#333
    style I2 fill:#9f9,stroke:#333
    style I5 fill:#ff9,stroke:#333
--------------------------------------------------------------------------------
Tipos de Falha
FAILURE_TYPES:
  TYPE_1_AGENT_FAILURE:
    description: Agente específico falha ou fica indisponível
    examples:
      - agente_caiu
      - agente_timeout
      - agente_resposta_invalida
      - agente_violou_contrato

    propagation:
      - upstream: supervisor é notificado
      - downstream: dependentes ficam sem serviço
      - peers: podem ser afetados indiretamente

    isolation:
      - quarantine: agente isolado
      - circuit_breaker: chamadas bloqueadas

  TYPE_2_SERVICE_FAILURE:
    description: Serviço crítico (Hermes, NotebookLLM) falha
    examples:
      - hermes_offline
      - notebook_corrompido
      - strands_timeout

    propagation:
      - ALL_AGENTS: TODOS afetados
      - system: entra em modo degradado ou halt

    isolation:
      - failover: se disponível
      - kill_switch: se serviço crítico

  TYPE_3_DEPENDENCY_FAILURE:
    description: Dependência externa (API de banco) falha
    examples:
      - bank_api_offline
      - network_partition
      - rate_limit_externo

    propagation:
      - agentes_que_usam_dependencia
      - upstream_notificados

    isolation:
      - retry_queue
      - circuit_breaker
      - fallback_value

  TYPE_4_DATA_CORRUPTION:
    description: Dados inconsistentes ou corrompidos
    examples:
      - notebook_hash_invalido
      - estado_inconsistente
      - log_auditoria_quebrado

    propagation:
      - ALL_SYSTEM: risco de contaminação

    isolation:
      - read_only_mode
      - rollback_imediato
      - kill_switch

  TYPE_5_SECURITY_VIOLATION:
    description: Violação de segurança detectada
    examples:
      - cross_domain_tentado
      - sandbox_escape
      - auth_failure_repetida

    propagation:
      - agente_ofensor: isolado
      - domínio: pode ser isolado

    isolation:
      - quarantine_permanente
      - kill_switch_se_critico
--------------------------------------------------------------------------------
Mecanismos de Isolamento
1. Circuit Breaker
CIRCUIT_BREAKER:
  STATES:
    CLOSED:
      description: Circuito fechado, fluxo normal
      conditions: error_rate < 10%
      actions: permite todas chamadas

    OPEN:
      description: Circuito aberto, fluxo bloqueado
      conditions: error_rate > 50% por 30 segundos
      actions:
        - bloqueia novas chamadas
        - retorna erro imediato (fail fast)
        - notifica supervisor
      duration: 60 segundos (padrão)

    HALF_OPEN:
      description: Testando recuperação
      conditions: após OPEN timeout
      actions:
        - permite 1 chamada de teste
        - se sucesso → CLOSED
        - se falha → OPEN novamente

  IMPLEMENTATION:
    por_serviço: true
    por_agente: true
    por_dependencia: true

  example:
    service: "BANK_API"
    state: "OPEN"
    error_rate: 85%
    opened_at: "2026-01-24T10:30:00Z"
    will_try_at: "2026-01-24T10:31:00Z"
2. Bulkhead (Isolamento de Recursos)
BULKHEAD:
  description: Isola pools de recursos para evitar contaminação

  pools:
    DOM_BUSINESS:
      max_concurrent: 50
      queue_size: 200
      timeout_seconds: 30

    DOM_DOMESTIC:
      max_concurrent: 10
      queue_size: 50
      timeout_seconds: 10

    DOM_GOVERNANCE:
      max_concurrent: 20
      queue_size: 100
      timeout_seconds: 5 (prioridade)

  isolation_benefit:
    - falha em um domínio não afeta outros
    - recursos são dedicados
    - overflows são tratados localmente
3. Retry com Backoff
RETRY_POLICY:

  TRANSIENT_FAILURES:
    errors_retryable:
      - NETWORK_TIMEOUT
      - SERVICE_UNAVAILABLE
      - RATE_LIMIT
      - DEADLINE_EXCEEDED

    errors_non_retryable:
      - PERMISSION_DENIED
      - INVALID_INPUT
      - CONTRACT_VIOLATION
      - DATA_CORRUPTION

  RETRY_STRATEGY:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 100
    multiplier: 2
    max_delay_ms: 2000
    jitter: true (random ±20ms)

  example:
    attempt: 1, delay: 100ms
    attempt: 2, delay: 200ms
    attempt: 3, delay: 400ms
4. Timeout e Deadline
TIMEOUT_POLICY:
  PER_LAYER:
    AGENT: 30 segundos
    MANAGER: 60 segundos
    DIRECTOR: 120 segundos
    CEO: 300 segundos (exceção)

  PER_ACTION_TYPE:
    read: 5 segundos
    write: 10 segundos
    execute: 30 segundos
    critical: 60 segundos

  TIMEOUT_ACTION:
    - log_timeout
    - cancel_operation
    - notify_supervisor
    - retry_if_allowed
    - rollback_if_critical
--------------------------------------------------------------------------------
Cadeia de Falhas - Exemplos
Exemplo 1: Falha de Agente de Pagamento
FAILURE_CHAIN_EXAMPLE_1:
  INITIAL_FAILURE:
    component: AGT_PAY_001
    type: AGENT_FAILURE
    reason: "Bank API timeout (5s sem resposta)"
    timestamp: "10:30:00"

  PROPAGATION:
    - 10:30:01 → MGR_FIN_001 detecta falta de heartbeat
    - 10:30:02 → Mensagens para PAY acumulam na fila do Hermes
    - 10:30:05 → Fila atinge 100 mensagens pendentes
    - 10:30:06 → Circuit breaker para PAY é aberto

  ISOLATION:
    action: quarantine_agent PAY
    triggered_by: MGR_FIN_001 (automático)
    timestamp: 10:30:07

  RECOVERY:
    action: restart_agent PAY
    timestamp: 10:30:15
    result: "Bank API recuperada"
    replay: mensagens acumuladas são reprocessadas

  RESOLUTION:
    status: RESOLVED
    duration_seconds: 15
    messages_affected: 100
    messages_success: 98
    messages_failed: 2 (não retryable)
Exemplo 2: Corrupção do NotebookLLM
FAILURE_CHAIN_EXAMPLE_2:
  INITIAL_FAILURE:
    component: NOTEBOOKLLM
    type: DATA_CORRUPTION
    reason: "Hash chain mismatch at entry NB_1244"
    timestamp: "10:30:00"

  PROPAGATION:
    - 10:30:00.001 → Detecção imediata pelo integrity_checker
    - 10:30:00.002 → Leitura do sistema bloqueada (read-only)
    - 10:30:00.003 → Escrita trava
    - 10:30:00.010 → ALL_AGENTS notificados

  ISOLATION:
    action: read_only_mode + kill_switch (MODE_3)
    triggered_by: Aísio (automático)
    timestamp: 10:30:00.050

  RECOVERY:
    action: rollback_to_snapshot SNAP_1243
    triggered_by: CEO_001
    timestamp: 10:30:05
    duration: 30 segundos

  RESOLUTION:
    status: RESOLVED (rollback bem-sucedido)
    duration_seconds: 35
    data_loss: entries NB_1244 (corrompido) -> perdido
    root_cause: "Disk corruption"
    action_taken: "Migrar para storage redundante"
Exemplo 3: Violação Cross-Domain
FAILURE_CHAIN_EXAMPLE_3:
  INITIAL_FAILURE:
    component: AGT_SUSPECT (não registrado)
    type: SECURITY_VIOLATION
    reason: "Tentativa de acesso DOM_DOMESTIC → DOM_BUSINESS"
    timestamp: "10:30:00"

  PROPAGATION:
    - 10:30:00.001 → Zero Trust bloqueia mensagem
    - 10:30:00.002 → Log de violação
    - 10:30:00.010 → Aísio notificado

  ISOLATION:
    action: quarantine_agent + isolate_domain DOM_DOMESTIC
    triggered_by: Aísio (automático)
    timestamp: 10:30:00.100
    mode: MODE_5 (domestic isolation)

  RECOVERY:
    action: forensic_analysis + agent_review
    triggered_by: Aísio + CEO
    timestamp: 10:31:00
    duration: 2 horas (investigação)

  RESOLUTION:
    status: RESOLVED
    finding: "Certificado do agente expirado, renovação não autorizada"
    action: "Revogar certificado, reinstalar agente"
    domestic_released: "11:30:00"
--------------------------------------------------------------------------------
Matriz de Impacto de Falha
IMPACT_MATRIX:
  FAILURE → IMPACT:
    AGENT_FAILURE:
      - downstream: dependentes sem serviço
      - upstream: supervisor notificado
      - users: afetados se agente crítico
      - business: baixo a médio

    MANAGER_FAILURE:
      - downstream: agentes sem supervisão
      - upstream: diretor notificado
      - users: aprovações atrasam
      - business: médio

    DIRECTOR_FAILURE:
      - downstream: gerentes sem direção
      - upstream: CEO notificado
      - users: decisões estratégicas atrasam
      - business: alto

    AISIO_FAILURE:
      - system: KILL_SWITCH (crítico)
      - users: sistema para
      - business: MUITO ALTO (catastrófico)

    HERMES_FAILURE:
      - system: comunicação para
      - users: sem interação
      - business: MUITO ALTO

    NOTEBOOKLLM_FAILURE:
      - system: read-only ou halt
      - users: consultas apenas
      - business: ALTO
--------------------------------------------------------------------------------
Implementação do Gerenciamento de Falhas
class FailureChainManager:
    def __init__(self):
        self.circuit_breakers = {}
        self.failure_history = []

    def handle_failure(self, failure, context_id):
        """Gerencia falha e previne cascata"""

        # 1. Classificar falha
        failure_type = self.classify_failure(failure)

        # 2. Registrar
        self.log_failure(failure, failure_type, context_id)

        # 3. Aplicar isolamento
        isolation_action = self.isolate_failure(failure, failure_type, context_id)

        # 4. Notificar partes interessadas
        self.notify_stakeholders(failure, isolation_action, context_id)

        # 5. Tentar recuperação
        if self.can_recover(failure_type):
            recovery = self.attempt_recovery(failure, context_id)
            return recovery

        # 6. Se não pode recuperar, escalar
        return self.escalate_failure(failure, failure_type, context_id)

    def isolate_failure(self, failure, failure_type, context_id):
        """Isola falha para evitar cascata"""

        if failure_type == "AGENT_FAILURE":
            # Isolar agente
            self.circuit_breakers[failure.agent_id] = CircuitBreaker.OPEN
            agent_manager.quarantine(failure.agent_id)
            return {"action": "QUARANTINE_AGENT", "target": failure.agent_id}

        elif failure_type == "SERVICE_FAILURE":
            if failure.service == "NOTEBOOKLLM":
                system_state.set_read_only()
                return {"action": "READ_ONLY_MODE"}
            elif failure.service == "HERMES":
                activate_kill_switch("SERVICE_FAILURE", context_id)
                return {"action": "KILL_SWITCH"}

        elif failure_type == "SECURITY_VIOLATION":
            if failure.severity == "CRITICAL":
                activate_kill_switch("SECURITY_VIOLATION", context_id)
            else:
                agent_manager.quarantine(failure.agent_id)
            return {"action": "QUARANTINE + KILL_SWITCH"}

        return {"action": "LOG_ONLY"}
--------------------------------------------------------------------------------
Logs de Falha
{
  "failure_log": {
    "failure_id": "FAIL_20260124_001",
    "context_id": "CTX_7F3A9B2E",
    "failure_type": "AGENT_FAILURE",
    "component": "AGT_PAY_001",
    "error": "Bank API timeout after 5000ms",
    "severity": "HIGH",
    "propagation": {
      "affected_upstream": ["MGR_FIN_001"],
      "affected_downstream": [],
      "affected_peers": ["AGT_CASH_001", "AGT_CONT_001"],
      "affected_messages": 100
    },
    "isolation": {
      "action": "QUARANTINE_AGENT",
      "triggered_by": "auto_circuit_breaker",
      "timestamp": "2026-01-24T10:30:01Z"
    },
    "recovery": {
      "attempted": true,
      "success": true,
      "duration_seconds": 15,
      "method": "RESTART_AGENT"
    },
    "resolved_at": "2026-01-24T10:30:16Z",
    "duration_seconds": 16
  }
}
--------------------------------------------------------------------------------
Validação de Falhas
Para o sistema ser OPERACIONAL:
FAILURE_VALIDATION:
  - circuit_breakers_funcionando: true
  - isolamento_agente_funciona: true
  - rollback_restaura_estado: true
  - kill_switch_para_sistema: true (testado)
  - tempo_recuperação_aceitável: true
  - logs_de_todas_falhas: true
--------------------------------------------------------------------------------
Fim do Módulo
Status: 09_DEPENDENCY_GRAPH COMPLETO
Arquivos Gerados:
✅ AGENT_DEPENDENCIES.md
✅ SYSTEM_FLOW_GRAPH.md
✅ FAILURE_CHAIN_MODEL.md
---
# BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)

## PASSO 10 — 10_PRODUCTION_CRITERIA/

### 📄 KPI_SYSTEM_READY.md

```markdown
# KPI_SYSTEM_READY.md — Critérios de Sistema Vivo

## Princípio Fundamental

O sistema BRACHÁT só é considerado **VIVO** e **OPERACIONAL** se todos os KPIs definidos neste documento forem atendidos. KPIs são monitorados em tempo real por Aísio e pelo sistema de observabilidade.

---

## KPIs de Disponibilidade

```yaml
AVAILABILITY_KPIS:

  KPI_001_UPTIME:
    name: "Disponibilidade do Sistema"
    target: 99.9% (mensal)
    calculation: (tempo_operacional / tempo_total) * 100
    exceptions: manutenção programada (máx 4h/mês)
    current: 99.95%
    status: ✅ Atingido

  KPI_002_COMPONENT_HEALTH:
    name: "Saúde dos Componentes Críticos"
    components:
      - HERMES: 100% (obrigatório)
      - NOTEBOOKLLM: 100% (obrigatório)
      - AISIO: 100% (obrigatório)
      - STRANDS: >99%
      - CLAUDE_CODE: >99%
    current:
      HERMES: 100%
      NOTEBOOKLLM: 100%
      AISIO: 100%
      STRANDS: 99.5%
      CLAUDE_CODE: 99.2%
    status: ✅ Atingido

  KPI_003_NO_SINGLE_POINT_OF_FAILURE:
    name: "Ausência de SPOF Não Mitigado"
    target: Nenhum componente sem redundância
    critical_components:
      - NOTEBOOKLLM: replicado (3x)
      - HERMES: cluster (5x)
      - AISIO: standby quente
    status: ✅ Atingido
--------------------------------------------------------------------------------
KPIs de Performance
PERFORMANCE_KPIS:

  KPI_004_LATENCY_P50:
    name: "Latência Mediana"
    target: < 100ms (ação normal)
    measurement: p50 de todas ações
    current: 45ms
    status: ✅ Atingido

  KPI_005_LATENCY_P95:
    name: "Latência Percentil 95"
    target: < 500ms
    measurement: p95 de todas ações
    current: 320ms
    status: ✅ Atingido

  KPI_006_LATENCY_P99:
    name: "Latência Percentil 99"
    target: < 2000ms
    measurement: p99 de todas ações
    current: 850ms
    status: ✅ Atingido

  KPI_007_THROUGHPUT:
    name: "Vazão do Sistema"
    target: > 500 ações/segundo
    measurement: média de ações por segundo
    current: 750 ações/segundo
    status: ✅ Atingido

  KPI_008_QUEUE_DEPTH:
    name: "Profundidade da Fila"
    target: < 100 mensagens (média)
    measurement: tamanho médio das filas do Hermes
    current: 12 mensagens
    status: ✅ Atingido

  KPI_009_SANDBOX_STARTUP:
    name: "Tempo de Criação do Sandbox"
    target: < 500ms
    measurement: tempo para criar sandbox para execução
    current: 120ms
    status: ✅ Atingido
--------------------------------------------------------------------------------
KPIs de Qualidade
QUALITY_KPIS:

  KPI_010_SUCCESS_RATE:
    name: "Taxa de Sucesso de Ações"
    target: > 98% (ações normais)
    calculation: (ações_sucesso / ações_totais) * 100
    current: 99.2%
    status: ✅ Atingido

  KPI_011_ERROR_RATE:
    name: "Taxa de Erro"
    target: < 2%
    calculation: (ações_falha / ações_totais) * 100
    current: 0.8%
    status: ✅ Atingido

  KPI_012_RETRY_RATE:
    name: "Taxa de Retry"
    target: < 5%
    calculation: (ações_retry / ações_totais) * 100
    current: 1.2%
    status: ✅ Atingido

  KPI_013_ROLLBACK_RATE:
    name: "Taxa de Rollback"
    target: < 0.5%
    calculation: (ações_rollback / ações_totais) * 100
    current: 0.05%
    status: ✅ Atingido
--------------------------------------------------------------------------------
KPIs de Governança
GOVERNANCE_KPIS:
  KPI_014_POLICY_VIOLATIONS:
    name: "Violações de Política"
    target: 0 por dia (críticas), < 10 por dia (não-críticas)
    current:
      critical: 0
      non_critical: 3
    status: ✅ Atingido (críticas)

  KPI_015_KILL_SWITCH_ACTIVATIONS:
    name: "Ativações do Kill Switch"
    target: 0 por mês (falsas), < 2 por mês (reais)
    current:
      false: 0
      real: 0
    status: ✅ Atingido

  KPI_016_AUDIT_INTEGRITY:
    name: "Integridade do Audit Log"
    target: 100% (sem corrupção)
    measurement: hash chain validation
    current: 100%
    status: ✅ Atingido

  KPI_017_RESPONSE_TO_VIOLATION:
    name: "Tempo de Resposta a Violações"
    target: < 1 segundo (detecção), < 5 segundos (isolamento)
    current:
      detection: 0.3s
      isolation: 1.2s
    status: ✅ Atingido
--------------------------------------------------------------------------------
KPIs de Segurança
SECURITY_KPIS:
  KPI_018_ZERO_TRUST_EFFECTIVENESS:
    name: "Efetividade do Zero Trust"
    target: 100% (nenhuma violação não detectada)
    measurement: cross-domain tentativas bloqueadas
    current: 100%
    status: ✅ Atingido

  KPI_019_SANDBOX_BREAKOUTS:
    name: "Evasões de Sandbox"
    target: 0
    measurement: tentativas bem-sucedidas de escapar sandbox
    current: 0
    status: ✅ Atingido

  KPI_020_AUTH_FAILURE_RATE:
    name: "Taxa de Falha de Autenticação"
    target: < 0.1% (legítimas), alerta se > 1% (ataque)
    current: 0.02%
    status: ✅ Atingido

  KPI_021_PENTEST_COVERAGE:
    name: "Cobertura de Pentest"
    target: 100% dos componentes testados semanalmente
    current: 100%
    status: ✅ Atingido
--------------------------------------------------------------------------------
KPIs de Negócio
BUSINESS_KPIS:

  KPI_022_CONTRACT_PROCESSING:
    name: "Tempo de Processamento de Contratos"
    target: < 24 horas (simples), < 72 horas (complexo)
    current:
      simple: 4 horas
      complex: 28 horas
    status: ✅ Atingido

  KPI_023_PAYMENT_SUCCESS:
    name: "Taxa de Sucesso de Pagamentos"
    target: > 99%
    current: 99.3%
    status: ✅ Atingido

  KPI_024_DOMESTIC_EFFICIENCY:
    name: "Eficiência Doméstica (Nice)"
    target: redução de 30% no tempo de tarefas domésticas
    current: 35% (Lu report)
    status: ✅ Atingido

  KPI_025_STUDY_COMPLETION:
    name: "Conclusão de Estudos (Tuco)"
    target: 90% das metas semanais
    current: 92%
    status: ✅ Atingido
--------------------------------------------------------------------------------
KPIs de Confiabilidade
RELIABILITY_KPIS:

  KPI_026_MTBF:
    name: "Mean Time Between Failures"
    target: > 72 horas
    calculation: tempo médio entre falhas de sistema
    current: 168 horas (7 dias)
    status: ✅ Atingido

  KPI_027_MTTR:
    name: "Mean Time To Recovery"
    target: < 15 minutos (crítico), < 1 hora (não-crítico)
    current:
      critical: 8 minutos
      non_critical: 25 minutos
    status: ✅ Atingido

  KPI_028_RECOVERY_POINT_OBJECTIVE:
    name: "Recovery Point Objective (RPO)"
    target: < 5 minutos (perda máxima de dados)
    current: 2 minutos (snapshot a cada 5 min)
    status: ✅ Atingido

  KPI_029_RECOVERY_TIME_OBJECTIVE:
    name: "Recovery Time Objective (RTO)"
    target: < 30 minutos (recuperação total)
    current: 15 minutos
    status: ✅ Atingido
--------------------------------------------------------------------------------
Dashboard de KPIs
KPI_DASHBOARD:
  CRITICAL_METRICS:
    - uptime: 99.95%
    - p95_latency: 320ms
    - error_rate: 0.8%
    - policy_violations_critical: 0

  HEALTH_INDICATORS:
    - system_state: OPERATIONAL
    - kill_switch: INACTIVE
    - audit_integrity: VERIFIED
    - zero_trust: ACTIVE

  BUSINESS_INDICATORS:
    - contracts_this_week: 12
    - payments_this_month: R$ 45.000
    - domestic_tasks_automated: 85%
    - study_completion: 92%

  ALERTS_ACTIVE:
    - nenhum
--------------------------------------------------------------------------------
KPI Collection
class KPICollector:
    def __init__(self):
        self.metrics = {}
        self.alert_thresholds = self.load_thresholds()

    def collect_all(self):
        """Coleta todos os KPIs"""

        kpis = {
            # Availability
            "uptime": self.calculate_uptime(),
            "component_health": self.check_components(),

            # Performance
            "latency_p50": self.get_latency(50),
            "latency_p95": self.get_latency(95),
            "latency_p99": self.get_latency(99),
            "throughput": self.get_throughput(),
            "queue_depth": self.get_queue_depth(),

            # Quality
            "success_rate": self.calculate_success_rate(),
            "error_rate": self.calculate_error_rate(),
            "retry_rate": self.calculate_retry_rate(),
            "rollback_rate": self.calculate_rollback_rate(),

            # Governance
            "policy_violations": self.count_policy_violations(),
            "kill_switch_activations": self.count_kill_switch(),
            "audit_integrity": self.verify_audit_integrity(),

            # Security
            "zero_trust_block_rate": self.zero_trust_stats(),
            "sandbox_breakouts": self.count_sandbox_breakouts(),

            # Reliability
            "mtbf": self.calculate_mtbf(),
            "mttr": self.calculate_mttr(),
            "rpo": self.get_rpo(),
            "rto": self.get_rto()
        }

        # Verificar alertas
        alerts = self.check_alerts(kpis)
        if alerts:
            notify_aisio(alerts)

        return kpis

    def check_alerts(self, kpis):
        """Verifica se algum KPI está fora do alvo"""
        alerts = []

        if kpis["uptime"] < 99.9:
            alerts.append(f"Uptime abaixo: {kpis['uptime']}%")

        if kpis["error_rate"] > 2.0:
            alerts.append(f"Error rate alto: {kpis['error_rate']}%")

        if kpis["policy_violations"]["critical"] > 0:
            alerts.append(f"Violations críticas: {kpis['policy_violations']['critical']}")

        if kpis["audit_integrity"] != "VERIFIED":
            alerts.append("AUDIT INTEGRITY FAILED")
            activate_kill_switch("AUDIT_INTEGRITY_FAILURE")

        return alerts
--------------------------------------------------------------------------------
Relatório de KPIs
{
  "kpi_report": {
    "report_id": "KPI_20260124_001",
    "timestamp": "2026-01-24T23:59:59Z",
    "period": "daily",

    "availability": {
      "uptime_percent": 99.95,
      "component_health": "ALL_GREEN",
      "status": "PASS"
    },

    "performance": {
      "latency_p50_ms": 45,
      "latency_p95_ms": 320,
      "latency_p99_ms": 850,
      "throughput_actions_sec": 750,
      "status": "PASS"
    },

    "quality": {
      "success_rate_percent": 99.2,
      "error_rate_percent": 0.8,
      "retry_rate_percent": 1.2,
      "rollback_rate_percent": 0.05,
      "status": "PASS"
    },

    "governance": {
      "policy_violations_critical": 0,
      "kill_switch_activations": 0,
      "audit_integrity": "VERIFIED",
      "status": "PASS"
    },

    "security": {
      "zero_trust_effectiveness": 100,
      "sandbox_breakouts": 0,
      "status": "PASS"
    },

    "business": {
      "contracts_processed": 12,
      "payment_success_rate": 99.3,
      "domestic_efficiency_percent": 35,
      "status": "PASS"
    },

    "reliability": {
      "mtbf_hours": 168,
      "mttr_minutes": 8,
      "rpo_minutes": 2,
      "rto_minutes": 15,
      "status": "PASS"
    },

    "overall_status": "OPERATIONAL",
    "overall_score": 100
  }
}
--------------------------------------------------------------------------------
Validação de KPIs
Para o sistema ser OPERACIONAL:
KPI_VALIDATION:
  - todos_kpis_coletados: true
  - nenhum_kpi_crítico_falhando: true
  - sistema_operacional_últimas_24h: true
  - alertas_resolvidos: true
  - relatório_disponível: true

---

### 📄 TESTING_MODEL.md

```markdown
# TESTING_MODEL.md — Modelo de Testes

## Princípio Fundamental

O sistema BRACHÁT só é confiável se for **testado continuamente** em múltiplos níveis: unitário, integração, caos e runtime. Testes não são opcionais.

---

## Pirâmide de Testes

```mermaid
graph TB
    subgraph RUNTIME["Testes de Runtime<br/>(Contínuo)"]
        RT[Monitoramento<br/>Pentest Contínuo<br/>Caos em Produção]
    end

    subgraph CHAOS["Testes de Caos<br/>(Semanal)"]
        CH[Falhas Simuladas<br/>Kill Switch Teste<br/>Recuperação]
    end

    subgraph INTEGRATION["Testes de Integração<br/>(Diário)"]
        IT[Comunicação<br/>Cross-Domain<br/>Workflows Completos]
    end

    subgraph UNIT["Testes Unitários<br/>(Por Commit)"]
        UT[Agentes<br/>Workers<br/>Validadores]
    end

    RUNTIME --> CHAOS
    CHAOS --> INTEGRATION
    INTEGRATION --> UNIT
--------------------------------------------------------------------------------
Nível 1: Testes Unitários
UNIT_TESTS:
  COBERTURA_REQUERIDA:
    - Agentes: 100% das funções públicas
    - Workers Strands: 100%
    - Validadores: 100%
    - Transformadores: 100%
    - Regras de política: 100%

  TIPOS:
    TYPE_1_FUNCTION_TEST:
      description: Testa função isoladamente
      examples:
        - validador_de_schema
        - calculadora_de_preço
        - formatador_de_data
      mock_external: true

    TYPE_2_CONTRACT_TEST:
      description: Valida contrato do agente
      examples:
        - permissões permitidas vs proibidas
        - thresholds financeiros
        - input/output schemas

    TYPE_3_DETERMINISM_TEST:
      description: Garante que worker é determinístico
      method: mesma entrada → mesma saída (1000x)
      examples: todos workers Strands

  FERRAMENTA: pytest (Python)
  CI: executa por commit
  META: 100% passando antes do merge
Exemplo de Teste Unitário
# test_price_calculator.py
def test_price_calculator_deterministic():
    worker = PriceCalculatorWorker()
    input_data = {"base_price": 100, "tax_rate": 0.1, "discount": 0.2}

    results = []
    for i in range(100):
        result = worker.execute(input_data)
        results.append(result)

    # Todos os resultados devem ser idênticos
    assert all(r == results[0] for r in results)
    assert results[0]["final_price"] == 88.0  # 100 -20% =80, +10% =88

def test_price_calculator_invalid_input():
    worker = PriceCalculatorWorker()
    input_data = {"base_price": -100, "tax_rate": 0.1}

    with pytest.raises(InvalidInputError):
        worker.execute(input_data)

def test_price_calculator_contract():
    worker = PriceCalculatorWorker()

    # Verifica contrato
    assert worker.input_schema.validate({"base_price": 100, "tax_rate": 0.1})
    assert not worker.input_schema.validate({"base_price": "invalid"})
--------------------------------------------------------------------------------
Nível 2: Testes de Integração
INTEGRATION_TESTS:
  COBERTURA_REQUERIDA:
    - Comunicação Hermes: 100%
    - Cross-domain flows: 100%
    - Workflows LangGraph: 100%
    - Notificação Aísio: 100%
    - Persistência NotebookLLM: 100%

  TIPOS:
    TYPE_1_AGENT_COMMUNICATION:
      description: Agentes conversam via Hermes
      test: AGENT_A → Hermes → AGENT_B
      validation: mensagem entregue + logs

    TYPE_2_CROSS_DOMAIN:
      description: Cross-domain é bloqueado ou aprovado
      test: DOM_BUSINESS → DOM_DOMESTIC (deve bloquear)
      validation: zero_trust rejeita + log

    TYPE_3_WORKFLOW_COMPLETO:
      description: Workflow end-to-end
      test: trigger → validação → orquestração → execução → persistência
      validation: todos os steps executados

    TYPE_4_FAILOVER:
      description: Componente falha, sistema recupera
      test: derrubar STRANDS, verificar fallback
      validation: degradação controlada

  FERRAMENTA: docker-compose + pytest-integration
  FREQUÊNCIA: a cada commit na main
  AMBIENTE: staging (idêntico produção)
Exemplo de Teste de Integração
def test_hermes_routing():
    # Setup
    hermes = HermesClient()
    agent_a = MockAgent("AGT_A")
    agent_b = MockAgent("AGT_B")

    # Send message
    message = {
        "from": "AGT_A",
        "to": "AGT_B",
        "intent": "TEST",
        "context_id": "CTX_TEST",
        "risk_level": "low",
        "requires_approval": False,
        "payload": {"data": "test"}
    }

    response = hermes.send(message)

    # Assertions
    assert response["status"] == "DELIVERED"
    assert agent_b.received_message == message
    assert hermes.get_log(message["context_id"])["delivery_status"] == "SUCCESS"

def test_cross_domain_blocked():
    hermes = HermesClient()

    message = {
        "from": "AGT_BUSINESS_001",
        "to": "AGT_DOMESTIC_001",
        "intent": "ACCESS_DOMESTIC",
        "context_id": "CTX_CROSS",
        "risk_level": "high",
        "requires_approval": False,
        "payload": {}
    }

    with pytest.raises(ZeroTrustError):
        hermes.send(message)

    # Verify log
    assert hermes.get_violation_log("CTX_CROSS")["reason"] == "CROSS_DOMAIN_BLOCKED"
--------------------------------------------------------------------------------
Nível 3: Testes de Caos
CHAOS_TESTS:
  PRINCÍPIO: "Quebre o sistema propositalmente para testar resiliência"

  TIPOS:
    TYPE_1_COMPONENT_FAILURE:
      description: Derruba componente aleatório
      examples:
        - matar HERMES
        - derrubar NOTEBOOKLLM
        - desconectar sandbox
      expected: sistema degrada graciosamente ou kill switch ativa

    TYPE_2_LATENCY_INJECTION:
      description: Adiciona latência artificial
      parameters:
        - latency_ms: 1000-5000
        - duration_seconds: 30-120
      expected: sistema mantém operação (degradado)

    TYPE_3_RESOURCE_EXHAUSTION:
      description: Consome recursos propositalmente
      examples:
        - encher fila do Hermes
        - consumir memória
        - alto CPU
      expected: circuit breakers ativam, sistema protege

    TYPE_4_NETWORK_PARTITION:
      description: Isola parte da rede
      examples:
        - isolar DOM_DOMESTIC
        - isolar HERMES de NOTEBOOKLLM
      expected: isolamento funciona, sistema continua

    TYPE_5_DATA_CORRUPTION:
      description: Corrompe dados (controlado)
      examples:
        - modificar hash do notebook
        - corromper log de auditoria
      expected: detecção imediata + rollback/kill switch

  FREQUÊNCIA: semanal (2 horas)
  AMBIENTE: staging (mas com dados reais anonimizados)
  FERRAMENTA: Chaos Mesh + Litmus
  RESPONSÁVEL: Aísio + equipe de engenharia
Exemplo de Teste de Caos
chaos_experiment:
  name: "kill_hermes_and_recover"
  duration: 300s

  steps:
    - name: "kill_hermes"
      type: "pod_kill"
      target: "hermes-pod"
      duration: 30s

    - name: "verify_degradation"
      type: "http_check"
      endpoint: "/health"
      expected_status: 503 (service unavailable)
      duration: 30s

    - name: "restore_hermes"
      type: "pod_restore"
      target: "hermes-pod"

    - name: "verify_recovery"
      type: "http_check"
      endpoint: "/health"
      expected_status: 200
      duration: 60s

    - name: "verify_message_replay"
      type: "queue_check"
      expected: "pending_messages_processed"

  success_criteria:
    - system_recovered_within: 90s
    - no_data_loss: true
    - audit_logs_intact: true
--------------------------------------------------------------------------------
Nível 4: Testes de Runtime
RUNTIME_TESTS:
  DESCRIÇÃO: Testes que rodam continuamente em produção

  TIPOS:
    TYPE_1_HEALTH_CHECKS:
      description: Verifica saúde de componentes
      frequency: a cada 10 segundos
      endpoints:
        - /health (HERMES)
        - /ready (NOTEBOOKLLM)
        - /alive (AISIO)
      failure_action: notificar + tentar restart

    TYPE_2_CANARY_TESTS:
      description: Testa fluxo crítico periodicamente
      frequency: a cada 5 minutos
      test: enviar mensagem de teste pelo sistema
      validation: resposta em < SLA

    TYPE_3_PENTEST_CONTINUO:
      description: Agente pentester testa continuamente
      frequency: 1 ação/minuto
      tests: tentativas de violação controladas
      validation: defesas bloqueiam

    TYPE_4_CONSISTENCY_CHECKS:
      description: Verifica consistência de dados
      frequency: a cada 10 minutos
      checks:
        - notebook_hash_chain
        - audit_log_integrity
        - agent_states_vs_notebook
      failure_action: kill_switch se corrupção

  MONITORAMENTO: Aísio em tempo real
--------------------------------------------------------------------------------
Pipeline de Testes
TEST_PIPELINE:

  CI (CADA COMMIT):
    - unit_tests (2 min)
    - contract_tests (1 min)
    - determinism_tests (5 min)
    duration: ~8 min
    block_merge_if_fail: true

  CD (CADA DEPLOY):
    - integration_tests (15 min)
    - chaos_tests_smoke (5 min)
    - performance_tests (10 min)
    duration: ~30 min
    block_deploy_if_fail: true

  PERIÓDICO (DIÁRIO):
    - full_integration_suite (1 hora)
    - security_scan (30 min)
    - linting_and_style (10 min)

  PERIÓDICO (SEMANAL):
    - full_chaos_suite (2 horas)
    - penetration_test (2 horas)
    - performance_regression (1 hora)

  PERIÓDICO (MENSAL):
    - red_team_exercise (8 horas)
    - disaster_recovery_test (4 horas)
--------------------------------------------------------------------------------
Relatório de Testes
{
  "test_report": {
    "report_id": "TEST_20260124_001",
    "timestamp": "2026-01-24T23:59:59Z",

    "unit_tests": {
      "total": 1247,
      "passed": 1247,
      "failed": 0,
      "skipped": 0,
      "coverage_percent": 98.5
    },

    "integration_tests": {
      "total": 342,
      "passed": 341,
      "failed": 1,
      "failed_tests": ["test_cross_domain_timeout"]
    },

    "chaos_tests": {
      "total": 12,
      "passed": 12,
      "failed": 0,
      "avg_recovery_time_seconds": 45
    },

    "runtime_tests": {
      "health_checks_passed": 100,
      "canary_tests_passed": 100,
      "pentest_blocks": 1240,
      "pentest_success": 0
    },

    "overall_status": "PASSED_WITH_WARNINGS",
    "recommendation": "Fix test_cross_domain_timeout before next deploy"
  }
}
--------------------------------------------------------------------------------
Validação de Testes
Para o sistema ser OPERACIONAL:
TEST_VALIDATION:
  - unit_tests_passando: true (100%)
  - integration_tests_passando: true (95%+)
  - chaos_tests_passando: true (90%+)
  - runtime_tests_ativos: true
  - coverage_unit_acima_95: true
  - nenhum_teste_crítico_quebrado: true

---

### 📄 VALIDATION_GATES.md

```markdown
# VALIDATION_GATES.md — Gates Obrigatórios para Deploy

## Princípio Fundamental

Nada entra em produção no sistema BRACHÁT sem passar pelos **gates de validação**. Cada gate é uma verificação obrigatória que deve ser aprovada para prosseguir.

---

## Pipeline de Deploy com Gates

```mermaid
graph LR
    subgraph GATE_1["GATE 1: Código"]
        C1[Code Review]
        C2[Unit Tests]
        C3[Linter]
    end

    subgraph GATE_2["GATE 2: Integração"]
        I1[Integration Tests]
        I2[Contract Tests]
        I3[Security Scan]
    end

    subgraph GATE_3["GATE 3: Staging"]
        S1[Chaos Tests]
        S2[Performance Tests]
        S3[Canary Deploy]
    end

    subgraph GATE_4["GATE 4: Aprovação"]
        A1[Aísio Approval]
        A2[CEO Approval (se crítico)]
    end

    subgraph PROD["PRODUÇÃO"]
        P1[Deploy]
        P2[Smoke Tests]
        P3[Monitoramento]
    end

    GATE_1 --> GATE_2 --> GATE_3 --> GATE_4 --> PROD
--------------------------------------------------------------------------------
GATE 1: Código (Pre-commit)
GATE_1_CODE:
  name: "Validação de Código"
  location: CI pipeline (pre-merge)
  mandatory: true

  CHECKS:
    CHECK_1_1_CODE_REVIEW:
      description: Pelo menos 1 approver
      approvers:
        - manager_do_agente
        - Aísio (se segurança)
      duration_max: 24 horas

    CHECK_1_2_UNIT_TESTS:
      description: 100% dos testes unitários passando
      coverage_required: > 95%
      blocking: true

    CHECK_1_3_LINTER:
      description: Sem erros de lint
      rules: PEP8 (Python), shellcheck (bash)
      blocking: true

    CHECK_1_4_STATIC_ANALYSIS:
      description: Análise estática de segurança
      tools: bandit, safety
      blocking: true (se critical find)

    CHECK_1_5_DETERMINISM_CHECK:
      description: Workers são determinísticos
      method: execução 100x com mesma entrada
      blocking: true

  FAILURE_ACTION: "Bloquear merge"
  APPROVER: Gerente responsável
--------------------------------------------------------------------------------
GATE 2: Integração (Pre-merge)
GATE_2_INTEGRATION:
  name: "Validação de Integração"
  location: CI pipeline (merge request)
  mandatory: true

  CHECKS:
    CHECK_2_1_INTEGRATION_TESTS:
      description: Testes de integração passando
      required_passing_rate: 100% (críticos), 95% (não-críticos)
      blocking: true

    CHECK_2_2_CONTRACT_TESTS:
      description: Contratos de agentes válidos
      checks:
        - registry_consistente
        - permissões_válidas
        - sem_dependências_circulares
      blocking: true

    CHECK_2_3_SECURITY_SCAN:
      description: Scan de vulnerabilidades
      tools:
        - dependency_check (CVEs)
        - container_scan
        - secret_detection
      blocking: true (se high+ severity)

    CHECK_2_4_BACKWARDS_COMPATIBILITY:
      description: Compatível com versões anteriores?
      checks:
        - schemas_evoluíram corretamente
        - APIs mantidas ou versionadas
      blocking: true (se breaking change sem aviso)

  FAILURE_ACTION: "Bloquear merge + notificar equipe"
  APPROVER: Engenheiro senior
--------------------------------------------------------------------------------
GATE 3: Staging (Pre-deploy)
GATE_3_STAGING:
  name: "Validação em Staging"
  location: CD pipeline (antes do deploy)
  mandatory: true
  duration_min: 30 minutos

  CHECKS:
    CHECK_3_1_CHAOS_TESTS:
      description: Testes de caos em staging
      scenarios:
        - derrubar HERMES
        - matar NOTEBOOKLLM
        - injetar latência
      required_passing_rate: 90%
      blocking: false (warn apenas)

    CHECK_3_2_PERFORMANCE_TESTS:
      description: Performance dentro do SLA
      metrics:
        - latency_p95 < 500ms
        - throughput > 500 actions/sec
      blocking: true (se fora > 20%)

    CHECK_3_3_CANARY_DEPLOY:
      description: Deploy canário (10% do tráfego)
      duration: 15 minutos
      success_criteria:
        - error_rate < 1%
        - latency_p95 < baseline * 1.2
      blocking: true

    CHECK_3_4_DATA_MIGRATION:
      description: Migração de dados (se aplicável)
      validation:
        - dados_migrados_corretamente
        - rollback_funciona
        - sem_perda_de_dados
      blocking: true

  FAILURE_ACTION: "Bloquear deploy para produção"
  APPROVER: Aísio (via automação)
--------------------------------------------------------------------------------
GATE 4: Aprovação (Pre-deploy)
GATE_4_APPROVAL:
  name: "Aprovação Final"
  location: CD pipeline (antes do deploy em produção)
  mandatory: true
  approvers:
    DEFAULT: Aísio (DIR_AISIO_001)
    CRITICAL_CHANGE: Aísio + CEO

  CRITICAL_CHANGES:
    - modificação_na_governanca
    - mudança_de_policy_core
    - alteração_no_kill_switch
    - mudança_no_isolamento_domestico
    - deploy_em_sexta-feira (change advisory board)

  CHECK_4_1_DOCUMENTATION:
    description: Documentação atualizada?
    checks:
      - CHANGELOG atualizado
      - docs atualizadas
      - runbooks atualizados (se aplicável)
    blocking: true

  CHECK_4_2_ROLLBACK_PLAN:
    description: Plano de rollback documentado
    must_contain:
      - steps_to_rollback
      - estimated_duration
      - data_integrity_verification
    blocking: true (se critical change)

  CHECK_4_3_AISIO_VALIDATION:
    description: Aísio valida mudanças
    checks:
      - security_impact_assessed
      - policy_violations_checked
      - zero_trust_impact_analyzed
    blocking: true

  FAILURE_ACTION: "Bloquear deploy até aprovação manual"
--------------------------------------------------------------------------------
Gates Pós-Deploy
POST_DEPLOY_GATES:
  GATE_5_SMOKE_TESTS:
    name: "Smoke Tests em Produção"
    duration: 5 minutos
    checks:
      - health_check: /health → 200
      - canary_message: enviar mensagem de teste
      - agent_response: < SLA
      - audit_log: entrada criada
    failure_action: "Rollback automático"

  GATE_6_MONITORING_WINDOW:
    name: "Janela de Monitoramento"
    duration: 30 minutos
    checks:
      - error_rate < 1%
      - latency_p95 < SLA
      - nenhum_kill_switch_ativo
      - nenhuma_violação_crítica
    failure_action: "Rollback automático (se critical)"

  GATE_7_STAKEHOLDER_CONFIRMATION:
    name: "Confirmação das Partes"
    duration: 1 hora
    approvers:
      - Aísio: valida governança
      - Gerente responsável: valida negócio
      - Lu (se deploy doméstico)
    failure_action: "Reverter ou pausar"
--------------------------------------------------------------------------------
Exemplo de Passagem por Gates
deploy_request:
  id: "DEPLOY_20260124_001"
  component: "AGT_PAY_001"
  change_type: "bug_fix"

  gates:
    gate_1_code:
      status: "PASSED"
      checks:
        { code_review: "APPROVED", unit_tests: "PASSED", linter: "PASSED" }
      duration: "2h 30m"

    gate_2_integration:
      status: "PASSED"
      checks:
        { integration_tests: "PASSED (124/124)", contract_tests: "PASSED" }
      duration: "15m"

    gate_3_staging:
      status: "PASSED"
      checks: { chaos_tests: "PASSED (9/10)", performance: "PASSED" }
      duration: "45m"
      warnings: ["1 chaos test flaky"]

    gate_4_approval:
      status: "PASSED"
      approver: "DIR_AISIO_001"
      approval_time: "2026-01-24T14:30:00Z"

    post_deploy_gate_5_smoke:
      status: "PASSED"
      duration: "5m"

    post_deploy_gate_6_monitoring:
      status: "IN_PROGRESS"
      remaining: "25m"

  overall_status: "IN_PROGRESS"
  estimated_completion: "2026-01-24T15:05:00Z"
--------------------------------------------------------------------------------
Logs de Validação
{
  "validation_log": {
    "gate_id": "GATE_3_STAGING_20260124_001",
    "deploy_id": "DEPLOY_20260124_001",
    "timestamp": "2026-01-24T14:00:00Z",
    "gate_name": "Staging Validation",
    "checks": [
      {
        "check_name": "chaos_tests",
        "status": "PASSED",
        "details": "9/10 passed, 1 flaky",
        "duration_ms": 1800000
      },
      {
        "check_name": "performance_tests",
        "status": "PASSED",
        "metrics": { "latency_p95": 320, "throughput": 750 },
        "thresholds": { "latency_p95": 500, "throughput": 500 },
        "duration_ms": 600000
      }
    ],
    "result": "PASSED",
    "approved_by": "Aísio (auto)",
    "next_gate": "GATE_4_APPROVAL"
  }
}
--------------------------------------------------------------------------------
Validação de Gates
Para o sistema ser OPERACIONAL:
GATES_VALIDATION:
  - todos_gates_implementados: true
  - gate_1_ci_funcionando: true
  - gate_2_integration_funcionando: true
  - gate_3_staging_funcionando: true
  - gate_4_approval_funcionando: true
  - post_deploy_gates_ativos: true
  - rollback_automático_funciona: true

---

### 📄 FAILURE_MODEL.md

```markdown
# FAILURE_MODEL.md — Modos de Falha e Rollback Triggers

## Princípio Fundamental

O sistema BRACHÁT deve antecipar falhas. Este documento define **todos os modos de falha possíveis**, suas **consequências** e os **triggers** que ativam rollback automático.

---

## Modos de Falha

### 1. Falhas de Infraestrutura

```yaml
FAILURE_INFRA:

  F_001_SERVICE_CRASH:
    description: Serviço crítico caiu
    examples:
      - HERMES: mensagens param
      - NOTEBOOKLLM: estado inconsistente
      - AISIO: governança offline
    detection: health_check + heartbeat
    time_to_detect: < 5 segundos
    severity: CRITICAL (se HERMES, AISIO, NOTEBOOKLLM)

    triggers:
      - kill_switch_activation (MODE_3)
      - rollback_auto (se serviço restaurado com dados corrompidos)
      - failover (se redundância disponível)

  F_002_NETWORK_PARTITION:
    description: Rede isolada entre componentes
    examples:
      - DOM_DOMESTIC isolado
      - HERMES não alcança NOTEBOOKLLM
    detection: heartbeat_timeout + cross_check
    time_to_detect: < 10 segundos
    severity: HIGH

    triggers:
      - domain_isolation (se DOM_DOMESTIC)
      - queue_messages (até rede restaurar)
      - read_only_mode (se NOTEBOOKLLM inalcançável)

  F_003_RESOURCE_EXHAUSTION:
    description: Recursos esgotados
    examples:
      - memory_full
      - disk_full
      - cpu_throttled
    detection: resource_monitor
    time_to_detect: < 1 segundo
    severity: HIGH

    triggers:
      - circuit_breaker (abrir para novas ações)
      - shed_load (rejeitar ações low priority)
      - kill_switch (se não resolver em 60s)
2. Falhas de Dados
FAILURE_DATA:
  F_004_NOTEBOOK_CORRUPTION:
    description: NotebookLLM hash chain quebrada
    examples:
      - entry_hash_mismatch
      - signature_invalid
      - previous_hash_not_found
    detection: integrity_checker (cada escrita)
    time_to_detect: < 100ms
    severity: CRITICAL

    triggers:
      - kill_switch_activation (MODE_3) IMMEDIATE
      - read_only_mode
      - rollback_to_last_snapshot (após kill switch)
      - notify_Aísio + CEO

  F_005_AUDIT_CORRUPTION:
    description: Log de auditoria corrompido
    examples:
      - gRPC log missing
      - hash_chain_broken
      - timestamp_inconsistent
    detection: audit_verifier (a cada 5 min)
    time_to_detect: < 5 minutos
    severity: HIGH

    triggers:
      - halt_audit_writes
      - preserve_existing_logs
      - notify_Aísio
      - kill_switch (se corrupção extensa)

  F_006_INCONSISTENT_STATE:
    description: Estado entre agentes inconsistente
    examples:
      - AGENT_PAY pensa que tem R$1000, NOTEBOOKLLM diz R$500
      - agente_reporta_sucesso, log_diz_falha
    detection: cross_check (a cada 10 min)
    time_to_detect: < 10 minutos
    severity: MEDIUM

    triggers:
      - reconcile_state (agente ganha, notebook é fonte da verdade)
      - rollback_context (desfaz ações no context_id)
      - notify_manager
3. Falhas de Agentes
FAILURE_AGENT:
  F_007_AGENT_CRASH:
    description: Agente específico caiu
    examples:
      - processo_agente_morreu
      - agente_timeout
      - agente_resposta_invalida
    detection: heartbeat (30s) + message_timeout
    time_to_detect: < 35 segundos
    severity: MEDIUM (baixo se não crítico)

    triggers:
      - restart_agent (automático, até 3x)
      - quarantine_agent (se restart falhar)
      - failover_to_standby (se disponível)
      - notify_manager

  F_008_AGENT_VIOLATION:
    description: Agente violou contrato ou política
    examples:
      - cross_domain_attempt
      - financial_threshold_exceeded
      - forbidden_action_executed
    detection: zero_trust_checkpoint + Aísio
    time_to_detect: < 100ms
    severity: HIGH (CRITICAL se cross-domain doméstico)

    triggers:
      - quarantine_agent (imediato)
      - rollback_agent_actions (desfaz últimas N ações)
      - notify_Aísio
      - kill_switch (se tentativa de kill_switch por agente não autorizado)

  F_009_DEPENDENCY_FAILURE:
    description: Dependência externa do agente falhou
    examples:
      - BANK_API offline
      - EXTERNAL_SERVICE timeout
      - API_KEY expirada
    detection: executor_circuit_breaker
    time_to_detect: < 1 segundo (após timeout)
    severity: MEDIUM (HIGH se serviço financeiro)

    triggers:
      - circuit_breaker_open (para dependência)
      - queue_requests (para retry)
      - fallback_value (se disponível)
      - notify_manager
4. Falhas de Segurança
FAILURE_SECURITY:
  F_010_SANDBOX_BREAKOUT:
    description: Agente escapou do sandbox
    examples:
      - leu_arquivo_fora_sandbox
      - executou_comando_proibido
      - acessou_rede_externa
    detection: sandbox_monitor
    time_to_detect: < 100ms
    severity: CRITICAL

    triggers:
      - kill_switch (MODE_4_EMERGENCY_STOP)
      - isolate_host (se necessário)
      - forensic_snapshot
      - notify_CEO + Aísio

  F_011_ZERO_TRUST_BYPASS:
    description: Tentativa de burlar zero trust
    examples:
      - mTLS_certificado_falsificado
      - mensagem_assinatura_invalida
      - replay_attack
    detection: zero_trust_checkpoint
    time_to_detect: < 10ms
    severity: CRITICAL

    triggers:
      - reject_message
      - quarantine_agent (origem)
      - kill_switch (se bypass tentado por agente interno)
      - notify_Aísio

  F_012_AUTH_FAILURE_CASCADE:
    description: Múltiplas falhas de autenticação
    examples:
      - 10+ falhas em 1 minuto
      - mesmo_agente_tentando_vários_certificados
    detection: auth_monitor
    time_to_detect: < 1 minuto
    severity: HIGH

    triggers:
      - block_source_IP
      - quarantine_suspected_agent
      - notify_Aísio + security_team
--------------------------------------------------------------------------------
Rollback Triggers
ROLLBACK_TRIGGERS:
  TRIGGER_1_DATA_CORRUPTION:
    condition: NOTEBOOK_CORRUPTION_DETECTED
    rollback_level: SNAPSHOT
    rollback_target: last_valid_snapshot
    auto_execute: true
    requires_approval: false (kill switch já ativou)

  TRIGGER_2_CONSISTENCY_FAILURE:
    condition: agent_state != notebook_state
    rollback_level: CONTEXT
    rollback_target: context_id (último contexto consistente)
    auto_execute: false (requer investigação)
    requires_approval: Aísio

  TRIGGER_3_SECURITY_VIOLATION:
    condition: SANDBOX_BREAKOUT | ZERO_TRUST_BYPASS
    rollback_level: TIMESTAMP
    rollback_target: pre_attack_timestamp
    auto_execute: true (após kill switch)
    requires_approval: false (emergência)

  TRIGGER_4_KILL_SWITCH_MANUAL:
    condition: AISIO_ACTIVATED_KILL_SWITCH
    rollback_level: SNAPSHOT
    rollback_target: last_snapshot_before_kill
    auto_execute: true
    requires_approval: false (já aprovado)

  TRIGGER_5_DEPLOY_FAILURE:
    condition: post_deploy_error_rate > 5%
    rollback_level: SNAPSHOT
    rollback_target: pre_deploy_snapshot
    auto_execute: true
    requires_approval: false (automático)

  TRIGGER_6_MANUAL_ROLLBACK:
    condition: CEO_REQUEST | AISIO_REQUEST
    rollback_level: SPECIFIED (ACTION|CONTEXT|TIMESTAMP|SNAPSHOT)
    rollback_target: as_specified
    auto_execute: false (manual)
    requires_approval: quem solicitou
--------------------------------------------------------------------------------
Matriz de Decisão: Falha → Ação
Falha
Severidade
Detecção
Ação Imediata
Rollback?
Notificação
HERMES crash
CRITICAL
<5s
Kill Switch
SIM (snapshot)
Aísio + CEO
Notebook corrompido
CRITICAL
<100ms
Kill Switch
SIM (snapshot)
Aísio + CEO
Sandbox breakout
CRITICAL
<100ms
Kill Switch (MODE_4)
SIM (timestamp)
Aísio + CEO
Agente crash
MEDIUM
<35s
Restart (3x)
NÃO
Manager
Cross-domain tentado
HIGH
<100ms
Quarentena
SIM (context)
Aísio
Banco offline
MEDIUM
<1s
Circuit breaker + queue
NÃO
Manager
Dado inconsistente
MEDIUM
<10min
Reconciliar
PARCIAL
Aísio
Rate limit excedido
LOW
<1ms
Rejeitar + backoff
NÃO
Nenhum
--------------------------------------------------------------------------------
Implementação do Failure Model
class FailureModel:
    def __init__(self):
        self.failure_handlers = self.load_handlers()
        self.rollback_triggers = self.load_triggers()

    def handle_failure(self, failure, context_id):
        """Manipula falha baseado no modelo"""

        # 1. Classificar falha
        failure_type = self.classify(failure)

        # 2. Verificar severidade
        severity = self.get_severity(failure_type)

        # 3. Aplicar handler
        handler = self.failure_handlers.get(failure_type)
        if handler:
            action = handler(failure, context_id)
        else:
            action = self.default_handler(failure, context_id)

        # 4. Verificar se rollback é necessário
        if self.requires_rollback(failure_type, severity):
            rollback_level = self.get_rollback_level(failure_type)
            chronicle.rollback(level=rollback_level, context_id=context_id)

        # 5. Notificar
        if severity in ["CRITICAL", "HIGH"]:
            notify_aisio(failure, action, context_id)

        if severity == "CRITICAL":
            notify_ceo(failure, action, context_id)

        return action

    def requires_rollback(self, failure_type, severity):
        """Determina se falha requer rollback"""

        rollback_failures = [
            "NOTEBOOK_CORRUPTION",
            "SANDBOX_BREAKOUT",
            "ZERO_TRUST_BYPASS",
            "KILL_SWITCH_ACTIVATED",
            "DEPLOY_FAILURE"
        ]

        return failure_type in rollback_failures or severity == "CRITICAL"
--------------------------------------------------------------------------------
Logs de Falha
{
  "failure_log": {
    "failure_id": "FAIL_20260124_001",
    "failure_type": "NOTEBOOK_CORRUPTION",
    "severity": "CRITICAL",
    "detection_time_ms": 45,
    "details": {
      "entry_id": "NB_1244",
      "expected_hash": "sha256:abc...",
      "actual_hash": "sha256:def...",
      "previous_hash_valid": true
    },
    "action_taken": {
      "immediate": "KILL_SWITCH_ACTIVATED (MODE_3)",
      "rollback": "SNAPSHOT (SNAP_1243)",
      "rollback_success": true
    },
    "notifications": ["Aísio", "CEO"],
    "resolved_at": "2026-01-24T10:30:30Z",
    "resolution": "ROLLBACK_COMPLETED",
    "rpo_seconds": 300,
    "rto_seconds": 30
  }
}
--------------------------------------------------------------------------------
Validação de Falhas
Para o sistema ser OPERACIONAL:
FAILURE_VALIDATION:
  - todos_modos_de_falha_documentados: true
  - handlers_implementados: true
  - rollback_triggers_funcionando: true (testado)
  - tempo_resposta_falhas < SLA: true
  - logs_de_falhas_completos: true
  - recovery_testado_semanalmente: true
--------------------------------------------------------------------------------
Fim do Módulo
Status: 10_PRODUCTION_CRITERIA COMPLETO
Arquivos Gerados:
✅ KPI_SYSTEM_READY.md
✅ TESTING_MODEL.md
✅ VALIDATION_GATES.md
✅ FAILURE_MODEL.md
---
# BRACHÁT — DOCUMENT STRUCTURE TREE (END-TO-END SYSTEM)

## PASSO 11 — 11_BOOTSTRAP/

### 📄 SYSTEM_BOOTSTRAP.md

```markdown
# SYSTEM_BOOTSTRAP.md — Ordem de Inicialização do Sistema

## Princípio Fundamental

O sistema BRACHÁT não pode ser iniciado em qualquer ordem. Existe uma **sequência estrita** de inicialização que garante que todas as dependências estejam disponíveis antes de cada componente ser ativado.

---

## Ordem de Inicialização

```mermaid
graph TB
    subgraph PHASE_0["FASE 0: PRÉ-BOOTSTRAP"]
        P0_1[Verificar Ambiente]
        P0_2[Carregar Configurações]
        P0_3[Validar Certificados]
    end

    subgraph PHASE_1["FASE 1: INFRAESTRUTURA CRÍTICA"]
        P1_1[Storage Imutável]
        P1_2[NotebookLLM - SSOT]
        P1_3[Audit Log gRPC]
    end

    subgraph PHASE_2["FASE 2: SEGURANÇA"]
        P2_1[Zero Trust Checkpoint]
        P2_2[Aísio - Governança]
        P2_3[Kill Switch]
    end

    subgraph PHASE_3["FASE 3: ORQUESTRAÇÃO"]
        P3_1[Hermes]
        P3_2[LangGraph]
        P3_3[Priority Queues]
    end

    subgraph PHASE_4["FASE 4: EXECUÇÃO"]
        P4_1[Strands Workers]
        P4_2[Claude Code Runtime]
        P4_3[Sandbox Manager]
    end

    subgraph PHASE_5["FASE 5: VALIDAÇÃO"]
        P5_1[CrewAI Teams]
        P5_2[Double Check]
    end

    subgraph PHASE_6["FASE 6: AGENTES"]
        P6_1[Agentes CEO/Directors]
        P6_2[Agentes Managers]
        P6_3[Agentes Operacionais]
        P6_4[Agente Pentester]
    end

    subgraph PHASE_7["FASE 7: DOMÉSTICO"]
        P7_1[Sandbox Doméstico]
        P7_2[Nice]
        P7_3[Agentes Domésticos]
    end

    PHASE_0 --> PHASE_1 --> PHASE_2 --> PHASE_3
    PHASE_3 --> PHASE_4 --> PHASE_5 --> PHASE_6
    PHASE_6 --> PHASE_7
--------------------------------------------------------------------------------
FASE 0: PRÉ-BOOTSTRAP (Verificação de Ambiente)
BOOTSTRAP_PHASE_0:
  name: "Pré-Bootstrap - Verificação de Ambiente"
  duration_estimate: 5 segundos
  can_parallelize: false
  blocking: true (sistema não inicia se falhar)

  STEPS:
    STEP_0_1_VERIFY_ENVIRONMENT:
      description: Verifica ambiente de execução
      checks:
        - sistema_operacional: Linux (Ubuntu 22.04+)
        - python_version: 3.11+
        - docker_version: 24.0+
        - kubernetes: (se em cluster) versão 1.28+
        - rede: conectividade com serviços externos
        - clock_sync: NTP sincronizado
      failure_action: ABORT_BOOTSTRAP + log_erro

    STEP_0_2_LOAD_CONFIGURATIONS:
      description: Carrega configurações do sistema
      sources:
        - /etc/brachat/config.yaml (principal)
        - /etc/brachat/secrets.yaml (credenciais)
        - /etc/brachat/policies.yaml (políticas)
      validations:
        - schema_valido: true
        - chaves_obrigatorias_presentes: true
        - sem_syntax_errors: true
      failure_action: ABORT_BOOTSTRAP

    STEP_0_3_VALIDATE_CERTIFICATES:
      description: Valida certificados mTLS
      checks:
        - CA_certificate: válido, não expirado
        - agente_certificates: mínimo 1 (Aísio)
        - certificate_revocation_list: carregada
        - renew_window: > 7 dias
      failure_action: ABORT_BOOTSTRAP + notify_security

    STEP_0_4_CHECK_DEPENDENCIES:
      description: Verifica dependências externas
      checks:
        - BANK_API: health_check (se configuração financeira)
        - STORAGE_BACKEND: acessível
        - OBSERVABILITY_STACK: Prometheus/Grafana online
      failure_action: WARN + CONTINUE (modo degradado)
--------------------------------------------------------------------------------
FASE 1: INFRAESTRUTURA CRÍTICA
BOOTSTRAP_PHASE_1:
  name: "Infraestrutura Crítica"
  duration_estimate: 10 segundos
  depends_on: PHASE_0
  blocking: true

  STEPS:
    STEP_1_1_STORAGE_IMMUTABLE:
      description: Inicializa storage imutável para logs
      actions:
        - montar_volume_immutable
        - verificar_integridade_estrutura
        - carregar_chave_encryptacao
      health_check: /storage/health → 200
      failure_action: ABORT_BOOTSTRAP

    STEP_1_2_NOTEBOOKLLM_SSOT:
      description: Inicializa NotebookLLM (Single Source of Truth)
      actions:
        - carregar_last_snapshot
        - verificar_hash_chain (últimos 100 entries)
        - validar_assinaturas
        - carregar_agent_registry
        - carregar_policies_ativas
      health_check: /notebook/health → 200
      integrity_check: hash_chain_valid → true
      failure_action:
        if minor_corruption: repair_attempt + notify
        if critical: ABORT_BOOTSTRAP

    STEP_1_3_AUDIT_LOG_GRPC:
      description: Inicializa coletor de logs gRPC
      actions:
        - iniciar_servidor_gRPC (porta 50051)
        - conectar_com_storage_imutavel
        - carregar_filtros_auditoria
      health_check: grpc_health_check → SERVING
      failure_action: ABORT_BOOTSTRAP (logs são críticos)
--------------------------------------------------------------------------------
FASE 2: SEGURANÇA
BOOTSTRAP_PHASE_2:
  name: "Camada de Segurança"
  duration_estimate: 5 segundos
  depends_on: PHASE_1
  blocking: true

  STEPS:
    STEP_2_1_ZERO_TRUST_CHECKPOINT:
      description: Ativa Zero Trust
      actions:
        - carregar_policy_engine
        - carregar_matriz_permissoes
        - ativar_mTLS_verifier
        - iniciar_rate_limiter
      health_check: /zerotrust/health → 200
      failure_action: ABORT_BOOTSTRAP

    STEP_2_2_AISIO_GOVERNANCA:
      description: Inicializa Aísio (Governança)
      actions:
        - carregar_regras_governanca
        - carregar_historico_veto
        - iniciar_monitoramento_real_time
        - conectar_kill_switch
        - verificar_heartbeat_aisio (ativo)
      health_check: /aisio/health → 200
      failure_action: ABORT_BOOTSTRAP (sistema sem governança)

    STEP_2_3_KILL_SWITCH:
      description: Ativa Kill Switch
      actions:
        - carregar_config_kill_switch
        - testar_ativacao_simulada (sem parar sistema)
        - verificar_override_CEO
        - conectar_com_aisio
      health_check: /killswitch/health → READY
      failure_action: ABORT_BOOTSTRAP
--------------------------------------------------------------------------------
FASE 3: ORQUESTRAÇÃO
BOOTSTRAP_PHASE_3:
  name: "Orquestração"
  duration_estimate: 10 segundos
  depends_on: PHASE_2
  blocking: true

  STEPS:
    STEP_3_1_HERMES:
      description: Inicializa Hermes (Message Bus)
      actions:
        - carregar_routing_table
        - iniciar_message_receiver (porta 8080)
        - iniciar_priority_queues
        - carregar_dlq (dead letter queue)
        - conectar_com_notebook
        - conectar_com_aisio
      health_check: /hermes/health → 200
      queue_initialization: criar filas (critical, high, normal, low)
      failure_action: ABORT_BOOTSTRAP

    STEP_3_2_LANGGRAPH:
      description: Inicializa LangGraph (State Machines)
      actions:
        - carregar_workflows_registrados
        - validar_workflows (sem ciclos, determinísticos)
        - carregar_state_machines
        - iniciar_worker_pool
      health_check: /langgraph/health → 200
      failure_action: DEGRADED (apenas workflows não LangGraph)

    STEP_3_3_PRIORITY_QUEUES:
      description: Inicializa filas de prioridade
      actions:
        - criar_queues (critical, high, normal, low)
        - configurar_sizes (100, 1000, 10000, 50000)
        - iniciar_consumers
        - conectar_hermes
      health_check: /queues/stats → response
      failure_action: DEGRADED (sem priorização)
--------------------------------------------------------------------------------
FASE 4: EXECUÇÃO
BOOTSTRAP_PHASE_4:
  name: "Execução"
  duration_estimate: 15 segundos
  depends_on: PHASE_3
  blocking: false (pode iniciar em modo degradado)

  STEPS:
    STEP_4_1_STRANDS_WORKERS:
      description: Inicializa Strands Workers
      actions:
        - carregar_todos_workers_registrados
        - validar_determinismo (amostra)
        - iniciar_worker_pool (50 transformers, 30 validators, 10 executors)
        - carregar_workflows_strands
      health_check: /strands/health → 200
      failure_action: DEGRADED (execução mais lenta)
      workers_loaded: 124

    STEP_4_2_CLAUDE_CODE_RUNTIME:
      description: Inicializa Claude Code Runtime (Terminal)
      actions:
        - criar_sandbox_base
        - carregar_whitelist_binarios
        - configurar_timeouts
        - iniciar_terminal_api (porta 8081)
      health_check: /claude/health → 200
      failure_action: DEGRADED (terminal execution off)

    STEP_4_3_SANDBOX_MANAGER:
      description: Inicializa gerenciador de sandboxes
      actions:
        - configurar_isolation_levels
        - criar_sandbox_template (domestic, corporate, pentest)
        - montar_filesystem_isolado
        - configurar_network_policies
      health_check: /sandbox/health → 200
      failure_action: WARN + CONTINUE (alguns agentes não executam)
--------------------------------------------------------------------------------
FASE 5: VALIDAÇÃO
BOOTSTRAP_PHASE_5:
  name: "Validação"
  duration_estimate: 5 segundos
  depends_on: PHASE_4
  blocking: false

  STEPS:
    STEP_5_1_CREWAI_TEAMS:
      description: Inicializa times CrewAI
      actions:
        - carregar_teams_registrados
        - validar_membros (existem no registry)
        - configurar_quorum
        - iniciar_validation_pool
      health_check: /crewai/health → 200
      failure_action: WARN + CONTINUE (validação redundante off)

    STEP_5_2_DOUBLE_CHECK:
      description: Inicializa Double Check
      actions:
        - carregar_acoes_que_requerem_double_check
        - configurar_ambiente_isolado_para_replay
        - iniciar_comparador_resultados
      health_check: /doublecheck/health → 200
      failure_action: WARN + CONTINUE
--------------------------------------------------------------------------------
FASE 6: AGENTES
BOOTSTRAP_PHASE_6:
  name: "Agentes"
  duration_estimate: 30 segundos
  depends_on: PHASE_5
  blocking: false

  STEPS:
    STEP_6_1_CEO_AND_DIRECTORS:
      description: Inicializa CEO e Diretores
      order:
        1: CEO_001 (Fábio Barbosa Everton)
        2: DIR_AISIO_001 (Governança) - prioritário
        3: DIR_EZRA_001 (Operações)
        4: DIR_GILMARIO_001 (Ensino)
        5: DIR_JESSICA_001 (Jurídico)
      actions:
        - carregar_contratos_agentes
        - verificar_permissoes
        - iniciar_heartbeat
        - conectar_hermes
      health_check: cada agente reporta /health
      failure_action:
        if CEO or AISIO fails: SYSTEM_HALT
        if others fail: CONTINUE (notificar)

    STEP_6_2_MANAGERS:
      description: Inicializa Gerentes
      parallel: true
      max_concurrent: 10
      actions:
        - carregar_gerentes_do_registry
        - verificar_supervisor_online
        - iniciar_agente
        - conectar_com_hermes
      health_check: heartbeat (30s)
      failure_action: RETRY (3x) + NOTIFY_DIRECTOR

    STEP_6_3_OPERATIONAL_AGENTS:
      description: Inicializa Agentes Operacionais
      parallel: true
      max_concurrent: 50
      actions:
        - carregar_agentes_do_registry
        - verificar_manager_online
        - iniciar_agente
        - conectar_com_hermes
        - iniciar_strands_workers
      health_check: heartbeat (60s)
      failure_action: RETRY (3x) + NOTIFY_MANAGER

    STEP_6_4_PENTESTER:
      description: Inicializa Agente Pentester
      actions:
        - verificar_autorizacao (Aísio)
        - carregar_cenarios_ataque
        - iniciar_em_modo_passivo (apenas monitoramento)
        - aguardar_trigger_para_modo_ativo
      health_check: /pentest/health → 200
      failure_action: WARN + CONTINUE (pentest suspenso)
--------------------------------------------------------------------------------
FASE 7: DOMÉSTICO (Isolado)
BOOTSTRAP_PHASE_7:
  name: "Núcleo Doméstico"
  duration_estimate: 10 segundos
  depends_on: PHASE_6
  blocking: false
  isolation: AIR_GAP (rede isolada)

  STEPS:
    STEP_7_1_SANDBOX_DOMESTICO:
      description: Cria sandbox isolado para doméstico
      actions:
        - criar_network_namespace_isolado
        - configurar_egress_block (ALL)
        - configurar_ingress_only_from_CEO
        - montar_filesystem_domestico
      health_check: network_isolation_verified
      failure_action: ABORT_DOMESTIC (núcleo doméstico não inicia)

    STEP_7_2_NICE_PRINCIPAL:
      description: Inicializa Nice (agente principal doméstico)
      actions:
        - carregar_contrato_nice
        - verificar_supervisor (NODE_LU_001 - humano, pode estar offline)
        - iniciar_agente
        - conectar_observabilidade_isolda
      health_check: nice_heartbeat → 30s
      failure_action: WARN + NOTIFY_LU (humano)

    STEP_7_3_AGENTES_DOMESTICOS:
      description: Inicializa subagentes domésticos (Nice subordinates)
      order:
        1: NICE_FIN_001 (finanças)
        2: NICE_CAL_001 (agenda)
        3: NICE_MKT_001 (compras)
        4: NICE_WELL_001 (bem-estar)
        5: NICE_LU_001 (apoio)
      actions:
        - carregar_agentes_domesticos
        - verificar_nice_online
        - iniciar_em_sandbox_isolado
      health_check: cada agente reporta (mas isolado)
      failure_action: CONTINUE (degradado doméstico)
--------------------------------------------------------------------------------
Bootstrap Completo - Checklist de Validação
BOOTSTRAP_VALIDATION:
  AFTER_PHASE_0:
    - ✅ environment_verified
    - ✅ configurations_loaded
    - ✅ certificates_valid
    - ⚠️ dependencies: BANK_API offline (warning)

  AFTER_PHASE_1:
    - ✅ storage_immutable_mounted
    - ✅ notebook_llm_loaded (hash_chain_valid)
    - ✅ audit_grpc_serving

  AFTER_PHASE_2:
    - ✅ zero_trust_active
    - ✅ aisio_monitoring
    - ✅ kill_switch_ready

  AFTER_PHASE_3:
    - ✅ hermes_routing_active
    - ✅ langgraph_workflows_loaded (124 workflows)
    - ✅ priority_queues_created

  AFTER_PHASE_4:
    - ✅ strands_workers_loaded (124 workers)
    - ⚠️ claude_code_runtime: DEGRADED (sandbox issue)
    - ✅ sandbox_manager_ready

  AFTER_PHASE_5:
    - ✅ crewai_teams_loaded (12 teams)
    - ✅ double_check_active

  AFTER_PHASE_6:
    - ✅ CEO_001_online
    - ✅ AISIO_001_online
    - ✅ directors_online (4/4)
    - ✅ managers_online (19/20 - 1 falhou)
    - ✅ agents_online (78/80 - 2 restartando)
    - ⚠️ pentester_passive_mode

  AFTER_PHASE_7:
    - ✅ domestic_sandbox_isolated
    - ✅ nice_online
    - ✅ domestic_agents_online (5/5)

  SYSTEM_READY:
    status: OPERATIONAL (DEGRADED)
    issues:
      - "BANK_API offline"
      - "Claude Code Runtime sandbox issue"
      - "1 manager offline"
      - "2 agents restarting"
    overall: "Sistema operacional com limitações"
    requires_attention: ["BANK_API"]
--------------------------------------------------------------------------------
Script de Bootstrap
#!/usr/bin/env python3
# bootstrap.py - Orquestrador de inicialização do sistema

import asyncio
import sys
from enum import Enum

class BootstrapPhase(Enum):
    PHASE_0 = "PRÉ-BOOTSTRAP"
    PHASE_1 = "INFRAESTRUTURA"
    PHASE_2 = "SEGURANÇA"
    PHASE_3 = "ORQUESTRAÇÃO"
    PHASE_4 = "EXECUÇÃO"
    PHASE_5 = "VALIDAÇÃO"
    PHASE_6 = "AGENTES"
    PHASE_7 = "DOMÉSTICO"

class BootstrapOrchestrator:
    def __init__(self):
        self.phases = {
            BootstrapPhase.PHASE_0: Phase0PreBootstrap(),
            BootstrapPhase.PHASE_1: Phase1Infrastructure(),
            BootstrapPhase.PHASE_2: Phase2Security(),
            BootstrapPhase.PHASE_3: Phase3Orchestration(),
            BootstrapPhase.PHASE_4: Phase4Execution(),
            BootstrapPhase.PHASE_5: Phase5Validation(),
            BootstrapPhase.PHASE_6: Phase6Agents(),
            BootstrapPhase.PHASE_7: Phase7Domestic()
        }
        self.results = {}

    async def bootstrap(self):
        """Executa bootstrap sequencial"""

        print("🚀 INICIANDO BOOTSTRAP DO BRACHÁT")
        start_time = time.time()

        for phase in BootstrapPhase:
            print(f"\n📌 FASE {phase.value}...")
            phase_start = time.time()

            try:
                result = await self.phases[phase].execute()
                self.results[phase] = result

                if result.status == "FAILED" and result.blocking:
                    print(f"❌ Fase {phase.value} falhou (blocking). Abortando.")
                    self.rollback_bootstrap()
                    return {"status": "ABORTED", "phase": phase}

                elif result.status == "FAILED" and not result.blocking:
                    print(f"⚠️ Fase {phase.value} falhou (não blocking). Continuando.")

                else:
                    print(f"✅ Fase {phase.value} concluída em {time.time() - phase_start:.2f}s")

            except Exception as e:
                print(f"❌ ERRO na fase {phase.value}: {e}")
                if self.phases[phase].blocking:
                    return {"status": "ABORTED", "phase": phase, "error": str(e)}

        total_time = time.time() - start_time
        print(f"\n🎉 BOOTSTRAP CONCLUÍDO em {total_time:.2f}s")

        return {
            "status": "COMPLETED",
            "total_duration_seconds": total_time,
            "phase_results": self.results
        }

    def rollback_bootstrap(self):
        """Rollback em caso de falha crítica"""
        print("🔄 Executando rollback do bootstrap...")
        # Implementar limpeza
        pass

if __name__ == "__main__":
    orchestrator = BootstrapOrchestrator()
    result = asyncio.run(orchestrator.bootstrap())

    if result["status"] != "COMPLETED":
        sys.exit(1)
--------------------------------------------------------------------------------
Logs de Bootstrap
{
  "bootstrap_log": {
    "boot_id": "BOOT_20260124_001",
    "start_time": "2026-01-24T10:00:00Z",
    "end_time": "2026-01-24T10:01:15Z",
    "total_duration_seconds": 75,

    "phases": {
      "phase_0": { "status": "SUCCESS", "duration_seconds": 5 },
      "phase_1": { "status": "SUCCESS", "duration_seconds": 10 },
      "phase_2": { "status": "SUCCESS", "duration_seconds": 5 },
      "phase_3": { "status": "SUCCESS", "duration_seconds": 10 },
      "phase_4": {
        "status": "DEGRADED",
        "duration_seconds": 15,
        "warnings": ["Claude Code sandbox issue"]
      },
      "phase_5": { "status": "SUCCESS", "duration_seconds": 5 },
      "phase_6": {
        "status": "DEGRADED",
        "duration_seconds": 20,
        "warnings": ["1 manager offline", "2 agents restarting"]
      },
      "phase_7": { "status": "SUCCESS", "duration_seconds": 5 }
    },

    "system_ready": true,
    "system_state": "OPERATIONAL_DEGRADED",
    "notifications_sent": ["Aísio", "CEO"]
  }
}
--------------------------------------------------------------------------------
Validação do Bootstrap
Para o sistema ser OPERACIONAL:
BOOTSTRAP_VALIDATION:
  - bootstrap_completo: true (todas fases executadas)
  - components_criticos_online: true (Aísio, Hermes, NotebookLLM)
  - estado_sistema_definido: true
  - logs_bootstrap_persistidos: true
  - health_checks_passando: true
  - tempo_bootstrap < 120s: true

---

### 📄 SYSTEM_CONSISTENCY_CHECK.md

```markdown
# SYSTEM_CONSISTENCY_CHECK.md — Validação Inicial do Runtime

## Princípio Fundamental

Antes de qualquer operação, o sistema BRACHÁT deve passar por uma **verificação de consistência** que valida registry, governança e memória. O sistema só é considerado consistente se todos os checks passarem.

---

## Tipos de Consistency Check

```yaml
CONSISTENCY_CHECKS:

  CHECK_1_REGISTRY_CONSISTENCY:
    description: Verifica integridade do agent registry
    frequency: A CADA BOOTSTRAP + A CADA 1 HORA
    blocking: true (se falha → sistema não opera)

  CHECK_2_GOVERNANCE_CONSISTENCY:
    description: Verifica políticas e regras de governança
    frequency: A CADA BOOTSTRAP + A CADA MUDANÇA
    blocking: true (se falha → read-only mode)

  CHECK_3_MEMORY_CONSISTENCY:
    description: Verifica NotebookLLM vs agentes
    frequency: A CADA BOOTSTRAP + A CADA 5 MINUTOS
    blocking: false (se falha → reconciliação)

  CHECK_4_DEPENDENCY_CONSISTENCY:
    description: Verifica dependências entre agentes
    frequency: A CADA BOOTSTRAP
    blocking: true (se ciclo detectado → abort)

  CHECK_5_SECURITY_CONSISTENCY:
    description: Verifica configurações de segurança
    frequency: A CADA BOOTSTRAP + A CADA 1 HORA
    blocking: true (se critical → kill switch)
--------------------------------------------------------------------------------
CHECK 1: Registry Consistency
REGISTRY_CONSISTENCY:
  CHECKS:
    CHECK_1_1_ALL_AGENTS_DEFINED:
      description: Todos agentes têm entrada no registry
      method:
        - carregar AGENT_REGISTRY.md
        - parsear agent_ids
        - verificar duplicatas
      failure: "Agente duplicado ou faltando"
      severity: CRITICAL

    CHECK_1_2_HIERARCHY_VALID:
      description: Hierarquia (supervisor) é válida
      checks:
        - supervisor existe no registry
        - não há ciclo (A supervisor B, B supervisor A)
        - CEO não tem supervisor
        - AGENT tem supervisor MANAGER+
      failure: "Hierarquia inválida"
      severity: HIGH

    CHECK_1_3_PERMISSIONS_VALID:
      description: Permissões são consistentes
      checks:
        - allowed_actions são strings válidas
        - forbidden_actions não intersecta allowed_actions
        - tools listadas existem no sistema
      failure: "Permissões inconsistentes"
      severity: HIGH

    CHECK_1_4_CONTRACTS_VALID:
      description: Contratos de execução são válidos
      checks:
        - contrato assinado por supervisor
        - contrato não expirado
        - thresholds realísticos
        - cross-domain rules respeitadas
      failure: "Contrato inválido"
      severity: CRITICAL

  AUTOMATIC_FIXES:
    - duplicatas: remover (prioridade mais recente)
    - small_cycles: quebrar (promover AGENT para MANAGER)
    - contratos_expirados: renovar automaticamente se auto-renewable
--------------------------------------------------------------------------------
CHECK 2: Governance Consistency
GOVERNANCE_CONSISTENCY:
  CHECKS:
    CHECK_2_1_POLICIES_LOADABLE:
      description: Políticas podem ser carregadas
      method: parsear GOVERNANCE.md + policies
      checks:
        - syntax válida
        - referências existem
        - sem conflitos (policy A diz X, policy B diz not X)
      failure: "Políticas inconsistentes"
      severity: CRITICAL

    CHECK_2_2_VETO_AUTHORITIES_VALID:
      description: Autoridades de veto existem
      checks:
        - DIR_AISIO_001 existe
        - DIR_JESSICA_001 existe
        - CEO_001 existe
        - NODE_LU_001 existe (para doméstico)
      failure: "Autoridade de veto não encontrada"
      severity: CRITICAL

    CHECK_2_3_KILL_SWITCH_CONFIGURED:
      description: Kill switch está configurado
      checks:
        - kill_switch_autoridades definidas
        - kill_switch_modos implementados
        - recovery_procedure documentada
        - override_CEO possível
      failure: "Kill switch não configurado"
      severity: CRITICAL

    CHECK_2_4_ZERO_TRUST_ACTIVE:
      description: Zero trust está ativo
      checks:
        - mTLS obrigatório
        - policy_engine online
        - rate_limiting ativo
        - isolation enforcement ativo
      failure: "Zero trust inativo"
      severity: CRITICAL
--------------------------------------------------------------------------------
CHECK 3: Memory Consistency
MEMORY_CONSISTENCY:
  CHECKS:
    CHECK_3_1_NOTEBOOK_HASH_CHAIN:
      description: Hash chain do NotebookLLM está íntegra
      method:
        - pegar último entry
        - verificar previous_hash do último = hash do anterior
        - verificar assinaturas
      failure: "Hash chain quebrada"
      severity: CRITICAL
      auto_fix: rollback para último snapshot íntegro

    CHECK_3_2_AGENT_VS_NOTEBOOK_STATE:
      description: Estado dos agentes vs NotebookLLM
      method:
        - para cada agente, comparar estado local com NotebookLLM
        - identificar divergências
      failure: "Estado inconsistente"
      severity: MEDIUM
      auto_fix: reconciliação (NotebookLLM ganha)

    CHECK_3_3_AUDIT_LOG_INTEGRITY:
      description: Integridade do audit log
      method: verificar hash chain do audit log
      failure: "Audit log corrompido"
      severity: HIGH
      auto_fix: preservar + notificar Aísio

    CHECK_3_4_SNAPSHOT_RECOVERABLE:
      description: Snapshots são recuperáveis
      method:
        - tentar carregar último snapshot
        - verificar integridade
        - simular restore
      failure: "Snapshot não recuperável"
      severity: HIGH
      auto_fix: criar novo snapshot
--------------------------------------------------------------------------------
CHECK 4: Dependency Consistency
DEPENDENCY_CONSISTENCY:
  CHECKS:
    CHECK_4_1_NO_CYCLES:
      description: Sem dependências circulares
      method: análise de grafo (DFS)
      failure: "Ciclo de dependência detectado"
      severity: CRITICAL
      auto_fix: quebrar ciclo (promover ou despriorizar)

    CHECK_4_2_ALL_DEPENDENCIES_RESOLVABLE:
      description: Dependências existem
      method: verificar cada dependência
      checks:
        - agente_dependencia existe
        - serviço_dependencia está disponível
        - versões compatíveis
      failure: "Dependência não resolvível"
      severity: HIGH
      auto_fix: notificar + fallback (se disponível)

    CHECK_4_3_CRITICAL_DEPENDENCIES_AVAILABLE:
      description: Dependências críticas estão disponíveis
      method: health check das dependências críticas
      failure: "Dependência crítica indisponível"
      severity: CRITICAL
      auto_fix: abortar bootstrap ou kill switch
--------------------------------------------------------------------------------
CHECK 5: Security Consistency
SECURITY_CONSISTENCY:
  CHECKS:
    CHECK_5_1_CERTIFICATES_VALID:
      description: Certificados mTLS estão válidos
      method:
        - verificar expiração (próximos 7 dias)
        - verificar revogação (CRL)
        - verificar chain of trust
      failure: "Certificado inválido"
      severity: HIGH
      auto_fix: renovação automática (se possível)

    CHECK_5_2_SANDBOX_CONFIGURATION:
      description: Sandbox está configurado corretamente
      checks:
        - isolation_levels definidos
        - network_policies ativas
        - filesystem_limits configurados
      failure: "Sandbox mal configurado"
      severity: HIGH
      auto_fix: recarregar configuração padrão

    CHECK_5_3_PENTESTER_AUTHORIZED:
      description: Pentester está autorizado a operar
      method: verificar assinatura do Aísio
      failure: "Pentester não autorizado"
      severity: MEDIUM
      auto_fix: desativar pentester (modo passivo)
--------------------------------------------------------------------------------
Implementação do Consistency Check
class ConsistencyChecker:
    def __init__(self):
        self.checks = [
            RegistryConsistencyCheck(),
            GovernanceConsistencyCheck(),
            MemoryConsistencyCheck(),
            DependencyConsistencyCheck(),
            SecurityConsistencyCheck()
        ]

    def run_all_checks(self, context_id):
        """Executa todos os checks de consistência"""

        results = []
        system_consistent = True

        for check in self.checks:
            print(f"🔍 Executando {check.name}...")
            result = check.execute(context_id)
            results.append(result)

            if not result.passed:
                if result.severity == "CRITICAL":
                    print(f"❌ {check.name} falhou (CRITICAL)")
                    system_consistent = False

                    if result.auto_fix:
                        print(f"🔧 Aplicando auto-fix: {result.auto_fix_action}")
                        fix_result = result.apply_fix()
                        if not fix_result.success:
                            activate_kill_switch("CONSISTENCY_CHECK_FAILED")
                            return {"consistent": False, "fatal": True}
                    else:
                        activate_kill_switch("CONSISTENCY_CHECK_FAILED")
                        return {"consistent": False, "fatal": True}

                else:
                    print(f"⚠️ {check.name} falhou ({result.severity}) - {result.message}")
                    system_consistent = False

        return {
            "consistent": system_consistent,
            "results": results,
            "timestamp": now()
        }

class RegistryConsistencyCheck:
    name = "Registry Consistency"

    def execute(self, context_id):
        # Implementação dos checks do registry
        issues = []

        # Check 1.1: All agents defined
        agents_in_code = self.scan_agents_in_code()
        agents_in_registry = self.load_agent_registry()

        missing = agents_in_code - agents_in_registry
        if missing:
            issues.append(f"Agentes faltando no registry: {missing}")

        duplicates = self.find_duplicates(agents_in_registry)
        if duplicates:
            issues.append(f"Agentes duplicados: {duplicates}")

        # Check 1.2: Hierarchy valid
        cycles = self.detect_hierarchy_cycles()
        if cycles:
            issues.append(f"Ciclos na hierarquia: {cycles}")

        # Check 1.4: Contracts valid
        expired = self.find_expired_contracts()
        if expired:
            issues.append(f"Contratos expirados: {expired}")

        return ConsistencyResult(
            passed=len(issues) == 0,
            severity="CRITICAL" if issues else "OK",
            message="; ".join(issues) if issues else "Registry consistente",
            auto_fix=True,
            auto_fix_action="renew_expired_contracts" if expired else None
        )
--------------------------------------------------------------------------------
Relatório de Consistency Check
{
  "consistency_report": {
    "report_id": "CC_20260124_001",
    "timestamp": "2026-01-24T10:00:00Z",
    "context_id": "CTX_BOOTSTRAP",

    "checks": {
      "registry": {
        "passed": true,
        "severity": "OK",
        "details": {
          "agents_total": 124,
          "agents_defined": 124,
          "hierarchy_cycles": 0,
          "contracts_expired": 0
        }
      },

      "governance": {
        "passed": true,
        "severity": "OK",
        "details": {
          "policies_loaded": 42,
          "veto_authorities": ["AISIO", "JESSICA", "CEO", "LU"],
          "kill_switch_configured": true,
          "zero_trust_active": true
        }
      },

      "memory": {
        "passed": false,
        "severity": "MEDIUM",
        "details": {
          "notebook_hash_chain": "VALID",
          "agents_inconsistent": [
            { "agent": "AGT_PAY_001", "local": "R$1000", "notebook": "R$950" },
            { "agent": "NICE_FIN_001", "local": "R$150", "notebook": "R$145" }
          ],
          "audit_integrity": "VALID",
          "snapshot_recoverable": true
        },
        "auto_fix_applied": true,
        "auto_fix_result": "RECONCILIED"
      },

      "dependency": {
        "passed": true,
        "severity": "OK",
        "details": {
          "cycles_detected": 0,
          "unresolved_dependencies": 0,
          "critical_dependencies_available": true
        }
      },

      "security": {
        "passed": true,
        "severity": "OK",
        "details": {
          "certificates_valid": true,
          "sandbox_configured": true,
          "pentester_authorized": true
        }
      }
    },

    "overall_consistent": true,
    "auto_fixes_applied": 1,
    "warnings": 2,
    "system_state_after_check": "OPERATIONAL"
  }
}
--------------------------------------------------------------------------------
Pós-Check: Ações
POST_CONSISTENCY_ACTIONS:
  IF_CONSISTENT:
    - iniciar operações normais
    - notificar Aísio: "System consistent"
    - gravar no NotebookLLM: consistency_check_passed

  IF_INCONSISTENT_BUT_FIXABLE:
    - aplicar auto_fixes
    - re-executar checks (até 3x)
    - se ainda inconsistente: escalate para Aísio

  IF_INCONSISTENT_AND_CRITICAL:
    - ativar kill switch
    - notificar CEO + Aísio
    - preservar logs
    - aguardar intervenção humana

  IF_CONSISTENCY_CHECK_FAILS_ON_BOOTSTRAP:
    - abortar bootstrap
    - sistema não inicia
    - log detalhado
--------------------------------------------------------------------------------
Logs de Consistency Check
{
  "consistency_log": {
    "check_id": "CC_20260124_001",
    "timestamp": "2026-01-24T10:00:00Z",
    "trigger": "BOOTSTRAP",
    "checks_executed": 5,
    "checks_passed": 4,
    "checks_failed": 1,
    "critical_failures": 0,
    "auto_fixes_applied": 1,
    "overall_consistent": true,
    "system_state": "OPERATIONAL",
    "duration_ms": 2500,
    "notified": ["Aísio"]
  }
}
--------------------------------------------------------------------------------
Validação da Consistência
Para o sistema ser OPERACIONAL:
CONSISTENCY_VALIDATION:
  - registry_consistente: true
  - governance_consistente: true
  - memory_consistente: true (ou reconciliação aplicada)
  - dependency_consistente: true
  - security_consistente: true
  - nenhum_critical_failure: true
  - auto_fixes_bem_sucedidos: true (se aplicado)
--------------------------------------------------------------------------------
Fim do Módulo
Status: 11_BOOTSTRAP COMPLETO
Arquivos Gerados:
✅ SYSTEM_BOOTSTRAP.md
✅ SYSTEM_CONSISTENCY_CHECK.md
--------------------------------------------------------------------------------
🎉 PASSO 11 CONCLUÍDO — DOCUMENTAÇÃO BRACHÁT 10/10 COMPLETA
Todos os 36 arquivos da estrutura v10/10 foram gerados com sucesso.
ESTRUTURA_COMPLETA:
  01_AGENT_REGISTRY: [AGENT_REGISTRY.md, AGENT_EXECUTION_CONTRACTS.md] ✅
  02_ORGANIZATION_MODEL: [ORGANOGRAM.md, DOMAIN_BOUNDARIES.md] ✅
  03_GOVERNANCE: [GOVERNANCE.md] ✅
  04_RUNTIME_ARCHITECTURE: [HERMES_SPEC.md, STRANDS_SPEC.md, LANGGRAPH_RULES.md, CREWAI_RULES.md, CLAUDE_CODE_RUNTIME.md, OBSERVABILITY.md] ✅
  05_COMMUNICATION: [EVENT_MODEL.md, MESSAGE_SCHEMA.md, FLOW_EXECUTION.md] ✅
  06_MEMORY_LAYER: [NOTEBOOKLLM_SPEC.md, MEMORY_POLICIES.md] ✅
  07_SECURITY: [ZERO_TRUST_MODEL.md, KILL_SWITCH.md, AUDIT_SYSTEM.md, PENTEST_MODEL.md] ✅
  08_EXECUTION_LAYER: [OPERATION_FLOW.md, STRANDS_WORKERS_MODEL.md, TERMINAL_EXECUTION.md, TASK_LIFECYCLE.md] ✅
  09_DEPENDENCY_GRAPH: [AGENT_DEPENDENCIES.md, SYSTEM_FLOW_GRAPH.md, FAILURE_CHAIN_MODEL.md] ✅
  10_PRODUCTION_CRITERIA: [KPI_SYSTEM_READY.md, TESTING_MODEL.md, VALIDATION_GATES.md, FAILURE_MODEL.md] ✅
  11_BOOTSTRAP: [SYSTEM_BOOTSTRAP.md, SYSTEM_CONSISTENCY_CHECK.md] ✅
  README.md: ✅ (raiz)
--------------------------