# BUILDER — Fábrica de Software BRACHÁT

Raiz operacional de todos os projetos autônomos.
Scripts, daemons e cloud vivem aqui.

## Scripts
- `clickup_daemon.py` — sincronização com ClickUp (CRUD tasks)

## Daemons (launchd macOS)
Rodam no Mac enquanto estiver ligado:
- `com.brachat.opencode.plist` → bridge EZRA (Telegram → Zen API)
- `com.brachat.nice.plist` → bridge NICE (Telegram → Zen API)

## Cloud (VPS — 24/7)
Os bridges também podem rodar num VPS (Hetzner €4/mês):
→ `cloud/README.md` contém instruções completas de deploy.
