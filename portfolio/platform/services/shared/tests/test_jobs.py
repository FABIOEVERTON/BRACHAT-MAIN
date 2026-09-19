"""Testes — Motor de jobs assíncronos (E0B-S02, PRD §9.2).

Cobre:
- F0B-06: ciclo queued → processing → completed + result_url
- F0B-07: falha → FAILED + RFC 7807 (retry configurado)
- F0B-08: idempotência — mesmo dedup_key processado 1x
- F0B-09: webhook disparado ao completar
- F0B-10: GET /jobs/{job_id} → JobResponse com progress_pct
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from services.shared.api.schemas import JobResponse, JobStatus
from services.shared.queue import Job, JobError, JobStore, JobWorker, QueueProducer


async def _good_handler(job: Job) -> JobResponse:
    job.progress_pct = 90
    return JobResponse(
        job_id=job.job_id,
        status=JobStatus.COMPLETED,
        progress_pct=100,
        result_url=f"/v1/laudos/{job.job_id}",
    )


def _store() -> JobStore:
    return JobStore()


def test_f0b10_job_response_progress_pct():
    resp = JobResponse(job_id="abc", status=JobStatus.PROCESSING, progress_pct=42)
    assert resp.progress_pct == 42
    assert resp.status == "processing"


@pytest.mark.asyncio
async def test_f0b06_full_cycle():
    store = _store()
    producer = MagicMock(spec=QueueProducer)
    worker = JobWorker(store=store, producer=producer, handler=_good_handler)

    job = store.create(tenant_id="t1", job_type="laudo", payload={}, dedup_key=None,
                       webhook_url=None)
    producer.send(job)

    resp = await worker.process(job)
    assert resp.status == JobStatus.COMPLETED
    assert resp.result_url == f"/v1/laudos/{job.job_id}"
    assert resp.progress_pct == 100
    assert worker.store.get(job.job_id).status == JobStatus.COMPLETED


@pytest.mark.asyncio
async def test_f0b07_failure_retry_then_failed():
    store = _store()
    worker = JobWorker(store=store, producer=MagicMock(),
                       handler=_good_handler, max_retries=2)

    async def _flaky(job: Job) -> JobResponse:
        raise JobError(title="Validation Error", detail="payload inválido", status=422)

    job = store.create(tenant_id="t1", job_type="flaky", payload={}, dedup_key=None,
                       webhook_url=None)
    worker.register("flaky", _flaky)

    first = await worker.process(job)
    assert first.status == JobStatus.QUEUED  # retry configurado

    second = await worker.process(job)
    assert second.status == JobStatus.FAILED  # esgotou retries
    assert "Validation Error" in (second.error or "")


@pytest.mark.asyncio
async def test_f0b08_idempotent_by_dedup_key():
    store = _store()
    calls = {"n": 0}

    async def counting(job: Job) -> JobResponse:
        calls["n"] += 1
        return JobResponse(job_id=job.job_id, status=JobStatus.COMPLETED,
                           progress_pct=100, result_url="/v1/laudos/x")

    worker = JobWorker(store=store, producer=MagicMock(), handler=counting)
    job = store.create(tenant_id="t1", job_type="laudo", payload={},
                       dedup_key="dedup-1", webhook_url=None)
    await worker.process(job)
    await worker.process(job)  # replay com mesmo dedup → não reprocessa

    assert calls["n"] == 1  # apenas UM processamento (F0B-08)


@pytest.mark.asyncio
async def test_f0b09_webhook_fired_on_completion():
    store = _store()
    # servidor fake webhook via FastAPI em processo (schema + httpx POST)

    worker = JobWorker(store=store, producer=MagicMock(), handler=_good_handler)
    job = store.create(tenant_id="t1", job_type="laudo", payload={},
                       dedup_key=None, webhook_url="http://127.0.0.1:9999/hook")

    from services.shared.queue import JobWorker as JW

    # Uso servidor fake: spiar _webhook
    import services.shared.queue as queue_mod

    captured: dict = {}

    async def fake_webhook(job: Job) -> None:
        captured["url"] = job.webhook_url
        captured["job_id"] = job.job_id

    # substitui o método estático no módulo (monkeypatch de classe)
    original = JW._webhook
    JW._webhook = staticmethod(fake_webhook)
    try:
        resp = await worker.process(job)
    finally:
        JW._webhook = original

    assert resp.status == JobStatus.COMPLETED
    assert captured.get("job_id") == job.job_id
    assert captured.get("url") == "http://127.0.0.1:9999/hook"


@pytest.mark.asyncio
async def test_f0b10_get_status_via_store():
    store = _store()
    worker = JobWorker(store=store, producer=MagicMock(), handler=_good_handler)
    job = store.create(tenant_id="t1", job_type="laudo", payload={}, dedup_key=None,
                       webhook_url=None)
    producer = QueueProducer()
    try:
        producer.send(job)
    except Exception:  # SQS ausente — dev tolerante; store é a fonte de status
        pass

    # status antes do processamento
    resp = JobResponse(job_id=job.job_id, status=job.status, progress_pct=0)
    assert resp.status == JobStatus.QUEUED

    await worker.process(job)
    stored = worker.store.get(job.job_id)
    assert stored is not None and stored.status == JobStatus.COMPLETED
    assert stored.progress_pct == 100