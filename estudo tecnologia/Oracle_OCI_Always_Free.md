# Oracle Cloud Infrastructure — Always Free Resources (documentação oficial)

**Fonte:** https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
**Obtido em:** 2026-07-31

Todos os recursos abaixo estão incluídos **sem custo** na tenancy OCI, na **home region**, pela vida da conta (recursos com rótulo "Always Free-eligible" no Console).

---

## Infraestrutura

### Certificados
- 5 certificate authorities (CAs)
- 150 certificados

### Compute
- **Micro instances (AMD):** até **2 VMs** `VM.Standard.E2.1.Micro` (AMD).
- **OCI Ampere A1 (ARM):** 1.500 OCPU-horas + 9.000 GB-horas/mês grátis = **2 OCPUs + 12 GB RAM** totais (flexíveis).
- Combinações possíveis: ex. 1 VM A1 com 2 OCPUs + 2 Micro; ou 2 VMs A1 com 1 OCPU cada + 0 Micro.
- Boot volume mínimo: **47 GB** por instância (default 50 GB).
- **Sem IP público obrigatório** — dá para criar em subnet pública/privada sem public IP.
- **Reclamação de instâncias ociosas:** se por 7 dias a utilização ficar abaixo de:
  - CPU (95º percentil) < 20%
  - Rede < 20%
  - Memória < 20% (só A1)
  → a instância pode ser **reclamada (apagada) pela Oracle**. (Precisa carga sintética.)
- Erro "out of host capacity" = falta temporária de shape na home region → trocar AD ou aguardar.

| Shape | CPU | RAM | Rede | Imagens |
|---|---|---|---|---|
| VM.Standard.E2.1.Micro | 1/8 OCPU | 1 GB | 1 VNIC, até 50 Mbps | Oracle Linux Dev 8, Oracle Linux, Ubuntu, CentOS |
| VM.Standard.A1.Flex | 2 OCPU total | 12 GB total | escala com OCPUs | Oracle Linux Dev, Oracle Linux, Ubuntu |

### Block Volume
- **200 GB total** (boot + block combinados) na home region.
- **5 backups** de volume no total.
- Boot volume default 50 GB; 4 instâncias = cota cheia.
- Volumes fora da home region = pagos.

### Object e Archive Storage
- **20 GB** combinados (Standard + Infrequent Access + Archive) — contas Always Free-only.
- Contas com créditos/paid: 10 GB por tier (Standard/IA/Archive).
- **50.000 requisições API** por mês.

### Vault
- Chaves master protegidas por software: ilimitadas grátis.
- **20 key versions HSM** + **150 segredos** Always Free (qualquer número de vaults).
- Virtual private vaults **não** incluídos.
- 40 versões por segredo (20 ativas + 20 pending deletion).

### Resource Manager (Terraform)
- 100 stacks, 100 configuration source providers, 100 private templates
- 2 jobs concorrentes (duração máx. 24h), 1 private endpoint

---

## Banco de Dados

- **Oracle Autonomous AI Database:** **2 instâncias** (1 OCPU + 20 GB cada, não escaláveis), 20 sessões simultâneas, serverless. Workloads: Transaction Processing, JSON, APEX, Lakehouse. Versões 19c ou 21c conforme região.
- **Oracle NoSQL Database:** até 133M reads/mês, 133M writes/mês, 3 tabelas × 25 GB.
- **MySQL HeatWave:** 1 standalone DB system, 50 GB storage + 50 GB backup.

---

## Rede

- **Cluster Placement Groups:** 10–50 por região.
- **Load Balancer (Flexible):** 1 grátis, 10 Mbps min/max, 16 listeners, 1024 backend servers.
- **Network Load Balancer:** 1 grátis (50 listeners, 512 backends/set, 1024 total).
- **VCNs:** até **2** VCNs em tenancies Free Tier.
- **VCN Flow Logs:** 10 GB/mês compartilhados com Logging.
- **Site-to-Site VPN:** até 50 conexões IPSec.
- Porta 25 (e-mail) bloqueada por padrão → pedir exceção.

---

## Observabilidade

- **APM:** 1.000 tracing events/hora + 10 Synthetic Monitor runs/hora.
- **Connector Hub:** 2 connectors.
- **Console Dashboards:** 100.
- **Email Delivery:** 3.000 e-mails/mês.
- **Monitoring:** 500M pontos de ingestão + 1B retrievals.
- **Notifications:** 1M https/mês + 1.000 e-mails/mês.
- **Bastion:** grátis (SSH restrito e temporário).

---

## Outros

- **Outbound Data Transfer:** 10 TB/mês.
- **Fleet Application Management:** 25 recursos/mês.
- **Limits/uso:** Console → Governance & Administration → Limits, Quotas and Usage.

---

## Notas para o projeto Ezra OS (R$0)

- 4 OCPU ARM + 24 GB **não** são "garantidos" — a doc oficial diz **2 OCPU + 12 GB** na alocação flexível. Verificar cotas reais na tenancy.
- Reclamação de ociosidade: **carga sintética** no stage é obrigatória (já no cloud-init).
- 200 GB block → VMs (47–50 GB boot cada) + volumes.
- Bastion grátis ✓, ALB 10 Mbps ✓, Vault 150 segredos ✓, 2× Autonomous DB 20 GB ✓, Object 20 GB ✓.
