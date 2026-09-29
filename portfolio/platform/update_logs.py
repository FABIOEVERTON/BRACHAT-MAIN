import re

with open("site_oficial/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update Log 1 (Gov AI)
html = html.replace(
    '<div class="cn-label">Filtro CR-058 · Controlador CPT</div>\n        <div class="cn-title">Decisão de IA bloqueada por viés detectado</div>',
    '<div class="cn-label" style="color: #ff5e5e; font-weight: bold;">🚨 GOVERNANÇA DE IA (RUNTIME)</div>\n        <div class="cn-title">Vazamento via Shadow AI bloqueado. Laudo pericial emitido.</div>'
)

# Update Log 2 (Muni)
html = html.replace(
    '<div class="cn-label">Convênio FNS-2024/0847 · RADAR</div>\n        <div class="cn-title">Certidão FGTS vencida — processo travado</div>',
    '<div class="cn-label" style="color: #e2c06a; font-weight: bold;">⚖️ RADAR PARA MUNICÍPIOS (CAUC)</div>\n        <div class="cn-title">Risco de bloqueio de repasses evitado! Alerta preventivo.</div>'
)

# Update Log 3 (Rig)
html = html.replace(
    '<div class="cn-label">PL 2338/2023 · LEX Monitor</div>\n        <div class="cn-title">Proposição com impacto tributário detectada</div>',
    '<div class="cn-label" style="color: #9b85f5; font-weight: bold;">🏛️ RISCO LEGISLATIVO (RIG)</div>\n        <div class="cn-title">Novo Projeto de Lei detectado com impacto tributário.</div>'
)

with open("site_oficial/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Logs updated!")
