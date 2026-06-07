#!/usr/bin/env python3
"""BRACHAT Dashboard — sistema + bridges + 13 agentes via WebSocket."""
import http.server, json, subprocess, time

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
h1{color:#58a6ff;font-size:18px;margin-bottom:4px}
h1 small{color:#8b949e;font-size:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px;margin-bottom:2px}
.card{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:10px}
.card h2{font-size:11px;color:#8b949e;margin:0 0 4px;text-transform:uppercase;letter-spacing:1px}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}
.on{background:#3fb950}.off{background:#484f58}.busy{background:#d29922}.er{background:#f85149}
.row{display:flex;justify-content:space-between;padding:2px 0;font-size:12px}
.row+.row{border-top:1px solid #21262d}
.l{color:#8b949e}.v{color:#c9d1d9;font-weight:600;text-align:right;max-width:60%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.msg{background:#0d1117;border-radius:4px;padding:3px 5px;margin-top:4px;font-size:11px;color:#8b949e;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.footer{text-align:center;color:#484f58;font-size:10px;margin:10px 0}
</style>
</head>
<body>
<h1>BRACHAT <small>painel de controle</small></h1>
<div class="grid">
  <div class="card"><h2><span class="dot" id="d-ezra"></span>Bridge EZRA</h2>
    <div class="row"><span class="l">Status</span><span class="v" id="ezra-status"></span><span class="l" style="margin-left:8px">Agente</span><span class="v" id="ezra-agent"></span></div>
    <div class="row"><span class="l">Uptime</span><span class="v" id="ezra-uptime"></span><span class="l" style="margin-left:8px">Fase</span><span class="v" id="ezra-phase"></span></div>
    <div class="msg" id="ezra-msg"></div><div class="msg" id="ezra-resp"></div></div>
  <div class="card"><h2><span class="dot" id="d-nice"></span>Bridge NICE</h2>
    <div class="row"><span class="l">Status</span><span class="v" id="nice-status"></span><span class="l" style="margin-left:8px">Threshold</span><span class="v" id="nice-threshold"></span></div>
    <div class="row"><span class="l">Uptime</span><span class="v" id="nice-uptime"></span></div>
    <div class="msg" id="nice-msg"></div><div class="msg" id="nice-resp"></div></div>
  <div class="card"><h2>💻 Sistema</h2>
    <div class="row"><span class="l">CPU</span><span class="v" id="sys-cpu"></span><span class="l" style="margin-left:8px">RAM</span><span class="v" id="sys-ram"></span></div>
    <div class="row"><span class="l">Disco</span><span class="v" id="sys-disk"></span><span class="l" style="margin-left:8px">Processos</span><span class="v" id="sys-procs"></span></div>
    <div class="row"><span class="l">Load</span><span class="v" id="sys-load"></span></div></div>
  <div class="card"><h2>📦 Git</h2>
    <div class="row"><span class="l">Branch</span><span class="v" id="git-branch"></span></div>
    <div class="row"><span class="l">Commit</span><span class="v" id="git-commit"></span></div></div>
</div>
<div class="grid" id="daily-header" style="margin-bottom:0"><div class="card" style="grid-column:1/-1;padding:6px 10px"><span id="daily-count"></span> agentes diarios</div></div>
<div class="grid" id="daily-grid"></div>
<div class="grid" id="dir-header" style="margin-bottom:0;margin-top:8px"><div class="card" style="grid-column:1/-1;padding:6px 10px"><span id="dir-count"></span> diretores</div></div>
<div class="grid" id="dir-grid"></div>
<div class="footer" id="footer"></div>
<script>
function set(id,v){ var e=document.getElementById(id); if(e) e.textContent=v??'-' }
function dot(id,st){
  var e=document.getElementById(id);
  if(!e)return;
  e.className='dot '+(st=='online'||st=='idle'?'on':st=='processing'?'busy':st=='error'?'er':'off');
}
function fmtDur(s){ if(!s)return'-'; var h=Math.floor(s/3600),m=Math.floor((s%3600)/60); return h+'h'+m+'m' }
function renderCards(data, gridId, countId){
  var html='', count=0;
  for(var name in data){
    var a=data[name], c=a.cache||{}; count++;
    var phase=[c.current_phase,c.current_module?'M'+c.current_module:'',c.current_day?'D'+c.current_day:''].filter(Boolean).join(' ');
    var info=c.threshold_atual||c.start_date||'';
    var log=''; if(c.daily_log&&c.daily_log.length) log=String(c.daily_log[c.daily_log.length-1]).slice(0,120);
    html+='<div class="card"><h2>'+a.nome+'</h2>';
    if(phase) html+='<div class="row"><span class="v">'+phase+'</span></div>';
    if(info) html+='<div class="row"><span class="l">Info</span><span class="v">'+info+'</span></div>';
    if(log) html+='<div class="msg">'+log+'</div>';
    html+='</div>';
  }
  document.getElementById(gridId).innerHTML=html;
  if(countId) document.getElementById(countId).textContent=count;
}

function connectWS(){
  var ws=new WebSocket('ws://'+location.hostname+':8765');
  ws.onmessage=function(e){
    var d=JSON.parse(e.data);
    var ez=d.bridges.ezra, ni=d.bridges.nice, sys=d.system;
    dot('d-ezra',ez.status); dot('d-nice',ni.status);
    set('ezra-status',ez.status); set('ezra-agent',ez.active_label||ez.active_agent||'-'); set('ezra-phase',ez.phase||'-'); set('ezra-uptime',fmtDur(ez.uptime));
    set('ezra-msg',ez.last_msg?'📩 '+ez.last_msg.slice(0,140):''); set('ezra-resp',ez.last_resp?'💬 '+ez.last_resp.slice(0,140):'');
    set('nice-status',ni.status); set('nice-threshold',ni.threshold||'-'); set('nice-uptime',fmtDur(ni.uptime));
    set('nice-msg',ni.last_msg?'📩 '+ni.last_msg.slice(0,140):''); set('nice-resp',ni.last_resp?'💬 '+ni.last_resp.slice(0,140):'');
    set('sys-cpu',sys.cpu||'-'); set('sys-ram',sys.memory||'-'); set('sys-disk',sys.disk||'-'); set('sys-procs',sys.processes||'-'); set('sys-load',sys.load||'-');
    set('footer','Atualizado: '+d.timestamp);
    if(d.daily) renderCards(d.daily,'daily-grid','daily-count');
    if(d.directors) renderCards(d.directors,'dir-grid','dir-count');
  };
  ws.onclose=function(){ setTimeout(connectWS,2000) };
  ws.onerror=function(){ ws.close() };
}
connectWS();

// Git via HTTP polling (5s)
async function loadGit(){
  var r=await fetch('/api/status'), d=await r.json();
  set('git-branch',d.git.branch||'-'); set('git-commit',d.git.last_commit||'-');
}
setInterval(loadGit,5000); loadGit();
</script>
</body>
</html>"""

def run(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout.strip()
    except: return ""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            data = {
                "git":{
                    "branch":run(["bash","-c","git -C /opt/brachat/repo rev-parse --abbrev-ref HEAD 2>/dev/null||echo -"]),
                    "last_commit":run(["bash","-c","git -C /opt/brachat/repo log --oneline -1 2>/dev/null||echo -"]),
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
