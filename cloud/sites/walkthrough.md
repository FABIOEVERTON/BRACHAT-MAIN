# WALKTHROUGH — Infraestrutura BRACHÁT em Nuvem

> Guia prático de implantação da Hetzner → Oracle, serviços, dashboard e manutenção.

---

## 1. HISTÓRICO DA MIGRAÇÃO

| Etapa | Data | Servidor | IP | Status |
|-------|------|----------|----|--------|
| Original | mar/2026 | Hetzner CX22 | 167.233.30.115 | 🪦 Morto |
| Atual | jun/2026 | Oracle Always Free | 147.15.18.252 | ✅ Ativo |

**Motivo**: Hetzner custava €4/mês, Oracle é free. Migração para 1 vCPU + 2GB RAM + 4GB swap.

---

## 2. INFRAESTRUTURA FÍSICA (ORACLE)

### 2.1. Instância

- **Shape**: `VM.Standard.E2.1.Micro` (AMD, 1 vCPU, 2 GB RAM, 50 GB SSD)
- **Swap**: 4 GB em `/swapfile` (6 GB memória virtual total)
- **OS**: Oracle Linux 9 (compat RHEL)

### 2.2. Firewall — Duas Camadas

#### Camada 1 — VM (firewalld)
```bash
sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --add-port=8765/tcp --permanent
sudo firewall-cmd --reload
```

#### Camada 2 — OCI Security List
**Console OCI > Networking > Virtual Cloud Networks > [VCN] > Security Lists > [Default] > Add Ingress Rules**
| Source | Protocol | Port | Description |
|--------|----------|------|-------------|
| 0.0.0.0/0 | TCP | 8080 | Dashboard HTTP |
| 0.0.0.0/0 | TCP | 8765 | Malha WebSocket |

> ✅ **Portas 8080 e 8765 liberadas** na Security List em 10/06/2026.

---

## 3. SERVIÇOS SYSTEMD

### 3.1. Lista de Serviços

| Serviço | Executa | Porta | Depende |
|---------|---------|-------|---------|
| `brachat-ezra` | `bridge-ezra.py` | — | Internet |
| `brachat-nice` | `bridge-nice.py` | — | Internet |
| `brachat-dashboard` | `dashboard.py` | 8080 | `index.html` |
| `brachat-malha` | `server.py` | 8765 | WebSocket |

### 3.2. Estrutura de Diretórios no VPS

```
/opt/brachat/
├── repo/                         ← git clone do brachat-main
│   └── cloud/dashboard/
│       ├── dashboard.py          ← HTTP (porta 8080)
│       ├── server.py             ← WebSocket (porta 8765)
│       └── index.html            ← Frontend do organograma
├── state/
│   ├── malha.json                ← Estado da bridge EZRA
│   └── nice.json                 ← Estado da bridge NICE
├── dashboard.py → repo/cloud/dashboard/dashboard.py
├── server.py    → repo/cloud/dashboard/server.py
├── index.html   → repo/cloud/dashboard/index.html
├── bridge-ezra.py → repo/cloud/sites/bridge-ezra.py
├── bridge-nice.py → repo/cloud/sites/bridge-nice.py
└── .env
```

### 3.3. Gerenciamento

```bash
# Ver status
sudo systemctl status brachat-ezra brachat-nice brachat-dashboard brachat-malha

# Logs
sudo journalctl -u brachat-ezra -n 20 --no-pager
sudo journalctl -u brachat-malha -n 20 --no-pager

# Restart (após deploy)
sudo systemctl restart brachat-dashboard brachat-malha

# Parar bridges (se Mac for assumir)
sudo systemctl stop brachat-ezra brachat-nice
sudo systemctl disable brachat-ezra brachat-nice
```

---

## 4. DEPLOY

### 4.1. Dashboards (server.py + index.html)

```bash
# Editar localmente em /Users/mac/brachat-main/cloud/dashboard/
scp -i /path/to/ssh-key server.py index.html dashboard.py \
  opc@147.15.18.252:/opt/brachat/repo/cloud/dashboard/

# Restart
ssh -i /path/to/ssh-key opc@147.15.18.252 \
  'sudo systemctl restart brachat-dashboard brachat-malha'
```

