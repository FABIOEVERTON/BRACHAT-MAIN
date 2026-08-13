"""Camada RAG: busca semântica + rerank + montagem de contexto + geração."""

import os
import sys
import unicodedata
from dataclasses import dataclass, field

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)

from app import config  # noqa: E402
from app.ingest import get_collection  # noqa: E402
from app.logging import QueryLogger, now_ms  # noqa: E402


# ============================================================
# INVENTÁRIO DE DOCUMENTOS
# ============================================================

_MAX_INVENTORY_DOCS = 12
_INVENTORY_CHARS_PER_DOC = 600


# ============================================================
# PROMPTS E RESPOSTAS PADRÃO
# ============================================================

SYSTEM_PROMPT = (
    "Você é o EZRA CURATOR, um agente de IA que responde perguntas "
    "com base SOMENTE nos documentos anexados ao sistema. "
    "Regras: "
    "1) responda apenas com base nos documentos fornecidos no contexto; "
    "2) se a pergunta não tiver relação com esses documentos, responda "
    "educadamente que você só tem permissão para falar sobre os documentos "
    "disponíveis; "
    "3) cite a fonte de cada informação no formato [arquivo]; "
    "4) nunca invente dados."
)

FALLBACK_ANSWER = (
    "Não encontrei essa informação nos documentos disponíveis. "
    "Posso ajudar com perguntas sobre os documentos indexados. "
    "Lembrando que só tenho permissão para falar sobre os documentos."
)

GREETING_ANSWER = (
    "Olá! Tudo bem? Sou o EZRA CURATOR, um agente de IA que responde "
    "perguntas com base nos documentos anexados. "
    "Posso listar os documentos, resumi-los ou responder perguntas "
    "sobre o conteúdo deles. Como posso ajudar?"
)

WHOAMI_ANSWER = (
    "Sou o EZRA CURATOR, um agente de IA que responde perguntas "
    "com base nos documentos anexados ao sistema. "
    "Só tenho permissão para falar sobre esses documentos."
)


# ============================================================
# COMANDOS CONVERSACIONAIS
# ============================================================

GREETING_WORDS = {
    "oi",
    "ola",
    "olá",
    "oii",
    "oie",
    "oi tudo bem",
    "oii tudo bem",
    "eai",
    "e ai",
    "opa",
    "hey",
    "hi",
    "hello",
    "bom dia",
    "boa tarde",
    "boa noite",
    "tudo bem",
    "tudo bom",
    "bom te ver",
    "salve",
}

WHOAMI_WORDS = {
    "quem e voce",
    "quem é você",
    "o que voce faz",
    "o que você faz",
    "quem voce e",
    "você é o que",
    "voce e um robo",
    "que agente é esse",
}

DOCS_WORDS = {
    "quais documentos",
    "que documentos",
    "quais documentos voce tem",
    "quais documentos você tem",
    "quais documentos voce possui",
    "quais documentos você possui",
    "quais arquivos",
    "quais arquivos voce tem",
    "quais arquivos você tem",
    "documentos disponiveis",
    "documentos disponíveis",
    "documentos internos",
    "quais documentos voce pode",
    "quais documentos você pode",
    "o que voce tem",
    "o que você tem",
    "o que esta anexado",
    "o que está anexado",
    "o que tem anexado",
    "quais anexos",
    "me liste os documentos",
    "lista de documentos",
}

SUMMARIZE_DOCS_WORDS = {
    "resuma os documentos",
    "resuma todos os documentos",
    "resumo geral",
    "resumo dos documentos",
    "resuma tudo",
    "resumo de tudo",
    "o que dizem os documentos",
    "o que diz os documentos",
    "sobre o que são os documentos",
    "fale sobre todos os documentos",
    "fale sobre os documentos",
    "faz um resumo",
    "faça um resumo",
    "faca um resumo",
    "me de um resumo",
    "me dê um resumo",
    "sumarize",
    "resumo",
}


# ============================================================
# NORMALIZAÇÃO
# ============================================================

