# BRACHÁT CLOUD — Bridges 24/7

Only the Telegram bridges go to the cloud. The rest of the system stays on the Mac.

## What goes

| Script | What it does | Wakes when |
|--------|-------------|------------|
| `bridge-ezra.py` | Listens to Telegram @Baruch_Everton_bot, responds via Zen API | Message in chat |
| `bridge-nice.py` | Listens to Telegram @luevertonbot, responds via Zen API | Message in chat |

## What does NOT go (stays on Mac)

- OpenCode CLI — only makes sense with you using it
- Your files and agents (`state.json`, `daily/*`, `AGENT.md`, etc.)
- `cloud/daemons/` (launchd)

## How to deploy

### 1. Create a VPS (Hetzner, DigitalOcean, etc.)

- Hetzner CX22: €4/month
- DigitalOcean Basic: $6/month
- Ubuntu 22.04 or 24.04

### 2. Send the files

```bash
scp -r /Users/mac/brachat-main/builder/cloud user@YOUR_IP:~
```

### 3. Enter the VPS and install

```bash
ssh user@YOUR_IP
cd ~/cloud
cp .env.example .env
nano .env              # paste tokens
sudo bash deploy.sh
```

### 4. Done

```bash
systemctl status brachat-ezra
systemctl status brachat-nice
```

Now the bots respond 24/7 — the Mac can hibernate, restart, shut down.

## How to switch back to Mac

```bash
# On VPS
sudo systemctl stop brachat-ezra brachat-nice
sudo systemctl disable brachat-ezra brachat-nice
```

The local bridges on Mac (launchd) remain configured as well.
