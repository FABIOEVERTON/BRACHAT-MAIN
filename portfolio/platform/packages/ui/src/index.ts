// Design system base — packages/ui (shadcn/ui base conforme PRD §2.2)
// Stub FASE 0: componentes serão implementados com shadcn/ui na FASE 0 (S09) e refinados por Mantis.
import type { WhitelabelConfig } from '@ezra/types';

export interface ThemeTokens {
  colorPrimary: string;
  colorSecondary: string;
}

// PRD §3.6 / §8.3 — ThemeProvider white-label com CSS vars
export function applyTheme(config: WhitelabelConfig): Record<string, string> {
  return {
    '--color-primary': config.primaryColor,
    '--color-secondary': config.secondaryColor,
  };
}

export function resolveThemeTokens(config: WhitelabelConfig): ThemeTokens {
  return {
    colorPrimary: config.primaryColor,
    colorSecondary: config.secondaryColor,
  };
}