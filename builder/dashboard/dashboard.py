#!/usr/bin/env python3
"""BRACHAT Dashboard — organograma bridges + diretores + operarios."""
import http.server, json, subprocess, time

HOST = "0.0.0.0"; PORT = 8080

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BRACHAT — Organograma</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font:13px/1.5 monospace;background:#0d1117;color:#c9d1d9;padding:16px;text-align:center}
h1{color:#58a6ff;font-size:18px;margin-bottom:18px}
h1 small{color:#8b949e;font-size:12px}
.lvl{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;position:relative;margin-bottom:24px}
.lvl:not(:last-child)::after{content:'';display:block;position:absolute;bottom:-14px;left:50%;width:2px;height:10px;background:#30363d}
.lvl-label{width:100%;font-size:10px;color:#484f58;text-transform:uppercase;letter-spacing:2px;margin-bottom:2px}
.card{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:8px 12px;min-width:130px;text-align:left;position:relative}
.card.orchestrator{background:#1f6feb11;border-color:#1f6feb66;min-width:180px}
.card.director{background:#d2992211;border-color:#d2992266}
.card.operario{background:#3fb95011;border-color:#3fb95044}
.card h2{font-size:11px;color:#8b949e;margin:0 0 3px;text-transform:uppercase;letter-spacing:1px}
.card h2 b{color:#c9d1d9;text-transform:none;letter-spacing:0}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:3px}
.on{background:#3fb950}.off{background:#484f58}.busy{background:#d29922}.er{background:#f85149}
.row{display:flex;justify-content:space-between;padding:1px 0;font-size:11px}
.l{color:#8b949e}.v{color:#c9d1d9;max-width:55%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:right}
.msg{background:#0d1117;border-radius:3px;padding:2px 4px;margin-top:3px;font-size:10px;color:#8b949e;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.connector{position:relative;height:20px;margin:-8px 0}
.connector::before{content:'';position:absolute;top:0;left:50%;width:2px;height:100%;background:#30363d}
.connector::after{content:'';position:absolute;top:50%;left:0;right:0;height:2px;background:#30363d}
.footer{text-align:center;color:#484f58;font-size:10px;margin:14px 0}
</style>
</head>
<body>
<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:18px">
  <h1 style="margin:0">BRACHAT <small>organograma</small></h1>
  <div style="font-size:10px;color:#8b949e;text-align:right">
    <div>💻 <span id="sys-cpu"></span> · <span id="sys-ram"></span> · <span id="sys-load"></span></div>
    <div style="margin-top:1px">📦 <span id="git-branch"></span> <span id="git-commit"></span></div>
  </div>
</div>

<!-- ORCHESTRATOR -->
<div class="lvl"><div class="lvl-label">orquestrador</div>
  <div class="card orchestrator" id="orchestrator-card">
    <h2><span class="dot" id="d-ezra"></span>Bridge <b>EZRA</b></h2>
    <div class="row"><span class="l">Status</span><span class="v" id="ezra-status"></span></div>
    <div class="row"><span class="l">Agente ativo</span><span class="v" id="ezra-agent"></span></div>
    <div class="row"><span class="l">Fase</span><span class="v" id="ezra-phase"></span></div>
    <div class="msg" id="ezra-msg"></div><div class="msg" id="ezra-resp"></div>
  </div>
  <div class="card" style="min-width:auto;flex:0">
    <h2><span class="dot" id="d-nice"></span>Bridge <b>NICE</b></h2>
    <div class="row"><span class="l"><span id="nice-status"></span></span><span class="v" id="nice-threshold"></span></div>
    <div class="msg" id="nice-msg"></div>
  </div>
</div>

<!-- DIRECTORS -->
<div class="lvl"><div class="lvl-label">diretores</div>
  <div id="dir-grid" style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px"></div>
</div>

<!-- OPERARIOS -->
<div class="lvl"><div class="lvl-label"><span id="daily-count"></span> operarios</div>
  <div id="daily-grid" style="display:flex;flex-wrap:wrap;justify-content:center;gap:6px"></div>
</div>

<div class="footer" id="footer"></div>
<script>
function set(id,v){ var e=document.getElementById(id); if(e) e.textContent=v??'-' }
function dot(id,st){
  var e=document.getElementById(id);
  if(!e)return;
  e.className='dot '+(st=='online'||st=='idle'?'on':st=='processing'?'busy':st=='error'?'er':'off');
}
function fmtDur(s){ if(!s)return'-'; var h=Math.floor(s/3600),m=Math.floor((s%3600)/60); return h+'h'+m+'m' }

function cardHTML(a,cl){
  var c=a.cache||{};
  var fase=[c.current_phase||'',c.current_module?'M'+c.current_module:'',c.current_day?'D'+c.current_day:''].filter(Boolean).join(' ')||'-';
  var info=c.threshold_atual||c.ultima_tarefa||c.ultima_acao||c.start_date||'';
  var log='';
  if(c.daily_log&&typeof c.daily_log==='object'){
    if(Array.isArray(c.daily_log)&&c.daily_log.length) log=String(c.daily_log[c.daily_log.length-1]).slice(0,80);
    else if(Object.keys(c.daily_log).length) log=JSON.stringify(Object.values(c.daily_log).pop()).slice(0,80);
  }
  var ativo=fase!='-'||!!info||!!log;
  var html='<div class="card '+cl+'"><h2><b>'+a.nome+'</b>&nbsp;<span class="dot '+(ativo?'on':'off')+'"></span></h2>';
  html+='<div class="row"><span class="l">Status</span><span class="v"><b>'+(ativo?'🟢 Ativo':'⭘ Inativo')+'</b></span></div>';
  html+='<div class="row"><span class="l">Fase</span><span class="v">'+fase+'</span></div>';
  html+='<div class="row"><span class="l">Info</span><span class="v">'+(info||'-')+'</span></div>';
  if(log) html+='<div class="msg">'+log+'</div>';
  return html+'</div>';
}

function renderOrg(data,gridId,cl,countId){
  var html='',count=0;
  for(var n in data){ count++; html+=cardHTML(data[n],cl); }
  document.getElementById(gridId).innerHTML=html;
  if(countId) document.getElementById(countId).textContent=count;
}

function connectWS(){
  var ws=new WebSocket('ws://'+location.hostname+':8765');
  ws.onmessage=function(e){
    var d=JSON.parse(e.data), ez=d.bridges.ezra, ni=d.bridges.nice, sys=d.system;
    dot('d-ezra',ez.status); dot('d-nice',ni.status);
    set('ezra-status',ez.status+' · '+fmtDur(ez.uptime));
    set('ezra-agent',ez.active_label||ez.active_agent||'-');
    set('ezra-phase',ez.phase||'-');
    set('ezra-msg',ez.last_msg?'📩 '+ez.last_msg.slice(0,130):'');
    set('ezra-resp',ez.last_resp?'💬 '+ez.last_resp.slice(0,130):'');
    set('nice-status',ni.status); set('nice-threshold',ni.threshold||'-');
    set('nice-msg',ni.last_msg?'📩 '+ni.last_msg.slice(0,100):'');
    set('sys-cpu','CPU '+sys.cpu+'%'); set('sys-ram','RAM '+sys.memory); set('sys-load','Load '+sys.load);
    set('footer','Atualizado: '+d.timestamp);
    if(d.directors) renderOrg(d.directors,'dir-grid','director');
    if(d.daily) renderOrg(d.daily,'daily-grid','operario','daily-count');
  };
  ws.onclose=function(){ setTimeout(connectWS,2000) };
  ws.onerror=function(){ ws.close() };
}
connectWS();

// Git via HTTP (5s)
async function loadGit(){
  var r=await fetch('/api/status'), d=await r.json();
  set('git-branch',d.git.branch||''); set('git-commit',d.git.last_commit||'');
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
    print(f"BRACHAT Organograma em http://{HOST}:{PORT}")
    http.server.HTTPServer((HOST,PORT),Handler).serve_forever()
