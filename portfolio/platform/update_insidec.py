with open(".wize/DECISIONS.md", "r", encoding="utf-8") as f:
    text = f.read()

old_section = """## 11. Marketplace de Resolução (Lead Generation Jurídico)
- **Decisão:** A plataforma não apenas resolve problemas via IA, mas atua como um canal de **Geração de Leads (Marketplace B2B)** para escritórios de advocacia parceiros da BrachaTec.
- **Mecânica (O Botão "SOS Jurídico"):** 
  - Quando a prefeitura se depara com um bloqueio grave (CAUC crônico) ou uma notificação pesada do TCE, a IA gera o laudo preliminar e apresenta um botão: *"Solicitar Orçamento de Defesa Especializada"*.
  - O sistema empacota o dossiê (com os hashes WORM) e envia como um "Lead Quente" para a rede de advogados parceiros da BrachaTec.
  - O advogado parceiro avalia o dossiê e envia um orçamento (honorários) diretamente pela plataforma para o prefeito aprovar.
- **Justificativa:** Cria uma nova linha de receita secundária (comissionamento/repasse) e fortalece o ecossistema. A BrachaTec não presta o serviço jurídico, mas se torna a "ponte" (Uber/Marketplace) entre o prefeito desesperado e o advogado especialista de confiança."""

new_section = """## 11. BT Strategy: O Hub Profissional de Consultoria e Representação (Efeito Insidec)
- **Decisão:** Em vez de um simples botão de "SOS Jurídico", a plataforma terá um módulo oficial integrado chamado **BT Strategy** (ou Hub de Serviços Estratégicos). Ele consolida a capacidade de tecnologia da BrachaTec com o *know-how* humano de consultorias de Brasília (parceiros, advogados, contadores).
- **Escopo de Serviços (Oferecidos via Parceiros na Plataforma):**
  1. **Representação Técnica e Articulação Institucional em Brasília:** Para destravar recursos e emendas presencialmente nos ministérios.
  2. **Auditoria Administrativa, Financeira e Tributária:** Quando a plataforma (BT Muni) rastrear um rombo orçamentário crônico, ela recomenda e precifica a intervenção humana da equipe parceira.
  3. **Assessoria Profunda em Licitações e Contratos:** Para casos em que a IA diagnosticou um alto risco de TCU e o município precisa terceirizar a confecção de um edital de alta complexidade.
  4. **Cursos, Treinamentos e Palestras:** A plataforma identifica se os servidores de um município (ou DPOs de uma empresa) estão cometendo muitos erros, e aciona a venda de treinamentos especializados (Academy).
- **Mecânica Profissional:** O dashboard do cliente terá uma vitrine corporativa de "Serviços Especializados". O município solicita o orçamento, a IA empacota o diagnóstico (com hashes WORM e escopo do problema), e repassa como um "Briefing de Alto Nível" para os parceiros (advogados/consultores) da BrachaTec cotarem e assumirem a execução física/jurídica.
- **Justificativa:** Transforma a plataforma em um ecossistema definitivo ("One-Stop-Shop"). O que a tecnologia não pode assinar (por exigir OAB, CRC ou presença física em Brasília), a rede de parceiros homologados BrachaTec resolve, gerando comissionamento/receita cruzada para a plataforma com um posicionamento corporativo premium."""

if old_section in text:
    text = text.replace(old_section, new_section)
else:
    # Fallback to appending if exact string match fails
    text += "\n" + new_section

with open(".wize/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(text)
