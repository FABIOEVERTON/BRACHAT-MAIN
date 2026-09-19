// (dashboard) — layout consistente: sidebar (ramos) + header (tenant).
import Link from 'next/link';

import { RAMO_1_NAV, RAMO_2_NAV, RAMO_3_NAV, brandByTenant } from '../../components/dashboard/nav';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  // FASE 0: tenant default EZRA; S09-S08 integração usa middleware header
  const brand = brandByTenant('ezra');

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <aside
        style={{
          width: 240,
          background: '#111827',
          color: '#f9fafb',
          padding: '1rem',
          boxSizing: 'border-box',
        }}
      >
        <div style={{ fontWeight: 700, marginBottom: '1.5rem' }}>{brand.name}</div>
        <div style={{ fontSize: '0.75rem', opacity: 0.6, marginBottom: '0.5rem' }}>
          RAMO 1 — GOVERNAÇA DE IA
        </div>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.5rem' }}>
          {RAMO_1_NAV.map((n) => (
            <Link key={n.href} href={n.href} style={{ color: '#e5e7eb', textDecoration: 'none' }}>
              {n.label}
            </Link>
          ))}
        </nav>
        <div style={{ fontSize: '0.75rem', opacity: 0.6, marginBottom: '0.5rem' }}>
          RAMO 2 — GOVERNAÇA PÚBLICA
        </div>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {RAMO_2_NAV.map((n) => (
            <Link key={n.href} href={n.href} style={{ color: '#e5e7eb', textDecoration: 'none' }}>
              {n.label}
            </Link>
          ))}
        </nav>
        <div style={{ fontSize: '0.75rem', opacity: 0.6, marginBottom: '0.5rem' }}>
          RAMO 3 — GOVERNANÇA REGULATÓRIA
        </div>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {RAMO_3_NAV.map((n) => (
            <Link key={n.href} href={n.href} style={{ color: '#e5e7eb', textDecoration: 'none' }}>
              {n.label}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Main */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <header
          style={{
            height: 56,
            borderBottom: '1px solid #e5e7eb',
            display: 'flex',
            alignItems: 'center',
            padding: '0 1.5rem',
            justifyContent: 'space-between',
          }}
        >
          <span>Dashboard</span>
          <span style={{ color: brand.color, fontWeight: 600 }}>{brand.name}</span>
        </header>
        <main style={{ padding: '1.5rem', flex: 1 }}>{children}</main>
      </div>
    </div>
  );
}