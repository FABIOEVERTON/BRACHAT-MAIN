import re

with open('/Users/mac/brachat-main/portfolio/platform/frontend/site_oficial/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Procura o final da grid da academy para inserir o botão embaixo dela
pattern = r'(<div class="ac-desc" data-i18n="ac4-desc">Cultura corporativa contínua.</div>\n\s*</div>\n\s*</div>)'
replacement = r'\1\n    <div style="text-align:center; margin-top: 48px;">\n      <a href="academy/index.html" class="btn" style="background:var(--gold); color:var(--bg); border:none;" data-i18n="btn-go-academy">Acessar a Plataforma Academy →</a>\n    </div>'

content = re.sub(pattern, replacement, content)

# Adiciona tradução para o botão
content = content.replace("'sub-academy':'Educação regulatória estruturada para times que precisam dominar conformidade com profundidade técnica.',",
                          "'sub-academy':'Educação regulatória estruturada para times que precisam dominar conformidade com profundidade técnica.','btn-go-academy':'Acessar a Plataforma Academy →',")
content = content.replace("'sub-academy':'Educación regulatoria estructurada para equipos que necesitan dominar la conformidad.',",
                          "'sub-academy':'Educación regulatoria estructurada para equipos que necesitan dominar la conformidad.','btn-go-academy':'Acceder a la Plataforma Academy →',")
content = content.replace("'sub-academy':'Structured regulatory education for teams that need to master compliance with technical depth.',",
                          "'sub-academy':'Structured regulatory education for teams that need to master compliance with technical depth.','btn-go-academy':'Access the Academy Platform →',")

with open('/Users/mac/brachat-main/portfolio/platform/frontend/site_oficial/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
