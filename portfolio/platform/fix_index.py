import re

with open("site_oficial/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix scroll-margin-top to 40vh (middle of the screen)
html = html.replace('section[id],div[id]{scroll-margin-top: 25vh;}', 'section[id],div[id]{scroll-margin-top: 40vh;}')

# Inject "rastreamento de emendas" into Ramo 2 (BT Muni)
# PT
old_ramo2_pt = "'ramo2-desc':'Monitoramento contínuo e <strong>ativo</strong> do CAUC, TCE e certidões (diferente de alertas passivos). Capte recursos (BTCapta), faça gestão no Transferegov (BTGestor) e audite licitações com segurança (BTLicita) sem perder convênios.'"
new_ramo2_pt = "'ramo2-desc':'Monitoramento contínuo do CAUC e rastreamento de <strong>emendas parlamentares</strong>. Capte recursos (BTCapta), faça gestão no Transferegov (BTGestor) e audite licitações com segurança (BTLicita) antecipando bloqueios.'"
html = html.replace(old_ramo2_pt, new_ramo2_pt)

# ES
old_ramo2_es = "'ramo2-desc':'Monitoreo continuo y <strong>activo</strong> del CAUC, TCE y certificados (diferente de alertas pasivas). Capte recursos (BTCapta), gestione en Transferegov (BTGestor) y audite licitaciones con seguridad (BTLicita) sin perder convenios.'"
new_ramo2_es = "'ramo2-desc':'Monitoreo continuo del CAUC y rastreo de <strong>enmiendas parlamentarias</strong>. Capte recursos (BTCapta), gestione en Transferegov (BTGestor) y audite licitaciones con seguridad (BTLicita) previniendo bloqueos.'"
html = html.replace(old_ramo2_es, new_ramo2_es)

# EN
old_ramo2_en = "'ramo2-desc':'Continuous and <strong>active</strong> monitoring of CAUC, TCE, and certificates (unlike passive alerts). Capture federal funds (BTCapta), manage projects (BTGestor), and safely audit procurements (BTLicita) without losing covenants.'"
new_ramo2_en = "'ramo2-desc':'Continuous CAUC monitoring and tracking of <strong>parliamentary amendments</strong>. Capture federal funds (BTCapta), manage projects (BTGestor), and safely audit procurements (BTLicita) preempting blockages.'"
html = html.replace(old_ramo2_en, new_ramo2_en)

with open("site_oficial/index.html", "w", encoding="utf-8") as f:
    f.write(html)
