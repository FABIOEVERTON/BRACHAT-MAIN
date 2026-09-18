---
epic_id: 05-billing-quotas
status: ready-for-dev
owner: Tony Stark + Maria Hill
linked_prd: ÉPICO 5
trigger_map_row: 1
priority: 5
estimate: M
---

# Epic 05: Faturamento Recorrente e Gestão de Cotas

## Outcome

Super Admin tem limites de plano fiscalizados automaticamente, com soft-block, grace period e upgrade pro-rata sem interrupção de serviços essenciais.

## Stories
- E05-S01: Enforcement de cotas + soft-block com modal de upgrade (AC-05-1) — R-8
- E05-S02: Upgrade pro-rata via webhook idempotente (AC-05-3) — R-8
- E05-S03: Grace period 7d + retenção integral de laudos (AC-05-2) — R-8

## Dependencies
- Stripe / Pagar.me + webhooks idempotentes
- `Tenants.status` e billing configurados

## Success
Nenhuma duplicidade financeira/pericial em retries; laudos permanecem acessíveis.