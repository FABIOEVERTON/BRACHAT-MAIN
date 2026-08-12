"""Controle de hashes e manifesto da ingestão."""

import hashlib
import json
from pathlib import Path

from app import config


def file_hash(path: Path) -> str:
    """Calcula SHA-256 do arquivo."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for block in iter(
            lambda: file.read(65536),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def load_manifest() -> dict:
    """Carrega o manifesto de arquivos ingeridos."""
    manifest_path = (
        Path(config.VECTOR_DB_DIR)
        / "manifest.json"
    )

    try:
        return json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )
    except Exception:  # noqa: BLE001
        return {}


def save_manifest(manifest: dict) -> None:
    """Salva o manifesto de arquivos ingeridos."""
    manifest_path = (
        Path(config.VECTOR_DB_DIR)
        / "manifest.json"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
