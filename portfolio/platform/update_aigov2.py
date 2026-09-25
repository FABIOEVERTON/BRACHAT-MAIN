import re

with open('/Users/mac/brachat-main/portfolio/platform/frontend/site_oficial/aigovernance/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix BTMonitor
pattern1 = r'proxy reverso Commit-Bound com latência zero.*?vazamentos \(PII\) e ataques \(Jailbreak\)\.'
repl1 = 'Proxy reverso Commit-Bound com latência zero. O motor avalia instantaneamente 129 filtros de compliance em runtime (barrando PII, CPFs e código-fonte). SIMULTANEAMENTE, o BTMonitor aplica o <strong>QILIS Framework</strong> "em voo", extraindo a assinatura matemática da intenção do usuário para detectar e bloquear injeções de prompt ocultas.'
content = re.sub(pattern1, repl1, content, flags=re.DOTALL)

# Fix Vault
pattern2 = r'O sistema emite automaticamente um Relatório de Explicabilidade \(RIPD\) impossível de ser fraudado, garantindo prova pericial imediata para juízes e conselhos de compliance em caso de litígio\.'
repl2 = 'O sistema emite automaticamente um Relatório de Explicabilidade (RIPD). Esse laudo não possui apenas o registro do evento, mas carrega o <strong>Hash SHA-256 + a Assinatura Matemática QILIS</strong>, fornecendo a prova pericial inquestionável da intenção original para juízes e conselhos de compliance.'
content = re.sub(pattern2, repl2, content, flags=re.DOTALL)

with open('/Users/mac/brachat-main/portfolio/platform/frontend/site_oficial/aigovernance/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
