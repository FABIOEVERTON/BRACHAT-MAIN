// Contratos de API gerados do OpenAPI — packages/api-contracts (PRD §2.2)
// NÃO EDITAR MANUALMENTE: regenerar via scripts/generate_api_types.sh
// Stub FASE 0 — tipos reais chegam na E0B-S05.

export interface ProblemDetail {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance: string;
}

export type JobStatus = 'queued' | 'processing' | 'completed' | 'failed';

export interface JobResponse {
  jobId: string;
  status: JobStatus;
  progressPct?: number;
  resultUrl?: string;
  error?: string;
  laudo?: unknown; // LaudoResult — tipado após E0B-S05
}