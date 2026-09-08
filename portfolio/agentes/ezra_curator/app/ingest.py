"""Ingestão de documentos em ChromaDB."""

import os
import sys
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)

from app import config  # noqa: E402
from app.embeddings import get_embeddings  # noqa: E402
from app.loaders import load_document  # noqa: E402
from app.manifest import (  # noqa: E402
    file_hash,
    load_manifest,
    save_manifest,
)


def get_collection():
    """Retorna a coleção persistida no ChromaDB."""
    Path(config.VECTOR_DB_DIR).mkdir(
        parents=True,
        exist_ok=True,
    )

    return Chroma(
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embeddings(),
        collection_name="pegasus_docs",
        collection_metadata={
            "hnsw:space": "cosine",
        },
    )


def _summary_chunk(
    path: Path,
    docs: list[Document],
) -> Document:
    """Cria um chunk de resumo por arquivo."""
    if path.suffix.lower() == ".csv":
        try:
            import pandas as pd

            df = pd.read_csv(path)

            cols = ", ".join(
                str(column)
                for column in df.columns
            )

            text = (
                f"Resumo do arquivo {path.name} (CSV). "
                f"Colunas: {cols}.\n"
                "Amostra de linhas:\n"
                f"{df.head(3).to_string(index=False)}"
            )

        except Exception:  # noqa: BLE001
            text = (
                f"Resumo do arquivo {path.name} (CSV).\n"
                f"{docs[0].page_content[:300]}"
            )

    else:
        text = (
            f"Resumo do documento {path.name} (PDF).\n"
            f"{docs[0].page_content[:400]}"
        )

    return Document(
        page_content=text,
        metadata={
            "source": path.name,
            "file": str(path),
            "category": docs[0].metadata.get(
                "category",
                "Geral",
            ),
            "chunk": "resumo",
            "tipo": "resumo",
        },
    )


def _find_files(data_dir: str) -> list[Path]:
    """Localiza arquivos elegíveis para ingestão."""
    files = sorted(Path(data_dir).rglob("*"))

    files = [
        file
        for file in files
        if file.is_file()
        and file.suffix.lower() in {".pdf", ".csv"}
    ]

    files = [
        file
        for file in files
        if "original" not in file.parts
    ]

    if config.DATA_INCLUDE:
        files = [
            file
            for file in files
            if any(
                keyword.lower() in file.name.lower()
                for keyword in config.DATA_INCLUDE
            )
        ]

    return files


def _ingest_file(
    path: Path,
    collection: Chroma,
) -> int:
    """Carrega e persiste um único arquivo."""
    docs = load_document(path)

    if not docs:
        return 0

    docs = [
        _summary_chunk(path, docs),
        *docs,
    ]

    ids = [
        f"{path.stem}-{doc.metadata['chunk']}"
        for doc in docs
    ]

    existing = collection.get(
        where={"source": path.name},
        include=[],
    )

    if existing and existing.get("ids"):
        collection.delete(ids=existing["ids"])

    collection.add_texts(
        texts=[
            doc.page_content
            for doc in docs
        ],
        metadatas=[
            doc.metadata
            for doc in docs
        ],
        ids=ids,
    )

    print(
        f"  + {path.name}: "
        f"{len(docs)} chunks "
        "(inclui resumo)"
    )

    return len(docs)


def ingest(
    data_dir: str | None = None,
    update_only: bool = False,
) -> dict:
    """Ingere PDFs e CSVs no ChromaDB."""
    data_dir = data_dir or config.DATA_DIR
    collection = get_collection()
    files = _find_files(data_dir)

    total = 0
    manifest = load_manifest()

    for path in files:
        current_hash = file_hash(path)

        if (
            update_only
            and manifest.get(path.name) == current_hash
        ):
            print(
                f"  = {path.name}: "
                "inalterado (pulado)"
            )
            continue

        chunks = _ingest_file(
            path,
            collection,
        )

        if chunks:
            manifest[path.name] = current_hash
            total += chunks

    save_manifest(manifest)

    print(
        f"Total: {total} chunks "
        f"em {config.VECTOR_DB_DIR}"
    )

    return {
        "files": len(files),
        "chunks": total,
    }


if __name__ == "__main__":
    ingest(
        update_only="--update" in sys.argv
    )
