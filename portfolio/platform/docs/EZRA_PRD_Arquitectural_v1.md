# PRD ARQUITECTURAL — PLATAFORMA EZRA
## Versão 1.0 | Documento de Referência para Agentes de Desenvolvimento
### Stack: Next.js · TypeScript · FastAPI · Python | Hospedagem: A definir (recomendação incluída)

---

## METADADOS DO DOCUMENTO

| Campo | Valor |
|---|---|
| Produto | Plataforma EZRA |
| Versão do PRD | 1.0 |
| Data | Setembro 2026 |
| Destinatário | Agentes autónomos de desenvolvimento (Claude Code, Cursor, Devin ou equivalente) |
| Língua de código | TypeScript (frontend) · Python (backend/IA) |
| Língua de documentação | Português brasileiro |
| Status | Rascunho para execução |

---

## ÍNDICE

1. Visão Geral e Princípios Arquitecturais
2. Estrutura de Repositório Monorepo
3. Núcleo Compartilhado (Shared Core)
4. Ramo 1 — Governança de IA (3 produtos)
5. Ramo 2 — Governança Municipal (6 produtos)
6. Infraestrutura, Hospedagem e Soberania de Dados
7. Segurança, Cadeia de Custódia e Cofre WORM
8. Modelo de Multi-tenancy e White-label
9. Contratos de API — Especificação OpenAPI por Serviço
10. Sequência de Implementação e Dependências
11. Critérios de Aceitação por Produto

---

## 1. VISÃO GERAL E PRINCÍPIOS ARQUITECTURAIS

### 1.1 Missão do Sistema

A Plataforma EZRA é um sistema SaaS multi-produto, multi-ramo e multi-tenant que entrega governança de IA e governança municipal com validade jurídica brasileira. O diferencial irredutível é: toda acção auditável do sistema gera um Laudo Pericial Oficial assinado digitalmente, com hash SHA-256 encadeado e gravado em cofre imutável (WORM).

### 1.2 Princípios Não Negociáveis

**P1 — Laudo como saída universal:** Nenhum produto entrega apenas um dashboard. Todo produto entrega um artefacto com validade probatória.

**P2 — Cadeia de custódia encadeada:** O hash SHA-256 do Laudo N é input do Laudo N+1. A cadeia é iniciada no primeiro produto contratado e nunca é reiniciada. Quebrar a cadeia é o principal argumento de lock-in legítimo da plataforma.

**P3 — Soberania de dados brasileira:** Nenhum dado do cliente trafega fora do território nacional. Isso é requisito de compliance LGPD (Art. 33) e argumento comercial contra concorrentes globais.

**P4 — Outcome-based pricing:** Nenhum produto é precificado por assento de usuário. A unidade de cobrança é sempre proporcional ao valor entregue (ativo monitorado, processo gerado, convênio encerrado, chamada interceptada).

**P5 — Multi-tenant isolado:** Cada tenant (empresa ou município) opera em namespace isolado. Dados de um tenant nunca são acessíveis por outro, nem por agentes de IA compartilhados.

**P6 — White-label nativo:** O sistema foi desenhado desde a base para operar sob marca de terceiros (bancas de advocacia, contabilidades, associações municipais). O white-label não é uma feature adicionada — é um modo de operação de primeira classe.

### 1.3 Diagrama de Alto Nível

```
┌─────────────────────────────────────────────────────────────────┐
│                        PLATAFORMA EZRA                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    SHARED CORE                           │   │
│  │  Auth · Tenant · Laudo Engine · WORM Vault · Billing     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │     RAMO 1 — GOV AI     │  │   RAMO 2 — GOV MUNICIPAL     │  │
│  │                         │  │                              │  │
│  │  SENTINEL  (P1)         │  │  RADAR    (P1)               │  │
│  │  AEGIS     (P2)         │  │  VIGÍLIA  (P2)               │  │
│  │  GUARDIAN  (P3)         │  │  COMPRAS  (P3)               │  │
│  │                         │  │  EXECUTA  (P4)               │  │
│  │                         │  │  ALERTA   (P5)               │  │
│  │                         │  │  PROVA    (P6)               │  │
│  └─────────────────────────┘  └──────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              INFRASTRUCTURE LAYER                        │   │
│  │  AWS São Paulo (ap-southeast-1) · RDS · S3-WORM · SQS   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. ESTRUTURA DE REPOSITÓRIO MONOREPO

### 2.1 Justificativa da escolha monorepo

O sistema compartilha: motor de laudos, engine de autenticação, modelo de tenant, cofre WORM e componentes de UI. Um monorepo com workspaces elimina duplicação de lógica crítica entre produtos e garante que uma mudança no motor de laudos se propaga para todos os produtos simultaneamente.

### 2.2 Estrutura de directórios

```
ezra/
├── apps/
│   ├── web/                          # Next.js 14+ — App Router
│   │   ├── app/
│   │   │   ├── (auth)/               # Login, onboarding, 2FA
│   │   │   ├── (dashboard)/          # Shell compartilhado
│   │   │   ├── gov-ai/               # Ramo 1 — rotas e páginas
│   │   │   │   ├── sentinel/
│   │   │   │   ├── aegis/
│   │   │   │   └── guardian/
│   │   │   └── gov-municipal/        # Ramo 2 — rotas e páginas
│   │   │       ├── radar/
│   │   │       ├── vigilia/
│   │   │       ├── compras/
│   │   │       ├── executa/
│   │   │       ├── alerta/
│   │   │       └── prova/
│   │   ├── components/               # Componentes React compartilhados
│   │   │   ├── ui/                   # shadcn/ui base
│   │   │   ├── laudo/                # Componentes de laudo e hash
│   │   │   ├── charts/               # Recharts wrappers
│   │   │   └── white-label/          # Theme provider e overrides
│   │   └── lib/
│   │       ├── api-client.ts         # Cliente HTTP tipado para todos os serviços
│   │       ├── auth.ts               # NextAuth.js config
│   │       └── tenant.ts             # Resolução de tenant por subdomínio
│   │
│   └── admin/                        # Next.js — painel interno EZRA
│       └── app/
│           ├── tenants/
│           ├── billing/
│           └── white-label-config/
│
├── services/                         # FastAPI — um serviço por produto
│   ├── shared/                       # Módulos Python compartilhados
│   │   ├── auth/                     # JWT validation, RBAC
│   │   ├── tenant/                   # Tenant context middleware
│   │   ├── laudo/                    # Motor de geração de laudos
│   │   │   ├── engine.py             # Orquestrador principal
│   │   │   ├── hash_chain.py         # SHA-256 encadeado
│   │   │   ├── worm_vault.py         # Interface com S3 Object Lock
│   │   │   └── pdf_generator.py      # ReportLab / WeasyPrint
│   │   ├── db/                       # SQLAlchemy models + migrations
│   │   └── queue/                    # SQS producers/consumers
│   │
│   ├── gov-ai/
│   │   ├── sentinel/                 # Serviço de varredura Shadow AI
│   │   │   ├── main.py
│   │   │   ├── scanner/
│   │   │   │   ├── network_scan.py   # Varredura de rede e APIs
│   │   │   │   ├── saas_detect.py    # Shadow SaaS via OAuth/DNS
│   │   │   │   └── factsheet.py      # Geração de AI Factsheets
│   │   │   └── agents/               # Agentes de descoberta
│   │   │
│   │   ├── aegis/                    # Motor de auditoria AGCP 122
│   │   │   ├── main.py
│   │   │   ├── controls/
│   │   │   │   ├── l1_juridico.py    # PL 2338 — controles jurídicos
│   │   │   │   ├── l2_dados.py       # LGPD — controles de dados
│   │   │   │   ├── l3_seguranca.py   # ISO 42001 / NIST AI RMF
│   │   │   │   └── l4_pericia.py     # Controles de perícia técnica
│   │   │   ├── scoring.py            # Score 0–100 e RIPD
│   │   │   ├── lifecycle/
│   │   │   │   └── model_monitor.py  # Detecção de mudança de versão
│   │   │   └── normative_map.py      # Mapeamento controle → norma → artigo
│   │   │
│   │   └── guardian/                 # Gateway de Runtime
│   │       ├── main.py
│   │       ├── proxy/
│   │       │   ├── interceptor.py    # Proxy de chamadas em tempo real
│   │       │   ├── prompt_guard.py   # Detecção de injeção de prompt
│   │       │   └── data_filter.py    # Filtro de PII e dados sensíveis
│   │       ├── hitl/                 # Human-in-the-Loop
│   │       │   └── approval_engine.py
│   │       └── trail/                # Trilha forense imutável
│   │           └── event_logger.py
│   │
│   └── gov-municipal/
│       ├── radar/                    # Inteligência de captação
│       │   ├── main.py
│       │   ├── dou_monitor.py        # Monitoramento DOU 24/7
│       │   ├── emenda_monitor.py     # EC 105/2019 — emendas impositivas
│       │   └── eligibility.py        # Análise de elegibilidade por CNPJ
│       │
│       ├── vigilia/                  # Regularidade fiscal
│       │   ├── main.py
│       │   ├── cauc_monitor.py       # CAUC / Transferegov
│       │   ├── tce_monitor.py        # TCE estadual
│       │   └── alert_engine.py       # Alertas preditivos de vencimento
│       │
│       ├── compras/                  # Fábrica de licitações
│       │   ├── main.py
│       │   ├── etp_generator.py      # Estudos Técnicos Preliminares
│       │   ├── tr_generator.py       # Termos de Referência
│       │   └── price_research/
│       │       ├── painel_precos.py  # API api.compras.gov.br
│       │       ├── pncp.py           # API PNCP
│       │       └── bec.py            # BEC-SP e equivalentes estaduais
│       │
│       ├── executa/                  # Monitor de execução de convênio
│       │   ├── main.py
│       │   ├── physical_monitor.py   # Cronograma físico vs. financeiro
│       │   ├── deviation_alert.py    # Alertas preditivos de desvio
│       │   └── compliance_checker.py # Conformidade de objeto
│       │
│       ├── alerta/                   # SOS Diligências
│       │   ├── main.py
│       │   ├── notification_parser/
│       │   │   ├── ocr_pipeline.py   # OCR + validação semântica
│       │   │   └── classifier.py     # Classificação de pendência
│       │   └── response_generator.py # Geração de Ofício de Resposta
│       │
│       └── prova/                    # Auditor de despesas
│           ├── main.py
│           ├── nfe_integration.py    # WebService SEFAZ
│           ├── sinapi_parser.py      # SINAPI + medições de obra
│           ├── extract_reconciler.py # Conciliação de extratos
│           └── payment_blocker.py    # Trava de pagamentos divergentes
│
├── packages/                         # Pacotes TypeScript compartilhados
│   ├── types/                        # Tipos compartilhados (Laudo, Tenant, etc.)
│   ├── ui/                           # Design system base
│   ├── api-contracts/                # Tipos gerados do OpenAPI
│   └── crypto/                       # Utilitários SHA-256 e verificação
│
├── infra/                            # Infrastructure as Code
│   ├── terraform/
│   │   ├── aws/
│   │   │   ├── vpc.tf                # VPC isolada por ambiente
│   │   │   ├── rds.tf                # PostgreSQL Multi-AZ
│   │   │   ├── s3_worm.tf            # S3 Object Lock (WORM)
│   │   │   ├── sqs.tf                # Filas de processamento assíncrono
│   │   │   ├── ecs.tf                # ECS Fargate por serviço
│   │   │   └── cloudfront.tf         # CDN com certificado BR
│   │   └── modules/
│   └── docker/
│       ├── docker-compose.dev.yml    # Ambiente local completo
│       └── Dockerfile.*              # Um por serviço
│
├── scripts/                          # Scripts de automação para agentes
│   ├── seed_controls.py              # Seed dos 122 controles AGCP
│   ├── seed_normative_map.py         # Seed do mapeamento normativo
│   └── generate_api_types.sh         # Geração de tipos TypeScript do OpenAPI
│
├── docs/
│   ├── architecture/                 # ADRs (Architecture Decision Records)
│   ├── api/                          # OpenAPI specs por serviço
│   └── contracts/                    # Contratos de interface entre serviços
│
├── turbo.json                        # Turborepo config
├── package.json                      # Workspace root
└── pyproject.toml                    # Python workspace (uv ou Poetry)
```

---

## 3. NÚCLEO COMPARTILHADO (SHARED CORE)

### 3.1 Motor de Autenticação e Autorização

**Stack:** NextAuth.js v5 (frontend) + Python JWT middleware (backend)

**Modelo RBAC por produto:**

```typescript
// packages/types/src/auth.ts

