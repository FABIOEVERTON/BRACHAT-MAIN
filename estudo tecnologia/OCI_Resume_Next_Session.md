# Estado da Configuração OCI — Retomada

**Data:** 2026-07-31
**Status:** Aguardando atribuição de IPs públicos nas duas VMs

---

## O que já está feito

| Item | Status |
|---|---|
| Tenancy OCI | Ativa (`ezra_Bots`, região `sa-saopaulo-1`) |
| VCN | `ezra_VCN` (10.0.0.0/16) com subnets `1339` (10.0.0.0/24) e `1402` (10.0.2.0/24) |
| Instâncias | 2× `VM.Standard.E2.1.Micro` (Always Free) |
| - `ezra_bot_2` | Ubuntu 22.04 Minimal, Private IP `10.0.0.240`, Subnet `1339` → **PROD** |
| - `ezra_bot_1` | Ubuntu 20.04, Private IP `10.0.2.15`, Subnet `1402` → **STANDBY** |
| Reserved Public IP | `ezra-prod-ip` = **163.176.111.95** (Created, Available, Compartment `ezra_Bots`) |
| Ephemeral IP | Não criado ainda (para STANDBY) |
| Telegram Bot | Token salvo no MCP como `TELEGRAM_BOT_TOKEN` |

---

## O que FALTA fazer (próximos passos manuais no console OCI)

### 1. Atribuir Reserved IP na PROD (`ezra_bot_2` / 22.04 / 10.0.0.240)
- Console → **Networking → Virtual cloud networks → ezra_VCN → Subnets → subnet-20260731-1339**
- Aba **Private IPs** → filtre `10.0.0.240` → clique no IP
- **Assign Public IP** → **Reserved IP** → selecione `ezra-prod-ip` (163.176.111.95) → **Assign**

### 2. Criar Ephemeral IP na STANDBY (`ezra_bot_1` / 20.04 / 10.0.2.15)
- Mesmo caminho na subnet `subnet-20260731-1402` (CIDR 10.0.2.0/24)
- Private IP `10.0.2.15` → **Assign Public IP** → **Ephemeral Public IP** → Assign
- **Anote o IP que aparecer** (ex.: `129.146.xxx.xxx`)

### 3. Me passe os dois IPs públicos
- PROD: `163.176.111.95` (já conhecido)
- STANDBY: (o Ephemeral que você criar)

---

## O que eu faço DEPOIS que você me der os IPs

1. Testa as **6 chaves SSH únicas** (já deduplicadas, permissões 600) contra as duas VMs via SSH
2. Identifica qual chave abre cada VM
3. Renomeia: `ezra-prod` e `ezra-standby`
3. Guarda as duas certas no MCP (`ezra-prod-key`, `ezra-standby-key`)
4. Apaga as 4 chaves restantes
5. Valida o `skill-gate` + sentinel na VM

### Comando de teste pronto (rodar 2x, uma por IP)

```bash
for k in \
  "ssh-key-2026-07-31.key" \
  "ssh-key-2026-07-31 (1).key" \
  "ssh-key-2026-07-31 (5).key" \
  "ssh-key-2026-07-31 (8).key" \
  "ssh-key-2026-07-31 (9).key" \
  "ssh-key-2026-07-31 (11).key"; do
  echo "== $k =="
  ssh -i "$HOME/Downloads/$k" -o BatchMode=yes -o ConnectTimeout=5 \
      -o StrictHostKeyChecking=no ubuntu@IP_PUBLICO 'echo OK; hostname' 2>&1 | tail -1
done
```

> Troque `IP_PUBLICO` pelo IP da VM. A chave que responder `OK` + hostname é a daquela VM.

---

## Arquivos-chave já salvos (não perde ao reiniciar)

- `estudo tecnologia/Oracle_OCI_Ezra_Telegram_Spec.md` (SPEC completa)
- `.opencode/mcp/credentials/secrets.env` (com `TELEGRAM_BOT_TOKEN`)
- `opencode.json` (com `manifest.md` em `instructions`, `permission` → `ask`)
- Plugins reescritos (`.opencode/plugin/*.ts`)

---

**Próxima sessão:** me dá os dois IPs públicos → eu faço o resto.