# SPEC - Ezra OS on OCI (Telegram control, Mac off)

**Date:** 2026-07-31 | **Status:** PENDING APPROVAL (Fabio) | **Routed by:** S12 deployment
**Cost:** R$0 (Oracle Always Free)

---

## 1. Goal / End state

After this delivery, Ezra OS runs 24/7 on OCI and is controlled by Fabio **via Telegram**, with the Mac off. The LLM (opencode/big-pickle via Zen) stays in the cloud - OCI only orchestrates (client). No public port besides SSH.

## 2. Topology (real tenancy)

| Instance | OS | Role |
|---|---|---|
| `ezra_bot_2` (22.04 Minimal) | Ubuntu 22.04 | **PROD** - opencode serve + bridge + mem0 MCP |
| `ezra_bot_2` (20.04) | Ubuntu 20.04 | **STANDBY** - stopped (avoids idle reclaim; reactivatable on failover) |

- Shape: 2x `VM.Standard.E2.1.Micro` (1 OCPU with 1/8, **1 GB RAM** each), VCN `ezra_VCN`, AD-1, region sa-saopaulo-1.
- **1 GB RAM is the bottleneck** - 1 GB swap on boot volume (47-50 GB available).

## 3. Flow architecture

```
Telegram (app) <-> Bot API (cloud)
               <-> long-polling (outbound, HTTPS 443)
bridge (PROD VM, Node) <-> opencode serve (PROD VM, 127.0.0.1:8080)
                         <-> Ezra brain: skills, plugins, state.json, mem0 MCP
```

- The bridge **pulls** messages from Telegram (outbound) and talks to serve via localhost. **No inbound port** besides SSH (22) needed.
- `opencode serve` runs with the project `opencode.json` + `.opencode/plugin/` (same plugin runtime) - **not** `--pure`.

## 4. Components

### 4.1 opencode serve (PROD)
- Install Node 22 + opencode (version aligned with local: 1.18.5) on the VM.
- `opencode serve --port 8080 --hostname 127.0.0.1 --log-level INFO`.
- Global config on VM (`~/.config/opencode/opencode.jsonc`): model `opencode/big-pickle`, provider API key, MCP mem0. Secrets via env (Section 6).

### 4.2 Telegram bridge (`ezra-bridge`)
Single Node script, zero dependencies besides Node (uses `globalThis.fetch`), long-polling on `getUpdates`.

Serve API consumed (validated against the SDK - real paths):
- `POST /session` - create session per `chat_id`
- `POST /session/{id}/message` with `parts: [{type:"text",text}]` - returns `{ info, parts }` (blocking until done)
- `POST /session/{id}/abort` - `/abort` command
- `GET /session/{id}` - status (busy/idle) for `/status`

Bridge rules:
- 1 session per `chat_id` (persistent map `chats.json`), continuous history.
- Concurrency: per-chat queue (1 request at a time; new turns wait for current to finish).
- Rate limit: ignore duplicate messages (`update_id`), minimum interval between commands.
- Commands: `/start`, `/status`, `/abort`, `/reset` (new session), `/resumo`.
- Response: extracts `parts` of type `text`; if empty, sends "done".
- Network failures: retry with backoff; log in `bridge.log`.

### 4.3 mem0 MCP (PROD)
- Python + `mem0-mcp-server` on the VM (like on Mac). Key in env.

### 4.4 systemd (PROD)
- `ezra-serve.service` - `ExecStart` of serve; `Restart=on-failure`, `RestartSec=5`.
- `ezra-bridge.service` - bridge; `After=ezra-serve.service`; `Restart=always`.
- `ezra-synth.service` - synthetic load (Section 8), active.

## 5. Brain sync (recommendation: private git remote)

**Best solution:** private **GitHub repo** for `brachat-main`.

| Item | Destination |
|---|---|
| Code (skills, plugins, instructions, opencode.json, mcp) | private git repo - clone on VM |
| Runtime data (`state.json`, `governance-ledger.jsonl`, `proposals/`, mem0) | VM volume only; **excluded from repo** (`.gitignore`) |
| Secrets | systemd env (never in repo) |

- Deploy = `git pull` + `systemctl restart ezra-serve`.
- Rollback = `git checkout <tag>` + restart.
- Alternative (rsync/scp) discarded: no history, no clean rollback, no diff tracking.

## 6. Secrets (systemd env, never in repo)

- `TELEGRAM_BOT_TOKEN` (already exists in BotFather)
- `MEM0_API_KEY`
- Model provider API key (Zen/custom-proxy)

## 7. Security

- Firewall (security list / UFW): allow only 22 (SSH) from my network; 8080 localhost only.
- SSH key auth; `PasswordAuthentication no`; no root.
- Bridge and serve run as dedicated user (`ezra`), not root.
- `opencode serve` bound to 127.0.0.1 - not exposed to the internet.
- fail2ban (SSH) recommended, optional.

## 8. Anti-reclaim + health check

Oracle reclaims Always Free instances with <20% usage for 7 days. Mitigations:
- `ezra-synth.service`: light periodic synthetic load (CPU ~5-15% for ~2 min every 30 min) + HTTP health check of serve.
- Health check: `curl localhost:8080/app` (or serve endpoint) every 5 min; failure - alert via Telegram (bridge's own message).

## 9. Backup / Rollback

- Code: git (tags per deploy).
- State: nightly `tar` of `.opencode/state.json`, ledger and mem0 - to Object Storage (20 GB free) via OCI CLI.
- Pre-deploy: copy `state.json` to `state.pre-<deploy>.bak` on volume.
- Automated rollback if health check fails within first 5 min after deploy (skill S12).

## 10. Risks and limitations

| Risk | Mitigation |
|---|---|
| 1 GB RAM insufficient | 1 GB swap; monitor `free`; if exhausted, move mem0 to standby instance |
| Idle reclaim | Synthetic load (Section 8) |
| Telegram latency | Acceptable for interactive use; bridge is long-polling |
| Response too long for Telegram | Truncate + `...` + `/resumo` command for the rest |
| Ezra plugins unproven at runtime | Sentinel validation ON THE VM before trusting (skill gate) |
| Mac off = no access to Mac files | Ezra acts only on OCI; repo is the code transport |

## 11. Execution phases (after approval)

1. **F1 Pre**: create private GitHub repo; `.gitignore` (state/ledger/proposals/mem0/secrets); push brachat-main.
2. **F2 PROD VM**: attach public IP (ephemeral), SSH, hardening (key, UFW), 1 GB swap, install Node 22 + opencode.
3. **F3 Config**: `~/.config/opencode/opencode.jsonc` with model + mem0; secrets in systemd env.
4. **F4 Code**: clone repo to `/home/ezra/brachat-main`; `opencode serve` running.
5. **F5 Bridge**: write `ezra-bridge`; systemd; manual test: Fabio sends msg on Telegram - response.
6. **F6 Sentinel + gate**: validate plugin loading on VM (boot mark); enable `skill-gate` there.
7. **F7 Anti-reclaim + backup**: `ezra-synth`, health check, nightly tar - to Object Storage.
8. **F8 Final validation (S12 checklist)**: pre-deploy backup ok, health check ok, rollback tested ok, version tagged ok.

## 12. Validation checklist (S12)

- [ ] Backup of previous state created before each deploy?
- [ ] Health check passed after deploy?
- [ ] Rollback restored state without loss?
- [ ] Version incremented/tagged?
- [ ] Plugins proven at runtime (sentinel) on the VM?
- [ ] Telegram responds from scratch with the Mac off?
