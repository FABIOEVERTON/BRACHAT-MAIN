"""Logs JSONL: registro de execução (auditoria, rastreabilidade, feedback)."""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import config  # noqa: E402


class QueryLogger:
    def __init__(self, log_dir: str | None = None):
        self.log_dir = Path(log_dir or config.LOG_DIR)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.log_dir / f"queries_{datetime.now().strftime('%Y%m%d')}.jsonl"

    def _write(self, record: dict) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def log(self, *, question: str, chunks: list[str], sources: list[dict],
            answer: str, latency_ms: float, provider: str, model: str,
            found: bool, feedback: str | None = None, fallback: str | None = None) -> None:
        self._write({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": question,
            "chunks": chunks,
            "sources": sources,
            "answer": answer,
            "latency_ms": round(latency_ms, 1),
            "provider": provider,
            "model": model,
            "found": found,
            "fallback": fallback,
            "feedback": feedback,
        })

    def feedback(self, question: str, value: str) -> None:
        self._write({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "feedback",
            "question": question,
            "value": value,
        })


def now_ms() -> float:
    return time.time() * 1000
