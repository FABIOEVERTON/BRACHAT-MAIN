---
epic_id: 03-custody-seal-report
status: ready-for-dev
owner: Tony Stark + Maria Hill
linked_prd: ÉPICO 3
trigger_map_row: 4
priority: 3
estimate: L
---

# Epic 03: Cadeia de Custódia SHA-256 e Laudo 1-Clique

## Outcome

Auditor clica "Compilar Laudo Pericial" e recebe PDF de 20 páginas white-label com hash SHA-256 selado no cofre WORM, verificável por QR code.

## Stories
- E03-S01: Compilação do laudo ReportLab 20p white-label (AC-03-1) — R-6
- E03-S02: Hasher + validation_manifest + selo WORM idempotente (AC-03-3) — R-4, R-10
- E03-S03: Página pública de validação por QR code (AC-03-2) — R-10

## Dependencies
- ADR-002 (WORM) + ADR-004 (pipeline Celery) implementados
- Cores/logo do tenant (Epic 01) disponíveis

## Success
p90 de compilação < 10 s; verificação pública stateless retorna autenticidade + hash.