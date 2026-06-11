#!/usr/bin/env python3
"""EZRA Bridge — orquestrador BRACHAT no Telegram."""
import os, sys, json, time, subprocess, urllib.request, logging
from pathlib import Path

TK = os.environ["TELEGRAM_TOKEN"]
CID = os.environ["ALLOWED_CHAT_ID"]
ZK = os.environ["ZEN_API_KEY"]
CK = os.environ.get("CLICKUP_TOKEN","")
REPO = Path("/opt/brachat/repo")
ST = Path("/tmp/ezra-state.json")
MALHA = Path("/opt/brachat/state/malha.json")
TG = f"https://api.telegram.org/bot{TK}"
ZN = "https://opencode.ai/zen/v1/chat/completions"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ezra")
START = time.time()

SCHED = [(7,0,"*","Saudacao"),(7,15,"justus","Job scan"),(7,30,"john","Ingles"),
    (8,0,"estudos","Estudo"),(8,30,"google","Google Skills"),(9,0,"estudos","Deep work"),
    (11,0,"dev","Python"),(12,0,None,"Almoco"),(14,0,"estudos","Deep work"),
    (17,0,"showcase","Portfolio"),(18,0,None,"Livre"),(20,0,"aristotle","Tora"),
    (21,0,None,"Review"),(22,30,None,"Dormir")]

def rj(p):
    try: return json.loads(Path(p).read_text()) if Path(p).exists() else {}
    except: return {}

def git_pull():
    try: subprocess.run(["git","pull"], cwd=REPO, capture_output=True, timeout=15); return True
    except: return False

def git_push(msg="update: ezra state"):
    try:
        subprocess.run(["git", "add", "."], cwd=REPO, check=True, capture_output=True, timeout=15)
        res = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, check=True, capture_output=True, text=True, timeout=15)
        if res.stdout.strip():
            subprocess.run(["git", "commit", "--no-verify", "-m", msg], cwd=REPO, check=True, capture_output=True, timeout=15)
            subprocess.run(["git", "push"], cwd=REPO, check=True, capture_output=True, timeout=15)
            log.info("Git changes pushed successfully.")
        return True
    except Exception as e:
        log.error(f"Git push failed: {e}")
        return False

def pub_state(**kw):
    try:
        MALHA.parent.mkdir(parents=True, exist_ok=True)
        now = time.strftime("%H:%M:%S")
        data = {"type":"ezra","timestamp":now,"uptime":int(time.time()-START),
            "chat":CID,**kw}
        tmp = MALHA.with_suffix(".tmp")
        tmp.write_text(json.dumps(data))
        tmp.rename(MALHA)
    except: pass

def build_context(msg):
    s = rj(REPO/"assistant_agents"/"state.json")
    est = rj(REPO/"assistant_agents"/"daily"/"estudos"/"cache.json")
    now = time.localtime(); hm = now.tm_hour*60+now.tm_min
    agent = label = None
    for h,m,a,l in SCHED:
        if hm >= h*60+m: agent, label = a, l
    ctx = {"user":s.get("user",{}).get("name","Fabio"),"bio":s.get("bio",""),
        "phase":f"{est.get('current_phase','?')} / M{est.get('current_module','?')} / D{est.get('current_day','?')}",
        "label":label,"agent":agent}
    if agent:
        d = REPO/"assistant_agents"/"daily"/agent
        if (d/"AGENT.md").exists(): ctx["inst"] = (d/"AGENT.md").read_text()[:1500]
        ac = rj(d/"cache.json")
        if ac:
            ctx["agent_cache"] = ac
            if "daily_log" in ac and ac["daily_log"]:
                ctx["last"] = str(ac["daily_log"][-1])[:200]
    return ctx

def ask_zen(msgs):
    # 1. Tenta OpenCode Zen (Primary)
    b = json.dumps({"model":"big-pickle","messages":msgs,"max_tokens":2048,"temperature":0.3}).encode()
    req = urllib.request.Request(ZN, data=b, headers={"Content-Type":"application/json","Authorization":f"Bearer {ZK}","User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.warning(f"Zen falhou: {e}. Tentando Ollama local (llama3.2:1b)...")
        
    # 2. Fallback local
    return "O sistema principal (OpenCode Zen) está indisponível e a VPS não possui recursos (RAM) para rodar a IA localmente. Tente novamente mais tarde."

def tg(m, d=None):
    url = f"{TG}/{m}"
    if d: d = json.dumps(d).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=d, headers={"Content-Type":"application/json"}) if d else urllib.request.Request(url), timeout=15) as r:
            return json.loads(r.read())
    except: return None

def send(c, t):
    if not t: return
    for ch in [t[i:i+4000] for i in range(0,len(t),4000)]:
        tg("sendMessage",{"chat_id":c,"text":ch,"parse_mode":"Markdown"})

