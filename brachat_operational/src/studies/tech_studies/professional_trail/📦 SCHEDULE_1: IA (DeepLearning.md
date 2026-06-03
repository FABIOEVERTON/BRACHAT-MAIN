📦 SCHEDULE_1: IA (DeepLearning.AI + Anthropic) — BLOCO ÚNICO COMPLETO

# 🧠 SCHEDULE_1: IA — SedeReg AI Core | 100% Coverage

**Provedores:** DeepLearning.AI, Anthropic/Skilljar, Elements of AI, Google AI Essentials, Coursera (Andrew Ng)  
**Objetivo:** Construir núcleo de IA da SedeReg — agentes, RAG, avaliação, guardrails, fine-tuning, MCP (Intro + Advanced), Claude Code  
**Início:** Dia 1 | **Execução:** Paralela | **LLM Access:** Uma por vez

## 🗂️ Arquitetura Alimentada

sede-reg/ai-core/
├── agents/ # LangChain, CrewAI, Subagents
├── rag/ # LlamaIndex + normas PDF
├── eval/ # Ragas, TruLens, métricas
├── guards/ # Guardrails: filter, validação
├── models/ # Fine-tuning Phi-3
├── mcp/ # MCP servers: filesystem, compliance, risco, advanced
├── skills/ # Claude Code custom skills
└── docs/
├── governance-flow.md
├── ai-fluency-foundations.md # ← NOVO: AI Fluency
└── advanced-mcp-arch.md # ← NOVO: Advanced MCP

## 📅 Cronograma — Todos os 40 Itens Incluídos

| Dia     | Data        | Tipo | Atividade                                                                              | Plataforma                                                            | Duração     | Entregável/PRINT                                        | Módulo SedeReg                                 | Certificação                   |
| ------- | ----------- | ---- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ----------- | ------------------------------------------------------- | ---------------------------------------------- | ------------------------------ |
| 1       | 16/05       | 📖   | AI Agents in LangChain                                                                 | deeplearning.ai                                                       | ~4h         | Certificado + PRINT                                     | —                                              | —                              |
| 2       | 17/05       | ✋   | Criar agente LangChain + Claude API; testar 3 prompts governança                       | VS Code + Claude API                                                  | ~2h         | Repo + PRINT código rodando                             | `ai-core/agents/clause-analyzer.py`            | —                              |
| 3       | 18/05       | 📖   | Multi AI Agent Systems with CrewAI                                                     | deeplearning.ai                                                       | ~4h         | Certificado + PRINT                                     | —                                              | —                              |
| 4       | 19/05       | ✋   | Orquestrar 2 agentes CrewAI: risco + controles                                         | VS Code + CrewAI                                                      | ~2h         | Repo + PRINT execução                                   | `ai-core/orchestrator/risk-controls.py`        | —                              |
| 5       | 20/05       | 📖   | Building Agentic RAG with LlamaIndex                                                   | deeplearning.ai                                                       | ~4h         | Certificado + PRINT                                     | —                                              | —                              |
| 6       | 21/05       | ✋   | RAG com LlamaIndex + base normas compliance (PDF); 5 consultas teste                   | VS Code + LlamaIndex                                                  | ~2h         | Repo + PRINT consulta respondida                        | `ai-core/rag/compliance-index/`                | —                              |
| 7       | 22/05       | 📖   | Building and Evaluating Advanced RAG                                                   | deeplearning.ai                                                       | ~4h         | Certificado + PRINT                                     | —                                              | —                              |
| 8       | 23/05       | ✋   | Aplicar métricas (faithfulness, relevance) no RAG do Dia 6                             | VS Code + Ragas/TruLens                                               | ~2h         | `eval-report.md` + PRINT métricas                       | `ai-core/eval/rag-metrics.py`                  | —                              |
| 9       | 24/05       | 📖   | LLMOps                                                                                 | deeplearning.ai                                                       | ~4h         | Certificado + PRINT                                     | —                                              | —                              |
| 10      | 25/05       | ✋   | Pipeline CI/CD básico para projeto RAG (GitHub Actions)                                | GitHub Actions + VS Code                                              | ~2h         | Workflow `.yml` + PRINT build passando                  | `ai-core/ci-cd/rag-test.yml`                   | —                              |
| 11      | 26/05       | 📖   | Evaluating and Debugging Generative AI                                                 | deeplearning.ai                                                       | ~3h         | Certificado + PRINT                                     | —                                              | —                              |
| 12      | 27/05       | ✋   | Suite de testes para prompts governança; corrigir 2 falhas de alucinação               | VS Code + Claude API                                                  | ~2h         | `test-prompts.md` + PRINT testes rodando                | `ai-core/tests/governance-prompts/`            | —                              |
| 13      | 28/05       | 📖   | Quality and Safety for LLM Applications                                                | deeplearning.ai                                                       | ~3h         | Certificado + PRINT                                     | —                                              | —                              |
| 14      | 29/05       | ✋   | Implementar guardrails básicos: filter tópicos, validação saída                        | VS Code + Guardrails library                                          | ~2h         | Código com guardrails + PRINT teste segurança           | `ai-core/guards/input-filter.py`               | —                              |
| 15      | 30/05       | 📖   | Finetuning Large Language Models                                                       | deeplearning.ai                                                       | ~4h         | Certificado + PRINT                                     | —                                              | —                              |
| 16      | 31/05       | ✋   | Fine-tunar Phi-3 com dataset cláusulas contrato; comparar desempenho                   | Google Colab + Hugging Face                                           | ~3h         | `finetune-contracts.ipynb` + PRINT métricas             | `ai-core/models/fine-tuned-phi3/`              | —                              |
| 16.1    | 01/06       | 📖   | **AI Fluency: Framework & Foundations** ← NOVO                                         | Anthropic Skilljar                                                    | ~2h         | PRINT módulo concluído                                  | `ai-core/docs/ai-fluency-foundations.md`       | —                              |
| 17      | 01/06       | 📖   | Revisão integrada: conectar 8 cursos em fluxo governança IA                            | deeplearning.ai + Anki                                                | ~2h         | `governance-flow.md` + PRINT Anki                       | `ai-core/docs/governance-flow.md`              | —                              |
| 18      | 02/06       | ✋   | Integrar componentes em projeto único: `ai-governance-pipeline`                        | GitHub + VS Code                                                      | ~3h         | Repo unificado + README + PRINT estrutura               | `ai-core/` v1.0                                | —                              |
| 19      | 03/06       | 📖   | Preparação candidaturas: mapear skills cursos para vagas Fase 1                        | LinkedIn + Anthropic Careers                                          | ~2h         | `skills-mapping.md` + PRINT vagas salvas                | —                                              | —                              |
| 20      | 04/06       | ✋   | Atualizar LinkedIn, GitHub, Upwork com certificados + projetos; 1 candidatura teste    | LinkedIn, GitHub, Upwork                                              | ~2h         | PRINTs: perfil atualizado + candidatura enviada         | —                                              | —                              |
| 21-29   | 05/06-13/06 | 📖✋ | Elements of AI (Capítulos 1-5) + Anki + Feynman                                        | elementsofai.com + Anki                                               | ~1h/dia     | 🏆 Certificado Elements of AI + PRINT LinkedIn          | `ai-core/docs/anki/`                           | Elements of AI                 |
| 30      | 14/06       | ✋   | Revisão Anki 30min + post LinkedIn: "8 certificados DeepLearning.AI + Elements of AI"  | Anki + LinkedIn                                                       | ~1h         | PRINT post publicado                                    | —                                              | —                              |
| 31-35   | 15/06-19/06 | 📖✋ | Google AI Essentials (Módulos 1-5) + prompts doc                                       | grow.google + Google Docs                                             | ~1-2h/dia   | 🏆 Certificado Google AI Essentials + PRINT             | `ai-core/prompts/governance-20.md`             | Google AI Essentials           |
| 36      | 20/06       | ✋   | Atualizar perfil Upwork com novos certificados + enviar 2 propostas serviço            | Upwork                                                                | ~1h         | PRINT propostas enviadas                                | —                                              | —                              |
| 37-40   | 21/06-24/06 | 📖✋ | AI for Everyone (Andrew Ng) — Semanas 1-2 + limitações mapeadas                        | Coursera + GitHub                                                     | ~1h/dia     | PRINT semanas concluídas + `ai-limitations.md` commit   | `ai-core/docs/ai-limitations.md`               | —                              |
| 66      | 20/07       | ✋   | Submeter projeto CS50x + emitir certificado + LinkedIn _(cross-schedule sync)_         | cs50.harvard.edu + LinkedIn                                           | ~2h         | 🏆 PRINT certificado CS50x + perfil atualizado          | —                                              | CS50x                          |
| 115-116 | 08/09-09/09 | 📖✋ | Anthropic: Claude with Amazon Bedrock + deploy teste                                   | Anthropic Skilljar + AWS Console                                      | ~2h/dia     | PRINT progresso + output modelo                         | `ai-core/deploy/bedrock-test/`                 | —                              |
| 117-118 | 10/09-11/09 | 📖✋ | Anthropic: Claude with Google Vertex AI + comparação Bedrock vs Vertex                 | Anthropic Skilljar + GCP + AWS                                        | ~2h/dia     | PRINT tabela comparativa GitHub                         | `ai-core/eval/cloud-comparison.md`             | —                              |
| 121-122 | 14/09-15/09 | 📖✋ | Anthropic: Claude Code 101 + instalar CLI + gerar script análise cláusulas             | Skilljar + Terminal + Claude Code                                     | ~2h/dia     | PRINT código gerado + execução                          | `ai-core/scripts/clause-analyzer-cli.py`       | —                              |
| 123-124 | 16/09-17/09 | 📖✋ | Anthropic: Claude Code in Action + automatizar GitHub Actions com Claude Code          | Skilljar + GitHub + VS Code                                           | ~2h/dia     | PRINT workflow `.yml` + build passing                   | `ai-core/ci-cd/auto-review.yml`                | —                              |
| 125-130 | 18/09-23/09 | 📖✋ | Anthropic: Intro to MCP (Módulos 1-3) + configurar 3 servidores MCP locais             | Skilljar + Localhost + Python + MCP SDK                               | ~1-2h/dia   | PRINT conexão ativa + servidores rodando                | `ai-core/mcp/` (filesystem, compliance, risco) | —                              |
| 130.1   | 24/09       | 📖   | **Model Context Protocol: Advanced Topics** ← NOVO (seu link)                          | https://anthropic.skilljar.com/model-context-protocol-advanced-topics | ~3h         | PRINT conclusão módulos avançados                       | `ai-core/mcp/advanced/` scaffold               | —                              |
| 130.2   | 25/09       | ✋   | **HANDS-ON Advanced MCP**: Implementar roteamento avançado + autenticação custom tools | Python + MCP SDK + Claude Code                                        | ~3h         | PRINT servidor MCP avançado rodando + logs orquestração | `ai-core/mcp/advanced/routing-server.py`       | —                              |
| 131-132 | 24/09-25/09 | 📖✋ | Anthropic: Intro to Agent Skills + criar Skill personalizada no Claude Code            | Skilljar + Claude Code + GitHub                                       | ~1.5-2h/dia | PRINT skill registrada + README                         | `ai-core/skills/governance-skill/`             | —                              |
| 133-134 | 26/09-27/09 | 📖✋ | Anthropic: Intro to Subagents + orquestrar subagentes com fila tarefas                 | Skilljar + Claude Code + Python                                       | ~1-2h/dia   | PRINT execução paralela + logs                          | `ai-core/orchestrator/subagent-queue.py`       | —                              |
| 137     | 30/09       | 📖   | Revisão integrada: MCP + Agentes + Claude Code + AI Fluency + Advanced MCP             | Docs + Anki                                                           | ~2h         | PRINT mapa mental `agent-architecture.md`               | `ai-core/docs/agent-architecture.md`           | —                              |
| 138     | 01/10       | ✋   | PROJETO 4: AI Compliance Monitor (Bedrock + MCP Advanced + Subagents)                  | GitHub + AWS/GCP                                                      | ~3h         | PRINT repo público + demo vídeo                         | `sede-reg/ai-core/` v1.0 público               | —                              |
| 148-154 | 11/10-17/10 | 📖✋ | CCA Prep + Simulados + EXAME CLAUDE CERTIFIED ARCHITECT                                | Anki + Claude + Anthropic Portal + Proctored Online                   | ~1.5-2h/dia | 🏆 PRINT certificado CCA + LinkedIn atualizado          | —                                              | **Claude Certified Architect** |
| 155-157 | 18/10-20/10 | ✋   | Atualizar Upwork ($150+/h) + candidaturas Fase 3 + post LinkedIn CCA aprovado          | Upwork + LinkedIn                                                     | ~1-2h/dia   | PRINT perfil + candidaturas + post publicado            | —                                              | —                              |

## 🔗 CANDIDATURAS (Datas Comuns — Cross-Schedule Sync)

| Data        | Dia     | Ação Comum a Todas as Schedules                                        | PRINT Esperado                          |
| ----------- | ------- | ---------------------------------------------------------------------- | --------------------------------------- |
| 03/06–04/06 | 19–20   | Mapear skills + atualizar LinkedIn/GitHub/Upwork + 1 candidatura teste | Perfil atualizado + candidatura enviada |
| 20/06       | 36      | Atualizar Upwork + enviar 2 propostas serviço                          | Propostas enviadas                      |
| 25/06       | 41      | Enviar 3 propostas Upwork com foco risco/IA                            | Propostas enviadas                      |
| 14/07       | 60      | Revisão Anki + enviar 3 propostas Upwork com projetos CS50x            | Propostas + deck atualizado             |
| 26/07       | 72      | Post LinkedIn: "CS50x + Probability Harvard concluídos"                | Post publicado                          |
| 01/08       | 78      | Atualizar Upwork + enviar 3 propostas risco/IA                         | Propostas enviadas                      |
| 07/09       | 114     | Candidaturas Fase 2 (vagas 12–15) + certificado GCP                    | 2 candidaturas enviadas                 |
| 18/10–20/10 | 155–157 | Upwork $150+/h + candidaturas Fase 3 + post LinkedIn CCA               | Perfil + candidaturas + post            |
| 10/11–16/11 | 178–184 | EXAME AIGP + candidaturas Fase 4 + premium applications                | Certificado + 5 candidaturas premium    |
| 02/12       | 200     | Envio 5 candidaturas remote (Dublin/SF/NY) + follow-up                 | Candidaturas + emails                   |

## ✅ CHECKLIST FINAL SCHEDULE_1 — 100%

- [x] Todos os 8 cursos DeepLearning.AI mapeados
- [x] Todos os 8 cursos Anthropic (incluindo AI Fluency + Advanced MCP) mapeados
- [x] Elements of AI, Google AI Essentials, AI for Everyone incluídos
- [x] Cada hands-on gera commit com tag `schedule-1-day-X`
- [x] Candidaturas sincronizadas por data com outras schedules
- [x] Certificações emitidas quando concluídas (Elements of AI, Google AI Essentials, CCA)
