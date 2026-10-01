import re

with open("master_admin/frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the current sidebar nav with the expanded one
old_nav = """    <nav class="flex-1 py-4 flex flex-col gap-2 px-2 md:px-4">
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 bg-[#3ecfbe]/10 text-[#3ecfbe] rounded-lg border border-[#3ecfbe]/20 transition-all hover:bg-[#3ecfbe]/20">
        <i data-lucide="activity" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Telemetria Global</span>
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
        <i data-lucide="layers" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Infraestrutura AWS</span>
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
        <i data-lucide="bug" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Log de Exceções</span>
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
        <i data-lucide="database" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Cofre WORM</span>
      </a>
    </nav>"""

new_nav = """    <nav class="flex-1 py-4 flex flex-col gap-2 px-2 md:px-4">
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 bg-[#3ecfbe]/10 text-[#3ecfbe] rounded-lg border border-[#3ecfbe]/20 transition-all hover:bg-[#3ecfbe]/20">
        <i data-lucide="activity" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Telemetria Global</span>
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
        <i data-lucide="users" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Clientes</span>
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
        <i data-lucide="shield" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Parceiros WL</span>
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
        <i data-lucide="dollar-sign" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Financeiro</span>
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
        <i data-lucide="layers" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Infraestrutura AWS</span>
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
        <i data-lucide="bug" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Log de Exceções</span>
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-all">
        <i data-lucide="database" class="w-5 h-5"></i> <span class="text-sm font-medium hidden md:block">Cofre WORM</span>
      </a>
    </nav>"""

html = html.replace(old_nav, new_nav)

with open("master_admin/frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)
