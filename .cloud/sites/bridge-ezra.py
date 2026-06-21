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
        subprocess.run(["git","add","."], cwd=REPO, check=True, capture_output=True, timeout=15)
        res = subprocess.run(["git","status","--porcelain"], cwd=REPO, check=True, capture_output=True, text=True, timeout=15)
        if res.stdout.strip():
            subprocess.run(["git","commit","--no-verify","-m",msg], cwd=REPO, check=True, capture_output=True, timeout=15)
            subprocess.run(["git","push"], cwd=REPO, check=True, capture_output=True, timeout=15)
        return True
    except Exception as e: log.error(f"Git push failed: {e}"); return False

def pub_state(**kw):
    try:
        MALHA.parent.mkdir(parents=True, exist_ok=True)
        data = {"type":"ezra","timestamp":time.strftime("%H:%M:%S"),"uptime":int(time.time()-START),"chat":CID,**kw}
        tmp = MALHA.with_suffix(".tmp")
        tmp.write_text(json.dumps(data)); tmp.rename(MALHA)
    except: pass

def get_day_content(day_num):
    path = REPO / "agents" / "studies_agents" / "materials" / "OFICIAL_SCHEDULE.md"
    if not path.exists(): return None
    try: lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as e: log.error(f"Schedule read err: {e}"); return None
    import re
    pat = re.compile(rf"^##\s*MÊS\s*\d+\s*[-—–]\s*DIA\s*{day_num}\b", re.IGNORECASE)
    start = next((i for i, l in enumerate(lines) if pat.match(l)), -1)
    if start == -1: return None
    res = []
    for i in range(start, len(lines)):
        if i > start and re.match(r"^##\s*MÊS\s*\d+", lines[i], re.IGNORECASE): break
        res.append(lines[i])
    return "\n".join(res).strip()

def build_context(msg):
    s, est = rj(REPO/"agents"/"state.json"), rj(REPO/"agents"/"studies_agents"/"studies"/"cache.json")
    now = time.localtime(); hm = now.tm_hour*60+now.tm_min
    agent, label = next(((a,l) for h,m,a,l in reversed(SCHED) if hm >= h*60+m), (None, None))
    ctx = {"user":s.get("user",{}).get("name","Fabio"),"bio":s.get("bio",""),
        "phase":f"{est.get('current_phase','?')} / M{est.get('current_module','?')} / D{est.get('current_day','?')}",
        "label":label,"agent":agent}
    if agent:
        dn = "studies" if agent == "estudos" else agent
        d = REPO/"agents"/"studies_agents"/dn
        if (d/f"{dn}.md").exists(): ctx["inst"] = (d/f"{dn}.md").read_text()[:1500]
        ac = rj(d/"cache.json")
        if ac:
            ctx["agent_cache"] = ac
            if ac.get("daily_log"): ctx["last"] = str(ac["daily_log"][-1])[:200]
    return ctx

def ask_llama(msgs):
    try:
        data = json.dumps({"model":"llama3.2:1b","prompt":json.dumps(msgs),"stream":False}).encode()
        req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=data, headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read())["response"].strip()
    except Exception as e: return f"Erro: Falha ao contatar Ollama ({e})"

def tg(m, d=None):
    try:
        req = urllib.request.Request(f"{TG}/{m}", data=json.dumps(d).encode() if d else None, headers={"Content-Type":"application/json"} if d else {})
        with urllib.request.urlopen(req, timeout=15) as r: return json.loads(r.read())
    except: return None

def send(c, t):
    if t:
        for ch in [t[i:i+4000] for i in range(0,len(t),4000)]: tg("sendMessage",{"chat_id":c,"text":ch,"parse_mode":"Markdown"})

