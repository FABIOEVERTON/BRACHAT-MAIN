// Homepage institucional EZRA (pública, PRD §2 / §4 / §5).
// Estática (compatível com next export / Cloudflare Pages). O tema white-label
// por subdomínio pertence ao dashboard autenticado (F0-38, aplicado via headers
// na S09); a landing pública usa a marca EZRA padrão.
import Link from 'next/link';

import { RAMO_1_NAV, RAMO_2_NAV } from '../components/dashboard/nav';
import { heroContent, heroTone } from '../components/home/hero';
import { productCards } from '../components/home/product-grid';

export default function HomePage() {
  const hero = heroContent('ezra');

  return (
    <main>
      {/* Hero */}
      <section style={{ ...heroTone(), padding: '4rem 2rem' }}>
        <div style={{ maxWidth: 960, margin: '0 auto' }}>
          <h1 style={{ fontSize: '2.5rem', margin: '0 0 0.75rem' }}>
            {hero.brand}
            <span style={{ fontWeight: 400 }}> — Plataforma de Governança</span>
          </h1>
          <p style={{ fontSize: '1.125rem', opacity: 0.85, maxWidth: 640 }}>{hero.claim}</p>
          <Link
            href="/login"
            style={{
              display: 'inline-block',
              marginTop: '1.5rem',
              padding: '0.75rem 1.5rem',
              background: '#f9fafb',
              color: '#111827',
              fontWeight: 600,
              borderRadius: 8,
              textDecoration: 'none',
            }}
          >
            {hero.cta}
          </Link>
        </div>
      </section>

      {/* Produtos */}
      <section style={{ maxWidth: 960, margin: '3rem auto', padding: '0 2rem' }}>
        <h2 style={{ fontSize: '1.25rem' }}>Ramo 1 — Governança de IA</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem', marginBottom: '2.5rem' }}>
          {productCards(RAMO_1_NAV, 'gov-ai').map((p) => (
            <Link
              key={p.slug}
              href={`/gov-ai/${p.slug}`}
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <div style={{ border: '1px solid #e5e7eb', borderRadius: 10, padding: '1.25rem', height: '100%' }}>
                <div style={{ fontWeight: 700 }}>{p.name}</div>
                <div style={{ color: '#6b7280', fontSize: '0.875rem', marginTop: '0.5rem' }}>{p.desc}</div>
              </div>
            </Link>
          ))}
        </div>

        <h2 style={{ fontSize: '1.25rem' }}>Ramo 3 — Governança Regulatória</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem' }}>
          {productCards(RAMO_3_NAV, 'gov-regulatorio').map((p) => (
            <Link
              key={p.slug}
              href={`/gov-regulatorio/${p.slug}`}
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <div style={{ border: '1px solid #e5e7eb', borderRadius: 10, padding: '1.25rem', height: '100%' }}>
                <div style={{ fontWeight: 700 }}>{p.name}</div>
                <div style={{ color: '#6b7280', fontSize: '0.875rem', marginTop: '0.5rem' }}>{p.desc}</div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Rodapé */}
      <footer style={{ borderTop: '1px solid #e5e7eb', padding: '1.5rem 2rem', color: '#6b7280', fontSize: '0.875rem' }}>
        Plataforma EZRA — laudo pericial imutável: WORM + cadeia SHA-256 (LGPD Art. 37)
      </footer>
    </main>
  );
}