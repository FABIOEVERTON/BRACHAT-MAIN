#!/usr/bin/env python3
"""NICE Bridge — governança doméstica BRACHAT no Telegram."""
import os, sys, json, time, subprocess, urllib.request, logging
from pathlib import Path

TK = os.environ.get("NICE_TELEGRAM_TOKEN","")
CID = os.environ.get("NICE_ALLOWED_CHAT_ID","")
ZK = os.environ.get("ZEN_API_KEY","")
CK = os.environ.get("CLICKUP_TOKEN","")
REPO = Path("/opt/brachat/repo")
ST = Path("/tmp/nice-state.json")
MALHA = Path("/opt/brachat/state/nice.json")
TG = f"https://api.telegram.org/bot{TK}"
ZN = "https://opencode.ai/zen/v1/chat/completions"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("/tmp/nice.log"),logging.StreamHandler()])
log = logging.getLogger("nice")
START = time.time()

def rj(p):
    try: return json.loads(Path(p).read_text()) if Path(p).exists() else {}
    except: return {}

def git_pull():
    try: subprocess.run(["git","pull"], cwd=REPO, capture_output=True, timeout=15); return True
    except: return False

def pub(**kw):
    try:
        MALHA.parent.mkdir(parents=True, exist_ok=True)
        data = {"type":"nice","timestamp":time.strftime("%H:%M:%S"),"uptime":int(time.time()-START),**kw}
        tmp = MALHA.with_suffix(".tmp")
        tmp.write_text(json.dumps(data)); tmp.rename(MALHA)
    except: pass

def ask_zen(msgs):
    b = json.dumps({"model":"big-pickle","messages":msgs,"max_tokens":1024,"temperature":0.2}).encode()
    req = urllib.request.Request(ZN, data=b, headers={"Content-Type":"application/json","Authorization":f"Bearer {ZK}","User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip()
    except Exception as e: log.error(f"Zen: {e}"); return None

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
    pub(status="processing",last_msg=text[:200])
    if text.startswith("/"):
        if text=="/start": send(cid,"NICE online.")
        pub(status="idle"); return
    tg("sendChatAction",{"chat_id":cid,"action":"typing"})
    git_pull()
    agent_dir = REPO/"assistant_agents"/"daily"/"nice"
    agent_md = agent_dir/"AGENT.md"
    ac = rj(agent_dir/"cache.json")
    instructions = agent_md.read_text()[:2000] if agent_md.exists() else ""
    sysp = f"Voce eh a NICE, agente de governanca domestica BRACHAT.\nData: {time.strftime('%d/%m/%Y %H:%M')}\n\n{instructions}\n\nThreshold: {ac.get('threshold_atual','R$100 auto')}\nRegras: Portugues, breve, sem emojis."
    r=ask_zen([{"role":"system","content":sysp},{"role":"user","content":text}])
    if r:
        send(cid,r); log.info(f">> {r[:100]}")
        pub(status="idle",last_msg=text[:200],last_resp=r[:200],threshold=ac.get("threshold_atual",""))
    else:
        send(cid,"Erro."); pub(status="error")

def main():
    st={"last_update_id":0}
    if ST.exists():
        try: st=json.loads(ST.read_text())
        except: pass
    log.info(f"NICE iniciado. Chat: {CID}")
    git_pull(); pub(status="online")
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
