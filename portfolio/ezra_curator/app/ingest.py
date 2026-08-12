"""Ingestão: embeddings + ChromaDB (persistido em disco)."""
import json
import os
import re
import sys
import time
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import config  # noqa: E402
from app.loaders import load_document  # noqa: E402


class _RetryEmbeddings(Embeddings):
    def __init__(self, inner: Embeddings, pause: float = 1.5, max_retries: int = 10):
        self.inner = inner
        self.pause = pause
        self.max_retries = max_retries

    def _call(self, fn, args):
        for attempt in range(self.max_retries):
            try:
                return fn(*args)
            except Exception as e:  # noqa: BLE001
                msg = str(e)
                if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                    m = re.search(r"in (\d+(?:\.\d+)?)s", msg)
                    delay = float(m.group(1)) if m else self.pause * (2 ** attempt)
                    print(f"  [429] aguardando {delay:.0f}s (tentativa {attempt + 1})...", flush=True)
                    time.sleep(min(delay, 90))
                else:
                    raise

    def embed_documents(self, texts):
        return self._call(self.inner.embed_documents, (texts,))

    def embed_query(self, text):
        return self._call(self.inner.embed_query, (text,))


class _LocalEmbeddings(Embeddings):
    _model_cache = {}

    def __init__(self, model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._model().encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def _model(self):
        if self.model not in self._model_cache:
            from sentence_transformers import SentenceTransformer

            self._model_cache[self.model] = SentenceTransformer(self.model)
        return self._model_cache[self.model]


_emb_state = {"emb": None, "provider": "cohere", "model": "", "error": ""}


def _build_embeddings():
    if config.EMBEDDING_PROVIDER == "cohere" and config.COHERE_API_KEY:
        try:
            from langchain_cohere import CohereEmbeddings

            emb = CohereEmbeddings(model=config.EMBEDDING_MODEL, cohere_api_key=config.COHERE_API_KEY)
            _emb_state.update(provider="cohere", model=config.EMBEDDING_MODEL, error="")
            return emb
        except Exception as exc:  # noqa: BLE001
            _emb_state["error"] = f"cohere: {exc}"
            print(f"  [WARN] Embeddings Cohere indisponíveis ({exc}); usando MiniLM local", flush=True)
    if config.EMBEDDING_PROVIDER == "google" and config.GOOGLE_API_KEY:
        try:
            emb = _RetryEmbeddings(GoogleGenerativeAIEmbeddings(
                model=config.EMBEDDING_MODEL, google_api_key=config.GOOGLE_API_KEY))
            _emb_state.update(provider="google", model=config.EMBEDDING_MODEL, error="")
            return emb
        except Exception as exc:  # noqa: BLE001
            _emb_state["error"] = f"google: {exc}"
    _emb_state.update(provider="local", model=config.EMBEDDING_FALLBACK, error=_emb_state["error"])
    return _LocalEmbeddings()


def get_embeddings() -> Embeddings:
    if _emb_state["emb"] is None:
        _emb_state["emb"] = _build_embeddings()
    return _emb_state["emb"]


def embedding_status() -> dict:
    get_embeddings()
    return dict(_emb_state)


def get_collection():
    Path(config.VECTOR_DB_DIR).mkdir(parents=True, exist_ok=True)
    return Chroma(
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embeddings(),
        collection_name="pegasus_docs",
        collection_metadata={"hnsw:space": "cosine"},
    )


def _summary_chunk(path: Path, docs) -> Document:
    """Chunk de resumo por arquivo: ancora perguntas agregadas (ano, categorias, total)."""
    if path.suffix.lower() == ".csv":
        try:
            import pandas as pd

            df = pd.read_csv(path)
            cols = ", ".join(str(c) for c in df.columns)
            text = f"Resumo do arquivo {path.name} (CSV). Colunas: {cols}.\nAmostra de linhas:\n{df.head(3).to_string(index=False)}"
        except Exception:  # noqa: BLE001
            text = f"Resumo do arquivo {path.name} (CSV).\n{docs[0].page_content[:300]}"
    else:
        text = f"Resumo do documento {path.name} (PDF).\n{docs[0].page_content[:400]}"
    return Document(
        page_content=text,
        metadata={
            "source": path.name,
            "file": str(path),
            "category": docs[0].metadata.get("category", "Geral"),
            "chunk": "resumo",
            "tipo": "resumo",
        },
    )


def _file_hash(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def _load_manifest() -> dict:
    mpath = Path(config.VECTOR_DB_DIR) / "manifest.json"
    try:
        return json.loads(mpath.read_text())
    except Exception:  # noqa: BLE001
        return {}


def _save_manifest(manifest: dict) -> None:
    mpath = Path(config.VECTOR_DB_DIR) / "manifest.json"
    mpath.write_text(json.dumps(manifest, indent=2))


def ingest(data_dir: str | None = None, update_only: bool = False) -> dict:
    data_dir = data_dir or config.DATA_DIR
    collection = get_collection()
    files = sorted(Path(data_dir).rglob("*"))
    files = [f for f in files if f.is_file() and f.suffix.lower() in {".pdf", ".csv"}]
    files = [f for f in files if "original" not in f.parts]
    if config.DATA_INCLUDE:
        files = [f for f in files if any(k in f.name for k in config.DATA_INCLUDE)]

    total = 0
    manifest = _load_manifest()
    for path in files:
        fhash = _file_hash(path)
        if update_only and manifest.get(path.name) == fhash:
            print(f"  = {path.name}: inalterado (pulado)")
            continue
        docs = load_document(path)
        if not docs:
            continue
        docs = [_summary_chunk(path, docs)] + docs
        ids = [f"{path.stem}-{d.metadata['chunk']}" for d in docs]
        existing = collection.get(where={"source": path.name}, include=[])
        if existing and existing.get("ids"):
            collection.delete(ids=existing["ids"])
        collection.add_texts(
            texts=[d.page_content for d in docs],
            metadatas=[d.metadata for d in docs],
            ids=ids,
        )
        manifest[path.name] = fhash
        total += len(docs)
        print(f"  + {path.name}: {len(docs)} chunks (inclui resumo)")
    _save_manifest(manifest)
    print(f"Total: {total} chunks em {config.VECTOR_DB_DIR}")
    return {"files": len(files), "chunks": total}


if __name__ == "__main__":
    import sys

    ingest(update_only="--update" in sys.argv)
