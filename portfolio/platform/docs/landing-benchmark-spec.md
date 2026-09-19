# ESPEC — Landing Page Institucional EZRA
## Benchmark Competitivo + Feature Matrix + Gap Analysis + Spec de Conteúdo
**Status:** RASCUNHO PARA REVISÃO (Fabio) | **Entrega:** 14 concorrentes extraídos via webfetch | **FASE 0 concluída 12/12**

---

## 1. RESUMO EXECUTIVO

A EZRA ocupa um **blue ocean** comprovado por esta análise: nenhum dos 14 concorrentes (8 internacionais de AI Governance + 6 GovTechs brasileiras) oferece **laudo pericial técnico imutável (WORM + cadeia SHA-256) como evidência válida para TCE/TCU/MP**, combinado com governança de IA **e** governança municipal em um único produto white-label.

- **Internacionais (IBM, ServiceNow, OneTrust, Purview, Credo, Holistic, ModelOp, Truyo):** AI Governance enterprise genérico. Sem contexto municipal brasileiro (LGPD, LRF/LEO, Lei 14.133, TCEs), sem laudo em pt-BR, sem white-label por ente, custo enterprise.
- **Nacionais (Gove, IGAM, Colab, Portal de Compras, Forseti, 1Doc):** burocracia digital, licitações, participação cidadã ou capacitação. **Nenhum** faz governança de IA. **Nenhum** emite evidência imutável verificável para controle externo.
- **Oportunidade:** "perícia técnica de governança digital" — a EZRA é o único player que transforma fiscalização pública em **prova técnica comprovável e imutável**.

---

## 2. BENCHMARK POR CONCORRENTE (síntese por extração)

### Bloco A — AI Governance internacional (enterprise)

| # | Concorrente | Proposta central | Público | Evidências | IA | Imutabilidade | White-label | Copy dominante | CTA |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **IBM watsonx.governance** | Governança de modelos de IA no ciclo de vida (drift, bias, risco) | Grandes corporações | Case studies enterprise | Sim (model governance) | Logs de auditoria (não WORM fiscal) | Não | "Governança de IA de ponta a ponta" | Demo/vendor |
| 2 | **ServiceNow AI Control Tower** | Torre de controle central de governança de IA | IT/empresas no ecossistema ServiceNow | Enterprise | Sim | Logs de workflow | Não | "Controle centralizado da IA" | Demo |
| 3 | **OneTrust AI Governance** | Mapeamento de modelos, avaliações e risco | GRC/legal/compliance | Enterprise | Sim | Trilhas de auditoria | Não | "IA responsável e confiável" | Demo |
| 4 | **Microsoft Purview** | Data governance + segurança + catalogação | Empresas M365/Azure | Enterprise | Sim (Copilot era) | Catalogação/data lineage | Não | "Governança de dados e IA" | Demo |
| 5 | **Credo AI** | AI governance policy-aware | Enterprise regulado | Enterprise | Sim | Registro de decisões | Não | "IA alinhada a políticas" | Demo |
| 6 | **Holistic AI** | Avaliação de risco e bias de IA | Enterprise | Enterprise | Sim | Relatórios | Não | "IA segura e auditável" | Demo |
| 7 | **ModelOp** | ModelOps/governança de ciclo de vida de modelos | Enterprise data science | Enterprise | Sim (MLOps) | Lineage de modelos | Não | "Governança de modelos em produção" | Demo |
| 8 | **Truyo** | Automação de privacidade (DSARs) | Enterprise LGPD/GDPR | Enterprise | Parcial | Trilhas de compliance | Não | "Automação de privacidade" | Demo |

**Padrão Bloco A:** demo-led, preço enterprise, inglês, sem carimbo de validade jurídica/normativa brasileira, sem WORM fiscal, sem municipalização.

### Bloco B — GovTechs brasileiras (setor público)