def on_msg(cid, text):
    if not text: return
    log.info(f"<< {text[:100]}"); pub_state(status="processing",last_msg=text[:200])
    if text.startswith("/"):
        if text=="/start": send(cid,"EZRA online.")
        elif text=="/status":
            ctx=build_context("")
            send(cid,f"Fase: {ctx['phase']}\nAgora: {ctx['label']}\nAgente: {ctx.get('agent','-')}")
        elif text.startswith("/tasks") and CK:
            try:
                req = urllib.request.Request(f"https://api.clickup.com/api/v2/list/{os.environ.get('CLICKUP_LIST_ID','901714234972')}/task", headers={"Authorization":CK})
                with urllib.request.urlopen(req, timeout=10) as r: ts = json.loads(r.read()).get("tasks",[])
                send(cid,"\n".join([f"  • {t['name']} ({t['status']['status']})" for t in ts[:10]]) or "Nenhuma tarefa ativa.")
            except Exception as e: send(cid,f"Erro: {e}")
        pub_state(status="idle"); return
    tg("sendChatAction",{"chat_id":cid,"action":"typing"})
    git_pull(); ctx=build_context(text)
    sysp = f"Voce eh o EZRA, orquestrador BRACHAT. Assistente de {ctx['user']}. Data: {time.strftime('%d/%m/%Y %H:%M')}. Fase: {ctx['phase']}. Atividade: {ctx['label']}. Contexto: {ctx.get('bio','')}"
    if ctx.get("inst"): sysp += f"\n\nInstrucoes do agente ativo:\n{ctx['inst']}"
    if ctx.get("last"): sysp += f"\n\nUltimo progresso: {ctx['last']}"
    import re
    day_match = re.search(r"\b[Dd]ia\s+(\d+)\b", text)
    if day_match:
        day_num = day_match.group(1); day_content = get_day_content(day_num)
        if day_content:
            sysp += f"\n\nConteudo do cronograma oficial para o Dia {day_num}:\n{day_content}"
            sysp += f"\n\nQuando o usuario colocar 'dia X' (onde X eh o numero solicitado), busque o que tem que ser ensnado no bloco correspondente acima e apresente de forma objetiva, guiando-o no aprendizado e na execucao das tarefas e evidencias daquele dia."
    sysp += "\n\nSe o usuario pedir para criar uma tarefa no ClickUp ou na agenda, inclua a tag [CREATE_TASK: Nome da Tarefa] no inicio ou final da resposta. Exemplo: [CREATE_TASK: Comprar cafe]."
    sysp += "\n\nResponda em portugues. Seja direto. Nao use emojis."
    r=ask_llama([{"role":"system","content":sysp},{"role":"user","content":text}])
    if r:
        if "[CREATE_TASK:" in r and CK:
            try:
                s_idx = r.find("[CREATE_TASK:") + 13; e_idx = r.find("]", s_idx); t_name = r[s_idx:e_idx].strip()
                req = urllib.request.Request(f"https://api.clickup.com/api/v2/list/{os.environ.get('CLICKUP_LIST_ID','901714234972')}/task", data=json.dumps({"name": t_name}).encode(), headers={"Authorization": CK, "Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=15): log.info(f"Task created: {t_name}")
                r = r.replace(f"[CREATE_TASK:{r[s_idx:e_idx]}]", "").strip() + f"\n\n[✓] Tarefa '{t_name}' criada no ClickUp!"
            except Exception as e: log.error(f"ClickUp task error: {e}"); r += f"\n\n[x] Nao consegui criar a tarefa: {e}"
        send(cid,r); log.info(f">> {r[:100]}")
        pub_state(status="idle",active_agent=ctx.get("agent"),active_label=ctx.get("label"),last_msg=text[:200],last_resp=r[:200],phase=ctx.get("phase"))
        git_push(f"update: ezra state on msg '{text[:20]}'")
    else:
        send(cid,"Erro. Tente de novo."); pub_state(status="error")

def main():
    st = rj(ST) if ST.exists() else {"last_update_id":0}
    log.info(f"EZRA iniciado. Chat: {CID}"); git_pull(); pub_state(status="online")
    while True:
        try:
            u = tg("getUpdates", {"offset":st.get("last_update_id",0)+1,"timeout":10,"allowed_updates":["message"]})
            if u and u.get("ok") and u.get("result"):
                for up in u["result"]:
                    st["last_update_id"] = up["update_id"]
                    if "message" in up and str(up["message"].get("chat",{}).get("id","")) == CID and "text" in up["message"]:
                        on_msg(CID, up["message"]["text"].strip())
            ST.write_text(json.dumps(st)); time.sleep(1)
        except KeyboardInterrupt: break
        except Exception as e: log.error(f"loop: {e}"); time.sleep(5)

if __name__=="__main__": main()
