# Spec de Tela: Painel Super Admin (`/admin/dashboard.html`)

## 1. Identificação da Tela
* **Caminho:** `/admin/dashboard.html` (Acesso exclusivo Super Admin)
* **Tema:** Dark theme com acentos em ouro e ciano corporativo.

## 2. Componentes & Seções

### 2.1. Top KPI Cards (Visão Financeira & Operacional)
1. **MRR Total:** Valor consolidado mensal (ex: `R$ 148.500,00`).
2. **Clientes Ativos:** Total de prefeituras, empresas e parceiros (ex: `42 ativos / 3 trials`).
3. **Inadimplência:** Clientes com fatura em atraso destacado em vermelho (ex: `2 pendentes - R$ 7.800`).
4. **Saúde do Sistema:** Badge verde "100% Operacional — Latência média 38ms".

### 2.2. Tabela de Gestão de Clientes (Tenants)
* Colunas:
  - `Organização / CNPJ`
  - `Ramo Principal` (Gov IA, Setor Público, RIG Tech, White-Label)
  - `Plano Contratado`
  - `Status Financeiro` (Pago / Pendente / Atrasado)
  - `Status de Acesso` (Ativo / Bloqueado)
  - `Ações Rápidas:` Botões `[Ver Detalhes]`, `[Liberar]`, `[Travar Acesso]`, `[Simular Visão do Cliente]`.

### 2.3. Painel de Logs de Alertas & Integração Slack
* Feed ao vivo das notificações enviadas ao Slack (novos cadastros, pagamentos e incidentes técnicos).
