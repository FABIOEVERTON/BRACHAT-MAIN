import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'EZRA — Plataforma',
  description: 'Plataforma EZRA de Governança de IA e Governança Pública',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body style={{ margin: 0, fontFamily: 'system-ui, sans-serif' }}>{children}</body>
    </html>
  );
}