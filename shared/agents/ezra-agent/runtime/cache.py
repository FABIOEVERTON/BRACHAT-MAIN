import json
import hashlib
from pathlib import Path
from typing import Any, Optional


class Cache:
    """
    Simple local cache for agent runtime optimization.
    Stores skill outputs indexed by input hash.
    """

    def __init__(self, path: str = "cache.json"):
        self.path = Path(path)
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text())
        return {}

    def _save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2))

    def _hash(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        return self.data.get(key)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save()

    def get_hashed(self, content: str) -> Optional[Any]:
        key = self._hash(content)
        return self.get(key)

    def set_hashed(self, content: str, value: Any) -> None:
        key = self._hash(content)
        self.set(key, value)
