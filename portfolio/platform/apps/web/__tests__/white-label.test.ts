// White-label: resolução + theme + assinatura + headers de tenant (E0-S08).
import { describe, expect, it } from 'vitest';

import { poweredByText, themeVars, laudoSignatory } from '../components/white-label/theme';
import { resolveTenant, seedWhitelabel } from '../lib/tenant';
import { resolveTenantHeadersForHost } from '../middleware';

describe('E0-S08 · white-label', () => {
  const bancaxyz = seedWhitelabel.bySlug.get('bancaxyz')!;

  it('F0-30 subdomain ezra -> slug tenant', async () => {
    // subdomain seeded → config white-label
    const seeded = await resolveTenant('bancaxyz.ezra.com.br');
    expect(seeded).toMatchObject({ tenantSlug: 'bancaxyz' });

    // subdomain não-seeded → null (FASE 0: registry estático, sem DB)
    expect(await resolveTenant('prefeitura-x.ezra.com.br')).toBeNull();
  });

  it('F0-31 customDomain -> config via lookup', async () => {
    const cfg = await resolveTenant('auditoria.bancaxyz.com.br');
    expect(cfg).not.toBeNull();
    expect(cfg!.tenantSlug).toBe('bancaxyz');
    expect(cfg!.customDomain).toBe('auditoria.bancaxyz.com.br');
  });

  it('F0-32 theme vars + branding + hidePoweredBy', () => {
    const vars = themeVars(bancaxyz);
    expect(vars['--color-primary']).toBe(bancaxyz.primaryColor);
    expect(vars['--color-secondary']).toBe(bancaxyz.secondaryColor);

    // hidePoweredBy=false -> EZRA apenas como sistema de suporte (nunca signatária)
    expect(poweredByText(bancaxyz)).toContain('Sistema tecnológico');
    // hidePoweredBy=true -> sem referência visual a EZRA
    expect(poweredByText({ ...bancaxyz, hidePoweredBy: true })).toBeNull();
    // tenant default EZRA
    expect(poweredByText()).toBe('Plataforma EZRA');
  });

  it('F0-33 signatário do laudo é o operador white-label', () => {
    const signer = laudoSignatory(bancaxyz);
    expect(signer.name).toBe('Maria Silva');
    expect(signer.register).toContain('CRC');
    // Cofre WORM nunca transferível
    expect(signer).not.toHaveProperty('worm');
  });

  it('F0-34 headers x-tenant-id e x-tenant-branch injetados', async () => {
    const h = await resolveTenantHeadersForHost('prefeitura-x.ezra.com.br');
    expect(h['x-tenant-id']).toBe('prefeitura-x');
    expect(h['x-tenant-branch']).toBe('gov_ai');
  });
});