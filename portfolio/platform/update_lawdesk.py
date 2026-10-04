with open(".wize/DECISIONS.md", "r", encoding="utf-8") as f:
    text = f.read()

new_section = """
## 11. Marketplace de Resolução (Lead Generation Jurídico)
- **Decisão:** A plataforma não apenas resolve problemas via IA, mas atua como um canal de **Geração de Leads (Marketplace B2B)** para escritórios de advocacia parceiros da BrachaTec.
- **Mecânica (O Botão "SOS Jurídico"):** 
  - Quando a prefeitura se depara com um bloqueio grave (CAUC crônico) ou uma notificação pesada do TCE, a IA gera o laudo preliminar e apresenta um botão: *"Solicitar Orçamento de Defesa Especializada"*.
  - O sistema empacota o dossiê (com os hashes WORM) e envia como um "Lead Quente" para a rede de advogados parceiros da BrachaTec.
  - O advogado parceiro avalia o dossiê e envia um orçamento (honorários) diretamente pela plataforma para o prefeito aprovar.
- **Justificativa:** Cria uma nova linha de receita secundária (comissionamento/repasse) e fortalece o ecossistema. A BrachaTec não presta o serviço jurídico, mas se torna a "ponte" (Uber/Marketplace) entre o prefeito desesperado e o advogado especialista de confiança.
"""

text += new_section

with open(".wize/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(text)
