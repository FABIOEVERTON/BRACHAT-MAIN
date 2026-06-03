from pathlib import Path
import subprocess
from datetime import datetime
import re

# --- CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS ---
VAULT = Path("/Users/mac/brachat-main/05_integration/obsidian/Join_Studies/Obsidian_Vault")
WIKI = VAULT / "02_wiki"
SYSTEM = VAULT / "03_system"
INDEX = SYSTEM / "index.md"
LOG = SYSTEM / "log.md"

def get_clipboard():
    try:
        return subprocess.check_output("pbpaste", text=True)
    except:
        return ""

def build_note(title: str, body: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Remove o título duplicado e o marcador de split
    clean_body = re.sub(r'^#\s+.*?\n', '', body.strip(), flags=re.MULTILINE)
    clean_body = clean_body.replace("###NEXT_NOTE###", "").strip()
    
    return f"""---
type: KIWI_NOTE
title: "{title}"
created: {ts}
source: clipboard
---

# {title}

{clean_body}
"""

def write_note(content: str, title: str):
    # Limpa o título para o sistema de arquivos
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(" ", "_")
    file_name = f"{safe_title}.md"
    
    # FORÇA O CAMINHO PARA DENTRO DA WIKI
    path = WIKI / file_name
    
    # Escreve o arquivo (sobrescreve para evitar duplicados no grafo)
    path.write_text(content, encoding="utf-8")
    return file_name

def update_system(filename: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    note_name = filename.replace('.md', '')
    
    # Atualiza o Index com o caminho relativo correto para o Obsidian
    with open(INDEX, "a", encoding="utf-8") as f:
        # Formato de link que o Obsidian entende mesmo em subpastas
        f.write(f"- [[02_wiki/{note_name}|{note_name}]]\n")
        
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] created {filename} in 02_wiki\n")

def main():
    # Garante que as pastas existam
    WIKI.mkdir(parents=True, exist_ok=True)
    SYSTEM.mkdir(parents=True, exist_ok=True)

    raw_text = get_clipboard()
    if not raw_text.strip():
        return print("Clipboard vazio.")

    # Split pelo marcador exclusivo
    notes = re.split(r'###NEXT_NOTE###', raw_text)
    
    for note_raw in notes:
        if not note_raw.strip() or len(note_raw.strip()) < 5:
            continue
        
        # Busca o título
        title_match = re.search(r'^#\s+(.*)', note_raw, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            lines = [l for l in note_raw.split('\n') if l.strip()]
            title = lines[0][:30].strip() if lines else "Sem_Titulo"

        content = build_note(title, note_raw)
        filename = write_note(content, title)
        update_system(filename)
        print(f"✅ Salvo em 02_wiki: {filename}")

if __name__ == "__main__":
    main()
