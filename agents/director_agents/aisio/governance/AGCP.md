# AGCP — AI Governance Control Plane (v1.0.0)

## 6 Core Principles
1. **Append-Only Ledger** — stage results imutáveis, só append
2. **Per-Action Total Ordering** — sequence values estritamente crescentes
3. **Deterministic Lifecycle Derivation** — estado derivado do ledger, nunca de mutable status
4. **Execution-Bound Authorization** — elegibilidade re-derivada no commit time contra canonical state
5. **Structural Invariant Separation** — control-plane opera independente de tenant policy
6. **Multitenant Isolation** — resolução de artefatos e acesso a ledger estruturalmente isolados

## Action Lifecycle (5 states)
```
SUBMITTED → AUTHORIZED / REJECTED / PENDING_HITL → EXECUTED
```
- SUBMITTED: ação recebida, início da validação
- AUTHORIZED: todas as validações passaram
- REJECTED: alguma validação falhou (hard fail)
- PENDING_HITL: aguardando aprovação humana ou cosign
- EXECUTED: ação confirmada como executada (terminal)
- TERMINAL: EXECUTED ou REJECTED — não aceitam transições

## Conformance Levels (L1-L5, cumulative)
| Level | Exige | O que valida |
|-------|-------|-------------|
| L1 | Schema & envelope | JSON schema, campos obrigatórios, endpoint `/meta` |
| L2 | Ordered validation pipeline | Ordem fixa: schema → signature → tenant → policy → constraints → invariants → HITL → decision → ledger |
| L3 | Deterministic governance | PEC contract, replay validation, hard invariant rejection |
| L4 | HITL & execution gating | Cosign tokens, quorum, ledger authorization antes de executar |
| L5 | Multitenant isolation | Namespace isolation, cross-tenant rejection |

## 8 Normative Assertions (A-XXXXX)
| ID | Descrição |
|----|-----------|
| A-ORDERING | Evaluation ordering determinístico |
| A-DERIVATION | Estado derivado do ledger, não de mutable fields |
| A-STATE-NO-SUBMITTED | SUBMITTED não observável externamente |
| A-COMMIT-GATING | Commit requer AUTHORIZED + ledger ref match |
| A-COSIGN-GATING | Cosign válido só em PENDING_HITL |
| A-TENANT-ACTIVE-GATING | Tenant ACTIVE requerido para submit/commit |
| A-IDEMPOTENCY-NO-MUTATION | Idempotency conflict não faz mutação |
| A-TERMINAL-NO-TRANSITION | Terminal states rejeitam transições |

## 23 Requirements (REQ-XXXXX)
Submit flow: REQ-SUBMIT-ACCEPT-AUTH, REQ-SUBMIT-HITL-PENDING, REQ-SUBMIT-INVARIANT-HARD-FAIL, REQ-SUBMIT-POLICY-NOT-FOUND, REQ-SUBMIT-PROV-FAIL, REQ-SUBMIT-SCHEMA-FAIL, REQ-SUBMIT-TENANT-INACTIVE
Commit flow: REQ-COMMIT-APPENDS-COMMITTED, REQ-COMMIT-AUTH-REF-MATCH, REQ-COMMIT-ONLY-AUTHORIZED, REQ-COMMIT-REPLAY-REJECT, REQ-COMMIT-TENANT-INACTIVE
Cosign: REQ-COSIGN-ONLY-PENDING, REQ-COSIGN-QUORUM-AUTH, REQ-COSIGN-VALIDITY
State: REQ-STATE-DERIVED-FROM-LEDGER, REQ-STATE-NO-SUBMITTED
Ledger: REQ-LEDGER-ORDERING
Idempotency: REQ-IDEMPOTENCY-CONFLICT, REQ-IDEMPOTENCY-REPLAY
Cross-tenant: REQ-CROSS-TENANT-PROFILE
Get: REQ-GET-NOT-FOUND, REQ-GET-NOT-READY-NO-SUBMITTED

## 9 Assertion Domains
SCHEMA, SECURITY, PEC, HITL, EXECUTION, MULTITENANT, REGISTRY, LEDGER, VERSIONING

## 7 Constraint Types
core.require_signature, core.require_role, core.max_ttl, core.require_approval, core.require_logging, core.require_evidence, core.require_policy_module

## 6 Invariant Types
core.no_cross_tenant_artifact_resolution, core.deterministic_pec_outputs, core.no_mutable_state_before_commit, core.ledger_append_only, core.replay_identical, core.tenant_active_required

## 20 Rejection Codes
SCHEMA_INVALID, SCHEMA_MISSING_FIELD, SIGNATURE_MISSING, SIGNATURE_INVALID, TENANT_INACTIVE, TENANT_NOT_FOUND, POLICY_NOT_FOUND, POLICY_VIOLATION, CONSTRAINT_VIOLATION, INVARIANT_VIOLATION, HITL_REQUIRED, EXECUTION_UNAUTHORIZED, EXECUTION_COMMITTED, REPLAY_DETECTED, IDEMPOTENCY_CONFLICT, CROSS_TENANT_DENIED, LEDGER_CONFLICT, NOT_READY, NOT_FOUND, INTERNAL_ERROR
