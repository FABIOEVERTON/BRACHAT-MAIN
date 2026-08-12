"""Gerenciamento de embeddings: Google, Cohere e fallback local."""

import re
import time

from langchain_core.embeddings import Embeddings

from app import config


class _RetryEmbeddings(Embeddings):
    """Wrapper para embeddings com retry em caso de rate limit."""

    def __init__(
        self,
        inner: Embeddings,
        pause: float = 1.5,
        max_retries: int = 10,
    ):
        self.inner = inner
        self.pause = pause
        self.max_retries = max_retries

    def _call(self, fn, args):
        for attempt in range(self.max_retries):
            try:
                return fn(*args)

            except Exception as exc:  # noqa: BLE001
                msg = str(exc)

                if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                    match = re.search(
                        r"in (\d+(?:\.\d+)?)s",
                        msg,
                    )

                    delay = (
                        float(match.group(1))
                        if match
                        else self.pause * (2**attempt)
                    )

                    print(
                        f"  [429] aguardando {delay:.0f}s "
                        f"(tentativa {attempt + 1})...",
                        flush=True,
                    )

                    time.sleep(min(delay, 90))
                else:
                    raise

        raise RuntimeError(
            "Número máximo de tentativas excedido."
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return self._call(
            self.inner.embed_documents,
            (texts,),
        )

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        return self._call(
            self.inner.embed_query,
            (text,),
        )


class _LocalEmbeddings(Embeddings):
    """Embeddings locais usando Sentence Transformers."""

    _model_cache = {}

    def __init__(
        self,
        model: str = (
            "sentence-transformers/"
            "paraphrase-multilingual-MiniLM-L12-v2"
        ),
    ):
        self.model = model

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return self._model().encode(
            texts,
            normalize_embeddings=True,
        ).tolist()

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        return self.embed_documents([text])[0]

    def _model(self):
        if self.model not in self._model_cache:
            from sentence_transformers import SentenceTransformer

            self._model_cache[self.model] = SentenceTransformer(
                self.model
            )

        return self._model_cache[self.model]


_emb_state = {
    "emb": None,
    "provider": "",
    "model": "",
    "error": "",
}


def _build_emb_google():
    """Cria embeddings Google quando configurados."""
    if not config.GOOGLE_API_KEY:
        return None

    try:
        from langchain_google_genai import (
            GoogleGenerativeAIEmbeddings,
        )

        embeddings = GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
        )

        _emb_state.update(
            provider="google",
            model=config.EMBEDDING_MODEL,
            error="",
        )

        return _RetryEmbeddings(embeddings)

    except Exception as exc:  # noqa: BLE001
        _emb_state["error"] = f"google: {exc}"

        print(
            f"  [WARN] Embeddings Google indisponíveis ({exc}); "
            "tentando fallback.",
            flush=True,
        )

        return None


def _build_emb_cohere():
    """Cria embeddings Cohere quando configurados."""
    if not config.COHERE_API_KEY:
        return None

    try:
        from langchain_cohere import CohereEmbeddings

        embeddings = CohereEmbeddings(
            model=config.EMBEDDING_MODEL,
            cohere_api_key=config.COHERE_API_KEY,
        )

        _emb_state.update(
            provider="cohere",
            model=config.EMBEDDING_MODEL,
            error="",
        )

        return _RetryEmbeddings(embeddings)

    except Exception as exc:  # noqa: BLE001
        _emb_state["error"] = f"cohere: {exc}"

        print(
            f"  [WARN] Embeddings Cohere indisponíveis ({exc}); "
            "tentando fallback.",
            flush=True,
        )

        return None


def _build_emb_local():
    """Cria embeddings locais como último fallback."""
    _emb_state.update(
        provider="local",
        model=config.EMBEDDING_FALLBACK,
        error=_emb_state.get("error", ""),
    )

    return _LocalEmbeddings(config.EMBEDDING_FALLBACK)


def _build_embeddings():
    """Constrói embeddings conforme provider configurado."""
    provider = config.EMBEDDING_PROVIDER.lower().strip()

    if provider == "google":
        embeddings = _build_emb_google()

        if embeddings is not None:
            return embeddings

        if config.COHERE_API_KEY:
            embeddings = _build_emb_cohere()

            if embeddings is not None:
                return embeddings

        return _build_emb_local()

    if provider == "cohere":
        embeddings = _build_emb_cohere()

        if embeddings is not None:
            return embeddings

        if config.GOOGLE_API_KEY:
            embeddings = _build_emb_google()

            if embeddings is not None:
                return embeddings

        return _build_emb_local()

    return _build_emb_local()


def get_embeddings() -> Embeddings:
    """Retorna a instância singleton de embeddings."""
    if _emb_state["emb"] is None:
        _emb_state["emb"] = _build_embeddings()

    return _emb_state["emb"]


def embedding_status() -> dict:
    """Retorna o estado atual do sistema de embeddings."""
    get_embeddings()
    return dict(_emb_state)
