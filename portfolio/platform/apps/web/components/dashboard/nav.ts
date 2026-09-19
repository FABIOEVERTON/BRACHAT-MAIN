// Dashboard shell props — usado por (dashboard)/layout.
// Estrutura de layout consistente: sidebar (ramos) + header (tenant/brand).
export interface DashboardNavItem {
  href: string;
  label: string;
  product: string;
}

export const RAMO_1_NAV: DashboardNavItem[] = [
  { href: '/gov-ai/sentinel', label: 'Sentinel', product: 'sentinel' },
  { href: '/gov-ai/aegis', label: 'Aegis', product: 'aegis' },
  { href: '/gov-ai/guardian', label: 'Guardian', product: 'guardian' },
];

export const RAMO_2_NAV: DashboardNavItem[] = [
  { href: '/gov-municipal/radar', label: 'Radar', product: 'radar' },
  { href: '/gov-municipal/vigilia', label: 'Vigília', product: 'vigilia' },
  { href: '/gov-municipal/compras', label: 'Compras', product: 'compras' },
  { href: '/gov-municipal/executa', label: 'Executa', product: 'executa' },
  { href: '/gov-municipal/alerta', label: 'Alerta', product: 'alerta' },
  { href: '/gov-municipal/prova', label: 'Prova', product: 'prova' },
];

// F0-38: integração com tema white-label (regra S08) — sem quebra de layout
export function brandByTenant(tenantId: string): { name: string; color: string } {
  // FASE 0: registry estático; FASE 5: lookup live
  if (tenantId === 'bancaxyz') return { name: 'Banco XYZ', color: '#0F4C81' };
  return { name: 'EZRA', color: '#111827' };
}

// F0-45: novos produtos Ramo 3 — Governança Regulatória & Legislativa (RIG Tech)
export const RAMO_3_NAV: DashboardNavItem[] = [
  { href: '/gov-regulatorio/lex', label: 'LEX', product: 'lex' },
  { href: '/gov-regulatorio/vanguarda', label: 'VANGUARDA MINERAL', product: 'vanguarda' },
];