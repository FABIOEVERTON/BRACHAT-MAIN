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

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("nice")
START = time.time()

def rj(p):
    try: return json.loads(Path(p).read_text()) if Path(p).exists() else {}
    except: return {}

def git_pull():
    try: subprocess.run(["git","pull"], cwd=REPO, capture_output=True, timeout=15); return True
    except: return False

def git_push(msg="update: nice state"):
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

def pub(**kw):
    try:
        MALHA.parent.mkdir(parents=True, exist_ok=True)
        data = {"type":"nice","timestamp":time.strftime("%H:%M:%S"),"uptime":int(time.time()-START),**kw}
        tmp = MALHA.with_suffix(".tmp")
        tmp.write_text(json.dumps(data)); tmp.rename(MALHA)
    except: pass

def ask_zen(msgs):
    # 1. Tenta OpenCode Zen (Primary)
    b = json.dumps({"model":"big-pickle","messages":msgs,"max_tokens":1024,"temperature":0.2}).encode()
    req = urllib.request.Request(ZN, data=b, headers={"Content-Type":"application/json","Authorization":f"Bearer {ZK}","User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.warning(f"Zen falhou: {e}. Tentando Ollama local (llama3.2:1b)...")
        
    # 2. Fallback local para o Ollama na VPS
    ollama_url = "http://127.0.0.1:11434/v1/chat/completions"
    b_local = json.dumps({"model":"llama3.2:1b","messages":msgs,"max_tokens":1024,"temperature":0.2}).encode()
    req_local = urllib.request.Request(ollama_url, data=b_local, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req_local, timeout=60) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip()
    except Exception as e_local:
        log.error(f"Ollama local falhou: {e_local}")
        return None

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
    agent_dir = REPO/"agents"/"director_agents"/"nice"
    agent_md = agent_dir/"nice.md"
    ac = rj(agent_dir/"cache.json")
    
    shopping_list_path = REPO/"integrations"/"nice"/"shopping_list.json"
    pantry_path = REPO/"integrations"/"nice"/"pantry.json"
    finance_path = REPO/"integrations"/"nice"/"finance.json"
    
    shopping_list = rj(shopping_list_path)
    pantry = rj(pantry_path)
    finance = rj(finance_path)
    
    instructions = agent_md.read_text() if agent_md.exists() else ""
    sysp = (
        f"Voce eh a NICE, agente de governanca domestica BRACHAT.\nData: {time.strftime('%d/%m/%Y %H:%M')}\n\n{instructions}\n\n"
        f"Threshold: {ac.get('threshold_atual','R$100 auto')}\n"
        f"Estado Atual (integrations/nice/):\n"
        f"- Lista de Compras: {json.dumps(shopping_list.get('items', []))}\n"
        f"- Despensa: {json.dumps(pantry.get('categories', {}))}\n"
        f"- Saldo/Financas: {json.dumps(finance)}\n\n"
        f"Regras: Portugues, breve, sem emojis."
    )
    r=ask_zen([{"role":"system","content":sysp},{"role":"user","content":text}])
    if r:
        action_json = None
        if "```json" in r:
            try:
                parts = r.split("```json")
                json_str = parts[1].split("```")[0].strip()
                action_json = json.loads(json_str)
                r = parts[0].strip()
                if len(parts[1].split("```")) > 1:
                    r += "\n" + parts[1].split("```")[1].strip()
                    r = r.strip()
            except Exception as je:
                log.error(f"Erro ao ler JSON de acao: {je}")
        
        if action_json:
            action = action_json.get("action")
            items = action_json.get("items", [])
            if action == "add_to_list" and items:
                shopping_list["items"] = list(set(shopping_list.get("items", []) + items))
                shopping_list["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    shopping_list_path.write_text(json.dumps(shopping_list, indent=2, ensure_ascii=False))
                    log.info(f"Itens adicionados: {items}")
                except Exception as fe: log.error(f"Erro ao salvar shopping_list: {fe}")
            elif action == "remove_from_list" and items:
                shopping_list["items"] = [i for i in shopping_list.get("items", []) if i not in items]
                shopping_list["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    shopping_list_path.write_text(json.dumps(shopping_list, indent=2, ensure_ascii=False))
                    log.info(f"Itens removidos: {items}")
                except Exception as fe: log.error(f"Erro ao salvar shopping_list: {fe}")
            elif action == "update_pantry":
                pantry["categories"] = action_json.get("categories", pantry.get("categories", {}))
                pantry["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    pantry_path.write_text(json.dumps(pantry, indent=2, ensure_ascii=False))
                except Exception as fe: log.error(f"Erro ao salvar pantry: {fe}")
            elif action == "update_balance":
                finance["account_balance"] = action_json.get("balance", finance.get("account_balance", 0.0))
                if "reconciliation" in action_json:
                    finance["reconciliation_log"].append({
                        "date": time.strftime("%Y-%m-%d"),
                        "note": action_json["reconciliation"]
                    })
                finance["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    finance_path.write_text(json.dumps(finance, indent=2, ensure_ascii=False))
                except Exception as fe: log.error(f"Erro ao salvar finance: {fe}")
                
        send(cid,r); log.info(f">> {r[:100]}")
        pub(status="idle",last_msg=text[:200],last_resp=r[:200],threshold=ac.get("threshold_atual",""))
        git_push(f"update: nice state on msg '{text[:20]}'")
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