| # | Concorrente | Proposta central | Público | Evidências (dados reais) | IA | Imutabilidade | White-label | Copy dominante | CTA |
|---|---|---|---|---|---|---|---|---|---|
| 9 | **Gove** | "Governo Zero Clique" — infraestrutura digital de gestão que sabe, antecipa e age | Municípios | — | Parcial | Não | Não | "O governo que sabe, antecipa e age" | Contato |
| 10 | **IGAM** (desde 1992) | Cursos + consultoria jurídica/contábil para órgãos públicos | Gestores municipais (RS/SC/PR) | Agenda mensal de cursos, notícias TCE | Parcial (formativa) | Não | Não | "Qualidade em cursos e consultoria" | Inscrição/contato |
| 11 | **Colab** | Participação cidadã: demandas urbanas, consultas públicas, serviços | Cidadãos + prefeituras | 1M+ cidadãos, 80% demandas resolvidas, 995k participações | Parcial | Não | Não (app de marca) | "Todos os serviços da prefeitura em um só lugar" | Baixar app/orçamento |
| 12 | **Portal de Compras Públicas** | Licitações: processos, marketplace, fornecedores | Compradores + fornecedores | R$616M oportunidades/dia, 4mil+ entes, 634mil fornecedores; ISO 9001/27001/27701/20000 | Parcial (robô de lances) | Não | Não | "Inovação, transparência e simplificação das licitações" | Criar conta/buscar processo |
| 13 | **Forseti/eLicitação** (18 anos) | Soluções e plataforma para empresas licitantes | Fornecedores | 18 anos, infraestrutura física de pregão | Não | Não | Não | "Licitação é o nosso negócio" | Quero conhecer |
| 14 | **1Doc (Softplan)** | Processos digitais municipais: fluxos, assinatura digital, central de atendimento, indicadores, IA | Prefeituras/câmaras | 26 estados, 900+ organizações, R$1 bi economia, 25% da população; ISO 27001/9001/14001/37001/37301, ICP-Brasil/GovBR | Sim (diagnóstico de maturidade) | Assinatura digital (MP 2200-2, Lei 14.063/2020) | Não | "Processos digitais, seguros e transparentes" | Orçamento/diagnóstico grátis |

**Padrão Bloco B:** forte em burocracia digital e licitações, prova social abundante (números reais e cases), mas **zero** em governança de IA e **zero** em evidência imutável pericial para controle externo.

---

## 3. FEATURE MATRIX — EZRA vs MERCADO

Legenda: ● = nativo e central | ◐ = parcial/terceirizado | ○ = ausente

| Feature | EZRA | IBM/SN/OneTrust/Purview/Credo/Holistic/ModelOp/Truyo | Gove | IGAM | Colab | Portal Compras | Forseti | 1Doc |
|---|---|---|---|---|---|---|---|---|
| Laudo pericial imutável (WORM + SHA-256) | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Cadeia hash verificável de evidências | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| PDF determinístico (mesma entrada → byte-idêntico) | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| White-label por ente municipal | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Scanner de Shadow AI / inventário de modelos | ● | ● (IBM/SN) | ○ | ○ | ○ | ○ | ○ | ○ |
| Governança de decisões automatizadas (LCA) | ● | ● (IBm/Credo/Holistic) | ○ | ○ | ○ | ○ | ○ | ○ |
| Monitoração de integridade em runtime (LIR) | ● | ● (IBM/ModelOp) | ○ | ○ | ○ | ○ | ○ | ○ |
| Varredura de gastos/transparência (LEO/LRF) | ● | ○ | ◐ | ◐ (consultoria) | ○ | ◐ (compras) | ○ | ◐ (indicadores) |
| Elegibilidade/preços/regularidade de fornecedores | ● | ○ | ○ | ○ | ○ | ● (forte) | ● (lado fornecedor) | ○ |
| Execução orçamentária e prestação de contas | ● | ○ | ◐ | ◐ | ○ | ○ | ○ | ◐ |
| Detecção de anomalias + alerta em tempo real | ● | ◐ | ● ("antecipa e age") | ○ | ○ | ◐ (alertas) | ○ | ○ |
| Trilha de auditoria imutável (Prova) | ● | ◐ (logs) | ○ | ○ | ○ | ○ | ○ | ○ |
| Conformidade LGPD/14.133/LRF com evidência | ● | ◐ (LGPD genérica) | ◐ | ◐ (consultoria) | ◐ | ● (14.133) | ◐ | ● (14.063, MP 2200-2) |
| Isolamento multi-tenant por ente | ● | ◐ | ○ | ○ | ○ | ○ | ○ | ○ |
| Participação cidadã / consultas públicas | ○ | ○ | ◐ | ○ | ● | ○ | ○ | ○ |
| Marketplace / pregão / licitação aberta | ○ | ○ | ○ | ○ | ○ | ● | ● | ○ |
| Assinatura digital (ICP) | ◐ (FASE futura) | ○ | ○ | ○ | ○ | ○ | ○ | ● |
| Cursos / capacitação | ○ | ○ | ○ | ● | ○ | ○ | ● | ○ |

---

## 4. GAP ANALYSIS → POSICIONAMENTO EZRA

### 4.1 Lacunas do mercado (dor não atendida)

