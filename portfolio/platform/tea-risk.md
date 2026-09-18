---
gate: risk
owner: Hawkeye
created: 2026-09-17
architecture_ref: architecture.md
status: complete
policy: enforcing
---

# TEA — Risk Profile (EZRA AI Governance Platform)

Gate **risk** — executado uma vez, após a assinatura da arquitetura (Tony, ADR-001..004). Cada hotspot tem: **probabilidade × impacto → score**, contrato de mitigação e vetor de teste (insumo para o gate `design`).

Escala: L=1, M=2, H=3. Score = prob × impacto (máx 9). Threshold: **score ≥ 6 = hotspot crítico** (mitigação obrigatória antes do gate da story).

## Matriz de risco

| ID | Hotspot | Cenário | Prob | Impacto | Score | Contrato de mitigação | Vetor de teste |
|---|---|---|---|---|---|---|---|
| R-1 | Isolamento multi-tenant (ADR-001) | Query sem `tenant_id` ou RLS desabilitado vaza dados entre bancas | M | H | **6** | RLS `FORCE` em 100% das tabelas + filtro explícito no SQLAlchemy + teste automatizado de tentativa cross-tenant | Integração: JWT do tenant A tenta ler recurso do tenant B → `0 rows` + HTTP 404. Migração Alembic CI: falha se tabela sem RLS |
| R-2 | Bypass do gate de compliance | UI/API decide conformidade em vez de `libs/compliance`, liberando laudo positivo com gap crítico | M | H | **6** | `libs/compliance` é a única fonte do gate; UI/API nunca calculam status `CERTIFIED` | Unit: 122 controles em `libs/compliance`; Integração: ALTO RISCO sem Art. 19/21 → `CERTIFIED` bloqueado |
| R-3 | MCP sem ledger (ADR-003) | Agente executa ferramenta sensível sem aprovação humana registrada | M | H | **6** | Gateway deny-by-default + HITL + `Decision Ledger` obrigatório; `execute_wire_transfer > R$5k` sempre retém | Integração: chamada > R$5k → estado RETIDO + linha no Decision Ledger + notificação |
| R-4 | Falha/duplicidade na custódia WORM (ADR-002/004) | Retry gera 2 registros periciais ou gravação WORM inconsistente | M | H | **6** | Idempotência por `protocol_code` + ETag confirmado antes de status CONCLUÍDO | Integração: falha simulada no upload → 5 retries, 1 único manifesto, sem duplicidade financeira |
| R-5 | Vazamento de PII fora do BR (SEC-2) | Telemetria/logs/backup com PII em região não-BR | L | H | **3** | PII nunca deixa a região; sanitização em logs; buckets/backup OCI BR criptografados | Config test: scan de destino de logs/backup = OCI BR; grep de PII em payload de observabilidade |
| R-6 | Compilação do laudo estoura SLA (PERF-2) | PDF 20 pág + hash + WORM > 10 s p90 sob carga | M | M | **4** | Workers dedicados + autoscaling por fila; budget por etapa instrumentado | Load: 50 compilações concorrentes → p90 < 10 s (relatório OTel) |
| R-7 | Auth/sessão (SEC-1/3) | Reuso de refresh token ou MFA contornado concede escopo elevado | L | H | **3** | Refresh rotativo com invalidação por reuso; `mfa:pending` sem escopo elevado | Segurança: replay de refresh → negado; acesso admin sem TOTP → 403 |
| R-8 | Webhook de pagamento (Épico 5) | Webhook duplicado/forjado altera cota indevidamente | M | M | **4** | Verificação de assinatura + idempotência por evento; mudança de cota só via evento válido | Integração: webhook duplicado → efeito idempotente; assinatura inválida → 401 sem mudança |
| R-9 | Shadow AI falso-negativo (Épico 2) | Ativo não autorizado não detectado, gerando laudo "limpo" incorreto | M | H | **6** | Varredura de descoberta com cobertura documentada; laudo registra escopo e limitações da varredura | Integração: ativo injetado fora do inventário → detectado + flag `is_shadow_ai` |
| R-10 | Integridade do hash/manifesto | Manifesto divergente do PDF entregue (adulteração pós-seal) | L | H | **3** | `master_hash` = SHA-256(manifesto); verificação pública por QR contra WORM | Integração: alterar PDF pós-seal → verificação pública falha |

## Hotspots críticos (score ≥ 6)

R-1, R-2, R-3, R-4, R-9 → **mitigação e teste obrigatórios** antes do gate da story correspondente. Qualquer story que toque um destes: gate `review` confirma o contrato (seção 3 do `wize-tea-review`).

## Política de gate

- `policy = enforcing` — justificado pelo PRD §1.4 (gate strategy validada): ALTO RISCO sem viés/supervisão humana **bloqueia** `CERTIFIED`.
- Gate FAIL bloqueia merge. WAIVED requer Wizer + razão registrada.

## Hand-off

> Risk profile em `tea-risk.md`. 5 hotspots críticos com contrato de mitigação. Tony, siga com os epics/stories; Shuri, queue up — cada story carrega o vetor de teste do seu `R-x`.