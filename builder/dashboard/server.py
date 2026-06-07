#!/usr/bin/env python3
"""Malha real BRACHAT — WebSocket bridges + agentes + sistema."""
import asyncio, json, time, subprocess
from pathlib import Path
import websockets

CLIENTS = set()
REPO = Path("/opt/brachat/repo")
EZRA_FILE = Path("/opt/brachat/state/malha.json")
NICE_FILE = Path("/opt/brachat/state/nice.json")

DAILY = [
    "certificacoes","estudos","filosofia","freelancer",
    "google-skills","ingles","job-hunter","ml-engineer",
    "nice","pmp","portfolio","python","torah",
]

def rj(p):
    try: return json.loads(p.read_text()) if p.exists() else {}
    except: return {}

def run_cmd(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=3).stdout.strip()
    except: return ""

def read_system():
    cpu = run_cmd(["bash","-c","top -bn1 | head -5 | grep 'Cpu(s)' | awk '{print $2}'"])
    mem = run_cmd(["bash","-c","free -h | grep Mem | awk '{print $3\"/\"$2}'"])
    disk = run_cmd(["bash","-c","df -h / | tail -1 | awk '{print $3\"/\"$2}'"])
    procs = run_cmd(["bash","-c","ps aux | wc -l"])
    load = run_cmd(["bash","-c","uptime | awk -F'load average:' '{print $2}' | xargs"])
    return {"cpu":cpu,"memory":mem,"disk":disk,"processes":procs,"load":load}

def read_daily():
    res = {}
    for name in DAILY:
        d = REPO / "assistant_agents" / "daily" / name
        cache = rj(d / "cache.json")
        meta = rj(d / "metadata.json")
        md = ""
        if (d / "AGENT.md").exists():
            for line in (d / "AGENT.md").read_text().split("\n"):
                if line.startswith("# ") and "NICE" not in line:
                    md = line.replace("# ","").strip(); break
        res[name] = {"nome": meta.get("label") or md or name.capitalize(), "cache": cache}
    return res

def build():
    ez = rj(EZRA_FILE); ni = rj(NICE_FILE)
    return {
        "bridges":{
            "ezra":{
                "status":ez.get("status","offline"),"uptime":ez.get("uptime",0),
                "last_msg":ez.get("last_msg",""),"last_resp":ez.get("last_resp",""),
                "active_agent":ez.get("active_agent",""),"active_label":ez.get("active_label",""),
                "phase":ez.get("phase",""),"timestamp":ez.get("timestamp","")},
            "nice":{
                "status":ni.get("status","offline"),"uptime":ni.get("uptime",0),
                "last_msg":ni.get("last_msg",""),"last_resp":ni.get("last_resp",""),
                "threshold":ni.get("threshold",""),"timestamp":ni.get("timestamp","")},
        },
        "system": read_system(),
        "daily": read_daily(),
        "timestamp": time.strftime("%H:%M:%S"),
    }

async def broadcast():
    global CLIENTS
    while True:
        if CLIENTS:
            data = json.dumps(build())
            dead = set()
            for ws in CLIENTS:
                try: await ws.send(data)
                except: dead.add(ws)
            CLIENTS -= dead
        await asyncio.sleep(1)

async def handler(ws):
    global CLIENTS
    CLIENTS.add(ws)
    try:
        async for _ in ws: pass
    finally:
        CLIENTS.discard(ws)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print(f"WS malha real em ws://0.0.0.0:8765")
        await broadcast()

asyncio.run(main())
