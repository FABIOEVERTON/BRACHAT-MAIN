#!/usr/bin/env python3
"""Josué — Vendas. Poder absoluto.
Recebe fotos + link OLX + preco do usuario, sai vendendo."""
import os, sys, json, time, urllib.request, logging, threading, requests as req, re
from pathlib import Path
from datetime import datetime

TK = os.environ.get("JOSUE_TELEGRAM_TOKEN", "")
CID = os.environ.get("JOSUE_ALLOWED_CHAT_ID", "8035491919")
ZK = os.environ["ZEN_API_KEY"]
GK = os.environ.get("GO_API_KEY", "")
CK = os.environ.get("CLICKUP_TOKEN", "")
TG = f"https://api.telegram.org/bot{TK}"
PENDING = Path("/tmp/josue-pending-task.json")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("josue")

DATA = Path("/opt/brachat/state/josue")
DATA.mkdir(exist_ok=True)
PRODS_FILE = DATA / "produtos.json"
PHOTOS_DIR = DATA / "fotos"
PHOTOS_DIR.mkdir(exist_ok=True)

SYSP = """Você é JOSUÉ, assistente de vendas.
REGRAS:
1. VENDA. Recebe fotos + link OLX + preco + descricao do dono. Sai vendendo.
2. So sai pra vender QUANDO tiver TODOS: fotos, link OLX, preco.
3. Promove o link da OLX + fotos + texto. Nao inventa precos.
4. Comprador interessado = manda o link da OLX. A venda fecha por la.
5. Negocia ATE 15% de desconto. Acima = pergunta dono.
6. Gera Pix se pedirem (pergunta dono antes).
7. SEMPRE educado e respeitoso."""

def load_json(p, default=None):
    if p.exists():
        try: return json.loads(p.read_text())
        except: return default or {}
    return default or {}

def save_json(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def ask_llm(msgs):
    for model, key, api_url in [
        ("big-pickle", ZK, "https://opencode.ai/zen/v1/chat/completions"),
        ("kimi-k2.6", GK, "https://opencode.ai/go/v1/chat/completions"),
    ]:
        if not key: continue
        try:
            data = json.dumps({"model": model, "messages": msgs, "stream": False}).encode()
            req = urllib.request.Request(api_url, data=data, headers={
                "Content-Type": "application/json", "Authorization": f"Bearer {key}",
                "User-Agent": "curl/8.0"
            })
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())["choices"][0]["message"]["content"].strip()
        except Exception as e:
            log.warning(f"LLM {model}: {e}")
            continue
    return "Erro sem resposta."

def tg(method, data=None):
    try:
        url = f"{TG}/{method}"
        body = json.dumps(data).encode() if data else None
        hdrs = {"Content-Type": "application/json"} if data else {}
        req = urllib.request.Request(url, data=body, headers=hdrs)
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        log.error(f"TG {method}: {e}")
        return None

def send(chat_id, text):
    if not text: return
    for ch in [text[i:i+4000] for i in range(0, len(text), 4000)]:
        tg("sendMessage", {"chat_id": chat_id, "text": ch, "parse_mode": "Markdown"})

def send_photos(chat_id, paths, caption=""):
    if not paths: return
    files = []
    for i, p in enumerate(paths):
        pobj = Path(p)
        if not pobj.exists(): continue
        files.append(("photo", (f"foto_{i}.jpg", pobj.read_bytes(), "image/jpeg")))
    if not files: return
    payload = {"chat_id": chat_id}
    if caption:
        payload["caption"] = caption[:1024]
    resp = req.post(f"{TG}/sendMediaGroup", data=payload, files=files, timeout=60)
    if resp.status_code != 200:
        log.error(f"sendMediaGroup: {resp.status_code} {resp.text}")
        # Fallback: send one by one
        for i, p in enumerate(paths):
            pobj = Path(p)
            if not pobj.exists(): continue
            with open(pobj, "rb") as f:
                r2 = req.post(f"{TG}/sendPhoto", data={"chat_id": chat_id}, files={"photo": f}, timeout=60)
            if r2.status_code != 200:
                log.error(f"sendPhoto {i}: {r2.status_code}")
                break

def auto_produto():
    """Retorna o produto ativo (incompleto ou ultimo cadastrado) ou cria um novo."""
    prods = load_json(PRODS_FILE, [])
    ativo = next((p for p in prods if p["status"] == "cadastrado" and (not p.get("fotos") or not p.get("link_olx"))), None)
    if ativo:
        return ativo
    # Cria novo
    prod = {"id": len(prods) + 1, "nome": "", "preco": 0, "descricao": "", "fotos": [], "link_olx": "", "status": "cadastrado", "criado": datetime.now().isoformat()}
    prods.append(prod)
    save_json(PRODS_FILE, prods)
    return prod