type Role =
  | 'EZRA_ADMIN'          // Operador interno EZRA
  | 'TENANT_ADMIN'        // Administrador do cliente
  | 'TENANT_AUDITOR'      // Auditor operacional
  | 'TENANT_VIEWER'       // Visualização somente leitura
  | 'WHITELABEL_OPERATOR' // Operador white-label (banca, contabilidade)
  | 'WHITELABEL_ADMIN';   // Administrador da marca white-label

type Permission =
  | 'laudo:emit'
  | 'laudo:view'
  | 'scan:execute'
  | 'monitor:configure'
  | 'gateway:configure'
  | 'tenant:manage'
  | 'billing:view'
  | 'whitelabel:configure';
```

**Fluxo de autenticação:**

```
Cliente → Next.js (NextAuth session) → API Gateway → FastAPI (JWT verify)
                                                    → Tenant context injection
                                                    → RBAC permission check
                                                    → Handler
```

**Requisitos:**
- JWT com expiração de 1h + refresh token de 7 dias
- MFA obrigatório para roles TENANT_ADMIN e WHITELABEL_OPERATOR
- Audit log de cada autenticação gravado no cofre WORM
- SSO via SAML 2.0 para clientes enterprise (fase 2)

---

### 3.2 Modelo de Multi-tenancy

**Estratégia:** Schema-per-tenant no PostgreSQL.

**Justificativa:** Isolamento de dados garantido por construção, sem risco de vazamento cross-tenant por query incorreta. Custo de operação é maior do que row-level security mas é o único modelo defensável para laudos com validade jurídica.

```python
# services/shared/tenant/context.py

from contextvars import ContextVar
from sqlalchemy import text

current_tenant: ContextVar[str] = ContextVar('current_tenant')

async def set_tenant_schema(db, tenant_id: str):
    schema = f"tenant_{tenant_id}"
    await db.execute(text(f"SET search_path TO {schema}, public"))
    current_tenant.set(tenant_id)
```

**Modelo de dados do tenant:**

```python
# services/shared/db/models/tenant.py

class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID
    slug: Mapped[str] = mapped_column(String(63), unique=True)      # subdomínio
    branch: Mapped[str] = mapped_column(Enum("gov_ai", "gov_municipal"))
    plan: Mapped[str] = mapped_column(Enum("direct", "whitelabel"))
    whitelabel_config_id: Mapped[str | None]
    active_products: Mapped[list[str]] = mapped_column(ARRAY(String))
    chain_anchor_hash: Mapped[str | None]  # Hash do primeiro laudo emitido
    created_at: Mapped[datetime]
    status: Mapped[str] = mapped_column(Enum("active", "suspended", "trial"))
```

---

### 3.3 Motor de Laudos (Laudo Engine)

Este é o componente mais crítico da plataforma. Toda falha aqui compromete a validade jurídica de todos os produtos.

**Arquitectura do motor:**

```python
# services/shared/laudo/engine.py

from dataclasses import dataclass
from enum import Enum
from services.shared.laudo.hash_chain import HashChain
from services.shared.laudo.worm_vault import WORMVault
from services.shared.laudo.pdf_generator import PDFGenerator

