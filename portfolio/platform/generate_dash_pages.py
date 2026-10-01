import re
import os

base_file = "master_admin/frontend/index.html"
with open(base_file, "r", encoding="utf-8") as f:
    html = f.read()

# Fix "Infraestrutura AWS" to "Infraestrutura"
html = html.replace("Infraestrutura AWS", "Infraestrutura")

pages = [
    {"file": "index.html", "id": "telemetria", "name": "Telemetria Global", "icon": "activity"},
    {"file": "clientes.html", "id": "clientes", "name": "Clientes", "icon": "users"},
    {"file": "parceiros.html", "id": "parceiros", "name": "Parceiros WL", "icon": "shield"},
    {"file": "financeiro.html", "id": "financeiro", "name": "Financeiro", "icon": "dollar-sign"},
    {"file": "infraestrutura.html", "id": "infraestrutura", "name": "Infraestrutura", "icon": "layers"},
    {"file": "logs.html", "id": "logs", "name": "Log de Exceções", "icon": "bug"},
    {"file": "cofre.html", "id": "cofre", "name": "Cofre WORM", "icon": "database"}
]

# Create the standard nav block
def build_nav(active_id):
    nav_html = '    <nav class="flex-1 py-4 flex flex-col gap-2 px-2 md:px-4">\n'
    for p in pages:
        if p["id"] == active_id:
            cls = "bg-[#3ecfbe]/10 text-[#3ecfbe] rounded-lg border border-[#3ecfbe]/20 transition-all hover:bg-[#3ecfbe]/20"
        else:
            cls = "text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all border border-transparent"
        
        nav_html += f'      <a href="{p["file"]}" class="flex items-center gap-3 px-3 py-2.5 {cls}">\n'
        nav_html += f'        <i data-lucide="{p["icon"]}" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">{p["name"]}</span>\n'
        nav_html += f'      </a>\n'
    nav_html += '    </nav>'
    return nav_html

# Find the existing <nav> block to replace
nav_pattern = re.compile(r'<nav class="flex-1 py-4 flex flex-col gap-2 px-2 md:px-4">.*?</nav>', re.DOTALL)

# Find the main content area (from <div class="flex-1 overflow-y-auto... to the end of main)
# We will use string splitting
parts = html.split('<!-- DASHBOARD SCROLL AREA -->')
header_part = parts[0]
content_part = parts[1].split('</main>')[0]
footer_part = '</main>' + parts[1].split('</main>')[1]

# Generate each page
for p in pages:
    # Build header with correct nav
    current_header = nav_pattern.sub(build_nav(p["id"]), header_part)
    
    if p["id"] == "telemetria":
        # Keep original content for index
        current_content = '<!-- DASHBOARD SCROLL AREA -->' + content_part
    else:
        # Create a placeholder content for the others
        current_content = f"""<!-- DASHBOARD SCROLL AREA -->
    <div class="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
      <div class="glass-card p-10 rounded-lg flex flex-col items-center justify-center text-center h-[60vh]">
        <i data-lucide="{p["icon"]}" class="w-16 h-16 text-[#3ecfbe] mb-6 opacity-80 animate-bounce"></i>
        <h2 class="text-2xl font-bold text-white mb-2">Módulo: {p["name"]}</h2>
        <p class="text-gray-400 max-w-md">Esta interface está sendo projetada. Os dados de {p["name"].lower()} da arquitetura Shared-Nothing serão conectados em breve.</p>
      </div>
    </div>
"""
    
    final_html = current_header + current_content + footer_part
    with open(f"master_admin/frontend/{p['file']}", "w", encoding="utf-8") as f:
        f.write(final_html)

print("All dashboard pages generated and linked!")