def _normalize(text: str) -> str:
    """Normaliza texto para comparação de comandos simples."""

    text = unicodedata.normalize("NFD", text)

    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    text = text.lower()

    for char in "?!.,;:":
        text = text.replace(char, "")

    return " ".join(text.split())


def _detect_intent(question: str) -> str | None:
    """Detecta a intenção da pergunta.

    Retorno:
        "greeting" | "whoami" | "list_docs" | "summarize_docs" | None
    """

    q = _normalize(question)

    if not q:
        return None

    normalized_whoami = {
        _normalize(word)
        for word in WHOAMI_WORDS
    }

    normalized_docs = {
        _normalize(word)
        for word in DOCS_WORDS
    }

    normalized_summarize = {
        _normalize(word)
        for word in SUMMARIZE_DOCS_WORDS
    }

    normalized_greetings = {
        _normalize(word)
        for word in GREETING_WORDS
    }

    if q in normalized_whoami:
        return "whoami"

    if any(
        word in q
        for word in normalized_whoami
        if len(word) > 8
    ):
        return "whoami"

    if q in normalized_summarize or any(
        word in q
        for word in normalized_summarize
        if len(word) >= 7
    ):
        return "summarize_docs"

    if q in normalized_docs or any(
        word in q
        for word in normalized_docs
        if len(word) >= 7
    ):
        return "list_docs"

    if q in normalized_greetings:
        return "greeting"

    if any(
        q.startswith(word)
        for word in normalized_greetings
        if len(word) >= 3
    ):
        return "greeting"

    return None


# ============================================================
# RESULTADO RAG
# ============================================================

@dataclass
class RagResult:
    """Resultado padronizado de uma consulta RAG."""

    answer: str
    sources: list[dict] = field(default_factory=list)
    found: bool = False
    provider: str = ""
    model: str = ""
    fallback: str = ""


# ============================================================
# STATUS DO SISTEMA
# ============================================================

def system_status() -> dict:
    """Retorna o estado atual dos componentes RAG."""

    from app.ingest import embedding_status

    emb = embedding_status()
    chain = _make_llm_chain()

    active = chain[0] if chain else None

    return {
        "llm_provider": (
            active[0]
            if active
            else "indisponível"
        ),
        "llm_model": (
            active[1]
            if active
            else "-"
        ),
        "llm_chain": [
            (provider, model)
            for provider, model, _ in chain
        ],
        "emb_provider": emb.get("provider", "unknown"),
        "emb_model": emb.get("model", "unknown"),
        "emb_error": emb.get("error", ""),
        "reranker": "BAAI/bge-reranker-base (local)",
        "fallback_chain": [
            "LLM: Cohere → Mistral → Anthropic → resposta extrativa local",
            "Embeddings: Google/Cohere → MiniLM local",
            "Reranker: BAAI local → ordenação por similaridade",
            "Fora do escopo: conversa guiada para os documentos",
        ],
    }


# ============================================================
# CONTROLE DE FALHAS DOS LLMS
# ============================================================

_llm_failed: set[str] = set()


# ============================================================
# FÁBRICAS DE LLM
# ============================================================

def _llm_factories() -> list[tuple[str, str, object]]:
    """
    Retorna os provedores LLM disponíveis em ordem de prioridade.

    Retorno:
        [(provider, model, factory), ...]
    """

    factories = []

    # --------------------------------------------------------
    # Cohere
    # --------------------------------------------------------

    if config.COHERE_API_KEY:
        from langchain_cohere import ChatCohere

        if config.LLM_PROVIDER.lower() == "cohere":
            model = config.LLM_MODEL
        else:
            model = "command-r7b-12-2024"

        factories.append(
            (
                "cohere",
                model,
                lambda m=model: ChatCohere(
                    model=m,
                    cohere_api_key=config.COHERE_API_KEY,
                    temperature=0.1,
                ),
            )
        )

    # --------------------------------------------------------
    # Mistral
    # --------------------------------------------------------

    if config.MISTRAL_API_KEY:
        from langchain_mistralai import ChatMistralAI

        if config.LLM_PROVIDER.lower() == "mistral":
            model = config.LLM_MODEL
        else:
            model = "mistral-small-latest"

        factories.append(
            (
                "mistral",
                model,
                lambda m=model: ChatMistralAI(
                    model=m,
                    mistral_api_key=config.MISTRAL_API_KEY,
                    temperature=0.1,
                ),
            )
        )

    # --------------------------------------------------------
    # Anthropic
    # --------------------------------------------------------

    if config.ANTHROPIC_API_KEY:
        from langchain_anthropic import ChatAnthropic

        if config.LLM_PROVIDER.lower() == "anthropic":
            model = config.LLM_MODEL
        else:
            model = "claude-sonnet-4-20250514"

        factories.append(
            (
                "anthropic",
                model,
                lambda m=model: ChatAnthropic(
                    model=m,
                    api_key=config.ANTHROPIC_API_KEY,
                    temperature=0.1,
                ),
            )
        )

    return factories