class LaudoType(Enum):
    # Ramo 1
    INVENTARIO_ALGORITIMICO = "LAI"
    CONFORMIDADE_ALGORITIMICA = "LCA"
    TRANSICAO_MODELO = "LTM"
    INTEGRIDADE_RUNTIME = "LIR"
    # Ramo 2
    ELEGIBILIDADE_ORCAMENTARIA = "LEO"
    REGULARIDADE_FISCAL = "LRF"
    JUSTIFICATIVA_PRECOS = "LJP"
    CONFORMIDADE_OBJETO = "LCO"
    SANEAMENTO_DILIGENCIAS = "LSD"
    PRESTACAO_CONTAS = "LPC"

@dataclass
class LaudoRequest:
    tenant_id: str
    product_id: str
    laudo_type: LaudoType
    payload: dict          # Dados específicos de cada produto
    generated_by: str      # user_id ou agent_id
    normative_refs: list[str]  # Artigos e normas referenciadas

@dataclass
class LaudoResult:
    laudo_id: str          # UUID único
    laudo_number: str      # Número sequencial por tenant (ex: LAI-2026-0042)
    sha256_hash: str       # Hash do conteúdo do laudo
    chain_hash: str        # SHA-256(laudo_hash + previous_chain_hash)
    worm_key: str          # Chave S3 onde o PDF está gravado
    pdf_url: str           # URL assinada (validade 1h) para download
    emitted_at: datetime

class LaudoEngine:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.hash_chain = HashChain(tenant_id)
        self.worm_vault = WORMVault()
        self.pdf_generator = PDFGenerator()

    async def emit(self, request: LaudoRequest) -> LaudoResult:
        # 1. Gerar PDF com conteúdo do laudo
        pdf_bytes = await self.pdf_generator.render(request)

        # 2. Calcular hash do conteúdo
        content_hash = self.hash_chain.hash_content(pdf_bytes)

        # 3. Encadear com hash anterior do tenant
        chain_hash = await self.hash_chain.chain(content_hash)

        # 4. Gravar em cofre WORM (imutável)
        worm_key = await self.worm_vault.store(
            tenant_id=self.tenant_id,
            laudo_type=request.laudo_type,
            content=pdf_bytes,
            metadata={
                "sha256": content_hash,
                "chain_hash": chain_hash,
                "normative_refs": request.normative_refs,
            }
        )

        # 5. Persistir registro no banco
        laudo = await self._persist_record(request, content_hash, chain_hash, worm_key)

        return LaudoResult(
            laudo_id=laudo.id,
            laudo_number=laudo.number,
            sha256_hash=content_hash,
            chain_hash=chain_hash,
            worm_key=worm_key,
            pdf_url=await self.worm_vault.get_signed_url(worm_key),
            emitted_at=laudo.emitted_at,
        )
```

---

### 3.4 Cadeia de Custódia SHA-256

```python
# services/shared/laudo/hash_chain.py

import hashlib
from services.shared.db import get_db

class HashChain:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    def hash_content(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    async def chain(self, content_hash: str) -> str:
        """
        Encadeia o hash do laudo atual com o hash do laudo anterior.
        chain_hash = SHA256(content_hash + previous_chain_hash)
        Se é o primeiro laudo do tenant, previous = tenant_id (âncora).
        """
        async with get_db(self.tenant_id) as db:
            previous = await db.scalar(
                "SELECT chain_hash FROM laudos ORDER BY emitted_at DESC LIMIT 1"
            )
            anchor = previous if previous else self.tenant_id
            combined = f"{content_hash}{anchor}".encode()
            chain_hash = hashlib.sha256(combined).hexdigest()
            return chain_hash
```

---

### 3.5 Cofre WORM (Write Once Read Many)

**Implementação:** AWS S3 com Object Lock em modo COMPLIANCE.

**Crítico:** O modo COMPLIANCE (diferente do modo GOVERNANCE) impede a deleção mesmo por administradores AWS com permissões elevadas. É o único modo que satisfaz o requisito de imutabilidade para validade judicial.

```python
# services/shared/laudo/worm_vault.py

import boto3
from datetime import datetime, timedelta

class WORMVault:
    def __init__(self):
        self.s3 = boto3.client('s3', region_name='sa-east-1')
        self.bucket = "ezra-worm-vault-prod"
        self.retention_years = 10  # LGPD Art. 37 — prazo mínimo de registos

    async def store(self, tenant_id: str, laudo_type, content: bytes, metadata: dict) -> str:
        key = f"{tenant_id}/{laudo_type.value}/{datetime.utcnow().isoformat()}.pdf"
        retain_until = datetime.utcnow() + timedelta(days=365 * self.retention_years)

        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType='application/pdf',
            Metadata={k: str(v) for k, v in metadata.items()},
            ObjectLockMode='COMPLIANCE',
            ObjectLockRetainUntilDate=retain_until,
            ServerSideEncryption='aws:kms',  # KMS com chave gerenciada por tenant
        )
        return key

    async def get_signed_url(self, key: str, expires_in: int = 3600) -> str:
        return self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': key},
            ExpiresIn=expires_in
        )
```

---

### 3.6 Motor de White-label

```typescript
// apps/web/lib/tenant.ts

export interface WhitelabelConfig {
  tenantSlug: string;
  brandName: string;
  logoUrl: string;
  primaryColor: string;
  secondaryColor: string;
  supportEmail: string;
  laudoSignatoryName: string;      // Nome do signatário nos laudos
  laudoSignatoryTitle: string;     // Cargo do signatário
  laudoSignatoryRegister: string;  // CRC, OAB, CREA conforme o caso
  customDomain: string | null;     // dominio.advocacia.com.br
  hidePoweredBy: boolean;
}

// Resolução de tenant por subdomínio ou domínio customizado
export async function resolveTenant(hostname: string): Promise<WhitelabelConfig> {
  // ex: prefeitura-xyz.ezra.com.br → slug = prefeitura-xyz
  // ex: auditoria.bancaxyz.com.br  → lookup por customDomain
}
```

**Regra de negócio crítica:** O laudo emitido sob white-label deve conter o nome, cargo e registro profissional do operador white-label como signatário. A EZRA aparece apenas como "sistema tecnológico de suporte" em rodapé, se `hidePoweredBy = false`. O hash SHA-256 e o registro WORM são sempre da EZRA e nunca transferíveis.

---

## 4. RAMO 1 — GOVERNANÇA DE IA

### 4.1 SENTINEL — Scanner de Shadow AI & Inventário Contínuo

#### Problema resolvido
Empresas não sabem quais modelos de IA estão operando em seu ambiente. Sem inventário, não há auditoria possível. Qualquer produto do Ramo 1 contratado sem SENTINEL audita um escopo desconhecido e incompleto.

#### Dependências
- Nenhuma. É o primeiro produto do Ramo 1.
- Pré-requisito técnico para AEGIS.

#### Módulos funcionais

**M1 — Network & API Scanner**
```python
# services/gov-ai/sentinel/scanner/network_scan.py

class NetworkScanner:
    """
    Varre a rede corporativa em busca de chamadas a endpoints de IA conhecidos.
    Opera via integração com logs de proxy/firewall (Zscaler, Palo Alto, Squid)
    ou via instalação de agente leve de coleta de tráfego DNS.
    """
    AI_ENDPOINTS = [
        "api.openai.com",
        "api.anthropic.com",
        "generativelanguage.googleapis.com",
        "api.mistral.ai",
        "api.cohere.ai",
        "api.together.xyz",
        # ... lista mantida e actualizada via feed interno
    ]

    async def scan(self, tenant_id: str, network_config: NetworkConfig) -> ScanResult:
        # 1. Conectar à fonte de logs (proxy, firewall, DNS)
        # 2. Filtrar por destinos em AI_ENDPOINTS
        # 3. Agregar por origem (usuário, aplicação, IP)
        # 4. Classificar: Autorizado | Não Autorizado | Zona Cinzenta
        pass
```

**M2 — Shadow SaaS Detector**
```python
# services/gov-ai/sentinel/scanner/saas_detect.py

