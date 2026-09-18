---
status: accepted
date: 2026-09-17
deciders: Tony Stark, Nick Fury
---

# ADR-002 — Cadeia de Custódia Imutável via OCI Object Storage WORM

## Contexto

PRD Épico 3: laudo pericial com selo SHA-256 válido para instruir processos (Arts. 464+ CPC). O documento precisa resistir a contestação de integridade e manipulação posterior.

## Opções

1. **Armazenar PDF + manifesto apenas no PostgreSQL** — simples; porém edição/restauração de backup pode alterar evidência sem rastro.
2. **OCI Object Storage com WORM Lock (5 anos)** + gravação pré-entrega — imutabilidade objetiva no storage; ETag como prova física de gravação.
3. **Blockchain externo** — caro, fora de soberania e sem ganho pericial no CPC para o MVP.

## Decisão

**Adotar opção 2**: gravar `validation_manifest.json` + PDF no cofre WORM da OCI **antes** de disponibilizar download; `master_hash_sha256` = SHA-256 do manifesto fica em `Forensic_Manifests`; integridade verificável via página pública (QR code).

## Consequências

- (+) Prova de imutabilidade forte, auditável e econômica; retenção de 5 anos padrão pericial.
- (+) Verificação pública stateless por hash — sem expor dados do tenant.
- (−) Escrita no WORM é final — exige pipeline de validação completo antes do seal (idempotência obrigatória, ver ADR-004).
- (−) Custo de retenção cresce com volume de laudos — monitorar via métrica de custo por tenant (COST-1).