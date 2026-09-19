"""API compartilhada — PRD §9.1/9.2.

create_service(): uniformidade de CORS/docs/OpenAPI para todos os serviços.
schemas: JobResponse, ProblemDetail (RFC 7807) — campos exatos do PRD §9.2.
"""

from services.shared.api.conventions import create_service
from services.shared.api.schemas import JobResponse, JobStatus, ProblemDetail

__all__ = ["create_service", "JobResponse", "JobStatus", "ProblemDetail"]