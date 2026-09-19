// ThemeProvider white-label (PRD §8.3, F0-32): CSS vars + branding.
// Sem referência visual a EZRA se hidePoweredBy=true.
import type { CSSProperties } from 'react';
import type { WhitelabelConfig } from '@ezra/types';

type ThemeVars = CSSProperties & {
  '--color-primary': string;
  '--color-secondary': string;
};

export function themeVars(config: WhitelabelConfig): ThemeVars {
  return {
    '--color-primary': config.primaryColor,
    '--color-secondary': config.secondaryColor,
  } as ThemeVars;
}

// F0-33: signatário do laudo é o operador white-label (regra crítica §3.6)
export function laudoSignatory(config: WhitelabelConfig) {
  return {
    name: config.laudoSignatoryName,
    title: config.laudoSignatoryTitle,
    register: config.laudoSignatoryRegister,
  };
}

// PRD §3.6: EZRA aparece apenas como "sistema tecnológico de suporte"
// em rodapé, se hidePoweredBy=false. Nunca como signatário.
export function poweredByText(tenant?: WhitelabelConfig): string | null {
  if (!tenant) return 'Plataforma EZRA';
  if (tenant.hidePoweredBy) return null;
  return 'Sistema tecnológico de suporte: EZRA';
}