def _make_llm_chain() -> list[tuple[str, str, object]]:
    """Inicializa os LLMs disponíveis e remove os que falharam."""

    chain = []

    for provider, model, factory in _llm_factories():

        if provider in _llm_failed:
            continue

        try:
            llm = factory()

            chain.append(
                (
                    provider,
                    model,
                    llm,
                )
            )

        except Exception:
            _llm_failed.add(provider)

    return chain


def _make_llm():
    """Retorna o primeiro LLM disponível."""

    chain = _make_llm_chain()

    if not chain:
        return None

    return chain[0][2]


# ============================================================
# RERANK
# ============================================================

def _rerank(
    query: str,
    chunks: list[tuple[float, dict]],
    top_k: int,
) -> list[tuple[float, dict]]:
    """
    Reordena os chunks usando CrossEncoder local.

    Se o reranker não estiver disponível, mantém a ordenação
    original baseada na similaridade.
    """

    if not chunks:
        return []

    try:
        from sentence_transformers import CrossEncoder

        model = CrossEncoder(
            "BAAI/bge-reranker-base"
        )

        pairs = [
            (
                query,
                chunk_data["text"],
            )
            for _, chunk_data in chunks
        ]

        scores = model.predict(pairs)

        scored = sorted(
            zip(scores, chunks),
            key=lambda item: float(item[0]),
            reverse=True,
        )

        return [
            (
                float(score),
                chunk_data,
            )
            for score, (_, chunk_data) in scored[:top_k]
        ]

    except Exception:
        return chunks[:top_k]


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(
    question: str,
    top_k: int | None = None,
    rerank_top: int | None = None,
) -> list[tuple[float, dict]]:
    """Executa busca semântica + filtro de confiança + rerank."""

    top_k = top_k or config.TOP_K
    rerank_top = rerank_top or config.RERANK_TOP_K

    collection = get_collection()

    # Busca mais candidatos para permitir reranking.
    search_k = max(top_k * 4, rerank_top)

    try:
        results_raw = collection.similarity_search_with_score(
            question,
            k=search_k,
        )
    except Exception:
        return []

    results = []

    for doc, distance in results_raw:

        # Chroma normalmente retorna distância.
        # Para distância cosine, 1 - distância funciona
        # como uma aproximação de similaridade.
        similarity = 1.0 - float(distance)

        if similarity < config.CONFIDENCE_THRESHOLD:
            continue

        metadata = dict(doc.metadata or {})

        results.append(
            (
                similarity,
                {
                    "text": doc.page_content,
                    **metadata,
                },
            )
        )

    if not results:
        return []

    return _rerank(
        question,
        results,
        rerank_top,
    )


# ============================================================
# RESPOSTA PRINCIPAL
# ============================================================

