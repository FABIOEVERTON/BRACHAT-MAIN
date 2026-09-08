"""Logs JSONL: registro de execução, auditoria, rastreabilidade e feedback."""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
)


from app import config  # noqa: E402


# ============================================================
# QUERY LOGGER
# ============================================================

class QueryLogger:
    """Persist query execution records and user feedback as JSONL."""

    def __init__(self, log_dir: str | Path | None = None):
        """
        Initialize the query logger.

        Args:
            log_dir: Optional directory where JSONL logs are stored.
                     Defaults to config.LOG_DIR.
        """

        self.log_dir = Path(
            log_dir or config.LOG_DIR
        )

        self.log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.path = (
            self.log_dir
            / f"queries_{datetime.now().strftime('%Y%m%d')}.jsonl"
        )

    # ========================================================
    # INTERNAL WRITE
    # ========================================================

    def _write(self, record: dict) -> None:
        """Append one JSON record to the current JSONL log."""

        with self.path.open(
            "a",
            encoding="utf-8",
        ) as file:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    # ========================================================
    # QUERY LOG
    # ========================================================

    def log(
        self,
        *,
        question: str,
        chunks: list[str],
        sources: list[dict],
        answer: str,
        latency_ms: float,
        provider: str,
        model: str,
        found: bool,
        feedback: str | None = None,
        fallback: str | None = None,
    ) -> None:
        """
        Record one RAG query execution.

        The record contains enough information to reconstruct
        the main execution context for auditing and debugging.
        """

        self._write(
            {
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),

                "type": "query",

                "question": question,

                "chunks": chunks,

                "sources": sources,

                "answer": answer,

                "latency_ms": round(
                    latency_ms,
                    1,
                ),

                "provider": provider,

                "model": model,

                "found": found,

                "fallback": fallback,

                "feedback": feedback,
            }
        )

    # ========================================================
    # FEEDBACK
    # ========================================================

    def feedback(
        self,
        question: str,
        value: str,
    ) -> None:
        """Record explicit user feedback for a query."""

        self._write(
            {
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),

                "type": "feedback",

                "question": question,

                "value": value,
            }
        )


# ============================================================
# TIME UTILITY
# ============================================================

def now_ms() -> float:
    """Return the current Unix timestamp in milliseconds."""

    return time.time() * 1000