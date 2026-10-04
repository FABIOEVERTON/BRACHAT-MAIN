with open(".wize/DECISIONS.md", "r", encoding="utf-8") as f:
    text = f.read()

new_section = """
## 12. Regras de Atuação Dinâmica do BT Muni (Onboarding e Execução)
Para garantir o "AHA Moment" (percepção de valor imediata) e eliminar atritos processuais para a prefeitura, o Ramo 2 (BT Muni) operará com as seguintes mecânicas obrigatórias:
1. **O Choque de Realidade no Onboarding (A "Geral" de Instalação):**
   - No milésimo de segundo em que a prefeitura conecta suas credenciais (SIAFI/CAUC) na plataforma pela primeira vez, o BTGestor executa uma **Auditoria de Raio-X Inicial**.
   - Ele varre todo o passado recente e o status atual, entregando um relatório de impacto na tela: *"Você tem 3 convênios prestes a estourar o prazo no Transferegov, 2 certidões bloqueadas e R$ 400 mil em risco de devolução."* O cliente vê o valor do software no Dia 1.
2. **Auto-Preenchimento de Prestação de Contas:**
   - O módulo de prestação de contas do BTGestor não atua apenas como um validador final. Ele atua como um **"Preparador Antecipado"**.
   - O sistema puxa os metadados do Transferegov e do SIAFI, estrutura os relatórios obrigatórios e já deixa a Prestação de Contas estruturada, aguardando apenas o upload das notas/fotos e o clique de confirmação do usuário. A máquina faz o trabalho braçal da contabilidade pública.
"""

text += new_section

with open(".wize/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(text)
