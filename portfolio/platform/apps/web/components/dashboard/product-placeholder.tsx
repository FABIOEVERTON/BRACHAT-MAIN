// Placeholder de produto (F0-35): landing consistente sem conteúdo de domínio.
export function ProductPlaceholder({ name, ramo }: { name: string; ramo: 'gov-ai' | 'gov-municipal' | 'gov-regulatorio' }) {
  return (
    <div>
      <h1 style={{ fontSize: '1.5rem', margin: '0 0 0.25rem' }}>{name}</h1>
      <p style={{ color: '#6b7280', margin: '0 0 1.5rem' }}>
        {ramo === 'gov-ai' ? 'Ramo 1 — Governança de IA' : ramo === 'gov-municipal' ? 'Ramo 2 — Governança Pública' : 'Ramo 3 — Governança Regulatória'}
      </p>
      <div
        style={{
          border: '1px dashed #d1d5db',
          borderRadius: 8,
          padding: '2rem',
          color: '#9ca3af',
          textAlign: 'center',
        }}
      >
        Módulo em construção — especificação em .wize/solutioning/stories
      </div>
    </div>
  );
}