def _document_inventory() -> list[dict]:
    """Retorna a lista real de documentos anexados no ChromaDB."""

    try:
        collection = get_collection()
        data = collection.get(
            include=["metadatas", "documents"],
        )
    except Exception:  # noqa: BLE001
        return []

    metadatas = data.get("metadatas") or []
    documents = data.get("documents") or []

    by_source: dict[str, dict] = {}

    for meta, text in zip(metadatas, documents):
        meta = meta or {}
        source = str(meta.get("source") or "?")

        entry = by_source.setdefault(
            source,
            {
                "source": source,
                "category": str(meta.get("category") or "Geral"),
                "chunks": 0,
                "summary": "",
            },
        )

        entry["chunks"] += 1

        if meta.get("tipo") == "resumo":
            entry["summary"] = str(text or "").strip()
        elif not entry["summary"]:
            entry["summary"] = str(text or "").strip()

    inventory = sorted(
        by_source.values(),
        key=lambda item: item["chunks"],
        reverse=True,
    )[:_MAX_INVENTORY_DOCS]

    return inventory


def _inventory_context(
    inventory: list[dict],
    include_summaries: bool,
) -> str:
    """Monta o texto de contexto a partir do inventário de documentos."""

    lines = ["Documentos anexados ao sistema:"]

    for doc in inventory:
        if include_summaries and doc["summary"]:
            snippet = doc["summary"].replace(
                "\n",
                " ",
            )[:_INVENTORY_CHARS_PER_DOC]
            lines.append(f"- {doc['source']}: {snippet}")
        else:
            lines.append(f"- {doc['source']}")

    return "\n".join(lines)


def _inventory_sources(inventory: list[dict]) -> list[dict]:
    """Converte o inventário no formato de fontes do RagResult."""

    return [
        {
            "source": doc["source"],
            "category": doc["category"],
            "chunk": doc["chunks"],
            "score": 0.0,
            "excerpt": str(doc["summary"])[:220],
        }
        for doc in inventory
    ]


def _generate_answer(
    messages: list[tuple[str, str]],
) -> tuple[str, str, str, list[str]]:
    """Invoca o primeiro LLM disponível com fallback entre provedores.

    Retorno:
        (answer, provider, model, fallback_messages)
    """

    answer = ""
    provider = ""
    model = ""
    fallback_messages: list[str] = []

    chain = _make_llm_chain()

    for (
        current_provider,
        current_model,
        llm,
    ) in chain:

        try:
            response = llm.invoke(messages)
            content = getattr(
                response,
                "content",
                response,
            )

            if isinstance(content, str):
                answer = content.strip()
            else:
                answer = str(content).strip()

            if answer:
                provider = current_provider
                model = current_model
                break

        except Exception as exc:  # noqa: BLE001
            _llm_failed.add(current_provider)
            fallback_messages.append(
                f"LLM {current_provider} indisponível: "
                f"{str(exc)[:120]}"
            )

    return answer, provider, model, fallback_messages


def _answer_document_intent(
    intent: str,
    logger: QueryLogger | None,
    t0: int,
    question: str,
) -> RagResult:
    """Responde intents sobre o inventário usando o LLM real."""

    inventory = _document_inventory()

    if not inventory:
        result = RagResult(
            answer=(
                "Ainda não há documentos anexados ao sistema. "
                "Assim que um documento for indexado, "
                "poderei listá-lo e resumi-lo."
            ),
            sources=[],
            found=False,
            provider="local",
            model="validation",
            fallback="sem documentos indexados",
        )

        if logger:
            logger.log(
                question=question,
                chunks=[],
                sources=[],
                answer=result.answer,
                latency_ms=now_ms() - t0,
                provider=result.provider,
                model=result.model,
                found=False,
                fallback=result.fallback,
            )

        return result

    include_summaries = intent == "summarize_docs"

    if include_summaries:
        task = (
            "Resuma o conteúdo de cada documento anexado, "
            "documento por documento, em tópicos curtos. "
            "Se houver muitos documentos, priorize os principais."
        )
    else:
        task = (
            "Liste os documentos anexados ao sistema, "
            "de forma organizada e legível, com uma descrição "
            "breve de cada um quando possível."
        )

    messages = [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            (
                f"{_inventory_context(inventory, include_summaries)}\n\n"
                f"Tarefa: {task}"
            ),
        ),
    ]

    answer, provider, model, fallback_messages = _generate_answer(
        messages,
    )

    sources = _inventory_sources(inventory)

    if not answer:
        answer = (
            "Encontrei os seguintes documentos anexados:\n"
            + "\n".join(
                f"- {doc['source']}"
                for doc in inventory
            )
        )
        provider = "extractive"
        model = "local"

    result = RagResult(
        answer=answer,
        sources=sources,
        found=True,
        provider=provider,
        model=model,
        fallback="; ".join(fallback_messages),
    )

    if logger:
        logger.log(
            question=question,
            chunks=[
                doc["summary"]
                for doc in inventory
            ],
            sources=sources,
            answer=result.answer,
            latency_ms=now_ms() - t0,
            provider=result.provider,
            model=result.model,
            found=result.found,
            fallback=result.fallback,
        )

    return result


