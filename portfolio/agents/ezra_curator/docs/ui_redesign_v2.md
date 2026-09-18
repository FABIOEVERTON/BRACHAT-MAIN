# UI Redesign v2 — chat-first (2026-08-12)

## Autorização
- Fabio confirmou execução em 2026-08-12.
- Constraint: somente dentro de `portfolio/ezra_curator/` (Google Drive). Nada fora das pastas pertinentes.
- Constraint: sem commit até autorização explícita.

## Escopo
Reconstrução da interface como página única de chat profissional, para
apresentação aos professores do Challenge Oracle ONE.

Decisões aprovadas:
1. Identidade neutra: **EZRA CURATOR** (sem persona "Maestro Santo Pegasus").
2. Página de chat para usuário perguntar à IA. **Sem métricas visíveis**
   (sem scores, latência, provider, fallback na UI).
3. Fontes citadas em accordion discreto com hover.
4. Upload de documentos discreto ("Documentos" na top bar).

## Backend (`app/rag.py`)
- `SYSTEM_PROMPT` reescrito: agente EZRA CURATOR, responde SOMENTE sobre
  documentos anexados; desvio de assunto -> mensagem de permissão;
  cita `[arquivo]`.
- `_detect_canned` -> `_detect_intent`:
  `greeting | whoami | list_docs | summarize_docs | None`.
- `DOCS_WORDS` e `SUMMARIZE_DOCS_WORDS` expandidos; saudações ampliadas.
- Novos helpers:
  - `_document_inventory()` — consulta real do ChromaDB, agrupa por fonte.
  - `_inventory_context()` / `_inventory_sources()`.
  - `_generate_answer()` — invocação LLM com fallback entre provedores.
  - `_answer_document_intent()` — listar/resumir documentos via LLM real.
- `answer_question()`:
  - Roteia intents; list/resumo usam LLM real (não resposta fixa).
  - Sem hits -> LLM responde o desvio com a mensagem de permissão
    (fallback local só se nenhum LLM disponível).
  - Contexto inclui inventário de documentos.
- `sources` agora carregam `excerpt` para o accordion.

## UI
- `app/ui/styles.py` — design system dark premium (chrome do Streamlit
  oculto, fonte Inter, hero, chips, bolhas, accordion com hover, digitação,
  feedback, input, footer, scrollbar).
- `app/ui/header.py` — top bar: marca + chip `● Ativo/Degradado` + upload.
- `app/ui/upload.py` — popover "Documentos" (salva em `data/`,
  `ingest(update_only=True)`), aceita PDF/CSV.
- `app/ui/chat.py` — hero + 4 sugestões (inclui "Quais documentos você tem?"
  e "Resuma os documentos"), histórico, bolhas, fontes em accordion,
  feedback 👍/👎 gravado em log, indicador de digitação, `st.chat_input`.
- `app/app.py` — rewire chat-first (header + chat + footer). Dashboard e
  activity fora da renderização (arquivos mantidos vazios).
- `.streamlit/config.toml` — cores alinhadas ao tema.

## Validação
- `ast.parse` OK em todos os arquivos alterados.
- `ruff check --isolated --select F,E9` — "All checks passed!".
- Intents validadas via stub (list_docs, summarize_docs, greeting, whoami).
- Smoke-test de import da cadeia completa (header -> upload -> chat -> app.main) OK.
- Execução visual real: pendente (rodar `streamlit run app/app.py` na VM/Docker —
  máquina local não possui as dependências).

## Governança
Regra registrada: **"Nunca salvar nada fora das pastas pertinentes"**.
Este registro foi criado dentro do projeto (Google Drive) conforme instrução
de Fabio ("faça somente no google drive"), sem tocar em arquivos do Mac
(`~/.opencode/...`) e sem commit.