class ShadowSaaSDetector:
    """
    Detecta IA embutida em SaaS de terceiros via análise de
    concessões OAuth e registos de aplicações no diretório corporativo.
    Não requer instalação de agente — opera via API do Azure AD ou Google Workspace.
    """
    SAAS_WITH_EMBEDDED_AI = {
        "Microsoft 365 Copilot": ["copilot.microsoft.com"],
        "Notion AI": ["api.notion.so"],
        "Grammarly": ["api.grammarly.com"],
        "Adobe Firefly": ["firefly.adobe.com"],
        "GitHub Copilot": ["copilot-proxy.githubusercontent.com"],
        # ... lista mantida via feed interno
    }

    async def detect(self, tenant_id: str, directory_config: DirectoryConfig) -> list[SaaSAsset]:
        # 1. Listar aplicações OAuth autorizadas no diretório
        # 2. Cruzar com SAAS_WITH_EMBEDDED_AI
        # 3. Verificar se uso está coberto por política do tenant
        pass
```

**M3 — AI Factsheet Generator**
```python
# services/gov-ai/sentinel/scanner/factsheet.py

@dataclass
class AIFactsheet:
    asset_id: str
    name: str                      # Nome do modelo/serviço
    provider: str                  # OpenAI, Anthropic, Google, etc.
    model_version: str | None      # Versão do modelo se identificável
    access_type: str               # API_CALL | SAAS_EMBEDDED | INTERNAL
    authorization_status: str      # AUTHORIZED | UNAUTHORIZED | GRAY_ZONE
    data_categories_exposed: list[str]  # PII, FINANCIAL, HEALTH, etc.
    first_seen: datetime
    last_seen: datetime
    request_volume_30d: int | None
    risk_score: int                # 0–100
    normative_gaps: list[str]      # Artigos LGPD/PL2338 potencialmente violados
```

#### Laudo gerado
```python
# Chamada ao motor de laudos após varredura concluída
laudo = await engine.emit(LaudoRequest(
    laudo_type=LaudoType.INVENTARIO_ALGORITIMICO,
    payload={
        "total_assets": len(factsheets),
        "unauthorized_count": sum(1 for f in factsheets if f.authorization_status == "UNAUTHORIZED"),
        "risk_distribution": {...},
        "factsheets": [f.__dict__ for f in factsheets],
    },
    normative_refs=["LGPD Art. 7", "LGPD Art. 37", "PL 2338 Art. 15"],
))
```

#### API Contract
```yaml
# docs/api/sentinel.yaml (OpenAPI 3.1)

paths:
  /sentinel/scan:
    post:
      summary: Iniciar varredura de Shadow AI
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ScanRequest'
      responses:
        202:
          description: Varredura iniciada (assíncrona)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/JobStatus'

  /sentinel/inventory:
    get:
      summary: Retornar inventário atual de ativos de IA
      parameters:
        - name: status
          in: query
          schema:
            enum: [authorized, unauthorized, gray_zone, all]
      responses:
        200:
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AIFactsheet'

  /sentinel/laudo/{scan_id}:
    get:
      summary: Obter laudo da varredura
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LaudoResult'
```

#### Critérios de aceitação
- [ ] Varredura de rede identifica 100% dos endpoints em `AI_ENDPOINTS` nos logs de proxy
- [ ] Shadow SaaS Detector identifica aplicações OAuth em Azure AD e Google Workspace sem instalação de agente
- [ ] Factsheet gerado para cada ativo com todos os campos obrigatórios preenchidos
- [ ] Laudo emitido em até 60 segundos após conclusão da varredura
- [ ] Hash SHA-256 do laudo verificável independentemente (algoritmo público)
- [ ] PDF gravado em S3 WORM com Object Lock COMPLIANCE activado

---

### 4.2 AEGIS — Plataforma de Auditoria, Monitoramento Contínuo & Ciclo de Vida de Modelos

#### Problema resolvido
Empresas precisam demonstrar conformidade contínua com LGPD, PL 2338 e ISO 42001. O processo manual custa semanas de consultoria por ciclo e não produz evidência forense. Quando o modelo de IA é atualizado pelo fornecedor, toda a auditoria anterior torna-se inválida sem revalidação — e isso ocorre sem que ninguém na empresa perceba.

#### Dependências
- SENTINEL activo com inventário completo.
- O AEGIS audita exclusivamente ativos presentes no inventário do SENTINEL.

#### Os 122 Controles AGCP — Estrutura

```python
# services/gov-ai/aegis/controls/base.py

from abc import ABC, abstractmethod

@dataclass
class ControlResult:
    control_id: str           # ex: "L1-001"
    control_name: str
    level: str                # L1 | L2 | L3 | L4
    status: str               # PASS | FAIL | PARTIAL | NOT_APPLICABLE
    score: int                # 0–100 para este controle
    evidence: list[str]       # Evidências coletadas
    gaps: list[str]           # Lacunas identificadas
    normative_refs: list[dict] # [{"norm": "LGPD", "article": "Art. 37", "clause": "caput"}]
    remediation: str | None   # Orientação de remediação se FAIL

class BaseControl(ABC):
    level: str
    control_id: str
    control_name: str
    normative_refs: list[dict]

    @abstractmethod
    async def evaluate(self, asset: AIFactsheet, tenant_context: dict) -> ControlResult:
        pass
```

```python
# Exemplo de controle L1 (Jurídico / PL 2338)
# services/gov-ai/aegis/controls/l1_juridico.py

class L1_001_BaseJuridicaControl(BaseControl):
    level = "L1"
    control_id = "L1-001"
    control_name = "Existência de base jurídica para uso de IA de alto risco"
    normative_refs = [
        {"norm": "PL 2338", "article": "Art. 10", "clause": "I"},
        {"norm": "LGPD", "article": "Art. 7", "clause": "caput"},
    ]

    async def evaluate(self, asset: AIFactsheet, tenant_context: dict) -> ControlResult:
        # Verifica se há documento de base jurídica registado para o ativo
        pass

# ... 121 controles adicionais estruturados da mesma forma
# Seed via: scripts/seed_controls.py
```

**Distribuição dos 122 controles:**

| Nível | Domínio | Nº de controles | Normas primárias |
|---|---|---|---|
| L1 | Jurídico | 38 | PL 2338, LGPD |
| L2 | Dados | 31 | LGPD, ANPD Res. 2/2022 |
| L3 | Segurança | 28 | ISO 42001, NIST AI RMF, ISO 27001 |
| L4 | Perícia | 25 | CPC Arts. 464–480, Res. CFO 1.389/2012 |
| **Total** | | **122** | |

#### Módulo: Model Lifecycle Monitor

```python
# services/gov-ai/aegis/lifecycle/model_monitor.py

class ModelLifecycleMonitor:
    """
    Verifica periodicamente (a cada 6h) se os modelos em produção
    foram atualizados, substituídos ou descontinuados pelo fornecedor.
    Quando detecta mudança, dispara revalidação automática dos 122 controles.
    """
    PROVIDER_VERSION_ENDPOINTS = {
        "openai": "https://api.openai.com/v1/models",
        "anthropic": "https://api.anthropic.com/v1/models",
        "google": "https://generativelanguage.googleapis.com/v1/models",
    }

    async def check_for_updates(self, tenant_id: str) -> list[ModelChange]:
        # 1. Buscar versões actuais dos modelos no inventário SENTINEL
        # 2. Consultar APIs dos providers para versões disponíveis
        # 3. Comparar com última versão auditada
        # 4. Se divergência: criar ModelChange event
        pass

    async def trigger_revalidation(self, change: ModelChange) -> str:
        # 1. Re-executar os 122 controles sobre o novo modelo
        # 2. Gerar LaudoType.TRANSICAO_MODELO com delta comparativo
        # 3. Retornar job_id
        pass