def answer_question(
    question: str,
    logger: QueryLogger | None = None,
) -> RagResult:
    """Executa o pipeline completo de perguntas."""

    t0 = now_ms()

    question = question.strip()

    if not question:
        return RagResult(
            answer=FALLBACK_ANSWER,
            sources=[],
            found=False,
            provider="local",
            model="validation",
            fallback="pergunta vazia",
        )

    # --------------------------------------------------------
    # 1. Conversação guiada (sem RAG)
    # --------------------------------------------------------

    intent = _detect_intent(question)

    if intent in {"greeting", "whoami"}:
        canned = (
            GREETING_ANSWER
            if intent == "greeting"
            else WHOAMI_ANSWER
        )
        result = RagResult(
            answer=canned,
            sources=[],
            found=False,
            provider="chat",
            model="canned",
            fallback="conversa guiada (sem RAG)",
        )

        if logger:
            logger.log(
                question=question,
                chunks=[],
                sources=[],
                answer=canned,
                latency_ms=now_ms() - t0,
                provider="chat",
                model="canned",
                found=False,
                fallback=result.fallback,
            )

        return result

    # --------------------------------------------------------
    # 2. Inventário de documentos (LLM real)
    # --------------------------------------------------------

    if intent in {"list_docs", "summarize_docs"}:
        return _answer_document_intent(
            intent,
            logger,
            t0,
            question,
        )

    # --------------------------------------------------------
    # 3. Retrieval
    # --------------------------------------------------------

    hits = retrieve(question)

    context_texts = []
    sources = []

    for score, hit in hits:

        source = hit.get(
            "source",
            "?",
        )

        category = hit.get(
            "category",
            "Geral",
        )

        chunk_number = hit.get(
            "chunk",
            "?",
        )

        context_texts.append(
            f"[{source} | chunk {chunk_number}]\n"
            f"{hit['text']}"
        )

        sources.append(
            {
                "source": source,
                "category": category,
                "chunk": chunk_number,
                "score": round(
                    float(score),
                    3,
                ),
                "excerpt": str(hit["text"])[:220],
            }
        )

    context = "\n\n".join(context_texts)

    inventory = _document_inventory()
    inventory_text = _inventory_context(
        inventory,
        include_summaries=True,
    )

    # --------------------------------------------------------
    # 4. Sem correspondência: LLM responde o desvio
    # --------------------------------------------------------

    if not hits:
        messages = [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                (
                    f"{inventory_text}\n\n"
                    f"Pergunta: {question}\n\n"
                    "Se a pergunta não for sobre os documentos "
                    "acima, responda que você só tem permissão "
                    "para falar sobre os documentos disponíveis."
                ),
            ),
        ]

        answer, provider, model, fallback_messages = (
            _generate_answer(messages)
        )

        if not answer:
            answer = FALLBACK_ANSWER
            provider = config.LLM_PROVIDER
            model = config.LLM_MODEL
            fallback_messages = (
                fallback_messages or ["nenhum LLM disponível"]
            )

        result = RagResult(
            answer=answer,
            sources=[],
            found=False,
            provider=provider,
            model=model,
            fallback="; ".join(fallback_messages),
        )

        if logger:
            logger.log(
                question=question,
                chunks=[],
                sources=[],
                answer=result.answer,
                latency_ms=now_ms() - t0,
                provider=result.provider,
                model=result.model,
                found=False,
                fallback=result.fallback,
            )

        return result

    # --------------------------------------------------------
    # 5. Geração com fallback entre provedores
    # --------------------------------------------------------

    messages = [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            (
                f"{inventory_text}\n\n"
                f"Contexto:\n{context}\n\n"
                f"Pergunta: {question}"
            ),
        ),
    ]

    answer, provider, model, fallback_messages = (
        _generate_answer(messages)
    )

    # --------------------------------------------------------
    # 6. Fallback extrativo local
    # --------------------------------------------------------

    if not answer:

        answer = _extractive_answer(
            question,
            context_texts,
        )

        provider = "extractive"
        model = "local"

        if fallback_messages:
            fallback = (
                "; ".join(fallback_messages)
                + "; todos os LLMs falharam; "
                "resposta extrativa local"
            )
        else:
            fallback = (
                "nenhum LLM disponível; "
                "resposta extrativa local"
            )

    else:

        fallback = (
            "; ".join(fallback_messages)
            if fallback_messages
            else ""
        )

    # --------------------------------------------------------
    # 7. Resultado
    # --------------------------------------------------------

    result = RagResult(
        answer=answer,
        sources=sources,
        found=True,
        provider=provider,
        model=model,
        fallback=fallback,
    )

    # --------------------------------------------------------
    # 8. Auditoria
    # --------------------------------------------------------

    if logger:
        logger.log(
            question=question,
            chunks=context_texts,
            sources=sources,
            answer=result.answer,
            latency_ms=now_ms() - t0,
            provider=result.provider,
            model=result.model,
            found=True,
            fallback=result.fallback,
        )

    return result


