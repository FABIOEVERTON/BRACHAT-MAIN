"""Schemas de API compartilhados (PRD §9.2) — campos EXATOS do PRD."""

from enum import StrEnum

from pydantic import BaseModel


class JobStatus(StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    progress_pct: int | None = None
    result_url: str | None = None  # Disponível quando status = COMPLETED
    error: str | None = None  # Disponível quando status = FAILED
    laudo: dict | None = None  # Disponível quando status = COMPLETED (LaudoResult)


class ProblemDetail(BaseModel):
    """RFC 7807 (PRD §9.2)."""

    type: str
    title: str
    status: int
    detail: str
    instance: str