```

#### Critérios de aceitação
- [ ] 122 controles implementados, cada um com `normative_refs` populados com artigo e cláusula específicos
- [ ] Score 0–100 calculado como média ponderada por nível (L1: 30%, L2: 25%, L3: 25%, L4: 20%)
- [ ] RIPD gerado automaticamente para ativos com dados pessoais detectados
- [ ] Model Lifecycle Monitor executa a cada 6h e enfileira revalidação ao detectar mudança de versão
- [ ] Laudo de Transição emitido com delta de score entre versão anterior e nova
- [ ] Todos os laudos emitidos em até 5 minutos após conclusão da avaliação

---

### 4.3 GUARDIAN — Gateway de Runtime, Firewall de Agentes & Human-in-the-Loop

#### Problema resolvido
Auditoria de postura (AEGIS) certifica que as políticas estão correctas. O GUARDIAN garante que essas políticas são aplicadas em tempo real, chamada a chamada. Sem o GUARDIAN, a conformidade certificada pelo AEGIS pode ser violada em milissegundos por um usuário ou agente autónomo.

#### Dependências
- AEGIS activo com políticas configuradas.
- As regras de bloqueio do GUARDIAN são derivadas dos controles L3 e L4 do AEGIS.

#### Arquitectura do proxy

```
Usuário / Agente
      │
      ▼
┌─────────────────┐
│  GUARDIAN Proxy │  ← Instalado entre o cliente e o provider de IA
│                 │
│  1. Auth check  │
│  2. PII scan    │
│  3. Prompt      │
│     injection   │
│     detection   │
│  4. Policy      │
│     evaluation  │
│  5. HITL gate   │
│     (se req.)   │
└────────┬────────┘
         │  PASS
         ▼
   Provider de IA
   (OpenAI, Anthropic, etc.)
         │
         ▼
┌─────────────────┐
│  Response scan  │  ← Scan da resposta antes de devolver ao cliente
│  - PII leak     │
│  - Sensitive    │
│    data filter  │
└────────┬────────┘
         │
         ▼
    Usuário / Agente
         +
    Event logged → WORM
```

#### Modelos de deploy

```python
# services/gov-ai/guardian/proxy/interceptor.py

class GuardianProxy:
    """
    Suporta três modos de deploy:
    
    CLOUD: Proxy hospedado na infraestrutura EZRA (AWS São Paulo).
           Cliente aponta SDK para endpoint EZRA em vez do provider.
           
    VPC:   Proxy deployado dentro da VPC do cliente (ECS task ou K8s pod).
           Dados nunca saem da rede do cliente.
           
    ON_PREMISE: Docker container no data center do cliente.
                Dados não trafegam para nenhuma nuvem.
    """
    
    async def intercept(self, request: AIRequest) -> AIRequest | BlockedEvent:
        checks = [
            self.check_auth(request),
            self.scan_pii(request),
            self.detect_prompt_injection(request),
            self.evaluate_policy(request),
        ]
        
        results = await asyncio.gather(*checks)
        
        if any(r.should_block for r in results):
            event = await self.log_blocked_event(request, results)
            await self.emit_laudo_if_threshold_reached()
            return BlockedEvent(reason=..., event_id=event.id)
        
        if any(r.requires_hitl for r in results):
            return await self.route_to_hitl(request)
        
        return request  # Deixar passar
```

```python
# services/gov-ai/guardian/proxy/prompt_guard.py

class PromptInjectionDetector:
    """
    Detecta padrões de injeção de prompt usando combinação de:
    1. Regex para padrões conhecidos (ignore previous instructions, etc.)
    2. Classificador fine-tuned (modelo leve local, não envia dados ao provider)
    3. Análise de anomalia semântica vs. contexto da sessão
    """
    
    INJECTION_PATTERNS = [
        r"ignore (all |previous |your )?(instructions|rules|constraints)",
        r"you are now (a )?DAN",
        r"pretend you (have no|don't have) (restrictions|guidelines)",
        r"forget (everything|all) (you|I) (told|said)",
        # ... lista mantida e actualizada
    ]
```

#### Critérios de aceitação
- [ ] Latência adicionada pelo proxy inferior a 50ms no percentil 95
- [ ] Taxa de falsos positivos na detecção de injeção de prompt inferior a 2%
- [ ] Modo VPC deployável via `docker run` com configuração de variável de ambiente
- [ ] Cada evento bloqueado gravado no WORM em até 500ms após o bloqueio
- [ ] HITL notifica aprovador via webhook (Slack, Teams, e-mail) em até 5 segundos
- [ ] Painel de Exposição de Runtime (para clientes sem GUARDIAN) actualizado em tempo real

---

## 5. RAMO 2 — GOVERNANÇA MUNICIPAL

### 5.1 RADAR — Inteligência de Captação Federal & Emendas

#### Problema resolvido
Municípios perdem oportunidades de captação porque monitoram o DOU manualmente ou não monitoram. Emendas impositivas (EC 105/2019) são o canal de maior volume financeiro e são as menos monitoradas sistematicamente.

#### Módulos funcionais

```python
# services/gov-municipal/radar/dou_monitor.py

class DOUMonitor:
    """
    Integra com a API oficial do DOU (api.lexml.gov.br) para
    monitoramento em tempo real de publicações relevantes.
    Executa a cada 30 minutos em dias úteis, a cada 2h nos demais.
    """
    DOU_API = "https://api.lexml.gov.br/v1"
    
    RELEVANT_TYPES = [
        "Chamamento Público",
        "Edital de Credenciamento",
        "Portaria de Abertura",
        "Aviso de Licitação",
        "Resolução de Repasse",
    ]
    
    async def monitor(self, tenant_id: str, cnpj: str, keywords: list[str]) -> list[Opportunity]:
        pass

# services/gov-municipal/radar/emenda_monitor.py

class EmendaImpositivaMonitor:
    """
    Monitora emendas impositivas via:
    - API SIOP (siop.planejamento.gov.br/api)
    - Painel do Beneficiário de Emendas Parlamentares
    Filtra por CNPJ do município para identificar emendas alocadas.
    """
    
    async def monitor(self, tenant_id: str, cnpj: str) -> list[Emenda]:
        # 1. Consultar SIOP por beneficiário (CNPJ)
        # 2. Filtrar emendas com status RP 6, 7 ou 8 (executáveis)
        # 3. Verificar prazo de habilitação
        # 4. Retornar com checklist de documentação exigida
        pass
```

#### Critérios de aceitação
- [ ] Monitoramento DOU com latência máxima de 30 minutos após publicação
- [ ] Cobertura de emendas impositivas individuais, de bancada e de comissão (EC 105/2019)
- [ ] Alerta enviado por e-mail + webhook em até 5 minutos após identificação de oportunidade
- [ ] Laudo de elegibilidade emitido com referência ao edital específico e CNPJ analisado

---

### 5.2 VIGÍLIA — Guardião da Regularidade Fiscal & Estadual

#### Problema resolvido
Um município com qualquer certidão vencida no CAUC fica impedido de receber transferências voluntárias federais. A irregularidade pode ser prevenida com antecedência de dias ou semanas mas não há sistema que faça isso automaticamente.

```python
# services/gov-municipal/vigilia/cauc_monitor.py

class CAUCMonitor:
    """
    Monitora regularidade via Transferegov API.
    Executa a cada 4h.
    Classifica cada pendência por urgência (dias até vencimento).
    """
    TRANSFEREGOV_API = "https://api.transferegov.gestao.gov.br/v1"
    
    CRITICALITY_THRESHOLDS = {
        "CRITICAL": 7,    # Vence em até 7 dias
        "WARNING": 30,    # Vence em até 30 dias
        "ATTENTION": 60,  # Vence em até 60 dias
        "OK": 9999,
    }
    
    async def check(self, tenant_id: str, cnpj: str) -> CAUCStatus:
        pass

# services/gov-municipal/vigilia/tce_monitor.py

class TCEMonitor:
    """
    Monitora regularidade perante TCEs estaduais.
    Cada TCE tem API ou sistema próprio — implementação por estado.
    Fase 1: SP, MG, RJ, RS, PR, BA (cobertura de 60% dos municípios).
    Fase 2: demais estados.
    """
    
    TCE_CONNECTORS = {
        "SP": TCE_SP_Connector,
        "MG": TCE_MG_Connector,
        "RJ": TCE_RJ_Connector,
        # ... expansão iterativa
    }
