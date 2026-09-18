---
status: accepted
date: 2026-09-17
deciders: Tony Stark, Maria Hill (SLA), Nick Fury
---

# ADR-004 — Pipeline de Compilação do Laudo com Celery + ReportLab

## Contexto

PRD Épico 3 (SLO p90 < 10 s) + custo de entrada. Compilar PDF de 20 páginas white-label + hashing + gravação WORM em sincronia travaria a API e quebraria o SLA.

## Opções

1. **Síncrono na API** — simples; p95 > 10 s com PDF + WORM; degrada CRUD e viola PERF-1.
2. **Filas com 3 workers especializados (discovery / reportlab / hasher) + idempotência por protocolo** — assíncrono, 202 Accepted, SSE/poll de status; workers escalam por fila.
3. **Função serverless por etapa** — bom isolamento; complexidade de estado distribuído e custo por invocação no volume do MVP.

## Decisão

**Adotar opção 2**: `POST /compile` valida cota/token e enfileira job com `task_id`; worker `hasher` gera `validation_manifest.json` (SHA-256 das evidências); worker `reportlab` compila o PDF; gravação WORM com ETag; retries até 5 com chave de idempotência (protocolo) e DLQ após falhas.

## Consequências

- (+) SLA p90 < 10 s alcançável; API permanece responsiva; workers autoscalam por profundidade de fila (COST-2).
- (+) Falha de rede no upload WORM não duplica registros (idempotência por protocolo).
- (−) Mais peças móveis: Redis broker, observabilidade por `X-Trace-Id` entre API→worker.
- (−) Estado intermediário exige `status` rastreável (IN_PROGRESS/SUBMITTED/CERTIFIED/REJECTED) e UI de progresso.