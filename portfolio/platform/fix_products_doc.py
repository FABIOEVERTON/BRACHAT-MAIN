with open(".wize/DECISIONS.md", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the short version of section 8 with the fully enumerated version
old_section = """## 8. Arquitetura de Microsserviços e Modularidade de Vendas
- **Decisão:** A plataforma oficializa o escopo em **3 Ramos Principais** (BT Gov AI, BT Muni, BT Rig). Contudo, cada "módulo/produto" interno (ex: BTCapta, BTLicita, BTScan) será construído como um **microsserviço 100% independente**, com seu próprio servidor e próprio banco de dados.
- **Justificativa:** Essa hiper-modularidade permite extrema flexibilidade de negócios. O fechamento comercial une os microsserviços sob o guarda-chuva de um "Ramo" (vendendo o pacote completo), mas se a BrachaTec decidir vender o BTCapta isoladamente no futuro, não haverá nenhum gargalo técnico ou acoplamento de código impedindo a venda separada.
- **Estrutura:** 
  - Ramo = Macrosserviço (Ecossistema / Front-end unificado).
  - Produto Interno = Microsserviço (Backend próprio, Banco de dados próprio)."""

new_section = """## 8. Arquitetura de Microsserviços e Nomenclatura dos 8 Produtos
- **Decisão:** A plataforma oficializa o escopo em **3 Ramos Principais**, abrigando **8 Produtos (Microsserviços) 100% independentes**. Cada um dos 8 produtos terá seu próprio servidor e próprio banco de dados isolado.
- **Justificativa:** A hiper-modularidade permite vender o pacote completo do "Ramo" no checkout, mas dá liberdade técnica e comercial para vender qualquer microsserviço isoladamente no futuro.
- **Mapeamento Oficial dos 8 Microsserviços:**

  **RAMO 1: BT Gov AI**
  1. **BTScan:** Microsserviço de mapeamento passivo e diagnóstico de Shadow AI.
  2. **BTMonitor:** Microsserviço de Controlador CPT (Runtime) para interceptação ativa e bloqueio.

  **RAMO 2: BT Muni**
  3. **BTCapta:** Microsserviço de rastreamento e captação de emendas parlamentares.
  4. **BTGestor:** Microsserviço de gestão e auditoria do CAUC, SIAFI e Transferegov.
  5. **BTLicita:** Microsserviço de auditoria em tempo real de licitações (Lei 14.133).

  **RAMO 3: BT Rig**
  6. **BTLex:** Microsserviço de scraping massivo (Câmara, Senado, Diários Oficiais).
  7. **BTAlerta:** Microsserviço de notificações Push/Email sobre impactos tributários.
  8. **BTProva:** Microsserviço gerador de dossiês jurídicos automatizados.

- **Estrutura de Fechamento:** O cliente assina o "Ramo" (Macrosserviço) pelo Master Admin, que orquestra e libera o acesso aos microsserviços subjacentes adquiridos."""

text = text.replace(old_section, new_section)

with open(".wize/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(text)
