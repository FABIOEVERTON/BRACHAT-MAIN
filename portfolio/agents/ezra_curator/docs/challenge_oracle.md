# SPEC — Challenge Oracle ONE (FASE TECH): Agente RAG "Santo Pegasus"

**Trilha:** ONE AI FOR TECH | **Curso:** Challenge Alura Agente (RAG ONE BR)
**Empresa fictícia escolhida:** Santos Pegasus Soluciones (docs oficiais do desafio)
**Agente:** Maestro "Santo Pegasus" — base de conhecimento conversacional para colaboradores
**Gerente de execução:** Ezra (ADLC: build → test → eval → deploy → register → monitor)

---

## 0. DECISÕES DE ARQUITETURA (refinamento do planejamento PEGASUS)

O planejamento original foi reduzido de catálogo para **stack mínima viável**, atendendo 100% das instruções do challenge e usando ao menos 1 serviço OCI (usaremos 3).

### 0.1 Stack decidida (sem menu)

| Camada | Decisão | Justificativa |
|---|---|---|
| Linguagem | Python 3.11+ | Requisito do curso |
| Framework RAG | LangChain + LangGraph | Sugestão oficial; LangGraph p/ fluxo com estado e persistência |
| Leitura de docs | pypdf, python-docx, openpyxl, python-pptx, markdown, pandas (CSV), BeautifulSoup (HTML) | Multi-formato exigido (PDF, Word, Excel, PPT, MD, CSV, JSON, HTML) |
| Embeddings | Google `text-embedding-004` (primário) + BGE-M3 local (fallback) | Grátis/barato; fallback garante execução offline no deploy |
| Vector store | ChromaDB (persistido em disco) | Leve, roda no A1.Flex, suporta filtro por metadados |
| Reranker | cross-encoder local (BGE-reranker-base) | Melhora precisão sem custo de API |
| LLM | Gemini 2.5 Flash (primário) + fallback Groq/Claude via OmniRoute | Latência/custo baixos; fallback automático |
| Interface | Streamlit (chat) | Sugestão oficial; simples e funcional |
| Logging | JSON Lines local (perguntas, chunks, respostas, latência) | Requisito "Registrar execução" |
| Deploy | OCI Compute (A1.Flex free tier) + Docker + OCI Object Storage + OCI Vault | 3 serviços OCI → supera o mínimo exigido |
| CI/CD | Dockerfile + script de deploy + (opcional) GitHub Actions | Build e publicidade reproduzíveis |
| Repo | GitHub público, commits incrementais | Entregável obrigatório |

### 0.2 Escopo do MVP (o que NÃO entra agora)
- Nada de Bare Metal, OKE, Pinecone, Milvus, Oracle 23ai, n8n, Zapier, fine-tuning (T-Few), LAMP, 7.io, Telegram/Slack bots.
- Multi-agente (CrewAI) só se sobrar tempo após o MVP (fase de extras).

### 0.3 Critérios de aceite (checklist da avaliação)
- [ ] App funciona e responde perguntas com base nos documentos
- [ ] Código organizado, histórico de commits no GitHub público
- [ ] README: descrição, arquitetura (diagrama), tecnologias, instruções, exemplos de Q&A, link/print da app na nuvem
- [ ] Deploy na OCI provado (link público funcionando)
- [ ] Ao menos 1 serviço OCI usado (faremos 3)
- [ ] Registro de execução em nuvem (print/vídeo)

---

## FASE 1 — Preparação e repositório GitHub