### 4.2. Bridges (ezra + nice)

```bash
scp -i /path/to/ssh-key cloud/sites/bridge-ezra.py cloud/sites/bridge-nice.py \
  opc@147.15.18.252:/opt/brachat/repo/cloud/sites/

# (symlinks apontam para repo/cloud/sites -- arquivos novos são pickados automaticamente)
sudo systemctl restart brachat-ezra brachat-nice
```

---

## 5. ESTRUTURA DE AGENTES (NO VPS)

```
/opt/brachat/repo/agents/
├── orchestrator_agent/           ← EZRA (estado, cache)
├── director_agents/              ← 5 diretores
│   ├── aisio/                    ← Governance + compliance
│   ├── nice/                     ← Casa + finanças
│   ├── josue/                    ← Operações
│   ├── gilmario/                 ← Ensino + branding
│   └── jessica/                  ← Jurídico
├── builder_agents/               ← 2 builders
│   ├── architect/                ← Planejamento
│   └── artur/                    ← Implementação
├── studies_agents/               ← 11 estudos
│   ├── aristotle/                ← Filosofia
│   ├── badge/                    ← Certificações
│   ├── calculus/                 ← ML Engineering
│   ├── dev/                      ← Python
│   ├── eduardo/                  ← PMP
│   ├── freela/                   ← Freelancer
│   ├── google/                   ← Google Skills
│   ├── john/                     ← Inglês C2
│   ├── justus/                   ← Job Hunter
│   ├── showcase/                 ← Portfólio
│   └── temer/                    ← Política
├── shared/                       ← Skills + ferramentas
├── auditing/                     ← Auditorias
└── scripts/                      ← Scripts de infra
```

Cada agente de estudo tem `state.json` com `daily_log` — o dashboard lê esses arquivos via WebSocket para mostrar status **real** (nada fake).

---

## 6. DASHBOARD — FUNCIONAMENTO TÉCNICO

### Fluxo

```
index.html (browser)
    │
    ├── HTTP GET /api/status ← dashboard.py (porta 8080)
    │                         └── Git branch + último commit + timestamp
    │
    └── WebSocket ws://hostname:8765 ← server.py
                                       ├── Lê /opt/brachat/state/malha.json (EZRA)
                                       ├── Lê /opt/brachat/state/nice.json (NICE)
                                       ├── Escaneia agents/{director,builder,studies}_agents/*/state.json
                                       └── Envia JSON (1s) para todos os clients conectados
```

### O que o dashboard mostra

- **Orchestrator**: EZRA + NICE (status das bridges Telegram)
- **Directors**: 5 diretores com nome + cargo
- **Builders**: architect + artur (destaca se EZRA está usando)
- **Studies**: 11 agentes de estudo (verde se tem `daily_log`, cinza se vazio)
- **Sistema**: CPU, RAM, Load (atualizado a cada broadcast)

Nada é fake — o dashboard reflete exatamente o estado no disco.

---

## 7. SEGURANÇA

### Acesso SSH
```bash
ssh -i /path/to/key opc@147.15.18.252
```

### Chave
- Local: `/Users/mac/brachat-main/integrations/apis/ssh-key-2026-06-10.key`
- Pública: adicionada ao `~/.ssh/authorized_keys` do usuário `opc`

### Secrets
- `/opt/brachat/.env` — tokens Telegram + API keys
- Apenas os bridges leem (ezra + nice)
- `.env` não entra no git (`.gitignore`)

---

## 8. MANUTENÇÃO

### Diária
```bash
# Verificar se tudo está rodando
ssh -i /path/key opc@147.15.18.252 'sudo systemctl is-active brachat-ezra brachat-nice brachat-dashboard brachat-malha'

# Ver dashboard localmente
ssh -i /path/key opc@147.15.18.252 'curl -s http://localhost:8080 | head -3'
```

### Suspeita de queda
```bash
ssh -i /path/key opc@147.15.18.252 'sudo journalctl -u brachat-malha -n 30 --no-pager'
```

### Atualização de agentes
```bash
# Sincronizar repositório
ssh -i /path/key opc@147.15.18.252 \
  'cd /opt/brachat/repo && git pull origin main'
```
