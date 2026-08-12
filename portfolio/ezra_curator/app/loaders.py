"""Loaders PDF/CSV: extração, limpeza, chunking e metadados."""
import re
from pathlib import Path

import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

SUPPORTED = {".pdf", ".csv"}

SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def _clean(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _read_pdf(path: Path) -> str:
    parts = []
    for page in PdfReader(str(path)).pages:
        text = page.extract_text() or ""
        if text.strip():
            parts.append(text)
    return _clean("\n".join(parts))


def _read_csv(path: Path) -> str:
    df = pd.read_csv(path)
    return _clean(df.to_csv(index=False))


READERS = {
    ".pdf": _read_pdf,
    ".csv": _read_csv,
}


def _infer_category(path: Path) -> str:
    name = path.name.lower()
    if "backend" in name:
        return "Back-end"
    if "frontend" in name:
        return "Front-end"
    if "onboarding" in name:
        return "Onboarding"
    if "microserv" in name or "arquitetura" in name:
        return "Arquitetura"
    if "incidente" in name or "resili" in name:
        return "Resiliência"
    if "venda" in name:
        return "Vendas"
    return "Geral"


def load_document(path: str | Path) -> list[Document]:
    path = Path(path)
    if path.is_dir():
        docs = []
        for child in sorted(path.rglob("*")):
            if child.is_file() and child.suffix.lower() in SUPPORTED:
                docs.extend(load_document(child))
        return docs

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED:
        raise ValueError(f"Formato não suportado: {path.suffix} (apenas PDF e CSV)")

    text = READERS[suffix](path)
    if not text:
        return []

    chunks = SPLITTER.split_text(text)
    metadata = {
        "source": path.name,
        "file": str(path),
        "category": _infer_category(path),
    }
    return [
        Document(page_content=chunk, metadata={**metadata, "chunk": i})
        for i, chunk in enumerate(chunks)
    ]


if __name__ == "__main__":
    import sys

    for p in sorted(Path(sys.argv[1] if len(sys.argv) > 1 else "data").rglob("*")):
        if p.is_file() and p.suffix.lower() in SUPPORTED:
            docs = load_document(p)
            print(f"{p.name}: {len(docs)} chunks | categoria={docs[0].metadata['category'] if docs else '-'}")
