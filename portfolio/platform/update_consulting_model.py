with open(".wize/DECISIONS.md", "r", encoding="utf-8") as f:
    text = f.read()

new_section = """
## 13. Modelo Híbrido de Escala (Absorção do Mercado de Consultorias Tradicionais)
- **Decisão:** A plataforma BrachaTec atua como a digitalização completa de uma "Consultoria Estratégica de Brasília" (Cobrindo 100% do escopo de escritórios tradicionais, como gestão de recursos, licitações, lobby, auditoria e capacitação).
- **Mecânica de Absorção (A Divisão Inteligente):**
  A operação é dividida em duas camadas para garantir escala infinita e margem de lucro máxima:
  1. **A Camada SaaS (O Trabalho Braçal - Feito pela IA):** Tudo o que for rastreamento de emendas (BTCapta), prestação de contas, monitoramento 24/7 (SIAFI/CAUC) e leitura de editais (BTLicita) é feito por robôs. Isso permite que a BrachaTec atenda centenas de municípios simultaneamente sem inchar a folha de pagamento de consultores humanos.
  2. **A Camada BT Strategy (O Trabalho Premium - Feito por Parceiros):** Tudo o que exigir articulação física em Brasília, assinatura de advogado/contador (OAB/CRC), lobby técnico ou treinamento presencial/eventos, é diagnosticado pela IA e repassado como um *Briefing de Alto Nível* para a rede de parceiros homologados da BrachaTec.
- **Justificativa Comercial:** Consultorias físicas não escalam porque dependem de horas humanas para analisar papéis. O BT Muni analisa os papéis em segundos e só repassa aos parceiros o momento de cobrar os honorários premium. É o fim do modelo artesanal de consultoria pública.
"""

text += new_section

with open(".wize/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(text)
