// Resolução de subdomínio → tenant (PRD §8.2, F0-34).
// Pure function testável sem Next. O thin edge middleware (next/server) entra na E0-S09.

export type TenantBranch = 'gov_ai' | 'gov_municipal';

export interface TenantContextHeaders {
  'x-tenant-id': string;
  'x-tenant-branch': TenantBranch;
}

// S08: lookup white-label real (customDomain começa do registry lib/tenant.ts).
import { resolveTenant } from './tenant';

export async function resolveTenantHeaders(hostname: string): Promise<TenantContextHeaders> {
  const root = hostname.replace(/^www\./, '').toLowerCase();
  const config = await resolveTenant(hostname);

  if (config) {
    return { 'x-tenant-id': config.tenantSlug, 'x-tenant-branch': 'gov_municipal' };
  }

  // Subdomínio ezra genérico (mesmo sem seed): slug = primeiro label (F0-34)
  if (root !== 'ezra.com.br' && root.endsWith('.ezra.com.br')) {
    return { 'x-tenant-id': root.split('.')[0] ?? 'ezra', 'x-tenant-branch': 'gov_ai' };
  }

  // tenant EZRA default (gov_ai)
  return { 'x-tenant-id': 'ezra', 'x-tenant-branch': 'gov_ai' };
}

// Sync fallback (uso em FASE-0 na ausência de async edge loader)
export function resolveTenantSync(hostname: string): TenantContextHeaders {
  const root = hostname.replace(/^www\./, '').toLowerCase();
  const isEzra = root === 'ezra.com.br' || root.endsWith('.ezra.com.br');

  if (isEzra) {
    const slug = root === 'ezra.com.br' ? 'ezra' : (root.split('.')[0] ?? 'ezra');
    return { 'x-tenant-id': slug, 'x-tenant-branch': 'gov_ai' };
  }

  // customDomain white-label (S08: registry estático com cache curto)
  const byCustom = seedByCustomDomain(root);
  if (byCustom) {
    return { 'x-tenant-id': byCustom, 'x-tenant-branch': 'gov_municipal' };
  }

  return { 'x-tenant-id': root.split('.')[0] ?? 'ezra', 'x-tenant-branch': 'gov_municipal' };
}

function seedByCustomDomain(root: string): string | undefined {
  // FASE 0: espelha o registry estático de lib/tenant.ts (mesmo objeto).
  // Mapa estático aqui p/ manter tenant-resolver autossuficiente (testável).
  const customMap: Record<string, string> = {
    'auditoria.bancaxyz.com.br': 'bancaxyz',
  };
  return customMap[root];
}