```

#### Critérios de aceitação
- [ ] Verificação CAUC executada a cada 4h com resultado persistido
- [ ] Alerta CRITICAL disparado imediatamente (não aguardar próximo ciclo)
- [ ] Plano de acção gerado automaticamente para cada pendência identificada
- [ ] Cobertura TCE de 6 estados na fase 1 (SP, MG, RJ, RS, PR, BA)
- [ ] Laudo de regularidade emitido com histórico dos últimos 12 meses

---

### 5.3 COMPRAS — Fábrica de Licitações & Instrução Processual

```python
# services/gov-municipal/compras/price_research/painel_precos.py

class PainelPrecosIntegration:
    """
    Integração nativa com Painel de Preços do MPOG via API pública.
    Documentação: https://api.compras.gov.br/pesquisa-preco/v1/swagger-ui.html
    """
    BASE_URL = "https://api.compras.gov.br/pesquisa-preco/v1"
    
    async def search(self, description: str, uasg: str | None = None) -> list[PriceReference]:
        # Retorna referências de preço com:
        # - Valor unitário mediano
        # - Valor unitário médio
        # - UASG de referência
        # - Data da compra
        # - Link para o processo original
        pass

# services/gov-municipal/compras/etp_generator.py

class ETPGenerator:
    """
    Gera Estudos Técnicos Preliminares conforme:
    - Lei 14.133/2021 Art. 18
    - IN SEGES/ME 58/2022 (estrutura obrigatória do ETP)
    """
    
    MANDATORY_SECTIONS = [
        "descrição_necessidade",
        "estimativa_quantidade",
        "levantamento_mercado",
        "descricao_solucao",
        "estimativa_custo",
        "justificativa_modalidade",
        "contratacoes_correlatas",
        "resultados_pretendidos",
        "providencias_contratacao",
        "impacto_ambiental",  # Se aplicável
        "posicao_plan_contratacoes",
    ]
```

#### Critérios de aceitação
- [ ] Integração nativa com Painel de Preços (api.compras.gov.br) operacional
- [ ] Integração nativa com PNCP operacional
- [ ] ETP gerado com todas as seções obrigatórias da IN SEGES/ME 58/2022
- [ ] TR gerado com especificações técnicas e critérios de aceitação preenchidos
- [ ] Laudo de justificativa de preços com referência explícita às fontes consultadas e metodologia

---

### 5.4 EXECUTA — Monitor de Execução & Conformidade de Objeto *(produto novo)*

#### Problema resolvido
O gap mais frequente e menos visível do ciclo de convênios: municípios tornam-se inadimplentes técnicos durante a execução, não na prestação de contas final. O cronograma físico diverge do financeiro sem justificativa formalizada e ninguém percebe até a visita do fiscal.

```python
# services/gov-municipal/executa/physical_monitor.py

class PhysicalExecutionMonitor:
    """
    Monitora execução física vs. financeira de convênios.
    Dados de entrada:
    - Cronograma físico-financeiro aprovado (upload pelo gestor)
    - Desembolsos realizados (integração com conta vinculada via OFX/CNAB)
    - Relatórios de execução (upload periódico ou integração Transferegov)
    """
    
    async def check_deviation(self, convenio_id: str) -> DeviationReport:
        physical_progress = await self.get_physical_progress(convenio_id)
        financial_progress = await self.get_financial_progress(convenio_id)
        
        deviation = physical_progress - financial_progress
        
        if abs(deviation) > 0.10:  # Desvio superior a 10%
            return DeviationReport(
                level="WARNING" if abs(deviation) < 0.20 else "CRITICAL",
                deviation_pct=deviation,
                days_to_justification_deadline=...,
                recommended_action=...,
            )
```

#### Critérios de aceitação
- [ ] Integração com extratos OFX/CNAB de contas vinculadas
- [ ] Alerta de desvio disparado quando divergência físico-financeira supera 10%
- [ ] Alerta CRITICAL quando desvio supera 20% ou prazo de justificativa é inferior a 15 dias
- [ ] Laudo de conformidade de objeto emitido mensalmente e sob demanda

---

### 5.5 ALERTA — SOS Diligências & Destravador Transferegov

#### Por que é o MVP do Ramo 2
- Dor com prazo fatal: o município já perdeu dinheiro por isso antes
- ROI imediato e mensurável: um convênio salvo cobre anos de assinatura
- Demonstração em 30 minutos com um caso real
- Porta de entrada natural para upsell de EXECUTA e PROVA

```python
# services/gov-municipal/alerta/notification_parser/ocr_pipeline.py

class NotificationOCRPipeline:
    """
    Pipeline de extração em duas camadas para heterogeneidade de formatos:
    
    Camada 1 — Extracção estrutural:
    - PDFs com texto seleccionável: extracção directa via pdfplumber
    - PDFs scaneados: AWS Textract (OCR com layout awareness)
    - Formato DOCX: python-docx
    
    Camada 2 — Validação semântica:
    - LLM local (modelo leve: Llama 3.1 8B ou equivalente) classifica
      o tipo de pendência e extrai dados estruturados
    - Não envia dados do município para APIs externas nesta etapa
    
    LIMITAÇÃO DECLARADA EM CONTRATO:
    Formatos não suportados na fase 1:
    - Plantas de engenharia (CAD/DWG)
    - Vídeos e áudios de vistoria
    - Planilhas com macros complexas
    """
    
    SUPPORTED_FORMATS = [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".jpg", ".png"]
    
    async def extract(self, file: bytes, mime_type: str) -> ExtractedNotification:
        pass

# services/gov-municipal/alerta/notification_parser/classifier.py

class PendencyClassifier:
    PENDENCY_TYPES = [
        "ENGENHARIA",       # Medição, ART, memorial descritivo
        "CONTABILIDADE",    # Conciliação, nota fiscal, extrato
        "JURIDICA",         # Documentação societária, ata, procuração
        "DOCUMENTAL",       # Certidões, declarações, formulários
        "TECNICA_OBJETO",   # Conformidade com plano de trabalho
    ]
    
    async def classify(self, notification: ExtractedNotification) -> ClassifiedPendency:
        pass
```

#### Critérios de aceitação
- [ ] Pipeline OCR processa PDF de até 50 páginas em até 30 segundos
- [ ] Taxa de classificação correcta de pendência superior a 85% (medida em conjunto de testes)
- [ ] Ofício de Resposta gerado dentro do formato oficial do ministério concedente
- [ ] Lista de formatos não suportados declarada explicitamente na UI e no contrato
- [ ] Laudo de saneamento emitido com protocolo de envio registado

---

### 5.6 PROVA — Auditor de Despesas, Conciliação & Prestação de Contas

```python
# services/gov-municipal/prova/nfe_integration.py

class NFEIntegration:
    """
    Integração via WebService SEFAZ (protocolo padrão nacional).
    Endpoint varia por estado mas protocolo SOAP é uniforme.
    Consulta NF-e por chave de acesso (44 dígitos).
    """
    
    SEFAZ_ENDPOINTS = {
        "SP": "https://nfe.fazenda.sp.gov.br/ws/nfeConsultaProtocolo4.asmx",
        "MG": "https://nfe.fazenda.mg.gov.br/nfe/services/NFeConsultaProtocolo4",
        # ... todos os 27 estados + DF
    }
    
    async def validate_nfe(self, chave_acesso: str, estado: str) -> NFEValidationResult:
        # Valida autenticidade da NF-e directamente na SEFAZ
        # Retorna: status, valor, emitente, destinatário, data
        pass

# services/gov-municipal/prova/sinapi_parser.py

class SINAPIParser:
    """
    Integração com tabela SINAPI (IBGE/CEF).
    SINAPI é publicado mensalmente em formato XLSX pela CEF.
    Endpoint de download: https://www.caixa.gov.br/Downloads/sinapi-referencia-insumos-e-composicoes/
    """
    
    async def validate_price(self, item_code: str, uf: str, reference_month: str) -> SINAPIItem:
        pass
    
    async def parse_medicao_pdf(self, medicao_bytes: bytes) -> MedicaoReport:
        """
        Suporte declarado em contrato para formatos de medição:
        - Planilha SINAPI padrão CEF (XLSX)
        - PDF de boletim de medição com layout tabular
        
        NÃO suportado na fase 1:
        - Plantas de engenharia
        - Formatos proprietários de software de obra (MS Project, Primavera)
        """
        pass
