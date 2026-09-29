import re
import os

pages = [
    "site_oficial/aigovernance/index.html",
    "site_oficial/publicsector/index.html",
    "site_oficial/rigtech/index.html",
    "site_oficial/academy/index.html"
]

canvas_html = '<canvas id="hero-canvas" style="position: fixed; top: 0; left: 0; width: 100%; height: 100vh; z-index: -1; background: radial-gradient(circle at 50% 0%, rgba(10,30,40,1) 0%, #0a0e17 80%); pointer-events: none; opacity: 0.8;"></canvas>\n'

canvas_script = """
<script>
// High-Tech WebGL/Canvas Node Network Animation (Background)
const canvas = document.getElementById('hero-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height, particles;
    function init() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      particles = [];
      const particleCount = window.innerWidth < 768 ? 30 : 70;
      for(let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          size: Math.random() * 2 + 1
        });
      }
    }
    function animate() {
      requestAnimationFrame(animate);
      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = '#3ecfbe';
      ctx.strokeStyle = 'rgba(62, 207, 190, 0.1)';
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
          if(dist < 180) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.lineWidth = 1 - (dist / 180);
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

new_css = """
<style>
/* PREMIUM OVERRIDE - HIGH TECH ABYSSAL INK */
:root {
  --navy: #0a0e17 !important;
  --navy-2: #101622 !important;
  --navy-3: #141c2b !important;
  --navy-4: #1e2d44 !important;
  --gold: #3ecfbe !important;
  --gold-2: #cef79e !important;
  --cyan: #3ecfbe !important;
  --cyan-dim: rgba(62,207,190,0.1) !important;
  --violet: #9b85f5 !important;
  --white: #f8f9fa !important;
  --serif: 'Inter', sans-serif !important;
}
body { background-color: var(--navy) !important; }
.dor-card, .price-card, .wf-item, .filtro-cat, .ramo-card, .faq-item, .mod-card, .curso-card {
  background: rgba(20, 28, 43, 0.6) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(255,255,255,0.05) !important;
  transition: all 0.4s ease !important;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
  border-radius: 12px !important;
}
.dor-card:hover, .price-card:hover, .wf-item:hover, .filtro-cat:hover, .ramo-card:hover, .mod-card:hover, .curso-card:hover {
  border-color: rgba(62,207,190,0.3) !important;
  transform: translateY(-5px) !important;
  box-shadow: 0 10px 40px rgba(62,207,190,0.1) !important;
}
section[id],div[id]{scroll-margin-top: 40vh !important;}
.bt-color { color: var(--gold) !important; font-weight: 700 !important; }
</style>
"""

for page in pages:
    if os.path.exists(page):
        with open(page, "r", encoding="utf-8") as f:
            html = f.read()

        # Check if already injected
        if "PREMIUM OVERRIDE" in html:
            continue
            
        # Update Logo
        html = html.replace(
            '<div class="nav-logo">Bracha<span>Tec</span></div>',
            '<div class="nav-logo"><span class="bt-color">B</span>racha<span class="bt-color">T</span>ec</div>'
        )
        html = html.replace(
            '<span style="color:var(--white);"><span style="color:var(--gold);">B</span>racha<span style="color:var(--gold);">T</span>ec</span>',
            '<span style="color:var(--white);"><span class="bt-color">B</span>racha<span class="bt-color">T</span>ec</span>'
        )

        # Inject HTML and CSS
        html = html.replace('<body>', '<body>\n' + canvas_html)
        html = html.replace('</body>', canvas_script)
        html = html.replace('</head>', new_css + '</head>')
        
        with open(page, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Enhanced {page}")

print("All pages successfully upgraded to Premium!")
