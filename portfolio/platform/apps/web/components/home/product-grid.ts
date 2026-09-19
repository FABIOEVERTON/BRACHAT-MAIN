// Grid de produtos da homepage — ambos os ramos (PRD §1 / §4 / §5).
import type { DashboardNavItem } from '../dashboard/nav';

export interface ProductCard {
  slug: string;
  name: string;
  ramo: string;
  desc: string;
}

const DESCS: Record<string, string> = {
  sentinel: 'Scanner de Shadow AI e inventário contínuo de modelos (LAS)',
  aegis: 'Governança de decisões automatizadas e ciclo de vida de modelos (LCA)',
  guardian: 'Monitoração de integridade e runtime de sistemas de IA (LIR)',

  radar: 'RADAR — varredura de gastos públicos e transparência (LEO/LRF)',
  vigilia: 'Vigília — monitoramento contínuo de conformidade municipal',
  compras: 'Compras — elegibilidade, preços e regularidade de fornecedores (LJP/LCO)',
  executa: 'Executa — execução orçamentária e prestação de contas (LSD/LPC)',
  alerta: 'Alerta — detecção de anomalias e notificação em tempo real',
  prova: 'Prova — trilha de auditoria e evidências imutáveis',

  lex: 'Inteligência Legislativa Contínua & Risco Normativo',
  vanguarda: 'Hub de Inteligência em Minerais Críticos & Terras Raras',
};

export function productCards(nav: DashboardNavItem[], ramo: string): ProductCard[] {
  return nav.map((n) => ({
    slug: n.product,
    name: n.label,
    ramo,
    desc: DESCS[n.product] ?? 'Módulo da Plataforma EZRA',
  }));
}