1. **Fiscalização sem prova:** TCEs/TCU/MP exigem accountability, mas nenhuma ferramenta municipal gera **evidência técnica imutável** (WORM + hash) — só relatórios editáveis.
2. **IA chegou ao setor público sem governança:** nenhum concorrente nacional regula decisões automatizadas em prefeituras (LIC/decidibilidade, auditoria de modelo).
3. **Falta de white-label:** prefeituras/secretarias querem autoridade própria (marca do ente), não mais uma marca de SaaS sobreposta.
4. **LGPD no papel:** autodeclaração sem prova verificável de trilha.

### 4.2 Onde a EZRA vence (diferenciais defensáveis)

| Diferencial | Prova técnica (FASE 0) |
|---|---|
| Laudo pericial imutável | `worm_vault.py` — WORM COMPLIANCE + SSE-KMS, delete bloqueado (AccessDenied), RFC 7807, 26ms (NFR 500ms) |
| Cadeia SHA-256 | `hash_chain.py` — verificação de cadeia + tenant lock |
| PDF determinístico | `pdf_generator.py` — `_strip_volatile_metadata()`, extração pypdf nos testes |
| White-label exato ao PRD §3.6 | `WhitelabelConfig` + `theme.ts` (themeVars, poweredByText, laudoSignatory) |
| Plataforma real | Next shell 14.2.35, 11 rotas, middleware edge, p95=6ms, 92.6% cobertura, CI/CD ECS staging |

### 4.3 Posicionamento (single sentence)

> **EZRA é a plataforma de governança que transforma a fiscalização pública em perícia técnica comprovável — governança de IA e governança municipal com laudo pericial imutável (WORM + SHA-256), no padrão do seu ente.**

---

## 5. SPEC DA LANDING PAGE (conteúdo + layout + tokens)

### 5.1 Arquitetura da página (12 seções)

```
[1 Header/Nav]
[2 Hero]
[3 Barra de evidências]
[4 O problema]
[5 A solução: 2 ramos]
[6 Grid de produtos (9)]
[7 Diferenciais técnicos]
[8 Como funciona (3 passos)]
[9 Prova social (cases)]
[10 FAQ (6)]
[11 CTA final]
[12 Footer]
```

### 5.2 Seções — copy framework

**1. HEADER / NAV**
- Logo: "EZRA" (ou nome do ente em white-label) + marca d'água "plataforma de governança"
- Links: Plataforma · Gov-IA · Gov-Municipal · Diferenciais · FAQ
- CTA: `Acessar plataforma` (→ `/login`)
- Comportamento: sticky, fundo translúcido com blur; links rolam para âncoras.

**2. HERO** (mantém estrutura atual de `hero.ts`, eleva copy)
- Eyebrow: `Plataforma de governança · FASE 0 completa · 12/12 entregas`
- H1 (2 variações):
  - EZRA brand: **"Governança de IA e governança municipal com laudo pericial imutável."**
  - White-label: **"Plataforma de governança com laudo pericial habilitando {Ente}."**