1.1 Criar pasta do projeto local: `~/santo-pegasus/` com subpastas:
```
santo-pegasus/
├── app/
│   ├── app.py                  # Streamlit (chat)
│   ├── rag.py                  # pipeline RAG (indexar + buscar + gerar)
│   ├── loaders.py              # loaders multi-formato
│   ├── ingest.py               # script de ingestão/indexação
│   ├── config.py               # envs e constantes
│   └── logging.py              # logs JSONL
├── data/                       # documentos-fonte (não versionado)
├── docs/
├── scripts/
│   ├── download_docs.sh        # baixa os 5 PDFs Santos Pegasus
│   └── deploy_oci.sh           # build + deploy na OCI
├── tests/                      # eval set (perguntas/respostas esperadas)
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

1.2 Inicializar git (`git init`), criar `.gitignore` (data/, .env, *.jsonl, chroma/).
1.3 Criar repositório **público** no GitHub: `santo-pegasus` (via CLI `gh` ou navegador).
1.4 Primeiro commit: README.md inicial + estrutura + `.gitignore`. Política: **commits atômicos** por tarefa (mensagens descritivas em PT).
1.5 Ativar GitHub Actions (opcional) p/ lint/build.

## FASE 2 — Coleta e organização dos documentos

2.1 Baixar os 5 PDFs oficiais da Santos Pegasus Soluciones (CDN do curso) via `scripts/download_docs.sh`:
   - Guia Oficial de Engenharia Back-end (PT-BR)
   - Manual de Onboarding para Desenvolvedores (PT-BR)
   - Arquitetura de Microsserviços e Mapa de Domínios (PT-BR)
   - Guia Oficial de Engenharia Front-end (PT-BR)
   - Manual Maestro de Resiliência e Resposta a Incidentes v7.0 (PT-BR)
2.2 Categorizar por metadados: `categoria` (Back-end, Onboarding, Arquitetura, Front-end, Resiliência), `arquivo`, `data`, `autor`.
2.3 (Extra multi-formato) Gerar 1 CSV a partir de dados reais (ex.: métricas de incidentes do Manual de Resiliência) para provar suporte a CSV.
2.4 Armazenar os PDFs originais também no **OCI Object Storage** (bucket privado) durante a fase de deploy (Fase 9) — reuso via URL assinada (opcional).

## FASE 3 — Processamento e extração de conteúdo

3.1 `loaders.py`: implementar loader por extensão:
   - `.pdf` → pypdf (texto nativo) / PDF 2 imagem → OCR via Tesseract (só se necessário)
   - `.docx` → python-docx (preservar títulos/parágrafos)
   - `.xlsx` → openpyxl (linha a linha com cabeçalhos)
   - `.pptx` → python-pptx (slides + notas)
   - `.md` → markdown (remover sintaxe)
   - `.csv` → pandas (frases/tabelas)
   - `.json` → json (chave:valor → texto)
   - `.html` → BeautifulSoup (texto limpo)
3.2 Limpeza: remover cabeçalhos/rodapés repetidos, numeração de página, espaços duplicados, trechos corrompidos.
3.3 Chunking com `RecursiveCharacterTextSplitter` (chunk ~800 tokens, overlap 15%); preservar seção quando o formato permitir.
3.4 Atribuir metadados a cada chunk: categoria, arquivo, data, autor, localização (página/seção/slide).
3.5 Testar: `python -m app.ingest --dry-run` imprime amostra de chunks por documento.

## FASE 4 — Indexação vetorial

4.1 Embeddings: `text-embedding-004` (Google) com cache em disco; fallback automático p/ BGE-M3 local (sentence-transformers) se API indisponível.
4.2 Criar coleção ChromaDB persistida (`chroma/`) com metadados + IDs determinísticos (hash arquivo+chunk).
4.3 Indexação paralela dos metadados (filtros por categoria/data).
4.4 Script `ingest.py`: idempotente (reingestão sobrescreve chunks do mesmo documento; não duplica).
4.5 Sanidade: rodar 5 buscas de exemplo e conferir que os chunks retornados são relevantes.

## FASE 5 — Camada de recuperação (RAG)

5.1 `rag.py`: transformar pergunta → embedding (mesmo modelo da indexação).
5.2 Busca semântica ChromaDB: top-k=20 candidatos com filtro opcional por categoria.
5.3 Rerank local (cross-encoder) → reter top-3..5.
5.4 Montar contexto com metadados de origem (arquivo, seção, página, data).
5.5 Limiar de confiança: se nenhum chunk passar do score mínimo → **não gerar resposta** (Fallback, passo 6.4).

## FASE 6 — Geração e validação de respostas

6.1 Prompt de geração: responder **somente** com base no contexto; citar a fonte (arquivo, seção, página); admitir quando não souber; nunca inventar.
6.2 Modelo: Gemini 2.5 Flash (API key via env `GOOGLE_API_KEY`); fallback via OmniRoute (Groq/Claude).
6.3 Validação anti-alucinação: verificação de consistência resposta↔contexto (checar se as fontes citadas existem no contexto recuperado); se inconsistente → regenerar (máx. 1x) ou negar.
6.4 Fallback explícito: mensagem "Não encontrei essa informação nos documentos disponíveis" + sugestão de contato com a área responsável (back-end, onboarding etc.).
6.5 Formatação: resposta = resumo direto + lista de referências (nome do arquivo, seção, página).

## FASE 7 — Interface Streamlit (app.py)

7.1 Chat web: campo de pergunta, histórico de conversa na sessão (`st.session_state`), indicação clara de que é um agente de IA.
7.2 Cada resposta exibe as **fontes citadas** (expansíveis).
7.3 Botão de **feedback positivo/negativo** em cada resposta (grava em log JSONL).
7.4 Sidebar: nome do agente (Maestro Santo Pegasus), lista de documentos indexados, status (Qnt. de chunks).
7.5 Fallback visual quando o agente não encontra resposta (mensagem padrão + contatos).
7.6 Rodar local: `streamlit run app/app.py` — validar fluxo completo manualmente.

## FASE 8 — Testes locais e eval set

8.1 Criar `tests/qa.jsonl`: 15–20 perguntas (RH/onboarding, back-end, front-end, arquitetura, resiliência) com resposta esperada e documento-fonte.
8.2 Avaliar com LLM-as-judge (QA-Eval): medir correção, citação correta, ausência de alucinação.
8.3 Registrar métricas: taxa de acerto, taxa de "não encontrado", latência média.
8.4 Iterar no prompt/chunking até ≥90% de acerto no eval set.
8.5 Conferir que as respostas citam corretamente o arquivo/seção/página (critério da avaliação).

## FASE 9 — Deploy na OCI

9.1 Criar VCN com subnet pública (Security List: 22/SSH via Bastion opcional, 80/HTTP, 443/HTTPS, 8501 ou expor via porta 80 com proxy).
9.2 Criar instância **A1.Flex** (ARM, free tier) com imagem Ubuntu/Docker-ready + IP público.
9.3 Instalar Docker/Docker Compose na instância (user-data ou SSH).
9.4 **Dockerfile**: imagem slim Python 3.11; copiar `app/`, `requirements.txt`; porta 8501.
9.5 **docker-compose.yml**: serviço `app` (build) + volume para `chroma/` (persistência) e `logs/`.
9.6 Secrets: chaves de API no **OCI Vault** (segredo) — injetar via variável no container; **nunca** no git ou imagem.
9.7 Documentos: enviar os PDFs para bucket **OCI Object Storage** e sincronizar na ingestão (mount/`oci os object get`).
9.8 CI/CD: (a) GitHub Actions builda imagem e faz push para **OCIR** (OCI Container Registry) OU (b) script `deploy_oci.sh` (scp + `docker compose up -d`). Escolher (b) p/ simplicidade e (a) como extra.
9.9 Validar: `curl` na URL pública responde 200; app acessível pelo IP público (http://<ip>:8501 ou :80).
9.10 Capturar **evidência**: print de tela da app respondendo + vídeo curto (gravador de tela) — guardar em `docs/`.

## FASE 10 — Registro de execução e manutenção

10.1 `logging.py`: gravar JSONL por pergunta → pergunta, contexto recuperado (IDs), resposta, fontes, timestamp, latência, feedback.
10.2 Dashboard simples (opcional): `scripts/dashboard.py` lê os logs e mostra: perguntas sem resposta, feedback negativo, latência média.
10.3 Pipeline de atualização: script `ingest.py --update` reprocessa só documentos alterados (por hash); documentar rotina manual/cron.
10.4 Registrar todas as execuções em nuvem (prints/vídeos) na pasta `docs/` e no README.

## FASE 11 — README completo

11.1 Conteúdo obrigatório do `README.md`:
   - Título + descrição geral + badges (Shields.io: Python, license, status)
   - Índice navegável
   - **Arquitetura da solução** (diagrama Mermaid: usuário → Streamlit → RAG → ChromaDB → LLM → fontes)
   - Tecnologias e ferramentas utilizadas (tabela)
   - Instruções de execução (local + deploy OCI passo a passo)
   - **Exemplos de perguntas e respostas reais** (com fontes citadas)
   - **Link público + captura de tela/vídeo da app na nuvem** (evidência do deploy)
   - Status do projeto, autor (Fabio), licença, contato
11.2 Atualizar README conforme cada fase avança (commits).

## FASE 12 — Entrega final

12.1 `git push` final; revisar histórico de commits (mensagens claras, sem segredos).
12.2 Verificar que `.env`/chaves NÃO estão no repo; rodar `git grep` por chaves.
12.3 Enviar **URL do GitHub** no formulário do challenge (aceita apenas URLs do GitHub; 5 tentativas).
12.4 Baixar a **badge** após o envio.
12.5 Compartilhar no **LinkedIn** com #Alura e #oraclenexteducation.
12.6 (Opcional) Registrar no NotebookLM os resultados de execução e lições.

---

## ORDEM DE EXECUÇÃO RESUMIDA (prioridade)
1. Fase 1 (repo) → 2. Fase 2 (docs) → 3. Fases 3–6 (core RAG local) → 4. Fase 7 (UI local) → 5. Fase 8 (evals) → 6. Fase 9 (deploy OCI) → 7. Fase 10–11 (logs + README) → 8. Fase 12 (entrega).

## RISCOS E MITIGAÇÕES
- API Google sem quota → fallback BGE-M3 local (offline) + Groq/Claude via OmniRoute.
- A1.Flex (24 GB/4 OCPU) limitado → embedding local BGE-M3 pequeno; ChromaDB em disco; sem OKE.
- Deploy bloqueado por cota free tier → validar local primeiro; usar AMD Micro como fallback.
- Alucinação → prompt restrito + verificação de consistência + limiar de confiança + fallback explícito.
- Prazo (5 tentativas de envio) → priorizar MVP funcionando antes de extras.
