# Oracle Cloud Infrastructure - Always Free Resources (official documentation)

**Source:** https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
**Retrieved:** 2026-07-31

All resources below are included **at no cost** in the OCI tenancy, in the **home region**, for the life of the account (resources labeled "Always Free-eligible" in the Console).

---

## Infrastructure

### Certificates
- 5 certificate authorities (CAs)
- 150 certificates

### Compute
- **Micro instances (AMD):** up to **2 VMs** `VM.Standard.E2.1.Micro` (AMD).
- **OCI Ampere A1 (ARM):** 1,500 OCPU-hours + 9,000 GB-hours/month free = **2 OCPUs + 12 GB RAM** total (flexible).
- Possible combinations: e.g. 1 A1 VM with 2 OCPUs + 2 Micro; or 2 A1 VMs with 1 OCPU each + 0 Micro.
- Minimum boot volume: **47 GB** per instance (default 50 GB).
- **No mandatory public IP** - can be created in public/private subnet without public IP.
- **Idle instance reclaim:** if for 7 days utilization stays below:
  - CPU (95th percentile) < 20%
  - Network < 20%
  - Memory < 20% (A1 only)
  - the instance may be **reclaimed (deleted) by Oracle**. (Needs synthetic load.)
- "Out of host capacity" error = temporary shape shortage in home region - switch AD or wait.

| Shape | CPU | RAM | Network | Images |
|---|---|---|---|---|
| VM.Standard.E2.1.Micro | 1/8 OCPU | 1 GB | 1 VNIC, up to 50 Mbps | Oracle Linux Dev 8, Oracle Linux, Ubuntu, CentOS |
| VM.Standard.A1.Flex | 2 OCPU total | 12 GB total | scales with OCPUs | Oracle Linux Dev, Oracle Linux, Ubuntu |

### Block Volume
- **200 GB total** (boot + block combined) in the home region.
- **5 volume backups** total.
- Default boot volume 50 GB; 4 instances = full quota.
- Volumes outside home region = paid.

### Object and Archive Storage
- **20 GB** combined (Standard + Infrequent Access + Archive) - Always Free-only accounts.
- Accounts with credits/paid: 10 GB per tier (Standard/IA/Archive).
- **50,000 API requests** per month.

### Vault
- Software-protected master keys: unlimited free.
- **20 HSM key versions** + **150 secrets** Always Free (any number of vaults).
- Virtual private vaults **not** included.
- 40 versions per secret (20 active + 20 pending deletion).

### Resource Manager (Terraform)
- 100 stacks, 100 configuration source providers, 100 private templates
- 2 concurrent jobs (max 24h each), 1 private endpoint

---

## Database

- **Oracle Autonomous AI Database:** **2 instances** (1 OCPU + 20 GB each, not scalable), 20 concurrent sessions, serverless. Workloads: Transaction Processing, JSON, APEX, Lakehouse. Versions 19c or 21c depending on region.
- **Oracle NoSQL Database:** up to 133M reads/month, 133M writes/month, 3 tables x 25 GB.
- **MySQL HeatWave:** 1 standalone DB system, 50 GB storage + 50 GB backup.

---

## Networking

- **Cluster Placement Groups:** 10-50 per region.
- **Load Balancer (Flexible):** 1 free, 10 Mbps min/max, 16 listeners, 1024 backend servers.
- **Network Load Balancer:** 1 free (50 listeners, 512 backends/set, 1024 total).
- **VCNs:** up to **2** VCNs in Free Tier tenancies.
- **VCN Flow Logs:** 10 GB/month shared with Logging.
- **Site-to-Site VPN:** up to 50 IPSec connections.
- Port 25 (email) blocked by default - request exception.

---

## Observability

- **APM:** 1,000 tracing events/hour + 10 Synthetic Monitor runs/hour.
- **Connector Hub:** 2 connectors.
- **Console Dashboards:** 100.
- **Email Delivery:** 3,000 emails/month.
- **Monitoring:** 500M ingest points + 1B retrievals.
- **Notifications:** 1M https/month + 1,000 emails/month.
- **Bastion:** free (restricted, temporary SSH).

---

## Other

- **Outbound Data Transfer:** 10 TB/month.
- **Fleet Application Management:** 25 resources/month.
- **Limits/usage:** Console - Governance & Administration - Limits, Quotas and Usage.

---

## Notes for the Ezra OS project (R$0)

- 4 OCPU ARM + 24 GB are **not** "guaranteed" - the official doc says **2 OCPU + 12 GB** in flexible allocation. Check real quotas in the tenancy.
- Idle reclaim: **synthetic load** on stage is mandatory (already in cloud-init).
- 200 GB block - VMs (47-50 GB boot each) + volumes.
- Free Bastion ok, ALB 10 Mbps ok, Vault 150 secrets ok, 2x Autonomous DB 20 GB ok, Object 20 GB ok.
