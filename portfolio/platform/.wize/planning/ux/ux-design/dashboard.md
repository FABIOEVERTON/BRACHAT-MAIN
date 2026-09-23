# Spec de Tela: Dashboard da Área Logada (`/app/dashboard.html`)

## 1. Identificação da Tela
* **Caminho:** `/app/dashboard.html`
* **Tipo:** Painel de Controle do Tenant / Visão Geral Multi-Módulo
* **Estilo Visual:** Dark theme profissional (`--bg: #09090b`, `--panel: #121214`, `--border: rgba(255,255,255,0.1)`, `--cyan: #3ecfbe`, `--gold: #c9a84c`, `--violet: #9b85f5`).

## 2. Componentes & Layout

### 2.1. Sidebar de Navegação (Esquerda, 260px)
* **Logo:** Ícone vetorial BRACHATEC + nome.
* **Itens de Menu:**
  1. `Visão Geral` (ativo por padrão)
  2. `Radar Legislativo (RIG)`
  3. `Governança de IA`
  4. `Módulo Compras (Gov)`
  5. `Relatórios Forenses`
* **Rodapé Sidebar:** Link discreto `← Sair do Sistema` (faz logout e redireciona para a raiz).

### 2.2. Header Superior
* **Título:** "Painel de Controle"
* **Subtítulo:** "Bem-vindo ao centro de comando da sua operação."
* **Ação Primária (CTA):** Botão estilizado com `--cyan` com texto: `"Gerar Relatório Geral"` (dispara a geração assíncrona do Laudo Pericial).

### 2.3. Grid de Cards de Métricas (Top Cards)
* **Card 1 (RIG):** "Projetos de Lei (RIG)" ➔ Valor numérico dinâmico (ex: `1,248`).
* **Card 2 (IA):** "Requisições IA Validadas" ➔ Valor numérico dinâmico (ex: `45,902`).
* **Card 3 (Alertas):** "Alertas Críticos" ➔ Valor numérico destacado em vermelho `--red: #ff4a4a` (ex: `3`).

### 2.4. Painel Central de Últimas Atividades
* **Título:** "Últimas Atividades"
* **Lista de Eventos da Cadeia Probatória:** Cada item exibe:
  - Badge colorido por ramo (`Gov IA` em ciano, `Setor Público` em dourado, `RIG Tech` em violeta).
  - Título do evento / Filtro / Ação.
  - Hash SHA-256 truncado com link para validação de prova.
  - Timestamp relativo ("há 4 min", "há 12 min").

### 2.5. Modal de Relatório Forense Dinâmico (Novo)
* Ao clicar em "Gerar Relatório Geral", abre modal com o resumo do Laudo emitido, hash gerado, cadeia anterior e botões de download `[Baixar PDF Pericial]` e `[Exportar JSON Criptografado]`.