```

#### Critérios de aceitação
- [ ] Validação de NF-e operacional para todos os 26 estados + DF
- [ ] Parser SINAPI actualizado mensalmente via download automático da tabela CEF
- [ ] Pagamentos com divergência travados antes da execução com notificação ao gestor
- [ ] Laudo de prestação de contas emitido com cadeia de evidências rastreável do empenho ao pagamento

---

## 6. INFRAESTRUTURA, HOSPEDAGEM E SOBERANIA DE DADOS

### 6.1 Recomendação de Hospedagem

**Decisão recomendada: AWS São Paulo (sa-east-1)**

**Justificativa:**

| Critério | AWS sa-east-1 | GCP São Paulo | Azure Brazil South |
|---|---|---|---|
| Maturidade em compliance LGPD | Alta (BCR certificado) | Alta | Alta |
| S3 Object Lock (WORM) | Nativo | Equivalente (GCS) | Equivalente (Blob) |
| Cobertura de serviços gerenciados | Maior | Média | Alta |
| Referência no mercado GovTech BR | Predominante | Crescente | Média |
| Custo estimado para early stage | Médio | Médio | Médio |

**Não recomendado para fase 1:** Localweb, UOL Host, KingHost. Ausência de Object Lock nativo, sem SLA de 99,9% para serviços de banco de dados gerenciado, e ausência de suporte a deploy containerizado com auto-scaling.

### 6.2 Arquitectura AWS

```hcl
# infra/terraform/aws/vpc.tf

# Uma VPC por ambiente (prod, staging, dev)
# Subnets privadas para todos os serviços de backend
# Subnets públicas apenas para ALB (Application Load Balancer)
# NAT Gateway para acesso de saída controlado

# infra/terraform/aws/ecs.tf
# ECS Fargate — um cluster por ramo, um serviço por produto
# Auto-scaling baseado em CPU e número de mensagens na fila SQS

# infra/terraform/aws/rds.tf
# PostgreSQL 16 Multi-AZ (RDS)
# Backup automático diário, retenção 35 dias
# Encriptação em repouso com KMS (chave por tenant)

# infra/terraform/aws/s3_worm.tf
# S3 com Object Lock habilitado no nível do bucket
# Default retention: COMPLIANCE mode, 10 anos
# Versioning obrigatório (requisito para Object Lock)
# Encriptação SSE-KMS com chave por tenant
```

### 6.3 Ambiente de Desenvolvimento Local

```yaml
# infra/docker/docker-compose.dev.yml

version: '3.9'
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: dev_password
    ports: ["5432:5432"]
    volumes: ["postgres_data:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  localstack:
    image: localstack/localstack:3
    environment:
      SERVICES: s3,sqs,kms
      DEFAULT_REGION: sa-east-1
    ports: ["4566:4566"]
    # Simula S3 WORM e SQS localmente

  web:
    build: ./apps/web
    ports: ["3000:3000"]
    depends_on: [postgres, redis]

  sentinel:
    build: ./services/gov-ai/sentinel
    ports: ["8001:8000"]
    depends_on: [postgres, redis, localstack]

  aegis:
    build: ./services/gov-ai/aegis
    ports: ["8002:8000"]
    depends_on: [postgres, redis, localstack, sentinel]

  guardian:
    build: ./services/gov-ai/guardian
    ports: ["8003:8000"]
    depends_on: [postgres, redis, localstack, aegis]

  # ... serviços gov-municipal
```

---

## 7. SEGURANÇA

### 7.1 Princípios de Segurança

- **Zero Trust:** Nenhum serviço confia implicitamente em outro. Cada chamada interna é autenticada via JWT de serviço com escopo limitado.
- **Encriptação em trânsito:** TLS 1.3 obrigatório em todas as comunicações internas e externas.
- **Encriptação em repouso:** KMS com chave gerenciada por tenant para RDS e S3.
- **Princípio do menor privilégio:** IAM roles com permissões mínimas por serviço ECS.
- **Auditoria de acesso:** Todo acesso a dados de tenant gravado em log imutável separado.

### 7.2 Conformidade LGPD

| Obrigação LGPD | Implementação |
|---|---|
| Art. 37 — Registro de operações | Log de todas as operações de tratamento por tenant |
| Art. 38 — RIPD | Gerado automaticamente pelo AEGIS para ativos com dados pessoais |
| Art. 46 — Medidas de segurança | Encriptação KMS + S3 Object Lock + TLS 1.3 |
| Art. 33 — Transferência internacional | Proibido por construção (AWS sa-east-1 exclusivo) |
| Art. 18 — Direitos do titular | API de exportação e deleção (exceto dados em cofre WORM) |

**Nota sobre WORM e direito ao esquecimento:** Dados gravados em S3 Object Lock COMPLIANCE não podem ser deletados dentro do período de retenção — nem pelo titular, nem pela EZRA. Esta limitação deve ser declarada explicitamente no contrato com o cliente e na política de privacidade. A base legal para retenção é o Art. 16, II (exercício regular de direitos em processo judicial, administrativo ou arbitral) e Art. 37 (dever de manutenção de registos).

---

## 8. MODELO DE MULTI-TENANCY E WHITE-LABEL

### 8.1 Hierarquia de tenants

```
EZRA (root)
  └── WhitelabelOperator (banca, contabilidade, associação)
        └── EndClient (empresa, município, ONG)
```

**Regras:**
- Um WhitelabelOperator pode ter N EndClients
- Um EndClient pertence a exactamente um WhitelabelOperator ou directamente à EZRA
- Laudos emitidos para EndClient sob WhitelabelOperator carregam a identidade do Operator como signatário
- O hash SHA-256 e o cofre WORM são sempre da EZRA, independentemente da hierarquia

### 8.2 Resolução de subdomínio

```typescript
// apps/web/middleware.ts

export async function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') || ''

  // ezra.com.br → tenant padrão EZRA
  // cliente.ezra.com.br → tenant "cliente"
  // auditoria.bancaxyz.com.br → lookup por customDomain → tenant white-label
  
  const tenant = await resolveTenant(hostname)
  
  // Injectar tenant no header para downstream
  const headers = new Headers(request.headers)
  headers.set('x-tenant-id', tenant.id)
  headers.set('x-tenant-branch', tenant.branch)
  
  return NextResponse.next({ request: { headers } })
}
```

### 8.3 Theme provider white-label

```typescript
// apps/web/components/white-label/ThemeProvider.tsx

export function EzraThemeProvider({ config, children }: {
  config: WhitelabelConfig
  children: React.ReactNode
}) {
  return (
    <div
      style={{
        '--color-primary': config.primaryColor,
        '--color-secondary': config.secondaryColor,
      } as React.CSSProperties}
    >
      {children}
    </div>
  )
}
```

---

## 9. CONTRATOS DE API — PRINCÍPIOS GERAIS

### 9.1 Convenções obrigatórias para todos os serviços FastAPI

```python
# services/shared/api/conventions.py

"""
CONVENÇÕES OBRIGATÓRIAS:

1. Todos os endpoints recebem x-tenant-id no header (injectado pelo middleware Next.js)
2. Respostas de erro seguem RFC 7807 (Problem Details)
3. Operações longas (varredura, auditoria) retornam 202 Accepted + job_id
4. Status de jobs consultado via GET /jobs/{job_id}
5. Webhooks disparados ao completar jobs (configurável por tenant)
6. Paginação via cursor (não offset) para listas grandes
7. Rate limiting: 100 req/min por tenant por serviço
8. Versão na URL: /v1/...
"""

from fastapi import FastAPI, Header, Depends
from fastapi.middleware.cors import CORSMiddleware

