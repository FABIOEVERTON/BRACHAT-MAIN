with open(".wize/DECISIONS.md", "r", encoding="utf-8") as f:
    text = f.read()

new_section = """
## 9. Visão de Produto: Plataforma de Resolução e Atuação 360º (Não-Notificadora)
- **Decisão:** A plataforma BrachaTec (especialmente o BT Muni e BT Rig) é estritamente proibida de atuar como um "mero notificador de problemas". O sistema é um motor de **Resolução Ativa e Prevenção 360º**.
- **Regras de Atuação (O Padrão Ouro):**
  1. **Monitoramento Preventivo (Anti-Queda):** Robôs (RPA) rodam 24/7 nos portais governamentais (SIAFI, Transferegov, CAUC) para prever o vencimento de certidões e atuar *antes* da queda da documentação, garantindo que o município nunca seja bloqueado de receber repasses.
  2. **Análise de Conformidade 360º:** Editais e contratos são ingeridos pela IA e cruzados linha por linha com a legislação vigente (ex: Lei 14.133), apontando falhas e gerando as retificações necessárias de forma automática.
  3. **Preparação Documental e Defesa (TCU/TCE):** A plataforma não apenas aponta o erro, mas utiliza a base de dados em tempo real e jurisprudência para redigir preventivamente a documentação de defesa para os órgãos de controle.
  4. **Acompanhamento de Convênios:** Rastreabilidade fim-a-fim da prestação de contas dos convênios firmados.
- **Justificativa:** O verdadeiro valor do B2B de alto ticket não é dizer ao prefeito que ele tem um problema, é dizer a ele que o problema existiu, mas o sistema já gerou o ofício de resolução e a defesa jurídica automática.
"""

text += new_section

with open(".wize/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(text)
