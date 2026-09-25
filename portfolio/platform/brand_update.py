import re
import os
import glob

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        # Try with latin-1 or ignore
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

    # 1. Update Product Names
    # Public Sector
    content = re.sub(r'Módulo RADAR & VIGÍLIA', 'BTRadar & BTVigília', content, flags=re.IGNORECASE)
    content = re.sub(r'RADAR & VIGÍLIA', 'BTRadar & BTVigília', content, flags=re.IGNORECASE)
    content = re.sub(r'Módulo COMPRAS', 'BTCompras', content, flags=re.IGNORECASE)
    content = re.sub(r'Módulo EXECUTA', 'BTExecuta', content, flags=re.IGNORECASE)
    # RIG Tech
    content = re.sub(r'Módulo LEX', 'BTLex', content, flags=re.IGNORECASE)
    content = re.sub(r'Módulo ALERTA', 'BTAlerta', content, flags=re.IGNORECASE)
    content = re.sub(r'Módulo PROVA \(Dossiê\)', 'BTProva (Dossiê)', content, flags=re.IGNORECASE)
    content = re.sub(r'Módulo PROVA', 'BTProva', content, flags=re.IGNORECASE)

    # 2. Update BrachaTec brand name
    span_bt = '<span style="color:var(--white);"><span style="color:var(--gold);">B</span>racha<span style="color:var(--gold);">T</span>ec</span>'
    
    chunks = re.split(r'(<[^>]+>)', content)
    for i, chunk in enumerate(chunks):
        if not chunk.startswith('<'):
            chunks[i] = re.sub(r'Brachatec', span_bt, chunk, flags=re.IGNORECASE)
        else:
            chunks[i] = re.sub(r'Brachatec', 'BrachaTec', chunk, flags=re.IGNORECASE)

    content = "".join(chunks)
    
    content = re.sub(r'<title>(.*?)</title>', lambda m: '<title>' + m.group(1).replace(span_bt, 'BrachaTec') + '</title>', content, flags=re.DOTALL|re.IGNORECASE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

files = glob.glob('/Users/mac/brachat-main/portfolio/platform/frontend/site_oficial/**/*.html', recursive=True)
for f in files:
    update_file(f)

print("Branding update finished!")