def salvar():
    prods = load_json(PRODS_FILE, [])
    save_json(PRODS_FILE, prods)

def extrair_preco(texto):
    """Extrai o primeiro preco encontrado no texto. Retorna float ou None."""
    m = re.search(r'(?:R\s*\$\s*)?(\d{2,}(?:[.,]\s*\d{2})?)\s*(?:reais|r\$)?', texto, re.IGNORECASE)
    if m:
        val = m.group(1).replace(".", "").replace(",", ".").replace(" ", "")
        try:
            v = float(val)
            if v > 0: return v
        except: pass
    m = re.search(r'(\d+)\s*reais', texto, re.IGNORECASE)
    if m:
        try: return float(m.group(1))
        except: pass
    return None

def extrair_link_olx(texto):
    """Extrai URL da OLX."""
    m = re.search(r'https?://[^\s]*(?:olx|ml\.com\.br)[^\s]*', texto, re.IGNORECASE)
    return m.group(0) if m else None

def show_status(chat_id, prod):
    """Mostra estado do produto pro usuario."""
    partes = []
    if prod.get("nome"): partes.append(f"📦 *{prod['nome']}*")
    else: partes.append("📦 *Produto* — sem nome ainda")
    if prod.get("preco"): partes.append(f"💰 R$ {prod['preco']:.0f}")
    if prod.get("link_olx"): partes.append(f"🔗 [Link OLX]({prod['link_olx']})")
    if prod.get("descricao"): partes.append(f"📝 {prod['descricao'][:100]}")
    fotos_count = len(prod.get("fotos", []))
    partes.append(f"📸 {fotos_count} {'foto' if fotos_count==1 else 'fotos'}")
    status = "✅ COMPLETO" if complete(prod) else "⏳ INCOMPLETO"
    msg = f"*PRODUTO #{prod['id']} — {status}*\n" + "\n".join(partes)
    if not complete(prod):
        falta = []
        if not prod.get("nome"): falta.append("nome")
        if not prod.get("preco"): falta.append("preço")
        if not prod.get("link_olx"): falta.append("link OLX")
        if not prod.get("fotos"): falta.append("fotos (envie as imagens)")
        msg += f"\n\nFalta: _{', '.join(falta)}_"
    else:
        msg += f"\n\n✅ *Tudo pronto!* Quer que eu divulgue? Use /promover {prod['id']}"
    send(chat_id, msg)

def complete(prod):
    return bool(prod.get("nome")) and bool(prod.get("preco")) and bool(prod.get("link_olx")) and bool(prod.get("fotos"))

def download_photo(file_id):
    try:
        f = tg("getFile", {"file_id": file_id})
        if not f or "result" not in f: return None
        fp = f["result"]["file_path"]
        fname = f"{file_id[:12]}.jpg"
        local = PHOTOS_DIR / fname
        urllib.request.urlretrieve(f"{TG}/{fp}", local)
        return str(local)
    except Exception as e:
        log.error(f"Download photo: {e}")
        return None

def generate_pix(valor):
    txid = f"JOSUE{int(time.time())}"
    return f"💳 *PIX GERADO* — R$ {valor:.2f}\nChave: jae.engenharia@gmail.com\nCódigo: `{txid}`"

