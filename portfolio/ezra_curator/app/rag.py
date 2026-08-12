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
# PROMPTS E RESPOSTAS PADRÃO
# ============================================================

SYSTEM_PROMPT = (
    "Você é o Maestro Santo Pegasus, um agente corporativo que responde "
    "perguntas de colaboradores da Santos Pegasus Soluciones com base "
    "SOMENTE no contexto fornecido. "
    "Regras: "
    "1) responda apenas com base no contexto; "
    "2) se a informação não estiver no contexto, diga "
    "'Não encontrei essa informação nos documentos disponíveis.' "
    "e sugira contato com a área responsável; "
    "3) cite a fonte de cada informação no formato "
    "[arquivo, seção/página]; "
    "4) nunca invente dados."
)

FALLBACK_ANSWER = (
    "Não encontrei essa informação nos documentos disponíveis. "
    "Posso ajudar com perguntas sobre os documentos indexados. "
    "Caso precise de algo de outra área, sugiro entrar em contato "
    "com a área responsável."
)

GREETING_ANSWER = (
    "Olá! Tudo bem? Sou o Maestro Santo Pegasus 🦅, "
    "o agente de IA corporativo da Santos Pegasus Soluciones. "
    "Posso responder perguntas com base nos documentos internos. "
    "Como posso ajudar?"
)

WHOAMI_ANSWER = (
    "Sou o Maestro Santo Pegasus 🦅, um agente de IA corporativo "
    "da Santos Pegasus Soluciones. Respondo perguntas de colaboradores "
    "com base nos documentos internos da empresa."
)

DOCS_ANSWER = (
    "Tenho acesso aos documentos internos que foram indexados no "
    "banco vetorial do sistema. Posso responder perguntas sobre "
    "o conteúdo desses documentos."
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
    "quais arquivos",
    "quais arquivos voce tem",
    "documentos disponiveis",
    "documentos internos",
    "quais documentos voce pode",
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


def _detect_canned(question: str) -> str | None:
    """Detecta perguntas conversacionais que não precisam de RAG."""

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

    normalized_greetings = {
        _normalize(word)
        for word in GREETING_WORDS
    }

    if q in normalized_whoami:
        return WHOAMI_ANSWER

    if any(
        word in q
        for word in normalized_whoami
        if len(word) > 8
    ):
        return WHOAMI_ANSWER

    if any(
        word in q
        for word in normalized_docs
    ):
        return DOCS_ANSWER

    if q in normalized_greetings:
        return GREETING_ANSWER

    if any(
        q.startswith(word)
        for word in normalized_greetings
        if len(word) >= 3
    ):
        return GREETING_ANSWER

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

def answer_question(
    question: str,
    logger: QueryLogger | None = None,
) -> RagResult:
    """Executa o pipeline completo de perguntas."""

    t0 = now_ms()

    question = question.strip()

    if not question:
        result = RagResult(
            answer=FALLBACK_ANSWER,
            sources=[],
            found=False,
            provider="local",
            model="validation",
            fallback="pergunta vazia",
        )

        return result

    # --------------------------------------------------------
    # 1. Perguntas conversacionais
    # --------------------------------------------------------

    canned = _detect_canned(question)

    if canned:
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
    # 2. Retrieval
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
            }
        )

    context = "\n\n".join(context_texts)

    # --------------------------------------------------------
    # 3. Nenhum documento relevante
    # --------------------------------------------------------

    if not hits:

        result = RagResult(
            answer=FALLBACK_ANSWER,
            sources=[],
            found=False,
            provider=config.LLM_PROVIDER,
            model=config.LLM_MODEL,
            fallback="sem correspondência nos documentos",
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
    # 4. Geração com fallback entre provedores
    # --------------------------------------------------------

    messages = [
        (
            "system",
            SYSTEM_PROMPT,
        ),
        (
            "human",
            (
                f"Contexto:\n{context}\n\n"
                f"Pergunta: {question}"
            ),
        ),
    ]

    answer = None
    provider = ""
    model = ""
    fallback_messages = []

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

            _llm_failed.add(
                current_provider
            )

            fallback_messages.append(
                (
                    f"LLM {current_provider} indisponível: "
                    f"{str(exc)[:120]}"
                )
            )

    # --------------------------------------------------------
    # 5. Fallback extrativo local
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
    # 6. Resultado
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
    # 7. Auditoria
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