// API client (PRD §9.1, F0-36): injeta base URL por produto + x-tenant-id.
import type { WhitelabelConfig } from '@ezra/types';

// Mapa produto → serviço (PRD §1 / ramos)
const SERVICE_BY_PRODUCT: Record<string, string> = {
  // Ramo 1 — Governança de IA
  sentinel: 'http://localhost:8001', // services/gov-ai/sentinel
  aegis: 'http://localhost:8002',
  guardian: 'http://localhost:8003',
  // Ramo 2 — Governança Pública
  radar: 'http://localhost:9001', // services/gov-municipal/radar
  vigilia: 'http://localhost:9002',
  compras: 'http://localhost:9003',
  executa: 'http://localhost:9004',
  alerta: 'http://localhost:9005',
  prova: 'http://localhost:9006',
};

export interface ApiClientOptions {
  product: string;
  tenantId: string;
  baseUrl?: string;
  token?: string;
}

export interface ApiResponse<T> {
  status: number;
  body: T;
}

export function resolveBaseUrl(product: string, baseUrl?: string): string {
  if (baseUrl) return baseUrl;
  const url = SERVICE_BY_PRODUCT[product];
  if (!url) throw new Error(`produto sem serviço configurado: ${product}`);
  return url;
}

export class ApiClient {
  readonly baseUrl: string;
  readonly tenantId: string;
  readonly token: string | undefined;

  constructor(opts: ApiClientOptions) {
    this.baseUrl = resolveBaseUrl(opts.product, opts.baseUrl);
    this.tenantId = opts.tenantId;
    this.token = opts.token;
  }

  authHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'x-tenant-id': this.tenantId,
      'content-type': 'application/json',
    };
    if (this.token) headers.authorization = `Bearer ${this.token}`;
    return headers;
  }

  async get<T>(path: string): Promise<ApiResponse<T>> {
    const res = await fetch(`${this.baseUrl}${path}`, { headers: this.authHeaders() });
    return { status: res.status, body: (await res.json()) as T };
  }

  async post<T>(path: string, body: unknown): Promise<ApiResponse<T>> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: this.authHeaders(),
      body: JSON.stringify(body),
    });
    return { status: res.status, body: (await res.json()) as T };
  }
}

// Conveniência de bootstrap white-label (F0-38 integração)
export function clientFor(config: WhitelabelConfig, product: string): ApiClient {
  return new ApiClient({ product, tenantId: config.tenantSlug });
}