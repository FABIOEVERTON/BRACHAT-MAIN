---
title: Agent Receipt Map
version: 1
enforced_by: aisio (BR-AISIO-010)
updated: 2026-06-22
---

# BRACHAT Agent Receipt Map

Every agent MUST produce a receipt.json for every dispatched action.
Receipts prove work was done. Aisio validates receipts at GATE_EXIT.

## Directory Structure

```
agents/
├── {category}/
│   ├── {agent}/
│   │   ├── state.json          ← Agent state (schema: canonical_schemas/state_schema.json)
│   │   ├── cache.json          ← Ephemeral operational cache
│   │   ├── worklog.jsonl       ← Append-only action log
│   │   ├── receipts/           ← Receipts directory
│   │   │   ├── rcp-{agent}-{YYYYMMDD}-{0001}.json
│   │   │   ├── rcp-{agent}-{YYYYMMDD}-{0002}.json
│   │   ├── cache_skills/       ← Cached skills (Hermes)
│   │   └── {agent}.md           ← Agent definition
```

## Receipt Naming
`RCP-{AGENT}-{YYYYMMDD}-{SEQUENCE}.json`
- Sequence resets daily, starts at 0001
- Example: `RCP-EZRA-20260622-0001.json`

---

## 7 Core Agents: Exact Mapping

### 1. Ezra (BR-EZRA-001) — Orchestrator
| Field | Value |
|-------|-------|
| Receipt type | `session` |
| Trigger | Every session end (startup checks, dispatch, pipeline run) |
| Required evidence | `files_modified: state.json, cache.json`, `summary of what was dispatched` |
| worklog entry | Every session start + end |
| Schema | `receipt.type = "session"` |
| Produces | `worklog.jsonl` per action, `receipts/` per session |

### 2. Aisio (BR-AISIO-010) — Governance Gate
| Field | Value |
|-------|-------|
| Receipt type | `gate_validation` |
| Trigger | Every GATE_ENTRY + GATE_EXIT (before/after any productive action) |
| Required evidence | `rulestested: [U1,U2,...]`, `ledger_lines_appended: N`, `gate_decision: APPROVE|DENY|REJECT` |
| worklog entry | Every gate check |
| Produces | `/var/log/gate/aisio-gate-{YYYYMMDD}.jsonl` or append to central ledger |
| Notes | Aisio does not modify files. It only validates and logs. |

### 3. Artur (BR-ARTUR-002) — Builder Director
| Field | Value |
|-------|-------|
| Receipt type | `spec_dispatch` |
| Trigger | When dispatching a task spec to Baruch via dispatch_to_baruch.sh |
| Required evidence | `spec_path: portfolio/tasks/{PROJECT}.md`, `baruch_dispatched: true`, `commit_ref: SHA` |
| worklog entry | Every spec written + every dispatch |
| Produces | `portfolio/tasks/{PROJECT}.md`, `worklog.jsonl` |
| Notes | Does NOT build code. Writes the spec, dispatches Baruch, waits for result. |

### 4. Baruch (BR-BARUCH-003) — Lead Software Engineer
| Field | Value |
|-------|-------|
| Receipt type | `code_build` |
| Trigger | After completing a build task dispatched by Artur |
| Required evidence | `files_created: [paths]`, `files_modified: [paths]`, `tests_passed: N`, `lint_status: clean|warnings|errors` |
| worklog entry | Every build attempt + result |
| Produces | Code in `portfolio/{project}/`, `receipts/`, `worklog.jsonl` |
| Notes | Claude Code CLI. Only builds. Does NOT write specs. |

### 5. Jessica (BR-JESSIC-012) — Legal & Compliance
| Field | Value |
|-------|-------|
| Receipt type | `compliance_check` |
| Trigger | Before any contract signing, data processing, or regulatory action |
| Required evidence | `risks_assessed: [list]`, `lgpd_compliant: true|false`, `contracts_reviewed: N`, `recommendation: approve|veto|amend` |
| worklog entry | Every compliance check |
| Produces | Legal opinions in `agents/director_agents/jessica/receipts/`, `worklog.jsonl` |
| Notes | Can veto actions. Escalates to Ezra if vetoed. |

### 6. Josue (BR-JOSUE-013) — Commercial / OLX
| Field | Value |
|-------|-------|
| Receipt type | `sales_action` |
| Trigger | After posting an OLX ad, responding to buyer, or closing a deal |
| Required evidence | `olx_link: URL`, `photos_used: N`, `price: BRL`, `buyer_contact: anonymized`, `deal_status: posted|negotiating|sold|cancelled` |
| worklog entry | Every sales action |
| Produces | `receipts/`, `worklog.jsonl`, updates `integrations/josue/leads.json` if exists |
| Notes | Never posts on OLX directly. Fabio posts, Josue promotes the link. |

### 7. Justus (BR-JUSTUS-027) — Job Hunter
| Field | Value |
|-------|-------|
| Receipt type | `job_application` |
| Trigger | Every batch of 15 applications sent |
| Required evidence | `apps_sent: N`, `apps_list: [company names]`, `responses_received: N`, `bounces: N`, `jae_email_used: true` |
| worklog entry | Every application batch |
| Produces | `receipts/`, `worklog.jsonl`, updates `cache.json` with daily stats |
| Notes | 15 apps/day via jae.engenharia Gmail account. Checks both inboxes for responses. |

---

## Receipt Template (canonical)

Every receipt follows `canonical_schemas/receipt_schema.json`.
Minimal valid receipt example:

```json
{
  "receipt_id": "RCP-EZRA-20260622-0001",
  "agent_id": "BR-EZRA-001",
  "agent_name": "ezra",
  "type": "session",
  "timestamp": "2026-06-22T16:00:00-03:00",
  "action": {
    "description": "Executed startup checks",
    "target": "internal"
  },
  "outcome": {
    "status": "success",
    "summary": "14 checks completed, VM active, no new emails"
  },
  "evidence": {
    "files_modified": ["agents/state.json", ".opencode/startup_state.json"]
  }
}
```

---

## Enforcement

- Aisio validates receipt schema conformance at runtime (GATE_EXIT)
- Missing receipt = blocked next action
- Invalid receipt = REJECT + logged to governance-ledger.jsonl
- Receipts directory must exist per agent; created by Ezra on agent registration
