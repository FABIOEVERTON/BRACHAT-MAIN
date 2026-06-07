#!/usr/bin/env python3
"""BRACHAT Dashboard — sistema + malha real de agentes."""
import http.server, json, subprocess, time
from pathlib import Path

HOST = "0.0.0.0"; PORT = 8080

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BRACHAT — Painel</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font:13px/1.5 monospace;background:#0d1117;color:#c9d1d9;padding:16px}
h1{color:#58a6ff;font-size:18px;margin-bottom:2px}
h1 small,.sub{color:#8b949e;font-size:11px;margin-bottom:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px}
.card{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:12px}
.card h2{font-size:11px;color:#8b949e;margin:0 0 6px;text-transform:uppercase;letter-spacing:1px}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}
.on{background:#3fb950}.off{background:#484f58}.busy{background:#d29922}.er{background:#f85149}
.row{display:flex;justify-content:space-between;padding:2px 0;font-size:12px}
.row+.row{border-top:1px solid #21262d}
.l{color:#8b949e}.v{color:#c9d1d9;font-weight:600;text-align:right;max-width:60%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.msg{background:#0d1117;border-radius:4px;padding:4px 6px;margin-top:6px;font-size:11px;color:#8b949e;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.footer{text-align:center;color:#484f58;font-size:10px;margin-top:14px}
.mini{display:inline-flex;align-items:center;gap:4px;background:#0d1117;border:1px solid #21262d;border-radius:4px;padding:3px 8px;font-size:11px;margin:2px}
</style>
</head>
<body>
<h1>BRACHAT <small>painel de controle</small></h1>

<div class="grid">
  <div class="card"><h2><span class="dot" id="d-ezra"></span>Bridge EZRA</h2>
    <div class="row"><span class="l">Status</span><span class="v" id="ezra-status"></span><span class="l" style="margin-left:12px">Agente</span><span class="v" id="ezra-agent"></span></div>
    <div class="row"><span class="l">Uptime</span><span class="v" id="ezra-uptime"></span><span class="l" style="margin-left:12px">Fase</span><span class="v" id="ezra-phase"></span></div>
    <div class="msg" id="ezra-msg"></div><div class="msg" id="ezra-resp"></div></div>
  <div class="card"><h2><span class="dot" id="d-nice"></span>Bridge NICE</h2>
    <div class="row"><span class="l">Status</span><span class="v" id="nice-status"></span><span class="l" style="margin-left:12px">Threshold</span><span class="v" id="nice-threshold"></span></div>
    <div class="row"><span class="l">Uptime</span><span class="v" id="nice-uptime"></span></div>
    <div class="msg" id="nice-msg"></div><div class="msg" id="nice-resp"></div></div>
  <div class="card"><h2>💻 Sistema</h2>
    <div class="row"><span class="l">CPU</span><span class="v" id="sys-cpu"></span><span class="l" style="margin-left:12px">RAM</span><span class="v" id="sys-ram"></span></div>
    <div class="row"><span class="l">Disco</span><span class="v" id="sys-disk"></span><span class="l" style="margin-left:12px">Uptime</span><span class="v" id="sys-uptime"></span></div></div>
  <div class="card"><h2>📦 Git</h2>
    <div class="row"><span class="l">Branch</span><span class="v" id="git-branch"></span></div>
    <div class="row"><span class="l">Commit</span><span class="v" id="git-commit"></span><span class="l" style="margin-left:12px">Data</span><span class="v" id="git-date"></span></div></div>
</div>

<div style="margin:14px 0 6px;color:#8b949e;font-size:12px;text-transform:uppercase;letter-spacing:1px">📋 <span id="agents-count"></span> Agentes Diarios</div>
<div class="grid" id="daily-grid"></div>

<div class="footer" id="footer"></div>

<script>
function set(id, v){ var e=document.getElementById(id); if(e) e.textContent=v??'-' }
function dot(id, st){
  var e=document.getElementById(id);
  if(!e) return;
  e.className='dot '+(st=='online'||st=='idle'?'on':st=='processing'?'busy':st=='error'?'er':'off');
}

// Sistema (HTTP)
async function loadSys(){
  var r=await fetch('/api/status'), d=await r.json();
  set('sys-cpu',d.system.cpu||'-');
  set('sys-ram',d.system.memory||'-');
  set('sys-disk',d.system.disk||'-');
  set('sys-uptime',d.system.uptime||'-');
  set('git-branch',d.git.branch||'-');
  set('git-commit',d.git.last_commit||'-');
  set('git-date',d.git.last_date||'-');
  set('footer','Atualizado: '+d.timestamp);
}
setInterval(loadSys,5000); loadSys();

// Malha (WebSocket)
function fmtDur(s){ if(!s)return'-'; var h=Math.floor(s/3600),m=Math.floor((s%3600)/60); return h+'h'+m+'m' }
function renderAgents(daily){
  var html='', count=0;
  for(var name in daily){
    var a=daily[name], c=a.cache||{}; count++;
    var phase=c.current_phase||'', mod=c.current_module||'', day=c.current_day||'';
    var log=''; if(c.daily_log&&c.daily_log.length) log=String(c.daily_log[c.daily_log.length-1]).slice(0,120);
    var extra=c.threshold_atual||c.start_date||'';
    html+='<div class="card"><h2>🤖 '+a.nome+'</h2>';
    if(phase||mod) html+='<div class="row"><span class="l">Fase</span><span class="v">'+phase+' '+(mod?'M'+mod:'')+(day?' D'+day:'')+'</span></div>';
    if(extra) html+='<div class="row"><span class="l">Info</span><span class="v">'+extra.slice(0,30)+'</span></div>';
    if(log) html+='<div class="msg">'+log+'</div>';
    html+='</div>';
  }
  document.getElementById('daily-grid').innerHTML=html;
  document.getElementById('agents-count').textContent=count;
}

function connectWS(){
  var ws=new WebSocket('ws://'+location.hostname+':8765');
  ws.onmessage=function(e){
    var d=JSON.parse(e.data);
    // bridges
    var ez=d.bridges.ezra, ni=d.bridges.nice;
    dot('d-ezra',ez.status);
    set('ezra-status',ez.status);
    set('ezra-agent',ez.active_label||ez.active_agent||'-');
    set('ezra-phase',ez.phase||'-');
    set('ezra-uptime',fmtDur(ez.uptime));
    set('ezra-msg',ez.last_msg?'📩 '+ez.last_msg.slice(0,120):'');
    set('ezra-resp',ez.last_resp?'💬 '+ez.last_resp.slice(0,120):'');
    dot('d-nice',ni.status);
    set('nice-status',ni.status);
    set('nice-threshold',ni.threshold||'-');
    set('nice-uptime',fmtDur(ni.uptime));
    set('nice-msg',ni.last_msg?'📩 '+ni.last_msg.slice(0,120):'');
    set('nice-resp',ni.last_resp?'💬 '+ni.last_resp.slice(0,120):'');
    // daily agents
    if(d.daily) renderAgents(d.daily);
  };
  ws.onclose=function(){ setTimeout(connectWS,2000) };
  ws.onerror=function(){ ws.close() };
}
connectWS();
</script>
</body>
</html>"""

def run(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout.strip()
    except: return ""

def sysctl(name):
    out = run(["systemctl","show",name,"--property=ActiveState,PID,MemoryCurrent,ExecMainStartTimestamp"])
    info = {}
    for line in out.split("\n"):
        if "=" in line:
            k,v = line.split("=",1)
            info[k] = v
    return info

def bridge_status(name):
    svc = sysctl(f"brachat-{name}")
    active = svc.get("ActiveState") == "active"
    pid = svc.get("PID","")
    started = svc.get("ExecMainStartTimestamp","")
    uptime = ""
    if started:
        try:
            from datetime import datetime
            s = datetime.fromisoformat(started.replace("Z","+00:00").replace(" ","T"))
            delta = int(time.time()-s.timestamp())
            h,r = divmod(delta,3600); m,s = divmod(r,60)
            uptime = f"{h}h{m}m{s}s"
        except: pass
    mem_raw = svc.get("MemoryCurrent","")
    mem = ""
    if mem_raw and mem_raw != "0":
        try: mem = f"{int(mem_raw)/1024/1024:.1f}MB"
        except: pass
    log = run(["journalctl","-u",f"brachat-{name}","--no-pager","-n","3","--output=short-iso"])
    last_msg = ""
    for line in log.split("\n"):
        if "<<" in line or ">>" in line:
            last_msg = line[-80:]; break
    return {"active":active,"pid":pid,"uptime":uptime,"memory":mem,"last_msg":last_msg}

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            data = {
                "bridges":{"ezra":bridge_status("ezra"),"nice":bridge_status("nice")},
                "system":{
                    "cpu":run(["bash","-c","top -bn1|head -5|grep 'Cpu(s)'|awk '{print $2}'"]),
                    "memory":run(["bash","-c","free -h|grep Mem|awk '{print $3\"/\"$2}'"]),
                    "disk":run(["bash","-c","df -h /|tail -1|awk '{print $3\"/\"$2}'"]),
                    "uptime":run(["uptime","-p"]),
                },
                "git":{
                    "branch":run(["bash","-c","git -C /opt/brachat/repo rev-parse --abbrev-ref HEAD 2>/dev/null||echo -"]),
                    "last_commit":run(["bash","-c","git -C /opt/brachat/repo log --oneline -1 2>/dev/null||echo -"]),
                    "last_date":run(["bash","-c","git -C /opt/brachat/repo log -1 --format=%ci 2>/dev/null||echo -"]),
                },
                "timestamp":time.strftime("%d/%m/%Y %H:%M:%S"),
            }
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(json.dumps(data,indent=2).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode())

if __name__=="__main__":
    print(f"BRACHAT Dashboard em http://{HOST}:{PORT}")
    http.server.HTTPServer((HOST,PORT),Handler).serve_forever()