# ============================================================
# FALLBACK EXTRATIVO
# ============================================================

def _extractive_answer(
    question: str,
    contexts: list[str],
) -> str:
    """
    Gera uma resposta simples usando frases dos documentos.

    É o último fallback quando nenhum LLM está disponível.
    """

    if not contexts:
        return FALLBACK_ANSWER

    question_words = {
        word.lower()
        for word in _normalize(question).split()
        if len(word) > 4
    }

    if not question_words:
        return FALLBACK_ANSWER

    candidates = []

    for context in contexts:

        text = context.replace(
            "\n",
            " ",
        )

        sentences = [
            sentence.strip()
            for sentence in text.split(". ")
            if sentence.strip()
        ]

        for sentence in sentences:

            sentence_lower = sentence.lower()

            matches = sum(
                1
                for word in question_words
                if word in sentence_lower
            )

            if matches > 0:
                candidates.append(
                    (
                        matches,
                        sentence,
                    )
                )

    if not candidates:
        return FALLBACK_ANSWER

    candidates.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    selected = []
    seen = set()

    for _, sentence in candidates:

        normalized_sentence = sentence.lower()

        if normalized_sentence in seen:
            continue

        seen.add(normalized_sentence)
        selected.append(sentence)

        if len(selected) >= 3:
            break

    if not selected:
        return FALLBACK_ANSWER

    return (
        "Resposta baseada nos documentos "
        "(modo offline):\n"
        + "\n".join(
            f"- {sentence}"
            for sentence in selected
        )
    )


# ============================================================
# EXECUÇÃO DIRETA
# ============================================================

if __name__ == "__main__":

    question = (
        "Quais são as linguagens usadas "
        "no back-end da plataforma?"
    )

    result = answer_question(question)

    print("\n" + "=" * 60)
    print("EZRA / MAESTRO SANTO PEGASUS")
    print("=" * 60)
    print()
    print(result.answer)
    print()
    print(
        f"Provider: {result.provider}"
    )
    print(
        f"Model: {result.model}"
    )
    print(
        f"Found: {result.found}"
    )

    if result.fallback:
        print(
            f"Fallback: {result.fallback}"
        )

    print()

    for source in result.sources:
        print(
            "Fonte:",
            source,
        )