import re

with open("frontend/site_oficial/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Logo (Ensure it targets the nav-logo and footer logo properly)
html = html.replace(
    '<div class="nav-logo">Bracha<span>Tec</span></div>',
    '<div class="nav-logo"><span class="bt-color">B</span>racha<span class="bt-color">T</span>ec</div>'
)
html = html.replace(
    '<span style="color:var(--white);"><span style="color:var(--gold);">B</span>racha<span style="color:var(--gold);">T</span>ec</span>',
    '<span style="color:var(--white);"><span class="bt-color">B</span>racha<span class="bt-color">T</span>ec</span>'
)

# 2. Add Canvas and Script
canvas_html = '<canvas id="hero-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100vh; z-index: 0; background: radial-gradient(circle at 50% 0%, rgba(10,30,40,1) 0%, #0a0e17 80%); pointer-events: none;"></canvas>\n'
html = html.replace('<body>', '<body>\n' + canvas_html)

canvas_script = """
<script>
// High-Tech WebGL/Canvas Node Network Animation
const canvas = document.getElementById('hero-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height, particles;
    function init() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      particles = [];
      const particleCount = window.innerWidth < 768 ? 40 : 100;
      for(let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          size: Math.random() * 2 + 1
        });
      }
    }
    function animate() {
      requestAnimationFrame(animate);
      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = '#3ecfbe';
      ctx.strokeStyle = 'rgba(62, 207, 190, 0.15)';
      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        if(p.x < 0 || p.x > width) p.vx *= -1;
        if(p.y < 0 || p.y > height) p.vy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      });
      for(let i = 0; i < particles.length; i++) {
        for(let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if(dist < 150) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.lineWidth = 1 - (dist / 150);
            ctx.stroke();
          }
        }
      }
    }
    window.addEventListener('resize', init);
    init();
    animate();
}
</script>
</body>
"""
html = html.replace('</body>', canvas_script)

# 3. Modify CSS for new theme
new_css = """
<style>
/* NOVO ESTILO BT */
:root{
  --navy:#0a0e17; --navy-2:#101622; --navy-3:#141c2b; --navy-4:#1e2d44;
  --gold:#3ecfbe; --gold-2:#cef79e; --gold-3:#f0d990;
  --gold-dim:rgba(62,207,190,.12); --gold-border:rgba(62,207,190,.3);
  --white:#f7f4ee; --white-2:#e8e3d8;
  --muted:#9ba1a6; --muted-2:rgba(247,244,238,.32);
  --cyan:#3ecfbe; --cyan-dim:rgba(62,207,190,.1);
  --violet:#9b85f5; --violet-dim:rgba(155,133,245,.1);
  --green:#4caf82; --red:#ff5e5e;
  --serif:'Inter', sans-serif;
  --sans:'Inter', system-ui, sans-serif;
  --r:8px; --r2:12px; --r3:16px;
  --nav-h:72px; --max:1200px; --pad:5%;
}
.bt-color { color: var(--gold); font-weight: 700; }
.chain-node {
    background: rgba(20, 28, 43, 0.6) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08) !important;
    animation: float 6s ease-in-out infinite;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    border-radius: 12px;
}
.chain-node:nth-child(2) { animation-delay: 1s; border-color: rgba(255,94,94,0.3) !important; }
.chain-node:nth-child(3) { animation-delay: 2s; }
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
.hero-inner { z-index: 2; position: relative; }
</style>
"""
html = html.replace('</head>', new_css + '</head>')

# 4. Enhance Descriptions in JS i18n Dictionary
# Ramo 1: Add Runtime / Interceptação
old_ramo1 = "'ramo1-desc':'Governança contínua de ponta a ponta. Com o BTScan e BTMonitor, mapeie Shadow AI, bloqueie vazamentos de dados usando o superXAi e gere laudos forenses SHA-256.'"
new_ramo1 = "'ramo1-desc':'Nossa plataforma atua em <strong>Runtime</strong>. Interceptamos e bloqueamos enviesamentos ou violações (Shadow AI) no momento da decisão. Com o BTScan e BTMonitor, mapeie e bloqueie vazamentos usando o superXAi, gerando laudos periciais SHA-256.'"
html = html.replace(old_ramo1, new_ramo1)

# Ramo 2: Add Ativo vs Passivo
old_ramo2 = "'ramo2-desc':'A plataforma executiva para prefeituras. Capte recursos federais automaticamente (BTCapta), faça gestão de obras no Transferegov/SIAFI (BTGestor) e audite licitações com segurança (BTLicita).'"
new_ramo2 = "'ramo2-desc':'Monitoramento contínuo e <strong>ativo</strong> do CAUC, TCE e certidões (diferente de alertas passivos). Capte recursos (BTCapta), faça gestão no Transferegov (BTGestor) e audite licitações com segurança (BTLicita) sem perder convênios.'"
html = html.replace(old_ramo2, new_ramo2)

# Ramo 3: BTRig enhancement
old_ramo3 = "'ramo3-desc':'Inteligência legislativa em tempo real. Monitore Câmara, Senado e Diários (BTLex), receba alertas antecipados de risco (BTAlerta) e gere dossiês jurídicos (BTProva).'"
new_ramo3 = "'ramo3-desc':'Inteligência de Risco Legislativo com dossiês instantâneos (IA). Monitore Câmara, Senado e Diários (BTLex), receba alertas antecipados (BTAlerta) e gere dossiês jurídicos (BTProva) antes da concorrência.'"
html = html.replace(old_ramo3, new_ramo3)

# 5. Fix BT Product Titles
html = html.replace('Gov IA</span>', '<span class="bt-color">BT</span> Gov AI</span>')
html = html.replace('Setor Público</span>', '<span class="bt-color">BT</span> Muni</span>')
html = html.replace('BTRig</span>', '<span class="bt-color">BT</span> Rig</span>')

with open("site_oficial/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Merged perfectly!")
