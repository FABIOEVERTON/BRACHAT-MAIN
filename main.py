import os
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BrachatMain")

async def start_hermes_loop(app: FastAPI):
    from bot_hermes import get_app as get_hermes
    
    while True:
        try:
            logger.info("Tentando inicializar Bot do Hermes...")
            app.state.hermes_app = get_hermes()
            await app.state.hermes_app.initialize()
            await app.state.hermes_app.updater.start_polling()
            await app.state.hermes_app.start()
            logger.info("Bot do Hermes online e escutando com sucesso!")
            break
        except Exception as e:
            logger.error(f"Erro ao inicializar bot do Hermes: {str(e)}. Tentando novamente em 5 segundos...")
            # Limpa estados para a próxima tentativa
            try:
                if app.state.hermes_app:
                    await app.state.hermes_app.shutdown()
            except:
                pass
            app.state.hermes_app = None
            await asyncio.sleep(5)

async def start_antigravity_loop(app: FastAPI):
    from bot_antigravity import get_app as get_antigravity
    
    while True:
        try:
            logger.info("Tentando inicializar Bot da Antigravity...")
            app.state.antigravity_app = get_antigravity()
            await app.state.antigravity_app.initialize()
            await app.state.antigravity_app.updater.start_polling()
            await app.state.antigravity_app.start()
            logger.info("Bot da Antigravity online e escutando com sucesso!")
            break
        except Exception as e:
            logger.error(f"Erro ao inicializar bot da Antigravity: {str(e)}. Tentando novamente em 5 segundos...")
            # Limpa estados para a próxima tentativa
            try:
                if app.state.antigravity_app:
                    await app.state.antigravity_app.shutdown()
            except:
                pass
            app.state.antigravity_app = None
            await asyncio.sleep(5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # O painel de controle na nuvem serve apenas a interface web premium.
    # O polling dos bots de Telegram e a orquestracao rodam no Mac local (Construtor).
    logger.info("BRACHÁT Core Control Plane iniciado na nuvem.")
    yield
    logger.info("BRACHÁT Core Control Plane encerrado.")

app = FastAPI(title="BRACHÁT Core Control Plane", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BRACHÁT — Painel de Controle</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-primary: #0a0a16;
                --bg-secondary: rgba(18, 18, 38, 0.7);
                --glow-color: rgba(99, 102, 241, 0.15);
                --accent: #6366f1;
                --accent-glow: rgba(99, 102, 241, 0.4);
                --text-main: #f3f4f6;
                --text-muted: #9ca3af;
                --success: #10b981;
                --success-glow: rgba(16, 185, 129, 0.4);
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                background: radial-gradient(circle at 50% 50%, #151530 0%, var(--bg-primary) 80%);
                font-family: 'Outfit', sans-serif;
                color: var(--text-main);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                overflow-x: hidden;
            }

            .container {
                width: 90%;
                max-width: 900px;
                background: var(--bg-secondary);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 24px;
                padding: 40px;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3), 0 0 40px var(--glow-color);
                position: relative;
                animation: fadeIn 1s ease-out;
            }

            .container::before {
                content: '';
                position: absolute;
                top: -1px;
                left: -1px;
                right: -1px;
                bottom: -1px;
                border-radius: 24px;
                background: linear-gradient(45deg, transparent, rgba(99, 102, 241, 0.3), transparent);
                z-index: -1;
                pointer-events: none;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 40px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                padding-bottom: 20px;
            }

            .logo-area {
                display: flex;
                align-items: center;
                gap: 15px;
            }

            .logo-icon {
                width: 48px;
                height: 48px;
                background: linear-gradient(135deg, #6366f1, #a855f7);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                font-size: 24px;
                box-shadow: 0 0 20px var(--accent-glow);
            }

            .logo-title h1 {
                font-size: 24px;
                font-weight: 800;
                letter-spacing: 2px;
                background: linear-gradient(to right, #ffffff, #a855f7);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .logo-title p {
                font-size: 12px;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 1px;
                font-family: 'JetBrains Mono', monospace;
            }

            .status-badge {
                display: flex;
                align-items: center;
                gap: 8px;
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid var(--success);
                padding: 6px 14px;
                border-radius: 50px;
                font-size: 13px;
                font-weight: 600;
                color: var(--success);
                box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
            }

            .status-dot {
                width: 8px;
                height: 8px;
                background-color: var(--success);
                border-radius: 50%;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0% { transform: scale(0.9); box-shadow: 0 0 0 0 var(--success-glow); }
                70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
                100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 25px;
                margin-bottom: 40px;
            }

            .card {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                padding: 24px;
                transition: all 0.3s ease;
            }

            .card:hover {
                transform: translateY(-5px);
                background: rgba(255, 255, 255, 0.04);
                border-color: rgba(99, 102, 241, 0.3);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            }

            .card h3 {
                font-size: 16px;
                color: var(--text-muted);
                margin-bottom: 15px;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-family: 'JetBrains Mono', monospace;
            }

            .agent-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }

            .agent-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 14px;
                background: rgba(255, 255, 255, 0.03);
                border-radius: 8px;
                border-left: 3px solid var(--accent);
            }

            .agent-item span {
                font-weight: 600;
            }

            .agent-item .role {
                font-size: 12px;
                color: var(--text-muted);
                font-family: 'JetBrains Mono', monospace;
            }

            .console {
                background: #050510;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 13px;
                line-height: 1.6;
                color: #a78bfa;
                max-height: 200px;
                overflow-y: auto;
                margin-top: 20px;
                box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
            }

            .console-line::before {
                content: "$ ";
                color: var(--accent);
                font-weight: bold;
            }

            footer-text {
                margin-top: 30px;
                font-size: 12px;
                color: var(--text-muted);
                text-align: center;
                width: 100%;
            }

            .glow-btn {
                background: linear-gradient(135deg, #6366f1, #a855f7);
                border: none;
                color: white;
                padding: 12px 28px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 0 15px var(--accent-glow);
                transition: all 0.3s ease;
                display: block;
                width: fit-content;
                margin: 0 auto;
                text-decoration: none;
                text-align: center;
            }

            .glow-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 0 25px rgba(168, 85, 247, 0.6);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="logo-area">
                    <div class="logo-icon">B</div>
                    <div class="logo-title">
                        <h1>BRACHÁT</h1>
                        <p>Governance Engine v1.0</p>
                    </div>
                </div>
                <div class="status-badge">
                    <div class="status-dot"></div>
                    <span>CONNECTED & SECURE</span>
                </div>
            </header>

            <div class="grid">
                <div class="card">
                    <h3>🛡️ Diretorias Core</h3>
                    <div class="agent-list">
                        <div class="agent-item">
                            <span>Josué</span>
                            <span class="role">Operações/Ops</span>
                        </div>
                        <div class="agent-item">
                            <span>Gilmário</span>
                            <span class="role">Ensino/Branding</span>
                        </div>
                        <div class="agent-item">
                            <span>Aísio</span>
                            <span class="role">Control Plane/Veto</span>
                        </div>
                        <div class="agent-item">
                            <span>Jéssica</span>
                            <span class="role">Jurídico/Legal</span>
                        </div>
                        <div class="agent-item">
                            <span>Nice</span>
                            <span class="role">Doméstico</span>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h3>⚡ Integrações de Governança</h3>
                    <div class="agent-list">
                        <div class="agent-item" style="border-left-color: #10b981;">
                            <span>Git Control</span>
                            <span class="role" style="color: #10b981;">ACTIVE</span>
                        </div>
                        <div class="agent-item" style="border-left-color: #10b981;">
                            <span>Hugging Face Hub</span>
                            <span class="role" style="color: #10b981;">ONLINE</span>
                        </div>
                        <div class="agent-item" style="border-left-color: #a855f7;">
                            <span>Mem0 Cache</span>
                            <span class="role" style="color: #a855f7;">CONNECTED</span>
                        </div>
                        <div class="agent-item" style="border-left-color: #f59e0b;">
                            <span>Commit Limit Gate</span>
                            <span class="role" style="color: #f59e0b;">GATED</span>
                        </div>
                    </div>
                </div>
            </div>

            <a href="https://huggingface.co/spaces/fabiobaruch/brachat-core" target="_blank" class="glow-btn">
                Acessar Hugging Face Space
            </a>

            <div class="console">
                <div class="console-line">SYSTEM BOOTSTRAP COMPLETADO COM SUCESSO.</div>
                <div class="console-line">AÍSIO CONTROL PLANE MONITORANDO MENSAGENS DO HERMES.</div>
                <div class="console-line">CONEXÃO SECURE ESTABELECIDA SOB PROVENIÊNCIA WILLIS.</div>
                <div class="console-line">REGISTRY DE AGENTES ATIVADO COM PERSISTÊNCIA MEM0.</div>
            </div>
        </div>
        <div class="footer-text" style="margin-top: 20px; font-size: 11px; color: var(--text-muted);">
            © 2026 BRACHÁT Ecosystem. Desenvolvido em conjunto com Antigravity.
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/health")
async def health():
    return {"status": "ok", "environment": "Hugging Face Spaces"}

@app.get("/test-telegram")
async def test_telegram():
    import urllib.request
    
    status = {}
    # 1. Verificar presenca de variaveis
    status["TELEGRAM_HERMES_TOKEN_PRESENT"] = bool(os.environ.get("TELEGRAM_HERMES_TOKEN"))
    status["TELEGRAM_ANTIGRAVITY_TOKEN_PRESENT"] = bool(os.environ.get("TELEGRAM_ANTIGRAVITY_TOKEN"))
    status["TELEGRAM_CHAT_ID_PRESENT"] = bool(os.environ.get("TELEGRAM_CHAT_ID"))
    status["GOOGLE_API_KEY_PRESENT"] = bool(os.environ.get("GOOGLE_API_KEY"))
    status["CLICKUP_API_KEY_PRESENT"] = bool(os.environ.get("CLICKUP_API_KEY"))
    
    # 2. Verificar variaveis de proxy no ambiente
    proxy_vars = [k for k in os.environ.keys() if "proxy" in k.lower()]
    status["PROXY_ENV_VARIABLES"] = proxy_vars
    
    # 3. Testar conectividade com api.telegram.org
    try:
        req = urllib.request.Request("https://api.telegram.org", method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            status["TELEGRAM_API_CONNECTIVITY"] = f"OK (Status: {response.status})"
    except Exception as e:
        status["TELEGRAM_API_CONNECTIVITY"] = f"ERROR: {str(e)}"
        
    # 4. Testar conectividade com Google
    try:
        req = urllib.request.Request("https://www.google.com", method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            status["GOOGLE_CONNECTIVITY"] = f"OK (Status: {response.status})"
    except Exception as e:
        status["GOOGLE_CONNECTIVITY"] = f"ERROR: {str(e)}"

    # 5. Testar conectividade com GitHub
    try:
        req = urllib.request.Request("https://github.com", method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            status["GITHUB_CONNECTIVITY"] = f"OK (Status: {response.status})"
    except Exception as e:
        status["GITHUB_CONNECTIVITY"] = f"ERROR: {str(e)}"
        
    return status
