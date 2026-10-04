import os

recuperar_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Recuperar Senha — BrachaTec</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; background-color: #0a0e17; color: #f8f9fa; margin: 0; }
    .glass-card { background: rgba(20, 28, 43, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 10px 30px rgba(0,0,0,0.3); border-radius: 12px; }
    .input-field { width: 100%; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 12px 16px; border-radius: 8px; outline: none; transition: border 0.2s; }
    .input-field:focus { border-color: #3ecfbe; }
    .btn-primary { background: #3ecfbe; color: #0a0e17; font-weight: 700; width: 100%; padding: 12px; border-radius: 8px; text-transform: uppercase; transition: all 0.2s; }
    .btn-primary:hover { background: #f8f9fa; }
  </style>
</head>
<body class="min-h-screen flex items-center justify-center relative">
  <canvas id="bg-canvas" class="fixed top-0 left-0 w-full h-full -z-10 opacity-30"></canvas>
  <div class="glass-card p-8 w-full max-w-md m-4">
    <div class="text-center mb-8">
      <h1 class="text-2xl font-bold tracking-widest text-white mb-2"><span class="text-[#3ecfbe]">B</span>racha<span class="text-[#3ecfbe]">T</span>ec</h1>
      <p class="text-sm text-gray-400">Recuperação de Acesso Seguro</p>
    </div>
    <form class="space-y-5" onsubmit="event.preventDefault(); alert('Link enviado.'); window.location.href='login.html';">
      <div>
        <label class="block text-xs font-medium text-gray-400 mb-1 uppercase tracking-wider">E-mail corporativo cadastrado</label>
        <div class="relative">
          <input type="email" class="input-field pl-10" placeholder="voce@empresa.com.br" required>
          <i data-lucide="mail" class="w-5 h-5 text-gray-500 absolute left-3 top-3.5"></i>
        </div>
      </div>
      <button type="submit" class="btn-primary flex justify-center items-center gap-2">
        <i data-lucide="key" class="w-4 h-4"></i> Enviar Link
      </button>
      <div class="text-center mt-4">
        <a href="login.html" class="text-xs text-gray-400 hover:text-[#3ecfbe] transition-colors">Voltar para o Login</a>
      </div>
    </form>
  </div>
  <script>lucide.createIcons();</script>
</body>
</html>"""
with open("site_oficial/app/recuperar-senha.html", "w", encoding="utf-8") as f:
    f.write(recuperar_html)

config_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__BRANCH_NAME__ — Configurações</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; background-color: #060913; color: #f8f9fa; margin: 0; }
    .glass-card { background: rgba(14, 21, 33, 0.6); backdrop-filter: blur(12px); border: 1px solid __BORDER_COLOR__; box-shadow: 0 4px 30px rgba(0,0,0,0.5); }
    .input-field { width: 100%; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 10px 14px; border-radius: 6px; outline: none; font-size: 14px; }
    .input-field:focus { border-color: __TEXT_COLOR__; }
    .btn-save { background: __TEXT_COLOR__; color: #000; font-weight: 600; padding: 10px 24px; border-radius: 6px; transition: all 0.2s; }
    .btn-save:hover { opacity: 0.8; }
  </style>
</head>
<body class="flex h-screen">
  <main class="flex-1 overflow-y-auto p-8">
    <a href="dashboard.html" class="text-gray-400 hover:text-white flex items-center gap-2 mb-6"><i data-lucide="arrow-left" class="w-4 h-4"></i> Voltar ao Painel</a>
    <h2 class="text-2xl font-bold text-white mb-6 flex items-center gap-2">
      <i data-lucide="settings" class="w-6 h-6 __TEXT_CLASS__"></i> Configurações (__BRANCH_NAME__)
    </h2>
    <div class="max-w-3xl space-y-6">
      <div class="glass-card p-6 rounded-xl">
        <h3 class="text-sm font-mono text-gray-400 uppercase tracking-widest mb-4">Dados da Conta</h3>
        <div class="grid grid-cols-2 gap-4">
          <div><label class="block text-xs mb-1 text-gray-400">Nome</label><input type="text" class="input-field" value="__ADMIN_NAME__"></div>
          <div><label class="block text-xs mb-1 text-gray-400">E-mail</label><input type="email" class="input-field" value="__ADMIN_EMAIL__"></div>
          <div class="col-span-2"><label class="block text-xs mb-1 text-gray-400">__ORG_LABEL__</label><input type="text" class="input-field" value="__ORG_VALUE__"></div>
        </div>
        <div class="mt-4 flex justify-end"><button class="btn-save">Salvar Alterações</button></div>
      </div>
      <div class="glass-card p-6 rounded-xl">
        <h3 class="text-sm font-mono text-gray-400 uppercase tracking-widest mb-4">Integrações Específicas</h3>
        __SPECIFIC_HTML__
        <div class="mt-4 flex justify-end"><button class="btn-save">Atualizar Integrações</button></div>
      </div>
    </div>
  </main>
  <script>lucide.createIcons();</script>
</body>
</html>"""

def make_config(branch, border, text, tclass, name, email, label, value, specific):
    s = config_template.replace("__BRANCH_NAME__", branch)
    s = s.replace("__BORDER_COLOR__", border)
    s = s.replace("__TEXT_COLOR__", text)
    s = s.replace("__TEXT_CLASS__", tclass)
    s = s.replace("__ADMIN_NAME__", name)
    s = s.replace("__ADMIN_EMAIL__", email)
    s = s.replace("__ORG_LABEL__", label)
    s = s.replace("__ORG_VALUE__", value)
    s = s.replace("__SPECIFIC_HTML__", specific)
    return s

gov_ai = make_config("BT Gov AI", "rgba(62,207,190,0.1)", "#3ecfbe", "text-[#3ecfbe]", "Dr. Carlos", "dpo@hospital.com", "Empresa", "Hospital Einstein", '<input type="password" class="input-field" value="sk-123">')
muni = make_config("BT Muni", "rgba(234,179,8,0.1)", "#eab308", "text-yellow-500", "Prefeito", "gab@sp.gov.br", "Prefeitura", "São Paulo", '<input type="text" class="input-field" value="IBGE: 3550308">')
rig = make_config("BT Rig", "rgba(168,85,247,0.1)", "#a855f7", "text-purple-500", "Marina", "marina@adv.br", "Consultoria", "Alpha Gov", '<input type="text" class="input-field" value="Keywords: Tributos">')

with open("gov_ai/frontend/configuracoes.html", "w", encoding="utf-8") as f: f.write(gov_ai)
with open("gov_muni/frontend/configuracoes.html", "w", encoding="utf-8") as f: f.write(muni)
with open("rig_tech/frontend/configuracoes.html", "w", encoding="utf-8") as f: f.write(rig)
print("Done")