def on_msg(cid, text):
    if not text: return
    log.info(f"<< {text[:100]}")
    pub_state(status="processing",last_msg=text[:200])
    if text.startswith("/"):
        if text=="/start": send(cid,"EZRA online.")
        elif text=="/status":
            ctx=build_context("")
            send(cid,f"Fase: {ctx['phase']}\nAgora: {ctx['label']}\nAgente: {ctx.get('agent','-')}")
        elif text.startswith("/tasks") and CK:
            try:
                list_id = os.environ.get("CLICKUP_LIST_ID", "901714234972")
                req=urllib.request.Request(f"https://api.clickup.com/api/v2/list/{list_id}/task",headers={"Authorization":CK})
                with urllib.request.urlopen(req,timeout=10) as r:
                    ts=json.loads(r.read()).get("tasks",[])
                send(cid,"\n".join([f"  • {t['name']} ({t['status']['status']})" for t in ts[:10]]) or "Nenhuma tarefa ativa.")
            except Exception as e: send(cid,f"Erro: {e}")
        pub_state(status="idle")
        return
    tg("sendChatAction",{"chat_id":cid,"action":"typing"})
    git_pull(); ctx=build_context(text)
    sysp = f"Voce eh o EZRA, orquestrador BRACHAT. Assistente de {ctx['user']}. Data: {time.strftime('%d/%m/%Y %H:%M')}. Fase: {ctx['phase']}. Atividade: {ctx['label']}. Contexto: {ctx.get('bio','')}"
    if ctx.get("inst"): sysp += f"\n\nInstrucoes do agente ativo:\n{ctx['inst']}"
    if ctx.get("last"): sysp += f"\n\nUltimo progresso: {ctx['last']}"
    sysp += "\n\nSe o usuario pedir para criar uma tarefa no ClickUp ou na agenda, inclua a tag [CREATE_TASK: Nome da Tarefa] no inicio ou final da resposta. Exemplo: [CREATE_TASK: Comprar cafe]."
    sysp += "\n\nResponda em portugues. Seja direto. Nao use emojis."
    
    r=ask_zen([{"role":"system","content":sysp},{"role":"user","content":text}])
    if r:
        if "[CREATE_TASK:" in r and CK:
            try:
                start_idx = r.find("[CREATE_TASK:") + len("[CREATE_TASK:")
                end_idx = r.find("]", start_idx)
                task_name = r[start_idx:end_idx].strip()
                list_id = os.environ.get("CLICKUP_LIST_ID", "901714234972")
                url_create = f"https://api.clickup.com/api/v2/list/{list_id}/task"
                payload = json.dumps({"name": task_name}).encode()
                req_create = urllib.request.Request(url_create, data=payload, headers={
                    "Authorization": CK,
                    "Content-Type": "application/json"
                }, method="POST")
                with urllib.request.urlopen(req_create, timeout=15) as resp_c:
                    log.info(f"Tarefa criada com sucesso via NLP: {task_name}")
                r = r.replace(f"[CREATE_TASK:{r[start_idx:end_idx]}]", "").strip()
                r += f"\n\n[✓] Tarefa '{task_name}' criada no ClickUp!"
            except Exception as ex_c:
                log.error(f"Erro ao criar tarefa via NLP: {ex_c}")
                r += f"\n\n[x] Nao consegui criar a tarefa: {ex_c}"
                
        send(cid,r); log.info(f">> {r[:100]}")
        pub_state(status="idle",active_agent=ctx.get("agent"),active_label=ctx.get("label"),
            last_msg=text[:200],last_resp=r[:200],phase=ctx.get("phase"))
        git_push(f"update: ezra state on msg '{text[:20]}'")
    else:
        send(cid,"Erro. Tente de novo.")
        pub_state(status="error")

def main():
    st={"last_update_id":0}
    if ST.exists():
        try: st=json.loads(ST.read_text())
        except: pass
    log.info(f"EZRA iniciado. Chat: {CID}")
    git_pull()
    pub_state(status="online")
    while True:
        try:
            u=tg("getUpdates",{"offset":st.get("last_update_id",0)+1,"timeout":10,"allowed_updates":["message"]})
            if u and u.get("ok") and u.get("result"):
                for up in u["result"]:
                    st["last_update_id"]=up["update_id"]
                    if "message" in up:
                        m=up["message"]
                        if str(m.get("chat",{}).get("id",""))==CID and "text" in m:
                            on_msg(CID,m["text"].strip())
            ST.write_text(json.dumps(st))
            time.sleep(1)
        except KeyboardInterrupt: log.info("Shutdown."); break
        except Exception as e: log.error(f"loop: {e}"); time.sleep(5)

if __name__=="__main__": main()
