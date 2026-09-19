// Middleware edge (PRD §8.2, F0-34/F0-35): resolve tenant por subdomínio e
// injeta x-tenant-id + x-tenant-branch para downstream (api-client/SSR).
import { NextRequest, NextResponse } from 'next/server';

import { resolveTenantHeaders } from './lib/tenant-resolver';

// Export puro p/ testes unitários (vitest) sem instanciar NextRequest.
export type TenantHeaders = {
  'x-tenant-id': string;
  'x-tenant-branch': string;
};

export async function resolveTenantHeadersForHost(hostname: string): Promise<TenantHeaders> {
  return resolveTenantHeaders(hostname);
}

export async function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') ?? '';
  const headers = await resolveTenantHeadersForHost(hostname);

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-tenant-id', headers['x-tenant-id']);
  requestHeaders.set('x-tenant-branch', headers['x-tenant-branch']);

  return NextResponse.next({ request: { headers: requestHeaders } });
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};