with open(".wize/DECISIONS.md", "r", encoding="utf-8") as f:
    text = f.read()

new_section = """
## 10. Evoluções Críticas de Escopo (Anti-Churn e Venda em Lote)
Com base em simulações de Inteligência de Enxame (MiroFish) focadas no mercado real (ex: Municípios do Maranhão), a arquitetura incorpora duas exigências inegociáveis para garantir a adoção e barrar o churn:

1. **Evolução do BTGestor para BTAssist:**
   - **O Problema:** Municípios pequenos sem equipe técnica não conseguem agir em cima de um alerta de bloqueio.
   - **A Solução (BTAssist):** Todo alerta de restrição no CAUC/SIAFI gerado pelo BTGestor deve ser acompanhado de um "Checklist Guiado", gerando automaticamente os formulários e ofícios em PDF no formato exigido pela Receita/Órgão. A plataforma passa de um monitor para um solucionador braçal.

2. **Venda em Bloco (BT GovFed - Arquitetura de Consórcio):**
   - **O Problema:** Federações (ex: FAMEM) ou Consórcios Públicos compram licenças em lote, mas os prefeitos rejeitam a adoção por medo de perderem a soberania dos dados ou darem munição (liability) para opositores políticos que comandam a Federação.
   - **A Solução (BT GovFed):** Implementação obrigatória de *Master-Tenant Architecture* com consentimento granular. A Federação paga o boleto unificado e vê apenas a "taxa de adesão" no seu dashboard (quantos municípios ativaram). Os laudos WORM, dados financeiros e de licitação (BTLicita) de cada município ficam trancados criptograficamente apenas para o CPF/CNPJ do próprio prefeito. O consentimento e a trilha de isolamento de dados são gravados via hash SHA-256 no Cofre.
"""

text += new_section

with open(".wize/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(text)
