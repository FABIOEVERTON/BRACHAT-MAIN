// Tipos compartilhados da Plataforma EZRA — PRD §3.1 (auth), §3.6 (whitelabel), §3.3 (laudo)
// Font: packages/types/src

export type Role =
  | 'EZRA_ADMIN'
  | 'TENANT_ADMIN'
  | 'TENANT_AUDITOR'
  | 'TENANT_VIEWER'
  | 'WHITELABEL_OPERATOR'
  | 'WHITELABEL_ADMIN';

export type Permission =
  | 'laudo:emit'
  | 'laudo:view'
  | 'scan:execute'
  | 'monitor:configure'
  | 'gateway:configure'
  | 'tenant:manage'
  | 'billing:view'
  | 'whitelabel:configure';

export type Branch = 'gov_ai' | 'gov_municipal';
export type Plan = 'direct' | 'whitelabel';
export type TenantStatus = 'active' | 'suspended' | 'trial';

export interface Tenant {
  id: string; // UUID
  slug: string; // subdomínio
  branch: Branch;
  plan: Plan;
  whitelabelConfigId?: string;
  activeProducts: string[];
  chainAnchorHash?: string; // Hash do primeiro laudo emitido
  createdAt: string;
  status: TenantStatus;
}

// PRD §3.6
export interface WhitelabelConfig {
  tenantSlug: string;
  brandName: string;
  logoUrl: string;
  primaryColor: string;
  secondaryColor: string;
  supportEmail: string;
  laudoSignatoryName: string;
  laudoSignatoryTitle: string;
  laudoSignatoryRegister: string; // CRC, OAB, CREA
  customDomain: string | null;
  hidePoweredBy: boolean;
}

// PRD §3.3 — tipos de laudo (10)
export type LaudoType =
  | 'LAI' // INVENTARIO_ALGORITIMICO
  | 'LCA' // CONFORMIDADE_ALGORITIMICA
  | 'LTM' // TRANSICAO_MODELO
  | 'LIR' // INTEGRIDADE_RUNTIME
  | 'LEO' // ELEGIBILIDADE_ORCAMENTARIA
  | 'LRF' // REGULARIDADE_FISCAL
  | 'LJP' // JUSTIFICATIVA_PRECOS
  | 'LCO' // CONFORMIDADE_OBJETO
  | 'LSD' // SANEAMENTO_DILIGENCIAS
  | 'LPC'; // PRESTACAO_CONTAS

export interface LaudoResult {
  laudoId: string; // UUID único
  laudoNumber: string; // ex: LAI-2026-0042
  sha256Hash: string; // hash do conteúdo
  chainHash: string; // SHA256(laudo_hash + previous_chain_hash)
  wormKey: string; // chave S3
  pdfUrl: string; // URL assinada 1h
  emittedAt: string;
}

export interface LaudoRequest {
  tenantId: string;
  productId: string;
  laudoType: LaudoType;
  payload: Record<string, unknown>;
  generatedBy: string; // user_id ou agent_id
  normativeRefs: string[];
}

// PRD §3.6 — campos EXATOS (ADR-006 white-label first-class)
export interface WhitelabelConfig {
  tenantSlug: string;
  brandName: string;
  logoUrl: string;
  primaryColor: string;
  secondaryColor: string;
  supportEmail: string;
  laudoSignatoryName: string; // Nome do signatário nos laudos
  laudoSignatoryTitle: string; // Cargo do signatário
  laudoSignatoryRegister: string; // CRC, OAB, CREA conforme o caso
  customDomain: string | null; // dominio.advocacia.com.br
  hidePoweredBy: boolean;
}

// PRD §3.6 regra crítica: hash + WORM sempre da EZRA, nunca transferíveis.
export interface LaudoSignatory {
  name: string;
  title: string;
  register: string;
}

export function signatoryFromWhitelabel(wl: WhitelabelConfig): LaudoSignatory {
  return {
    name: wl.laudoSignatoryName,
    title: wl.laudoSignatoryTitle,
    register: wl.laudoSignatoryRegister,
  };
}

// JWT claims (PRD §3.1) — F0-07
export interface JwtClaims {
  sub: string;
  role: Role;
  permissions: Permission[];
  tenant_id: string | null;
  iat: number;
  exp: number;
  typ: 'access' | 'refresh';
}