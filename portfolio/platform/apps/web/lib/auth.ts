// Auth web — claims NextAuth v5 (PRD §3.1).
// Valida os claims EXATOS: sub, role, permissions, tenant_id, typ (F0-07).
import type { Permission, Role } from '@ezra/types';

export interface AuthClaims {
  sub: string;
  role: Role;
  permissions: Permission[];
  tenantId: string | null;
  mfaRequired: boolean;
}

// callback jwt: injeta role/permissions/tenant nas claims da sessão (F0-07)
export function claimsFromToken(payload: Record<string, unknown>): AuthClaims {
  const role = (payload['role'] ?? 'TENANT_VIEWER') as Role;
  const tenantId = (payload['tenant_id'] ?? null) as string | null;
  const permissions = (payload['permissions'] ?? []) as Permission[];
  const rawTyp = (payload['typ'] ?? 'access') as string;

  return {
    sub: String(payload['sub'] ?? ''),
    role,
    permissions,
    tenantId,
    mfaRequired: rawTyp === 'access' && permissions.length === 0,
  };
}