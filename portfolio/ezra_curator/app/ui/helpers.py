"""UI helper functions."""

import html
import unicodedata
from pathlib import Path

from app.rag import get_collection


def normalize_text(value: object) -> str:
    """Normalize text for case/accent-insensitive comparisons."""
    text = str(value or "")

    return "".join(
        char
        for char in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(char)
    ).lower()


def safe_text(value: object) -> str:
    """Escape untrusted text before inserting it into HTML."""
    return html.escape(str(value or ""))


def safe_score(value: object) -> float:
    """Convert a source score safely to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def get_collection_chunk_count() -> int:
    """Return the current ChromaDB collection size."""
    try:
        collection = get_collection()
        raw_collection = getattr(collection, "_collection", None)

        if raw_collection is not None:
            return int(raw_collection.count())

        if hasattr(collection, "count"):
            return int(collection.count())

    except Exception:
        pass

    return 0


def get_document_sources() -> list[str]:
    """Return unique indexed document sources."""
    try:
        collection = get_collection()
        data = collection.get(include=["metadatas"])

        metadatas = data.get("metadatas") or []

        return sorted(
            {
                str(metadata.get("source"))
                for metadata in metadatas
                if metadata and metadata.get("source")
            }
        )

    except Exception:
        return []


def get_file_document_id(
    file_name: str,
    file_bytes: bytes,
) -> str:
    """Create a stable document ID from filename and content."""
    import hashlib

    digest = hashlib.sha256(file_bytes).hexdigest()[:16]

    return f"{Path(file_name).stem}-{digest}"