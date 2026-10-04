with open(".wize/DECISIONS.md", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the specific mapping of BTGestor in Section 8 to include the Gerador de Defesa
old_text = "4. **BTGestor:** Microsserviço de gestão e auditoria do CAUC, SIAFI e Transferegov."
new_text = "4. **BTGestor:** Microsserviço de gestão, auditoria (CAUC, SIAFI e Transferegov) e atuação corretiva. Inclui os sub-módulos **BTAssist** (Checklists e formulários) e o **Gerador de Defesa (Advogado IA)** (que elabora automaticamente defesas prévias pro TCE baseadas em jurisprudência e no cofre WORM)."

if old_text in text:
    text = text.replace(old_text, new_text)

with open(".wize/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(text)
