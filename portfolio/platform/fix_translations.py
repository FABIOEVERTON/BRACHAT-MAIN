import re

with open("site_oficial/index.html", "r", encoding="utf-8") as f:
    html = f.read()

def replace_dict_val(lang, key, new_val):
    global html
    # Find the language block (es: { ... } or en: { ... })
    pattern = r'(' + lang + r':\s*\{.*?)(\'' + key + r'\':\s*\'.*?\')(.*?\})'
    replacement = r"\1'" + key + "':'" + new_val + r"'\3"
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# SPANISH TRANSLATIONS
replace_dict_val('es', 'ramo1-name', '<span class=\"bt-color\">BT</span> Gov AI')
replace_dict_val('es', 'ramo2-name', '<span class=\"bt-color\">BT</span> Muni')
replace_dict_val('es', 'ramo3-name', '<span class=\"bt-color\">BT</span> Rig')

replace_dict_val('es', 'ramo1-desc', 'Nuestra plataforma actúa en <strong>Runtime</strong>. Interceptamos y bloqueamos sesgos o violaciones (Shadow AI) en el momento de la decisión. Con BTScan y BTMonitor, mapee y bloquee fugas utilizando superXAi, generando informes periciales SHA-256.')
replace_dict_val('es', 'ramo2-desc', 'Monitoreo continuo y <strong>activo</strong> del CAUC, TCE y certificados (diferente de alertas pasivas). Capte recursos (BTCapta), gestione en Transferegov (BTGestor) y audite licitaciones con seguridad (BTLicita) sin perder convenios.')
replace_dict_val('es', 'ramo3-desc', 'Inteligencia de Riesgo Legislativo con informes instantáneos (IA). Monitoree Cámara, Senado y Diarios Oficiales (BTLex), reciba alertas anticipadas (BTAlerta) y genere expedientes jurídicos (BTProva) antes que la competencia.')

# ENGLISH TRANSLATIONS
replace_dict_val('en', 'ramo1-name', '<span class=\"bt-color\">BT</span> Gov AI')
replace_dict_val('en', 'ramo2-name', '<span class=\"bt-color\">BT</span> Muni')
replace_dict_val('en', 'ramo3-name', '<span class=\"bt-color\">BT</span> Rig')

replace_dict_val('en', 'ramo1-desc', 'Our platform operates in <strong>Runtime</strong>. We intercept and block bias or violations (Shadow AI) at the moment of decision. With BTScan and BTMonitor, map and block leaks using superXAi, generating SHA-256 forensic reports.')
replace_dict_val('en', 'ramo2-desc', 'Continuous and <strong>active</strong> monitoring of CAUC, TCE, and certificates (unlike passive alerts). Capture federal funds (BTCapta), manage projects (BTGestor), and safely audit procurements (BTLicita) without losing covenants.')
replace_dict_val('en', 'ramo3-desc', 'Legislative Risk Intelligence with instant AI dossiers. Monitor the House, Senate, and Official Gazettes (BTLex), receive early warnings (BTAlerta), and generate legal dossiers (BTProva) ahead of the competition.')

with open("site_oficial/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Translations fixed!")
