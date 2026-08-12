"""Camada RAG: busca semântica + rerank + montagem de contexto + geração."""
import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import config  # noqa: E402
from app.ingest import get_collection  # noqa: E402
from app.logging import QueryLogger, now_ms  # noqa: E402

SYSTEM_PROMPT = (
    "Você é o Maestro Santo Pegasus, um agente corporativo que responde perguntas "
    "de colaboradores da Santos Pegasus Soluciones com base SOMENTE no contexto "
    "fornecido. Regras: 1) responda apenas com base no contexto; 2) se a "
    "informação não estiver no contexto, diga 'Não encontrei essa informação nos "
    "documentos disponíveis.' e sugira contato com a área responsável; "
    "3) cite a fonte de cada informação no formato [arquivo, seção/página]; "
    "4) nunca invente dados."
)

FALLBACK_ANSWER = (
    "Não encontrei essa informação nos documentos disponíveis. "
    "Posso ajudar com perguntas sobre o Guia de Engenharia Back-end (PDF) "
    "ou as Vendas de 2015 (CSV). Caso precise de algo de outra área, sugiro "
    "entrar em contato com Engenharia, Recursos Humanos ou Suporte."
)

GREETING_ANSWER = (
    "Olá! Tudo bem? Sou o Maestro Santo Pegasus 🦅, o agente de IA corporativo "
    "da Santos Pegasus Soluciones. Posso responder perguntas com base nos "
    "documentos internos, como o Guia de Engenharia Back-end e as Vendas de "
    "2015. Como posso ajudar?"
)

WHOAMI_ANSWER = (
    "Sou o Maestro Santo Pegasus 🦅, um agente de IA corporativo da Santos "
    "Pegasus Soluciones. Respondo perguntas de colaboradores com base nos "
    "documentos internos da empresa, como o Guia de Engenharia Back-end (PDF) "
    "e as Vendas de 2015 (CSV). Pergunte algo sobre esses documentos!"
)

GREETING_WORDS = {
    "oi", "ola", "olá", "oii", "oie", "eai", "e ai", "opa", "hey", "hi",
    "hello", "bom dia", "boa tarde", "boa noite", "tudo bem", "tudo bom",
    "bom te ver", "salve",
}

WHOAMI_WORDS = {
    "quem e voce", "quem é você", "o que voce faz", "o que você faz",
    "quem voce e", "você é o que", "voce e um robo", "que agente é esse",
}

DOCS_WORDS = {
    "quais documentos", "que documentos", "quais documentos voce tem",
    "quais documentos você tem", "quais documentos voce possui",
    "quais arquivos", "quais arquivos voce tem", "documentos disponiveis",
    "documentos internos", "quais documentos voce pode",
}

DOCS_ANSWER = (
    "Tenho acesso aos seguintes documentos internos da Santos Pegasus Soluciones:\n"
    "- 📘 Guia de Engenharia Back-end (PDF) — linguagens, framework e arquitetura do back-end.\n"
    "- 📊 Vendas 2015 (CSV) — produtos, categorias e receita de vendas do ano de 2015.\n"
    "Posso responder perguntas sobre qualquer um deles. O que gostaria de saber?"
)


def _normalize(text: str) -> str:
    import unicodedata

    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return " ".join(text.lower().replace("?", "").replace("!", "").split())


def _detect_canned(question: str) -> str | None:
    q = _normalize(question)
    if not q:
        return None
    if q in WHOAMI_WORDS or any(w in q for w in WHOAMI_WORDS if len(w) > 8):
        return WHOAMI_ANSWER
    if any(w in q for w in DOCS_WORDS):
        return DOCS_ANSWER
    if q in GREETING_WORDS or any(q.startswith(w) for w in GREETING_WORDS if len(w) >= 3):
        return GREETING_ANSWER
    return None


@dataclass
class RagResult:
    answer: str
    sources: list[dict] = field(default_factory=list)
    found: bool = False
    provider: str = ""
    model: str = ""
    fallback: str = ""


def system_status() -> dict:
    from app.ingest import embedding_status

    emb = embedding_status()
    chain = _make_llm_chain()
    active = chain[0] if chain else None
    return {
        "llm_provider": active[0] if active else "indisponível",
        "llm_model": active[1] if active else "-",
        "llm_chain": [(p, m) for p, m, _ in chain],
        "emb_provider": emb["provider"],
        "emb_model": emb["model"],
        "emb_error": emb["error"],
        "reranker": "BAAI/bge-reranker-base (local)",
        "fallback_chain": [
            "LLM: Cohere → Mistral → Anthropic → resposta extrativa local",
            "Embeddings: Cohere → MiniLM local",
            "Reranker: local BAAI → ordenação por similaridade",
            "Fora do escopo: conversa guiada para os documentos",
        ],
    }


_llm_failed: set[str] = set()


