// App Admin (EZRA interna + white-label admin) — PRD §2.2 / scaffold E0-S01.
// Shell real entra na E0-S09. Stub compilável agora.
import type { Branch, Plan, Tenant } from '@ezra/types';

export function tenantSummary(t: Tenant): string {
  return `${t.slug} [${t.branch}] plan:${t.plan} status:${t.status}`;
}

export function planLabel(plan: Plan): string {
  return plan === 'whitelabel' ? 'White-label' : 'Direct';
}

export function branchLabel(branch: Branch): string {
  return branch === 'gov_ai' ? 'Governança IA' : 'Governança Municipal';
}