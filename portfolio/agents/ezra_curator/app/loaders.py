"""Loaders PDF/CSV: extração, limpeza, chunking e metadados."""

import re
import sys
from pathlib import Path

import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


# ============================================================
# SUPPORTED FORMATS
# ============================================================

SUPPORTED = {".pdf", ".csv"}


# ============================================================
# TEXT SPLITTER
# ============================================================

SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""],
)


# ============================================================
# TEXT CLEANING
# ============================================================

def _clean(text: str) -> str:
    """Normalize whitespace and remove excessive blank lines."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ============================================================
# PDF READER
# ============================================================

def _read_pdf(path: Path) -> str:
    """Extract text from all readable PDF pages."""
    parts: list[str] = []

    reader = PdfReader(str(path))

    for page in reader.pages:
        text = page.extract_text() or ""

        if text.strip():
            parts.append(text)

    return _clean("\n".join(parts))


# ============================================================
# CSV READER
# ============================================================

def _read_csv(path: Path) -> str:
    """Read a CSV file and convert it into normalized text."""
    df = pd.read_csv(path)

    return _clean(
        df.to_csv(index=False)
    )


# ============================================================
# READER REGISTRY
# ============================================================

READERS = {
    ".pdf": _read_pdf,
    ".csv": _read_csv,
}


# ============================================================
# CATEGORY INFERENCE
# ============================================================

def _infer_category(path: Path) -> str:
    """Infer a document category from its filename."""

    name = path.name.lower()

    if "backend" in name or "back-end" in name:
        return "Back-end"

    if "frontend" in name or "front-end" in name:
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


# ============================================================
# DOCUMENT LOADER
# ============================================================

def load_document(path: str | Path) -> list[Document]:
    """
    Load one document or recursively load all supported documents
    from a directory.

    Returns:
        list[Document]: Chunked LangChain documents with metadata.
    """

    path = Path(path)

    # --------------------------------------------------------
    # DIRECTORY
    # --------------------------------------------------------

    if path.is_dir():
        docs: list[Document] = []

        for child in sorted(path.rglob("*")):
            if (
                child.is_file()
                and child.suffix.lower() in SUPPORTED
            ):
                docs.extend(
                    load_document(child)
                )

        return docs

    # --------------------------------------------------------
    # FILE VALIDATION
    # --------------------------------------------------------

    suffix = path.suffix.lower()

    if suffix not in SUPPORTED:
        raise ValueError(
            f"Formato não suportado: {path.suffix} "
            f"(apenas PDF e CSV)"
        )

    # --------------------------------------------------------
    # EXTRACTION
    # --------------------------------------------------------

    text = READERS[suffix](path)

    if not text:
        return []

    # --------------------------------------------------------
    # CHUNKING
    # --------------------------------------------------------

    chunks = SPLITTER.split_text(text)

    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    metadata = {
        "source": path.name,
        "file": str(path),
        "category": _infer_category(path),
    }

    # --------------------------------------------------------
    # LANGCHAIN DOCUMENTS
    # --------------------------------------------------------

    return [
        Document(
            page_content=chunk,
            metadata={
                **metadata,
                "chunk": i,
            },
        )
        for i, chunk in enumerate(chunks)
    ]


# ============================================================
# CLI / TEST
# ============================================================

if __name__ == "__main__":

    data_dir = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else "data"
    )

    if not data_dir.exists():
        print(f"Diretório não encontrado: {data_dir}")
        sys.exit(1)

    for path in sorted(data_dir.rglob("*")):

        if (
            path.is_file()
            and path.suffix.lower() in SUPPORTED
        ):
            docs = load_document(path)

            category = (
                docs[0].metadata["category"]
                if docs
                else "-"
            )

            print(
                f"{path.name}: "
                f"{len(docs)} chunks | "
                f"categoria={category}"
            )