def _llm_factories() -> list[tuple[str, str, object]]:
    """Provedores LLM em ordem de prioridade: (provider, model, factory)."""
    from langchain_anthropic import ChatAnthropic
    from langchain_cohere import ChatCohere
    from langchain_mistralai import ChatMistralAI

    factories = []
    if config.COHERE_API_KEY:
        model = config.LLM_MODEL if config.LLM_PROVIDER == "cohere" else "command-r7b-12-2024"
        factories.append(("cohere", model, lambda m=model: ChatCohere(
            model=m, cohere_api_key=config.COHERE_API_KEY, temperature=0.1)))
    if config.MISTRAL_API_KEY:
        model = config.LLM_MODEL if config.LLM_PROVIDER == "mistral" else "mistral-small-latest"
        factories.append(("mistral", model, lambda m=model: ChatMistralAI(
            model=m, mistral_api_key=config.MISTRAL_API_KEY, temperature=0.1)))
    if config.ANTHROPIC_API_KEY:
        model = config.LLM_MODEL if config.LLM_PROVIDER == "anthropic" else "claude-sonnet-4-20250514"
        factories.append(("anthropic", model, lambda m=model: ChatAnthropic(
            model=m, api_key=config.ANTHROPIC_API_KEY, temperature=0.1)))
    return factories


def _make_llm_chain() -> list[tuple[str, str, object]]:
    chain = []
    for provider, model, factory in _llm_factories():
        if provider in _llm_failed:
            continue
        try:
            chain.append((provider, model, factory()))
        except Exception:
            _llm_failed.add(provider)
    return chain


def _make_llm():
    chain = _make_llm_chain()
    return chain[0][2] if chain else None


def _rerank(query: str, chunks: list[tuple[float, dict]], top_k: int) -> list[tuple[float, dict]]:
    try:
        from sentence_transformers import CrossEncoder

        model = CrossEncoder("BAAI/bge-reranker-base")
        pairs = [(query, c[1]["text"]) for c in chunks]
        scores = model.predict(pairs)
        scored = sorted(zip(scores.tolist(), chunks), key=lambda x: x[0], reverse=True)
        return [(float(s), c[1]) for s, c in scored[:top_k]]
    except Exception:
        return [(c[0], c[1]) for c in chunks[:top_k]]


def retrieve(question: str, top_k: int | None = None, rerank_top: int | None = None):
    top_k = top_k or config.TOP_K
    rerank_top = rerank_top or config.RERANK_TOP_K
    collection = get_collection()
    res = collection.similarity_search_with_score(question, k=top_k * 4)
    results = []
    for doc, dist in res:
        sim = 1.0 - dist
        if sim >= config.CONFIDENCE_THRESHOLD:
            results.append((sim, {"text": doc.page_content, **doc.metadata}))
    if not results:
        return []
    return _rerank(question, results, rerank_top)


def answer_question(question: str, logger: QueryLogger | None = None) -> RagResult:
    t0 = now_ms()

    canned = _detect_canned(question)
    if canned:
        result = RagResult(answer=canned, sources=[], found=False, provider="chat", model="canned",
                           fallback="conversa guiada (sem RAG)")
        if logger:
            logger.log(question=question, chunks=[], sources=[], answer=canned,
                       latency_ms=now_ms() - t0, provider="chat", model="canned", found=False)
        return result

    llm = _make_llm()
    hits = retrieve(question)
    ctx_texts = []
    sources = []
    for score, hit in hits:
        ctx_texts.append(f"[{hit.get('source', '?')}]\n{hit['text']}")
        sources.append({"source": hit.get("source"), "category": hit.get("category"), "score": round(score, 3)})
    context = "\n\n".join(ctx_texts)

    if not hits:
        result = RagResult(answer=FALLBACK_ANSWER, sources=sources, found=False,
                           provider=config.LLM_PROVIDER, model=config.LLM_MODEL,
                           fallback="sem correspondência nos documentos")
        if logger:
            logger.log(question=question, chunks=ctx_texts, sources=sources,
                       answer=result.answer, latency_ms=now_ms() - t0,
                       provider=config.LLM_PROVIDER, model=config.LLM_MODEL, found=False,
                       fallback=result.fallback)
        return result

    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", f"Contexto:\n{context}\n\nPergunta: {question}"),
    ]
    answer, provider, model, fallback = None, "", "", ""
    for provider, model, llm in _make_llm_chain():
        try:
            resp = llm.invoke(messages)
            answer = resp.content if isinstance(resp.content, str) else str(resp.content)
            break
        except Exception as exc:  # noqa: BLE001
            _llm_failed.add(provider)
            fallback = f"LLM {provider} indisponível ({str(exc)[:80]}); usado próximo provedor"
    if answer is None:
        answer = _extractive_answer(question, ctx_texts)
        provider = "extractive"
        model = "local"
        fallback = "todos os LLMs falharam; resposta extrativa local"

    result = RagResult(answer=answer, sources=sources, found=True,
                       provider=provider, model=model, fallback=fallback)
    if logger:
        logger.log(question=question, chunks=ctx_texts, sources=sources,
                   answer=answer, latency_ms=now_ms() - t0,
                   provider=provider, model=model, found=True, fallback=fallback)
    return result


def _extractive_answer(question: str, contexts: list[str]) -> str:
    sentences = []
    for ctx in contexts:
        for sent in ctx.replace("\n", " ").split(". "):
            q = question.lower()
            if any(w in sent.lower() for w in q.split() if len(w) > 4):
                sentences.append(sent.strip())
    if sentences:
        return "Resposta baseada nos documentos (modo offline):\n- " + "\n- ".join(sentences[:3])
    return FALLBACK_ANSWER


if __name__ == "__main__":
    r = answer_question("Quais são as linguagens usadas no back-end da plataforma?")
    print(r.answer)
    for s in r.sources:
        print("fonte:", s)