def agenda_flow(cid, text):
    """Fluxo 'coloca na agenda': pending → ask date → create task."""
    pending = json.loads(PENDING.read_text()) if PENDING.exists() else None

    if pending:
        date_patterns = [
            r"\b(hoje|amanha|depois de amanhã|segunda|terça|quarta|quinta|sexta|sábado|domingo)\b",
            r"\b\d{1,2}[/-]\d{1,2}\b", r"\b\d{1,2}h\b", r"\b\d{1,2}:\d{2}\b"
        ]
        has_date = any(re.search(p, text, re.IGNORECASE) for p in date_patterns)
        if has_date or text.lower() in ["sim", "ok", "pode ser", "cria"]:
            due_date = None
            due_time = None
            time_match = re.search(r"(\d{1,2})[h:](\d{2})?", text)
            if time_match:
                h, m = int(time_match.group(1)), int(time_match.group(2) or 0)
                due_time = f"{h:02d}:{m:02d}"
            date_match = re.search(r"(\d{1,2})[/-](\d{1,2})", text)
            if date_match:
                d, mo = int(date_match.group(1)), int(date_match.group(2))
                due_date = f"2026-{mo:02d}-{d:02d}"
            day_names = {"hoje":0,"amanha":1,"depois de amanha":2,"depois de amanhã":2}
            for name, offset in day_names.items():
                if name in text.lower():
                    from datetime import date, timedelta
                    due_date = (date.today() + timedelta(days=offset)).isoformat()
                    break
            task_name = pending.get("name", "Sem nome")
            payload = {"name": task_name}
            if due_date:
                dt_str = f"{due_date}T{due_time or '09:00'}:00"
                dt = datetime.fromisoformat(dt_str)
                payload["due_date"] = int(dt.timestamp() * 1000)
            try:
                req = urllib.request.Request(
                    f"https://api.clickup.com/api/v2/list/{os.environ.get('CLICKUP_LIST_ID','901714234972')}/task",
                    data=json.dumps(payload).encode(),
                    headers={"Authorization": CK, "Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=15): pass
                due_str = f" para {due_date} {due_time or '09:00'}" if due_date else ""
                send(cid, f"✅ Tarefa '{task_name}' criada{due_str} no ClickUp!")
            except Exception as e:
                send(cid, f"❌ Erro ao criar tarefa: {e}")
            PENDING.unlink(missing_ok=True)
            return True

    agenda_patterns = [
        r"coloca na agenda", r"coloca na minha agenda", r"cria tarefa",
        r"adiciona na agenda", r"cria na agenda", r"marca na agenda",
        r"agenda pra mim", r"coloca na lista", r"lembrete"
    ]
    is_agenda = any(re.search(p, text, re.IGNORECASE) for p in agenda_patterns)
    if is_agenda:
        task_match = re.search(r"(?:agenda|tarefa|lista|lembrete)\s*(?:pra|de|:)?\s*(.+?)$", text, re.IGNORECASE)
        task_name = task_match.group(1).strip().rstrip(".!?") if task_match else text
        PENDING.write_text(json.dumps({"name": task_name, "chat_id": cid}))
        send(cid, f"📝 Anotei: *{task_name}*\nPra que dia e horário? (ex: amanhã 10h, ou 15/07 14:30)")
        return True

    return False

def on_msg(chat_id, text):
    if str(chat_id) not in CID.split(","):
        return

    # Comandos manuais
    if text.startswith("/"):
        cmd = text.split()[0].lower()

        if cmd == "/vender":
            prod = auto_produto()
            parts = text.strip().split(None, 2)
            if len(parts) >= 3:
                try:
                    prod["preco"] = float(parts[1])
                    prod["nome"] = parts[2]
                except: pass
            salvar()
            show_status(chat_id, prod)
            return

        elif cmd == "/limpar":
            save_json(PRODS_FILE, [])
            send(chat_id, "🗑️ Todos produtos removidos.")
            return

        elif cmd == "/produtos":
            prods = load_json(PRODS_FILE, [])
            if not prods:
                send(chat_id, "Nenhum produto.")
                return
            msg = "*PRODUTOS:*\n"
            for p in prods:
                icon = "✅" if complete(p) else "⏳"
                n = p.get("nome","?") or "?"
                msg += f"{icon} #{p['id']} {n} — R$ {p.get('preco',0):.0f} — {p['status']} 📸{len(p.get('fotos',[]))}\n"
            send(chat_id, msg)
            return

        elif cmd == "/divulgar" or cmd == "/promover":
            try:
                pid = int(text.split()[1])
            except:
                send(chat_id, "Use: /promover <id>")
                return
            prods = load_json(PRODS_FILE, [])
            prod = next((p for p in prods if p["id"] == pid), None)
            if not prod: send(chat_id, "Produto nao encontrado."); return
            if not complete(prod): send(chat_id, f"⏳ Produto #{pid} incompleto. Veja /produtos"); return
            ctx = json.dumps({"nome":prod["nome"],"preco":prod["preco"],"descricao":prod.get("descricao",""),"link_olx":prod["link_olx"]}, ensure_ascii=False)
            msgs = [
                {"role":"system","content":f"Gere um texto promocional para vender este produto. Inclua o link OLX. Produto: {ctx}"},
                {"role":"user","content":"Gere o texto de venda."},
            ]
            resp = ask_llm(msgs)
            prod["status"] = "divulgando"
            salvar()
            fotos = prod.get("fotos",[])
            if fotos:
                send_photos(chat_id, fotos, f"📢 *{prod['nome']}* — R$ {prod['preco']:,.0f}\n{resp}"[:1024])
            send(chat_id, f"🔗 {prod['link_olx']}\n\nPronto! Copia e divulga.")
            return

        elif cmd == "/pix":
            try:
                valor = float(text.split()[1])
                send(chat_id, generate_pix(valor))
            except: send(chat_id, "Use: /pix <valor>")
            return

        elif cmd == "/ajuda":
            send(chat_id, "Mande preço, link OLX, descrição e fotos — detecto tudo automático.\n\nUse /promover <id> pra divulgar, /produtos pra listar, /limpar pra resetar.")
            return

        elif cmd in ("/fotos","/link","/status"):
            send(chat_id, "Agora detecto automaticamente! So mande os dados.")
            return

        return

    if CK and agenda_flow(chat_id, text):
        return

    # --- DETECCAO AUTOMATICA ---
    prod = auto_produto()
    mudou = False

    # Detecta link OLX
    link = extrair_link_olx(text)
    if link and link != prod.get("link_olx"):
        prod["link_olx"] = link
        mudou = True

    # Detecta preco
    preco = extrair_preco(text)
    if preco and preco != prod.get("preco"):
        prod["preco"] = preco
        mudou = True

    # Detecta nome: se nao tem nome ainda, tenta extrair do texto
    if not prod.get("nome"):
        # Remove link e preco do texto pra achar o nome
        resto = text
        if link: resto = resto.replace(link, "")
        if preco:
            # Remove R$ e numeros
            resto = re.sub(r'(?:R\s*\$\s*)?\d[\d\s.,]*\s*(?:reais)?', '', resto, flags=re.IGNORECASE)
        resto = resto.strip().strip(".,;:!?")
        if resto and len(resto) > 1:
            prod["nome"] = resto[:80]
            mudou = True

    # Descricao: se ja tem nome, texto restante vira descricao
    if prod.get("nome"):
        resto = text
        if link: resto = resto.replace(link, "")
        if preco: resto = re.sub(r'(?:R\s*\$\s*)?\d[\d\s.,]*\s*(?:reais)?', '', resto, flags=re.IGNORECASE)
        if prod.get("nome"): resto = resto.replace(prod["nome"], "", 1)
        resto = resto.strip().strip(".,;:!?-")
        if resto and len(resto) > 3:
            existing = prod.get("descricao", "")
            if resto not in existing:
                prod["descricao"] = (existing + "; " + resto) if existing else resto
                mudou = True

    if mudou:
        salvar()

    show_status(chat_id, prod)

def on_photo(chat_id, photos, caption=""):
    local_paths = []
    for p in photos[:5]:
        fp = p.get("file_id") or p.get("file_unique_id", "")
        path = download_photo(fp)
        if path: local_paths.append(path)
    if not local_paths:
        send(chat_id, "Erro ao baixar fotos. Tente de novo.")
        return

    # Auto-associa ao produto ativo
    prod = auto_produto()
    fotos = prod.get("fotos") or []
    fotos.extend(local_paths)
    prod["fotos"] = fotos

    # Se veio legenda, extrai informacoes
    if caption:
        link = extrair_link_olx(caption)
        if link: prod["link_olx"] = link
        preco = extrair_preco(caption)
        if preco: prod["preco"] = preco
        if not prod.get("nome"):
            resto = caption
            if link: resto = resto.replace(link,"")
            if preco: resto = re.sub(r'(?:R\s*\$\s*)?\d[\d\s.,]*\s*(?:reais)?','',resto,flags=re.IGNORECASE)
            resto = resto.strip().strip(".,;:!?")
            if resto and len(resto)>1: prod["nome"] = resto[:80]

    salvar()
    show_status(chat_id, prod)

def poll():
    offset = 0
    while True:
        try:
            updates = tg("getUpdates", {"offset": offset, "timeout": 30})
            if updates and "result" in updates:
                for u in updates["result"]:
                    offset = u["update_id"] + 1
                    msg = u.get("message")
                    if not msg: continue
                    cid = msg["chat"]["id"]
                    txt = msg.get("text", "")
                    photos = msg.get("photo", [])
                    cap = msg.get("caption", "")
                    if photos:
                        log.info(f"[{cid}] 📸 {cap[:60] or 'foto'} ({len(photos)} tamanhos)")
                        threading.Thread(target=on_photo, args=(cid, photos, cap)).start()
                    elif txt:
                        log.info(f"[{cid}] {txt[:80]}")
                        threading.Thread(target=on_msg, args=(cid, txt)).start()
        except Exception as e:
            log.error(f"Poll: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if not TK:
        log.error("JOSUE_TELEGRAM_TOKEN not set")
        sys.exit(1)
    log.info(f"Josue iniciado. Chat(s): {CID}")
    poll()
