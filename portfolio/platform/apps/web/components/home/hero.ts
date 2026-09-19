// Landing institucional — hero EZRA (homepage pública, PRD §2).
import type { CSSProperties } from 'react';

export type BrandTone = 'ezra' | 'white-label';

export function heroContent(brand: BrandTone, brandName?: string) {
  const name = brand === 'white-label' && brandName ? brandName : 'EZRA';
  return {
    brand: name,
    claim:
      brand === 'white-label'
        ? `Plataforma de governança com laudo pericial habilitando ${name}.`
        : 'Governança de IA e governança municipal com laudo pericial imutável (WORM + cadeia SHA-256).',
    cta: 'Acessar plataforma',
  };
}

export const heroTone = (brandColor?: string): CSSProperties => ({
  background:
    brandColor && brandColor !== '#111827'
      ? `linear-gradient(135deg, ${brandColor}, #0f172a)`
      : 'linear-gradient(135deg, #111827, #1e3a8a)',
  color: '#f9fafb',
});