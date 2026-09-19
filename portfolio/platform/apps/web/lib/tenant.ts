// Resolução de tenant white-label (PRD §3.6, ADR-006).
// Slots: lookup por subdomínio ezra (F0-30) e por customDomain (F0-31).
// Cache curto TTL 5min (NFR S08: resolveTenant < 50ms).
import type { WhitelabelConfig } from '@ezra/types';

export interface TenantRegistry {
  bySlug: Map<string, WhitelabelConfig>;
  byCustomDomain: Map<string, WhitelabelConfig>;
}

// FASE 0: registry fixo (provisionado via seed); FASE 5: admin white-label
// grava aqui (mesma interface). resolveTenant assíncrono p/ futuro fetch.
export const seedWhitelabel: TenantRegistry = {
  bySlug: new Map([
    [
      'bancaxyz',
      {
        tenantSlug: 'bancaxyz',
        brandName: 'Banco XYZ Auditoria',
        logoUrl: 'https://cdn.bancaxyz.com.br/logo.png',
        primaryColor: '#0F4C81',
        secondaryColor: '#D4AF37',
        supportEmail: 'suporte@bancaxyz.com.br',
        laudoSignatoryName: 'Maria Silva',
        laudoSignatoryTitle: 'Perita Contábil — CRC/SP 1SP234567',
        laudoSignatoryRegister: 'CRC/SP 1SP234567',
        customDomain: 'auditoria.bancaxyz.com.br',
        hidePoweredBy: false,
      },
    ],
  ]),
  byCustomDomain: new Map(),
};

// customDomain aponta para a mesma config do bySlug (referência, não cópia)
const bancaxyz = seedWhitelabel.bySlug.get('bancaxyz')!;
seedWhitelabel.byCustomDomain.set(bancaxyz.customDomain!, bancaxyz);

export async function resolveTenant(hostname: string): Promise<WhitelabelConfig | null> {
  const root = hostname.replace(/^www\./, '').toLowerCase();

  // F0-31: domínio custom white-label primeiro (prioridade de match)
  const byDomain = seedWhitelabel.byCustomDomain.get(root);
  if (byDomain) return byDomain;

  // F0-30: subdomínio ezra → slug (tenant white-label do registry ou esqueleto)
  if (root !== 'ezra.com.br' && root.endsWith('.ezra.com.br')) {
    const slug = root.split('.')[0] ?? '';
    const seeded = seedWhitelabel.bySlug.get(slug);
    if (seeded) return seeded;
    // subdomínio conhecido de tenant EZRA default (F0-30)
    return null;
  }

  return null;
}

// TTL cache (FASE 0: registries estáticos — o cache entra quando for DB/API)
export const WHITELABEL_CACHE_TTL_MS = 5 * 60 * 1000;