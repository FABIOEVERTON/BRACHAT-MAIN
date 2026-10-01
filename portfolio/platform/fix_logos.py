import re
import os

pages = [
    "site_oficial/aigovernance/index.html",
    "site_oficial/publicsector/index.html",
    "site_oficial/rigtech/index.html",
    "site_oficial/academy/index.html",
    "site_oficial/app/login.html",
    "site_oficial/app/cadastro.html"
]

for page in pages:
    if os.path.exists(page):
        with open(page, "r", encoding="utf-8") as f:
            html = f.read()
            
        # Fix logo with a link
        html = re.sub(
            r'<a href="/" class="nav-logo">Bracha<span>Tec</span></a>',
            r'<a href="/" class="nav-logo"><span class="bt-color">B</span>racha<span class="bt-color">T</span>ec</a>',
            html
        )
        
        # Apply CSS/Canvas to login and cadastro if not there yet
        if "PREMIUM OVERRIDE" not in html and "app/" in page:
            canvas_html = '<canvas id="hero-canvas" style="position: fixed; top: 0; left: 0; width: 100%; height: 100vh; z-index: -1; background: radial-gradient(circle at 50% 0%, rgba(10,30,40,1) 0%, #0a0e17 80%); pointer-events: none; opacity: 0.8;"></canvas>\n'
            html = html.replace('<body>', '<body>\n' + canvas_html)
            
            canvas_script = """
            <script>
            const canvas = document.getElementById('hero-canvas');
            if (canvas) {
                const ctx = canvas.getContext('2d');
                let width, height, particles;
                function init() { width = canvas.width = window.innerWidth; height = canvas.height = window.innerHeight; particles = []; for(let i=0; i<50; i++) particles.push({x:Math.random()*width, y:Math.random()*height, vx:(Math.random()-0.5)*0.3, vy:(Math.random()-0.5)*0.3, size:Math.random()*2+1}); }
                function animate() { requestAnimationFrame(animate); ctx.clearRect(0,0,width,height); ctx.fillStyle='#3ecfbe'; ctx.strokeStyle='rgba(62,207,190,0.1)'; particles.forEach(p=>{p.x+=p.vx; p.y+=p.vy; if(p.x<0||p.x>width)p.vx*=-1; if(p.y<0||p.y>height)p.vy*=-1; ctx.beginPath(); ctx.arc(p.x,p.y,p.size,0,Math.PI*2); ctx.fill();}); for(let i=0;i<particles.length;i++){for(let j=i+1;j<particles.length;j++){const dist=Math.hypot(particles[i].x-particles[j].x, particles[i].y-particles[j].y); if(dist<180){ctx.beginPath(); ctx.moveTo(particles[i].x,particles[i].y); ctx.lineTo(particles[j].x,particles[j].y); ctx.lineWidth=1-(dist/180); ctx.stroke();}}} }
                window.addEventListener('resize', init); init(); animate();
            }
            </script>
            </body>
            """
            html = html.replace('</body>', canvas_script)
            
            new_css = """
            <style>
            :root { --navy: #0a0e17 !important; --gold: #3ecfbe !important; --cyan: #3ecfbe !important; }
            body { background-color: var(--navy) !important; }
            .login-box, .auth-box, .card { background: rgba(20, 28, 43, 0.6) !important; backdrop-filter: blur(10px) !important; border: 1px solid rgba(255,255,255,0.05) !important; box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important; border-radius: 12px !important; }
            .bt-color { color: var(--gold) !important; font-weight: 700 !important; }
            /* PREMIUM OVERRIDE */
            </style>
            """
            html = html.replace('</head>', new_css + '</head>')
            
        with open(page, "w", encoding="utf-8") as f:
            f.write(html)
