"""Motor de jobs assíncronos (E0B-S02, PRD §9.2, ADR-007).

- Enfileira: 202 + job_id (SQS)
- Worker: queued → processing → completed|failed
- Idempotência: dedup por job/dedup_key (F0B-08) — nunca duplica laudo
- Webhook ao completar (F0B-09)
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Callable, Coroutine

import boto3

from services.shared.api.schemas import JobResponse, JobStatus
from services.shared.laudo.models import LaudoResult

JobHandler = Callable[[dict], Coroutine[Any, Any, JobResponse]]


class JobError(Exception):
    """Erro de job → status FAILED + RFC 7807 (F0B-07)."""

    def __init__(self, *, title: str, detail: str, status: int = 422):
        self.title = title
        self.detail = detail
        self.status = status
        super().__init__(detail)


@dataclass
class Job:
    job_id: str
    tenant_id: str
    job_type: str
    payload: dict
    dedup_key: str | None
    webhook_url: str | None
    status: JobStatus = JobStatus.QUEUED
    progress_pct: int = 0
    result_url: str | None = None
    error: str | None = None
    laudo: LaudoResult | None = None
    max_retries: int = 3
    attempt: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class JobStore:
    """Repositório em memória (FASE 0) — SQLAlchemy entra na FASE 1.

    Visible for testing: get, update; thread-agnostic (asyncio).
    """

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._by_dedup: dict[str, str] = {}

    def create(self, *, tenant_id: str, job_type: str, payload: dict,
               dedup_key: str | None, webhook_url: str | None) -> Job:
        job_id = uuid.uuid4().hex
        job = Job(job_id=job_id, tenant_id=tenant_id, job_type=job_type,
                  payload=payload, dedup_key=dedup_key, webhook_url=webhook_url)
        self._jobs[job_id] = job
        if dedup_key:
            self._by_dedup[dedup_key] = job_id
        return job

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def by_dedup(self, dedup_key: str) -> Job | None:
        jid = self._by_dedup.get(dedup_key)
        return self._jobs.get(jid) if jid else None

    def update(self, job: Job) -> None:
        self._jobs[job.job_id] = job


class QueueProducer:
    """Producer — enfileira mensagem no SQS (LocalStack dev).

    Auto-cria a fila ezra-jobs se não existir (dev convenience).
    """

    def __init__(self, *, queue_url: str | None = None, endpoint_url: str | None = None):
        self.endpoint = endpoint_url or os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
        self.queue_url = queue_url or os.environ.get(
            "SQS_JOBS_QUEUE_URL", "http://localhost:4566/000000000000/ezra-jobs"
        )
        self.sqs = boto3.client(
            "sqs",
            endpoint_url=self.endpoint,
            region_name="sa-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
        self._ensure_queue()

    def _ensure_queue(self) -> None:
        try:
            self.sqs.get_queue_url(QueueName="ezra-jobs")
        except Exception:
            r = self.sqs.create_queue(QueueName="ezra-jobs")
            self.queue_url = r["QueueUrl"]

    def send(self, job: Job) -> None:
        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps({
                "job_id": job.job_id,
                "tenant_id": job.tenant_id,
                "job_type": job.job_type,
                "payload": job.payload,
                "dedup_key": job.dedup_key,
                "webhook_url": job.webhook_url,
            }),
            MessageDeduplicationId=job.job_id,
        )


class JobWorker:
    """Worker — processa mensagens do SQS, dedup + retry + webhook."""

    def __init__(self, *, store: JobStore, producer: QueueProducer | None = None,
                 handler: JobHandler, max_retries: int = 3):
        self.store = store
        self.producer = producer or QueueProducer()
        self.handler = handler
        self.registry: dict[str, JobHandler] = {"default": handler}
        self.max_retries = max_retries

    def register(self, job_type: str, handler: JobHandler) -> None:
        self.registry[job_type] = handler

    async def process(self, job: Job) -> JobResponse:
        if not job:
            raise JobError(title="Not Found", detail="job inexistente", status=404)

        # Idempotência (F0B-08): se dedup_key já processada com sucesso → replay
        existing = self.store.by_dedup(job.dedup_key) if job.dedup_key else None
        if existing and existing.status == JobStatus.COMPLETED:
            return self._to_response(existing)

        handler = self.registry.get(job.job_type, self.registry["default"])
        job.status = JobStatus.PROCESSING
        job.progress_pct = 10
        self.store.update(job)

        try:
            result = await handler(job)
        except JobError as e:
            return self._fail(job, e)
        except Exception as e:  # noqa: BLE001 — erro desconhecido vira FAILED
            return self._fail(job, JobError(title="Internal Error", detail=str(e), status=500))

        # completed
        job.status = JobStatus.COMPLETED
        job.progress_pct = 100
        job.result_url = result.result_url
        job.laudo = result.laudo
        self.store.update(job)

        # Webhook (F0B-09)
        if job.webhook_url:
            await self._webhook(job)

        return self._to_response(job)

    def _fail(self, job: Job, err: JobError) -> JobResponse:
        job.attempt += 1
        if job.attempt < self.max_retries:
            # retry: volta para QUEUED (F0B-07 retry configurado)
            job.status = JobStatus.QUEUED
            job.error = err.detail
            self.store.update(job)
            return self._to_response(job)
        job.status = JobStatus.FAILED
        job.error = f"{err.title}: {err.detail}"
        self.store.update(job)
        return self._to_response(job)

    @staticmethod
    async def _webhook(job: Job) -> None:
        import httpx

        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(job.webhook_url or "", json={
                "job_id": job.job_id,
                "status": "completed",
                "result_url": job.result_url,
            })

    @staticmethod
    def _to_response(job: Job) -> JobResponse:
        return JobResponse(
            job_id=job.job_id,
            status=job.status,
            progress_pct=job.progress_pct,
            result_url=job.result_url if job.status == JobStatus.COMPLETED else None,
            error=job.error if job.status == JobStatus.FAILED else None,
            laudo=job.laudo.__dict__ if job.laudo else None,
        )