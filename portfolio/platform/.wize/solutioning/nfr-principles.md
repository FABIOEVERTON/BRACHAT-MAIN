# Princípios de Requisitos Não-Funcionais (NFR)

1. **Latência de Intercepção CPT:** O Controlador CPT deve avaliar regras de conformidade e filtros em menos de **50ms** (*P99 < 100ms*).
2. **Imutabilidade e Integridade Criptográfica:** 100% dos laudos e eventos forenses devem ter assinatura SHA-256 encadeada com o laudo imediatamente anterior.
3. **Isolamento Multi-Tenant:** Zero vazamento de dados entre clientes. Cada tenant possui seu próprio schema e chaves criptográficas isoladas.
4. **Disponibilidade & Resiliência:** SLA alvo de 99.9% para serviços Enterprise e Municipal, com fail-closed para regras de segurança.
5. **Acessibilidade & Responsividade:** Interface do usuário em conformidade com diretrizes WCAG 2.1 AA e suporte completo de mobile a monitores ultrawide.
