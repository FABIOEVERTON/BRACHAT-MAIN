// Utilitários SHA-256 e verificação (PRD §2.2 packages/crypto)
// Espelho TS do motor Python (services/shared/laudo/hash_chain.py) para verificação no frontend.

export async function sha256Hex(input: Uint8Array | string): Promise<string> {
  const bytes =
    typeof input === 'string' ? new TextEncoder().encode(input) : Uint8Array.from(input);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

// chain_hash = SHA256(content_hash + previous_chain_hash); âncora = tenant_id
export async function chainHash(contentHash: string, previous: string): Promise<string> {
  return sha256Hex(`${contentHash}${previous}`);
}

export interface ChainLink {
  contentHash: string;
  chainHash: string;
}

// Valida a cadeia completa: link[0].chainHash == SHA256(content[0] + anchor);
// link[i].chainHash == SHA256(content[i] + link[i-1].chainHash).
// Retorna lista de índices inválidos (vazia = cadeia íntegra).
export async function verifyChain(links: ChainLink[], anchor: string): Promise<number[]> {
  const invalid: number[] = [];
  let expected = anchor;
  for (let i = 0; i < links.length; i++) {
    const link = links[i];
    if (!link) continue;
    const computed = await chainHash(link.contentHash, expected);
    if (computed !== link.chainHash) {
      invalid.push(i);
    }
    if (link.chainHash !== '') {
      expected = link.chainHash;
    }
  }
  return invalid;
}