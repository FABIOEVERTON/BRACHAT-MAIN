// Dashboard shell libs (E0-S09): api-client, laudo, theme.
import { describe, expect, it, vi } from 'vitest';

import { downloadLink, laudoFields } from '../components/laudo/laudo-card';
import { ApiClient, resolveBaseUrl } from '../lib/api-client';
import { resolveTenantHeadersForHost } from '../middleware';
import { poweredByText, themeVars } from '../components/white-label/theme';
import { seedWhitelabel } from '../lib/tenant';

const laudo = {
  laudo_id: 'abc123',
  laudo_number: 'LAI-2026-0042',
  sha256_hash: 'a'.repeat(64),
  chain_hash: 'b'.repeat(64),
  worm_key: 't1/LAI/2026-01-01T00-00-00.pdf',
  pdf_url: 'http://localhost:4566/ezra-worm/t1/LAI/2026-01-01T00-00-00.pdf',
  emitted_at: '2026-01-01T00:00:00Z',
};

describe('E0-S09 · shell libs', () => {
  it('F0-36 api-client injeta x-tenant-id + base URL por produto', () => {
    const c = new ApiClient({ product: 'sentinel', tenantId: 'prefeitura-x' });
    expect(c.baseUrl).toBe('http://localhost:8001');
    expect(c.authHeaders()['x-tenant-id']).toBe('prefeitura-x');
    expect(c.authHeaders()['content-type']).toBe('application/json');

    expect(resolveBaseUrl('compras')).toBe('http://localhost:9003');
    expect(() => resolveBaseUrl('fantasma')).toThrow();
  });

  it('F0-37 componente laudo mostra SHA-256 + chain + link download', () => {
    const fields = laudoFields(laudo);
    const sha = fields.find((f) => f.label === 'SHA-256');
    const chain = fields.find((f) => f.label === 'Cadeia (chain)');
    expect(sha?.value).toBe('a'.repeat(64));
    expect(chain?.value).toBe('b'.repeat(64));
    expect(downloadLink(laudo)).toBe(laudo.pdf_url);
  });

  it('F0-38 theme white-label aplicado sem quebra + headers branco', async () => {
    const bancaxyz = seedWhitelabel.bySlug.get('bancaxyz')!;
    const vars = themeVars(bancaxyz);
    expect(vars['--color-primary']).toBe('#0F4C81');

    // integração com middleware (S08 em S09): customDomain → gov_municipal
    const h = await resolveTenantHeadersForHost('auditoria.bancaxyz.com.br');
    expect(h['x-tenant-id']).toBe('bancaxyz');

    // hidePoweredBy=true → sem EZRA no rodapé
    expect(poweredByText({ ...bancaxyz, hidePoweredBy: true })).toBeNull();
  });

  it('api-client faz GET com headers (fetch mockado)', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      status: 200,
      json: async () => ({ ok: true }),
    });
    vi.stubGlobal('fetch', fetchMock);

    const c = new ApiClient({ product: 'sentinel', tenantId: 't1' });
    const res = await c.get('/v1/inventario');
    expect(res.status).toBe(200);
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe('http://localhost:8001/v1/inventario');
    expect((init.headers as Record<string, string>)['x-tenant-id']).toBe('t1');
    vi.unstubAllGlobals();
  });
});