def create_service(name: str) -> FastAPI:
    app = FastAPI(
        title=f"EZRA — {name}",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://*.ezra.com.br"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app
```

### 9.2 Modelo de resposta de job assíncrono

```python
# services/shared/api/schemas.py

from pydantic import BaseModel
from enum import Enum

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    progress_pct: int | None = None
    result_url: str | None = None   # Disponível quando status = COMPLETED
    error: str | None = None        # Disponível quando status = FAILED
    laudo: LaudoResult | None = None # Disponível quando status = COMPLETED

class ProblemDetail(BaseModel):
    """RFC 7807"""
    type: str
    title: str
    status: int
    detail: str
    instance: str
```

---

## 10. SEQUÊNCIA DE IMPLEMENTAÇÃO E DEPENDÊNCIAS

### 10.1 Fases de desenvolvimento

**FASE 0 — Núcleo (Semanas 1–4)**
Nenhum produto pode ser entregue sem esta fase.

- [ ] Monorepo configurado (Turborepo + workspaces)
- [ ] Autenticação e RBAC (NextAuth + JWT middleware)
- [ ] Modelo de tenant e schema-per-tenant no PostgreSQL
- [ ] Motor de laudos (LaudoEngine completo e testado)
- [ ] Cadeia SHA-256 (HashChain)
- [ ] Cofre WORM (WORMVault com S3 Object Lock em LocalStack local)
- [ ] Motor de white-label (ThemeProvider + resolução de subdomínio)
- [ ] Shell de dashboard (Next.js App Router com roteamento por ramo)
- [ ] Docker Compose de desenvolvimento local completo
- [ ] CI/CD pipeline (GitHub Actions → ECS staging)

**FASE 1 — MVP Ramo 1 (Semanas 5–10)**

- [ ] SENTINEL: Network Scanner + Shadow SaaS Detector + Factsheet Generator
- [ ] AEGIS: L1 (38 controles) + Scoring + RIPD + Model Lifecycle Monitor
- [ ] Seed dos 122 controles (scripts/seed_controls.py)
- [ ] Seed do mapeamento normativo (scripts/seed_normative_map.py)
- [ ] Frontend: páginas SENTINEL e AEGIS

**FASE 2 — MVP Ramo 2 (Semanas 9–14, paralelo com fase 1 a partir da semana 9)**

- [ ] ALERTA: OCR Pipeline + Classificador + Response Generator (MVP Ramo 2)
- [ ] VIGÍLIA: CAUC Monitor + Alert Engine
- [ ] Frontend: páginas ALERTA e VIGÍLIA

**FASE 3 — Completar Ramo 1 (Semanas 11–16)**

- [ ] AEGIS: L2, L3, L4 (84 controles restantes)
- [ ] GUARDIAN: Proxy + Prompt Guard + Data Filter + HITL + Event Logger
- [ ] Frontend: página GUARDIAN + Painel de Exposição de Runtime

**FASE 4 — Completar Ramo 2 (Semanas 15–22)**

- [ ] RADAR: DOU Monitor + Emenda Monitor + Eligibility
- [ ] COMPRAS: ETP Generator + TR Generator + integrações de preços
- [ ] EXECUTA: Physical Monitor + Deviation Alert
- [ ] PROVA: NF-e Integration + SINAPI Parser + Extract Reconciler

**FASE 5 — White-label & Admin (Semanas 20–24)**

- [ ] Painel admin EZRA (gestão de tenants, billing, configuração white-label)
- [ ] Domínio customizado por white-label operator
- [ ] Billing engine (precificação por outcome, integração Stripe ou Pagar.me)

### 10.2 Grafo de dependências

```
SHARED CORE
    ├── SENTINEL (R1-P1)
    │       └── AEGIS (R1-P2)
    │               └── GUARDIAN (R1-P3)
    │
    ├── ALERTA (R2-P5) ← MVP independente
    │
    ├── VIGÍLIA (R2-P2)
    │
    ├── RADAR (R2-P1)
    │
    ├── COMPRAS (R2-P3)
    │
    ├── EXECUTA (R2-P4)
    │       └── PROVA (R2-P6)
    │
    └── PROVA (R2-P6)
```

**Nota:** Os produtos do Ramo 2 são tecnicamente independentes entre si (exceto EXECUTA → PROVA). A dependência entre eles é comercial (sequência do ciclo de convênio), não técnica.

---

## 11. CRITÉRIOS DE ACEITAÇÃO GLOBAIS

### 11.1 Performance

| Métrica | Alvo |
|---|---|
| Latência P95 de endpoints síncronos | < 300ms |
| Latência adicionada pelo GUARDIAN Proxy | < 50ms |
| Tempo de geração de laudo (simples) | < 60s |
| Tempo de geração de laudo (auditoria completa) | < 5min |
| Disponibilidade (SLA) | 99,5% |
| Tempo de detecção de mudança de modelo (AEGIS) | < 6h |
| Latência de alerta CAUC CRITICAL | < 5min após detecção |

### 11.2 Segurança

| Requisito | Verificação |
|---|---|
| Nenhum dado cross-tenant acessível | Teste de penetração por tenant isolado |
| WORM imutável | Tentativa de deleção via AWS CLI deve falhar |
| SHA-256 verificável externamente | Script de verificação documentado e público |
| TLS 1.3 em todos os endpoints | Scan SSL Labs mínimo A |
| Nenhum dado fora de sa-east-1 | AWS Config rule + alertas de VPC flow log |

### 11.3 Qualidade de código

| Requisito | Ferramenta |
|---|---|
| Cobertura de testes unitários mínima | 80% (Python: pytest, TS: Vitest) |
| Type coverage TypeScript | strict mode sem `any` explícito |
| Linting Python | Ruff |
| Linting TypeScript | ESLint + Biome |
| Testes de integração por serviço | Mínimo 1 por endpoint público |
| Testes E2E por produto | Playwright — happy path + laudo emitido |

---

## APÊNDICE A — VARIÁVEIS DE AMBIENTE OBRIGATÓRIAS

```bash
# .env.example (nunca commitar valores reais)

# Shared
DATABASE_URL=postgresql://user:pass@localhost:5432/ezra
REDIS_URL=redis://localhost:6379
JWT_SECRET=
JWT_SERVICE_SECRET=  # Para comunicação inter-serviços

# AWS
AWS_REGION=sa-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_WORM_BUCKET=ezra-worm-vault-prod
SQS_JOBS_QUEUE_URL=

# KMS (uma chave por tenant em prod; chave compartilhada em dev)
KMS_DEFAULT_KEY_ID=

# Next.js
NEXTAUTH_SECRET=
NEXTAUTH_URL=https://app.ezra.com.br

# Serviços externos — Ramo 2
TRANSFEREGOV_API_KEY=
DOU_API_KEY=
SIOP_API_KEY=
PNCP_API_KEY=

# LLM local (ALERTA — classificador de pendências)
LOCAL_LLM_MODEL_PATH=/models/llama-3.1-8b
LOCAL_LLM_GPU_LAYERS=0  # CPU-only em dev; ajustar em prod
```

---

## APÊNDICE B — GLOSSÁRIO TÉCNICO

| Termo | Definição no contexto da EZRA |
|---|---|
| AGCP | Algorithmic Governance Compliance Protocol — framework proprietário dos 122 controles |
| WORM | Write Once Read Many — modelo de armazenamento imutável implementado via S3 Object Lock |
| Chain Hash | SHA-256 encadeado: hash do laudo N combinado com hash do laudo N-1 |
| Shadow AI | Modelos ou serviços de IA em uso na organização sem autorização ou inventário formal |
| Shadow SaaS | SaaS de terceiros com IA embutida acessado por usuários corporativos sem controlo da TI |
| HITL | Human-in-the-Loop — mecanismo de aprovação humana para acções de agentes autónomos |
| CAUC | Cadastro Único de Convênios — sistema federal de regularidade para transferências voluntárias |
| RIPD | Relatório de Impacto à Proteção de Dados Pessoais (LGPD Art. 38) |
| ETP | Estudo Técnico Preliminar (Lei 14.133/2021 Art. 18) |
| TR | Termo de Referência — documento de especificação para contratações públicas |
| Tenant | Cliente (empresa ou município) com namespace isolado na plataforma |
| White-label Operator | Banca de advocacia, contabilidade ou associação que opera a EZRA sob sua própria marca |
| Object Lock COMPLIANCE | Modo AWS S3 que impede deleção mesmo por administradores com permissões elevadas |
```
