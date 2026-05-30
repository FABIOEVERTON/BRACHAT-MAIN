## Daily Diagnostic Report — Agent & Inference Provider Integration

**Date:** `[DATE]` | **Framework Version:** `[VERSION]` | **Platform:** `[OS / RUNTIME]`
**Reported by:** `[NAME / TEAM]` | **Session ID:** `[SESSION_ID]`

---

### Summary

> One-line description of the overall status at the end of the session.
> Example: *"Provider integration completed. Agent operational. 2 issues pending."*

---

### Issues Found & Resolved

| # | Issue | Root Cause | Resolution | Status |
|---|---|---|---|---|
| 1 | `[ISSUE_TITLE]` | `[ROOT_CAUSE]` | `[FIX_APPLIED]` | ✅ Resolved |
| 2 | `[ISSUE_TITLE]` | `[ROOT_CAUSE]` | `[FIX_APPLIED]` | ✅ Resolved |
| 3 | `[ISSUE_TITLE]` | `[ROOT_CAUSE]` | `[FIX_APPLIED]` | ⚠️ Workaround |
| 4 | `[ISSUE_TITLE]` | `[ROOT_CAUSE]` | `[FIX_APPLIED]` | ❌ Pending |

---

### Error Log Digest

```
[TIMESTAMP] [SEVERITY] [COMPONENT]: [ERROR_MESSAGE]
[TIMESTAMP] [SEVERITY] [COMPONENT]: [ERROR_MESSAGE]
```

**Errors classified:**

| Code | Type | Component | Retryable | Resolution |
|---|---|---|---|---|
| `[HTTP_CODE]` | `[TYPE]` | `[COMPONENT]` | `[YES/NO]` | `[ACTION]` |

---

### Configuration State

| Item | Previous Value | Current Value |
|---|---|---|
| Provider | `[OLD]` | `[NEW]` |
| Base URL | `[OLD]` | `[NEW]` |
| Model | `[OLD]` | `[NEW]` |
| Auth Variable | `[OLD]` | `[NEW]` |
| Config File | `[OLD]` | `[NEW]` |

---

### Final Working Configuration

```yaml
# [FRAMEWORK] — [CONFIG_FILE_PATH]
[KEY]: [VALUE]
[KEY]: [VALUE]
[KEY]: [VALUE]
```

---

### Environment

| Item | Value |
|---|---|
| OS | `[OS]` |
| Runtime | `[LANGUAGE / VERSION]` |
| Package Manager | `[TOOL / VERSION]` |
| Install Mode | `[EDITABLE / WHEEL / DOCKER]` |
| Process Mode | `[FOREGROUND / BACKGROUND / SYSTEMD]` |
| Cost / Plan | `[FREE / PAID / TIER]` |

---

### Known Limitations & Risks

- `[LIMITATION_1]` — `[IMPACT]` — `[WORKAROUND IF ANY]`
- `[LIMITATION_2]` — `[IMPACT]` — `[WORKAROUND IF ANY]`
- `[LIMITATION_3]` — `[IMPACT]` — `[WORKAROUND IF ANY]`

---

### Pending Items

| # | Item | Owner | Priority | Target Date |
|---|---|---|---|---|
| 1 | `[TASK]` | `[NAME]` | `[HIGH/MED/LOW]` | `[DATE]` |
| 2 | `[TASK]` | `[NAME]` | `[HIGH/MED/LOW]` | `[DATE]` |

---

### Next Session Checklist

- [ ] `[VERIFY_ITEM_1]`
- [ ] `[VERIFY_ITEM_2]`
- [ ] `[VERIFY_ITEM_3]`
- [ ] `[VERIFY_ITEM_4]`

---

### Evidence

| Claim | Source Type | Location |
|---|---|---|
| `[CLAIM]` | `[LOGS / DOCS / SOURCE_CODE / INFERENCE]` | `[FILE / URL / LINE]` |
| `[CLAIM]` | `[LOGS / DOCS / SOURCE_CODE / INFERENCE]` | `[FILE / URL / LINE]` |