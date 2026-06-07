# NUVEM BRACHÁT — Bridges 24/7

Só os bridges do Telegram vão pra nuvem. O resto do sistema fica no Mac.

## O que vai

| Script | O que faz | Acorda quando |
|---|---|---|
| `bridge-ezra.py` | Escuta Telegram @Baruch_Everton_bot, responde via Zen API | Mensagem no chat |
| `bridge-nice.py` | Escuta Telegram @luevertonbot, responde via Zen API | Mensagem no chat |

## O que NÃO vai (fica no Mac)

- OpenCode CLI — só faz sentido com você usando
- Seus arquivos e agentes (`state.json`, `daily/*`, `AGENT.md`, etc.)
- `cloud/daemons/` (launchd)

## Como subir

### 1. Cria um VPS (Hetzner, DigitalOcean, etc.)

- Hetzner CX22: €4/mês
- DigitalOcean Basic: $6/mês
- Ubuntu 22.04 ou 24.04

### 2. Envia os arquivos

```bash
scp -r /Users/mac/brachat-main/builder/cloud user@SEU_IP:~
```

### 3. Entra no VPS e instala

```bash
ssh user@SEU_IP
cd ~/cloud
cp .env.example .env
nano .env              # cola os tokens
sudo bash deploy.sh
```

### 4. Pronto

```bash
systemctl status brachat-ezra
systemctl status brachat-nice
```

Agora os bots respondem 24/7 — o Mac pode hibernar, reiniciar, desligar.

## Como voltar pro Mac

```bash
# No VPS
sudo systemctl stop brachat-ezra brachat-nice
sudo systemctl disable brachat-ezra brachat-nice
```

Os bridges locais no Mac (launchd) continuam configurados também.
