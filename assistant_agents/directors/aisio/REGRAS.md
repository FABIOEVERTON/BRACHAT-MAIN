# REGRAS DO ECOSSISTEMA — ASSISTANT AGENTS BRACHÁT

## 0. PADRÃO HARNESS — OBRIGATÓRIO EM TODO AGENTE

### 🧠 Núcleo Central
* **Harness**: Módulo central (o "cinto de segurança") que interliga, controla e estabiliza o agente.
* **LLM**: Configuração de modelo e temperatura.

### ⚙️ Módulo de Habilidades (Skills)
* **Operational Procedure**: Procedimentos operacionais e fluxos de execução.
* **Decision Heuristics**: Heurísticas de decisão (atalhos lógicos para resolver problemas).

### 🧩 Módulo de Memória (Memory)
* **Working Context**: Contexto imediato da tarefa atual.
* **Episodic Experience**: Histórico de eventos, sucessos e falhas.
* **Semantic Knowledge**: Base de fatos e conceitos.
* **Personal Memory**: Perfil do usuário e características do agente.

### 🔗 Módulo de Protocolos (Protocols)
* **Agent-Agent**: Protocolos de comunicação entre agentes.
* **Agent-Tools**: Regras e integrações com ferramentas externas.

### ⚖️ Ferramentas de Regulação, Avaliação e Operação
* **Normative Constraints**: Limites éticos, de segurança e regras inquebráveis.
* **Sandbox**: Ambiente isolado para testes/ações sem afetar o real.
* **Evaluator**: Avaliador interno que analisa resultados antes de prosseguir.
* **Approval Loop**: Ciclo de aprovação (humano no fluxo para ações críticas).
* **Sub-Agent Orchestration**: Coordenação e delegação para sub-agentes.
* **Observability**: Monitoramento e rastreamento das ações.
* **Compression**: Compressão de dados/contexto para não estourar tokens.

---

## 1. Hierarquia de LLM

| Layer | Agentes | Reasoning | Modelo | T° |
|-------|---------|-----------|--------|----|
| Orquestrador | `orquestrador/` | Mínimo (só dispatch) | Rápido (sonnet/gpt-4o-mini) | 0 |
| Gerentes | `daily/*/` (torah, ingles, pmp, ml, filosofia, certificacoes) | Moderado (preparar/ensinar) | Médio | 0.2 |
| Produtores | `daily/job-hunter/`, `daily/freelancer/` | ZERO — determinístico | Qualquer | 0 |

**Regra de ouro**: agentes de produção NUNCA têm reasoning agents. Só executam passos fixos.

## 2. Estrutura de cada agente

```
daily/{nome}/
├── AGENT.md      ← Prompt do agente (max 60 linhas)
├── cache.json    ← Resultados recentes (max 5KB)
└── metadata.json ← Metadados (dependencias, versao, autor)
```

## 3. Contrato de execução (todos os agentes)

- Sempre carregar `state.json` antes de agir
- Nunca escrever fora do diretório permitido
- Log obrigatório de cada ação
- Threshold financeiro: R$500 max sem aprovação humana
- Cross-domain: PROIBIDO sem aprovação do orquestrador
- Arquivos <200 linhas (MVI)
- Approval gate para deletar/arquivar
- Estudos: NUNCA oferecer/avançar para o próximo dia enquanto o checkpoint do dia atual não estiver marcado como [ENTREGUE] no cache.json
- Inglês: todo vocábulo novo DEVE ser agendado para revisão em 24h, 3d, 7d, 30d e 90d (spaced repetition). O cache.json do inglês mantém o deck ativo com as próximas revisões.
- Estudos: todo conteúdo ensinado OU colado pelo usuário DEVE ser organizado dentro de `writings_studies/{categoria}/` na subpasta correta. Cada sessão de estudo gera ou atualiza um arquivo na pasta correspondente com: data, tópico, resumo do conteúdo, checkpoint. Tudo agendado para revisão conforme ciclo 24h/3d/7d/30d/90d. O cache.json de `estudos` mantém o índice de revisões pendentes.
- Método de ensino: SEMPRE simplificar para memorização. Entregar em: tópicos curtos (bullet points), macetes/mnemônicos, exemplos práticos do contexto do Fábio. NUNCA despejar texto teórico longo sem resumo first.

## 4. Economia de tokens

- Prompts <60 linhas
- Cache substitui repetição de busca
- Respostas <5 linhas padrão (aprofundar só se perguntado)
- Sem reescrever arquivos inteiros — edições cirúrgicas
- ContextScout antes de qualquer implementação
- skills-cache/index.json carregado uma vez por sessão

## 5. Memória

- Fonte única: `/Users/mac/.opencode/state.json`
- Cada agente pode salvar cache em `daily/{nome}/cache.json`
- Cache é persistente por dia (NUNCA resetar entre sessões do mesmo dia). Reset apenas em virada de data via orquestrador no startup protocol.

## 6. Mem0 — Backup Seletivo

Mem0 NÃO é usado para memória operacional diária. Isso é responsabilidade do cache.json e state.json.

Mem0 É usado para backup permanente de:
1. Decisões estratégicas do usuário (ex: mudança de carreira, novo projeto aprovado)
2. Aprendizados consolidados marcados com flag `mem0: true` no cache
3. Pareceres jurídicos de Jéssica aprovados pelo usuário
4. Marcos de progresso (ex: certificação concluída, proposta aceita)

Formato de envio ao Mem0:
{"type": "strategic_memory", "agent": "<nome>", "content": "<resumo>", "date": "<ISO>"}

Quem pode enviar ao Mem0: qualquer agente, desde que a entrada tenha flag `mem0: true`.
Quem audita o Mem0: Aísio, semanalmente.
