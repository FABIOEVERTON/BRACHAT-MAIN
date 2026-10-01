import re

with open("site_oficial/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the CAUC specific log with a much stronger, broader feature set
html = html.replace(
    '<div class="cn-label" style="color: #e2c06a; font-weight: bold;">⚖️ RADAR PARA MUNICÍPIOS (CAUC)</div>\n        <div class="cn-title">Risco de bloqueio de repasses evitado! Alerta preventivo.</div>',
    '<div class="cn-label" style="color: #e2c06a; font-weight: bold;">🏛️ GOVERNANÇA MUNICIPAL 360º</div>\n        <div class="cn-title">Licitação auditada (Lei 14.133) e Nova Emenda Parlamentar captada.</div>'
)

# Also update the title in the Simulator if it only says CAUC
html = html.replace(
    "title: 'Diagnóstico: Gestão Municipal & CAUC'",
    "title: 'Diagnóstico: Captação & Auditoria Municipal'"
)
html = html.replace(
    "title: 'Diagnóstico: Gestión Pública & Bloqueos Fiscales'",
    "title: 'Diagnóstico: Captación & Auditoría Municipal'"
)
html = html.replace(
    "title: 'Diagnostic: Public Sector & Fiscal Blockades'",
    "title: 'Diagnostic: Public Sector & Audit Shielding'"
)

with open("site_oficial/index.html", "w", encoding="utf-8") as f:
    f.write(html)
