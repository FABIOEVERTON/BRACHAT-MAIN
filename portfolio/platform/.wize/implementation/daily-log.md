# Diário de Bordo (Daily Log)

Este arquivo registra o progresso contínuo, bloqueios e resoluções do dia a dia da plataforma BRACHATEC.

## Sessão Inicial: Planejamento & Fundação
- **O que foi feito:** O QG Global (Wizer) orquestrou o setup base. As políticas globais de Clean Code, estruturas de pastas e Idempotência foram cravadas. A nomenclatura dos produtos foi consolidada a partir do `site_oficial`.
- **Decisões Críticas:**
  - O site público é apenas funil de vendas.
  - A arquitetura **exige isolamento absoluto** entre os ramos (Governança IA, Público e RIG) devido à estratégia agressiva de parcerias White-Label. Compartilhar banco de dados de IA privada com licitação pública seria um pesadelo técnico e de segurança. Portanto:
    - **Backend:** Separado (`backend/gov_ai`, `backend/gov_muni`, `backend/rig_tech`).
    - **Banco de Dados:** Separado, 100% autônomo por ramo.
    - **Frontend:** Desacoplado na área logada para suportar white-label customizado.
- **Próximos Passos (Para a próxima sessão no projeto):** Iniciar a **Fase 2** do Cronograma (`roadmap.md`), começando pela montagem do Monorepo e setup de infraestrutura/Docker com os bancos separados.