- Sub: "Scanner de Shadow AI, monitoramento de conformidade e trilha de evidências que os Tribunais de Contas aceitam — em uma plataforma no padrão visual do seu ente."
- CTA primário: `Acessar plataforma` (→ `/login`)
- CTA secundário: `Conhecer os 9 produtos` (→ #produtos)
- Visual: gradiente grafite→azul (atual `heroTone`), sem foto stock — **consistência logo do setor público** (padrão observado em Colab/1Doc/Portal: ilustração de produto, não stock).

**3. BARRA DE EVIDÊNCIAS** (números que geram confiança — padrão 1Doc/Portal)
- `2` ramos — Gov-IA + Gov-Municipal
- `9` produtos em produção
- `56/56` testes FASE 0 · `92,6%` cobertura de branch
- `p95 6ms` latência do dashboard
- `10 anos` retenção WORM COMPLIANCE por objeto

**4. O PROBLEMA** (dor — copy direcional)
- H2: **"Fiscalizar sem prova não é fiscalizar."**
- 3 dores:
  - "IA nas prefeituras sem inventário, sem decidibilidade, sem auditoria."
  - "Relatórios editáveis que não resistem a um TCE."
  - "Plataformas genéricas que apagam a identidade do ente."
- CTA micro: `Ver a solução ↓`

**5. A SOLUÇÃO: 2 RAMOS** (espelha a arquitetura PRD)
- Bloco A — **Gov-IA:** Sentinel · Aegis · Guardian (governança de IA de ponta a ponta)
- Bloco B — **Gov-Municipal:** Radar · Vigília · Compras · Executa · Alerta · Prova (conformidade e transparência municipal)
- Cada bloco: 1 linha de proposição + link para o grid.

**6. GRID DE PRODUTOS** (reaproveitar `product-grid.ts`; copy do DESCS já validada)
- 9 cards: slug, nome, ramo, descrição única.
- Card: ícone (tipo minimal), nome, ramo badge, descrição, link.

**7. DIFERENCIAIS TÉCNICOS** (prova técnica — o que ninguém tem)
- **Laudo pericial imutável:** WORM COMPLIANCE + SSE-KMS; delete bloqueado a nível de storage.
- **Cadeia SHA-256:** cada evidência encadeia à anterior; qualquer alteração quebra a cadeia.
- **PDF determinístico:** mesma entrada → mesmo bytes → verificável por terceiros.
- **White-label:** visual do ente no laudo, no tema e no rodapé ("laudo signatário").

**8. COMO FUNCIONA** (3 passos — padrão Portal/1Doc)
1. **Conecte** o ente e os sistemas (identidade + tenant isolado).
2. **Monitore** — Sentinel varre Shadow AI; Radar varre gastos; Alerta dispara anomalias.
3. **Receba o laudo** — evidência imutável, encadeada e verificável, pronta para TCE/TCU/MP.

**9. PROVA SOCIAL (cases)** — placeholder rotulado **"Em breve: primeiros entes auditados"** (sem inventar clientes — determinismo ético).
- Variação: bloco de adoção "FASE 0 entregue: 12/12 stories, CI/CD em ECS staging, homepage em produção." (fato, não case fictício)

**10. FAQ (6)**
1. O laudo tem validade para TCE/TCU? → WORM + SHA-256: evidência imutável, verificável por terceiros; padrão de prova documental.
2. EZRA funciona para prefeituras de qualquer porte? → Multi-tenant isolado por ente; white-label.
3. Já fazemos LGPD manualmente... → Autodeclaração vira trilha encadeada e verificável.
4. E se precisarmos da marca da prefeitura? → White-label completo (tema, laudo, signatário).
5. A plataforma já está pronta? → FASE 0 completa (12/12); FASE 1 em curso (SQLAlchemy real, laudos via API, NextAuth).
6. Onde os dados ficam? → Infraestrutura própria/cloud com SSE-KMS; retenção WORM 10 anos por objeto.

**11. CTA FINAL**
- H2: **"Sua fiscalização merece prova, não promessa."**
- CTA: `Acessar plataforma` → `/login` (primário) + `Falar com o time` (mailto — placeholder).

**12. FOOTER**
- Marca EZRA · ramos · produtos · links legais (privacidade, termos) · `brachatec.com`
- Nota de conformidade: LGPD · Lei 14.133/2021 · Lei 14.129/2021 (gov. digital) · MP 2200-2/2001 (referência documental).

### 5.3 Design tokens (espelha `white-label/theme.ts`)

| Token | Valor | Uso |
|---|---|---|
| `--brand-900` | `#111827` (grafite) | fundo hero/ft — neutro herdado |
| `--brand-700` | `#1e3a8a` (azul profundo) | acentos, botões primários |
| `--accent` | definido por ente (white-label) | CTA e highlights |
| `--bg` | `#ffffff` / `#f9fafb` | seções alternadas |
| `--text` | `#111827` / `#4b5563` | títulos / corpo |
| Fonte | system-ui stack | sem dependência externa (estático CF) |
| Radius | 8–12px | cards |
| Espaçamento | 64–96px entre seções | ritmo vertical oficial |

### 5.4 Restrições técnicas (herdadas de FASE 0)

- **Estático puro:** `output: 'export'` — sem SSR/ISR (Cloudflare Workers + assets).
- **Sem emojis** no conteúdo.
- **Zero stock photos** (padrão setor público BR: ilustração/produto — Colab, 1Doc, Portal).
- **Acessibilidade:** contraste AA, labels visíveis, foco visível.
- **i18n:** pt-BR fixo nesta versão; estrutura de dados pronta para i18n futuro.

---

## 6. PRÓXIMOS PASSOS (após aprovação)

1. Fabio revisa e aprova esta spec (ou aponta ajustes de copy/seções).
2. Implementar `apps/web/app/page.tsx` v2 (12 seções, componentes novos: evidence-bar, problem, solution-two-ramps, how-it-works, faq, cta-final).
3. Garantir cobertura vitest dos novos componentes (`__tests__/landing.test.ts`).
4. `npm run build` → `out/` → `wrangler deploy --assets=out --name=ezra-web` em brachatec.com.
5. Verificar `www.brachatec.com` (TLS em provisioning).
6. Registrar a spec no governance ledger (STORY/LANDING_SPEC).