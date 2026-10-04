with open(".wize/DECISIONS.md", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the specific mapping of BTGestor in Section 8 again to include Prestação de Contas
old_text = "4. **BTGestor:** Microsserviço de gestão, auditoria (CAUC, SIAFI e Transferegov) e atuação corretiva. Inclui os sub-módulos **BTAssist** (Checklists e formulários) e o **Gerador de Defesa (Advogado IA)** (que elabora automaticamente defesas prévias pro TCE baseadas em jurisprudência e no cofre WORM)."
new_text = "4. **BTGestor:** Microsserviço de gestão, prestação de contas, auditoria (CAUC, SIAFI e Transferegov) e atuação corretiva. Inclui os sub-módulos **BTAssist** (Checklists e formulários), **Análise de Prestação de Contas IA** (validação cruzada de notas fiscais, extratos e medições de obras antes do envio para não reprovar convênios) e o **Gerador de Defesa (Advogado IA)** (que elabora automaticamente defesas prévias para o TCE baseadas em jurisprudência e no cofre WORM)."

if old_text in text:
    text = text.replace(old_text, new_text)

with open(".wize/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(text)
