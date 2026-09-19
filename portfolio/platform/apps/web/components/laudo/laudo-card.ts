// Componente de exibição de laudo (PRD §3.3, F0-37):
// mostra SHA-256 + chain_hash com link de download do PDF (WORM).
import type { CSSProperties } from 'react';

export interface LaudoDisplayData {
  laudo_id: string;
  laudo_number: string;
  sha256_hash: string;
  chain_hash: string;
  worm_key: string;
  pdf_url: string;
  emitted_at: string;
}

export function laudoFields(data: LaudoDisplayData): Array<{ label: string; value: string }> {
  return [
    { label: 'Número', value: data.laudo_number },
    { label: 'SHA-256', value: data.sha256_hash },
    { label: 'Cadeia (chain)', value: data.chain_hash },
    { label: 'WORM', value: data.worm_key },
    { label: 'Emitido em', value: data.emitted_at },
  ];
}

export function downloadLink(data: LaudoDisplayData): string {
  return data.pdf_url;
}

// Estilo p/ publicação (evita EZRA como signatária — regra crítica §3.6)
export const laudoStyles = (brandColor?: string): CSSProperties => ({
  fontFamily: 'ui-monospace, monospace',
  borderLeft: `4px solid ${brandColor ?? '#111827'}`,
  padding: '0.75rem 1rem',
});