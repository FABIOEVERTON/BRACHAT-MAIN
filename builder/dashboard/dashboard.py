#!/usr/bin/env python3
"""BRACHAT Dashboard — status em tempo real dos bridges e servidor."""
import http.server
import json
import subprocess
import time
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8080

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BRACHAT — Painel</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font:14px/1.5 monospace; background:#0d1117; color:#c9d1d9; padding:20px; }
  h1 { color:#58a6ff; font-size:20px; margin-bottom:20px; }
  h1 small { color:#8b949e; font-size:13px; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:12px; }
  .card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:16px; }
  .card h2 { font-size:14px; color:#8b949e; margin-bottom:8px; text-transform:uppercase; letter-spacing:1px; }
  .status { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }
  .ok { background:#3fb950; }
  .warn { background:#d29922; }
  .err { background:#f85149; }
  .row { display:flex; justify-content:space-between; padding:4px 0; }
  .row + .row { border-top:1px solid #21262d; }
  .label { color:#8b949e; }
  .value { color:#c9d1d9; font-weight:600; }
  .msg { background:#0d1117; border-radius:4px; padding:8px; margin-top:8px; font-size:12px; color:#8b949e; }
  .footer { text-align:center; color:#484f58; font-size:11px; margin-top:20px; }
</style>
</head>
<body>
<h1>BRACHAT <small>painel de controle</small></h1>
<div class="grid" id="grid"></div>
<div class="footer" id="footer"></div>
<script>
async function load() {
  const r = await fetch('/api/status');
  const d = await r.json();
  let html = '';

  // Bridges
  for (const name of ['ezra', 'nice']) {
    const b = d.bridges[name];
    html += '<div class="card"><h2><span class="status '+(b.active?'ok':'err')+'"></span>Bridge '+name.toUpperCase()+'</h2>';
    html += '<div class="row"><span class="label">Status</span><span class="value">'+(b.active?'Ativo':'Parado')+'</span></div>';
    html += '<div class="row"><span class="label">PID</span><span class="value">'+(b.pid||'-')+'</span></div>';
    html += '<div class="row"><span class="label">Uptime</span><span class="value">'+(b.uptime||'-')+'</span></div>';
    html += '<div class="row"><span class="label">Memória</span><span class="value">'+(b.memory||'-')+'</span></div>';
    if (b.last_msg) html += '<div class="msg">Ultima mensagem: '+b.last_msg+'</div>';
    html += '</div>';
  }

  // Sistema
  html += '<div class="card"><h2>Sistema</h2>';
  html += '<div class="row"><span class="label">CPU</span><span class="value">'+d.system.cpu+'</span></div>';
  html += '<div class="row"><span class="label">RAM</span><span class="value">'+d.system.memory+'</span></div>';
  html += '<div class="row"><span class="label">Disco</span><span class="value">'+d.system.disk+'</span></div>';
  html += '<div class="row"><span class="label">Uptime</span><span class="value">'+d.system.uptime+'</span></div>';
  html += '</div>';

  // Git
  html += '<div class="card"><h2>Git</h2>';
  html += '<div class="row"><span class="label">Branch</span><span class="value">'+d.git.branch+'</span></div>';
  html += '<div class="row"><span class="label">Ultimo commit</span><span class="value">'+d.git.last_commit+'</span></div>';
  html += '<div class="row"><span class="label">Data</span><span class="value">'+d.git.last_date+'</span></div>';
  html += '</div>';

  document.getElementById('grid').innerHTML = html;
  document.getElementById('footer').textContent = 'Atualizado: '+d.timestamp+' | Auto-refresh a cada 5s';
}
setInterval(load, 5000);
load();
</script>
</body>
</html>"""

def run(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout.strip()
    except: return ""

def sysctl(name):
    out = run(["systemctl", "show", name, "--property=ActiveState,PID,MemoryCurrent,ExecMainStartTimestamp"])
    info = {}
    for line in out.split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            info[k] = v
    return info

def bridge_status(name):
    svc = sysctl(f"brachat-{name}")
    active = svc.get("ActiveState") == "active"
    pid = svc.get("PID", "")
    started = svc.get("ExecMainStartTimestamp", "")
    uptime = ""
    if started:
        try:
            from datetime import datetime
            s = datetime.fromisoformat(started.replace("Z", "+00:00").replace(" ", "T"))
            delta = int(time.time() - s.timestamp())
            h, r = divmod(delta, 3600); m, s = divmod(r, 60)
            uptime = f"{h}h{m}m{s}s"
        except: pass
    mem_raw = svc.get("MemoryCurrent", "")
    mem = ""
    if mem_raw and mem_raw != "0":
        try: mem = f"{int(mem_raw)/1024/1024:.1f}MB"
        except: pass
    # last message from journal
    log = run(["journalctl", "-u", f"brachat-{name}", "--no-pager", "-n", "3", "--output=short-iso"])
    last_msg = ""
    for line in log.split("\n"):
        if "<<" in line or ">>" in line or "msg" in line.lower():
            last_msg = line[-80:] if len(line) > 80 else line
            break
    return {"active": active, "pid": pid, "uptime": uptime, "memory": mem, "last_msg": last_msg}

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            data = {
                "bridges": {
                    "ezra": bridge_status("ezra"),
                    "nice": bridge_status("nice"),
                },
                "system": {
                    "cpu": run(["bash", "-c", "top -bn1 | head -5 | grep 'Cpu(s)' | awk '{print $2}'"]),
                    "memory": run(["bash", "-c", "free -h | grep Mem | awk '{print $3\"/\"$2}'"]),
                    "disk": run(["bash", "-c", "df -h / | tail -1 | awk '{print $3\"/\"$2}'"]),
                    "uptime": run(["uptime", "-p"]),
                },
                "git": {
                    "branch": run(["bash", "-c", "git -C /opt/brachat rev-parse --abbrev-ref HEAD 2>/dev/null || echo '-'"]),
                    "last_commit": run(["bash", "-c", "git -C /opt/brachat log --oneline -1 2>/dev/null || echo '-'"]),
                    "last_date": run(["bash", "-c", "git -C /opt/brachat log -1 --format=%ci 2>/dev/null || echo '-'"]),
                },
                "timestamp": time.strftime("%d/%m/%Y %H:%M:%S"),
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, indent=2).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode())

if __name__ == "__main__":
    print(f"BRACHAT Dashboard em http://{HOST}:{PORT}")
    httpd = http.server.HTTPServer((HOST, PORT), Handler)
    httpd.serve_forever()
