#!/usr/bin/env python3
"""Malha real BRACHAT — WebSocket bridges + agentes + sistema."""
import asyncio, json, time, subprocess
from pathlib import Path
import websockets

CLIENTS = set()
REPO = Path("/opt/brachat/repo")
AGENTS = REPO / "agents"
EZRA_FILE = Path("/opt/brachat/state/malha.json")
NICE_FILE = Path("/opt/brachat/state/nice.json")

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

def read_agent_states():
    categories = {
        "director": AGENTS / "director_agents",
        "builder": AGENTS / "builder_agents",
        "studies": AGENTS / "studies_agents",
    }
    result = {}
    for cat, path in categories.items():
        if not path.exists():
            continue
        agents = []
        for d in sorted(path.iterdir()):
            if not d.is_dir():
                continue
            state = rj(d / "state.json")
            agents.append({
                "name": d.name,
                "label": d.name.capitalize(),
                "state": state,
            })
        result[cat] = agents
    return result

def build():
    ez = rj(EZRA_FILE); ni = rj(NICE_FILE)
    agents_data = read_agent_states()
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
        "agents": agents_data,
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
