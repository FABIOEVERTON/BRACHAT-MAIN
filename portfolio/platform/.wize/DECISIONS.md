# BrachaTec — Registro de Decisões Arquiteturais e de Design (ADR)

Este documento centraliza todas as decisões rígidas tomadas para a plataforma BrachaTec, garantindo que nenhum sub-agente ou desenvolvedor fuja do escopo ou perca o contexto das premissas de negócios e design estabelecidas.

## 1. Arquitetura do Sistema (Shared-Nothing)
- **Decisão:** A plataforma opera em um modelo **Shared-Nothing** (Arquitetura Desacoplada e Individualizada).
- **Justificativa:** O modelo *White-label* exige isolamento total de dados e zero latência compartilhada. Não existe pasta `/shared` para código em tempo de execução.
- **Estrutura:** Cada ramo (`gov_ai`, `gov_muni`, `rig_tech`) possui seu próprio frontend (Next.js) e backend (Python/FastAPI) com infraestruturas isoladas.

## 2. Design System & Identidade Visual (Site Oficial)
- **Referência:** Baseado no `DESIGN.md` (Integrated Biosciences), mas adaptado para o perfil SaaS de alta conversão.
- **Cores Oficiais:**
  - Background (Tinta Abissal / Rich Black): `#0a0e17`
  - Acento Principal (Bioluminescent Lime / Cyan): `#3ecfbe`
- **Tipografia:** `Inter` (Sans) e `JetBrains Mono` (Logs/Tags).
- **Estética:** Fundo escuro profundo, linhas de rede neural em WebGL (Cadeia Criptográfica SHA-256), *glassmorphism* nos cards flutuantes, sem poluição visual.

## 3. Padrão de Nomenclatura dos Produtos
Os produtos devem ser sempre referenciados como marcas registradas, utilizando o prefixo **BT**, que herda a cor exata do "B" e "T" da logo oficial (Ciano):
- **BT Gov AI**
- **BT Muni**
- **BT Rig**
*(Regra estrita: Esses nomes não devem ser traduzidos para Inglês ou Espanhol).*

## 4. Diferenciais de Venda (Copywriting Exigido)
Sempre que um produto for descrito, o seu "Killer Feature" deve estar explícito:
- **BT Gov AI:** Foco na atuação em **Runtime** (interceptação e bloqueio no milissegundo da decisão do algoritmo) e não apenas mapeamento passivo.
- **BT Muni:** Foco no monitoramento ativo do CAUC e no rastreamento de **emendas parlamentares** para garantir captação de recursos.
- **BT Rig:** Foco em dossiês instantâneos com Inteligência Artificial para antecipar impactos tributários e regulatórios.
- **O Motor Central:** SHA-256 (Cadeia probatória) e WORM (Cofre forense) hospedados na AWS sa-east-1.

## 5. UI / Navegação (Landing Page)
- **Scroll e Âncoras:** Links do menu devem rolar a página parando com uma margem de `40vh` (meio exato da tela) para focar a leitura do executivo.
- **Isolamento da Academy:** O link "Academy" é o único que não rola a página atual, direcionando imediatamente para `academy/index.html`, isolando o funil de compra de software do funil educacional.
