#!/usr/bin/env python3
"""Malha real BRACHAT — WebSocket com estado dos bridges + agentes diarios."""
import asyncio, json, time
from pathlib import Path
import websockets

CLIENTS = set()
REPO = Path("/opt/brachat/repo")
EZRA_FILE = Path("/opt/brachat/state/malha.json")
NICE_FILE = Path("/opt/brachat/state/nice.json")

DAILY_AGENTS = [
    "certificacoes", "estudos", "filosofia", "freelancer",
    "google-skills", "ingles", "job-hunter", "ml-engineer",
    "nice", "pmp", "portfolio", "python", "torah",
]

def rj(p):
    try: return json.loads(p.read_text()) if p.exists() else {}
    except: return {}

def read_daily_agents():
    res = {}
    for name in DAILY_AGENTS:
        d = REPO / "assistant_agents" / "daily" / name
        cache = rj(d / "cache.json")
        meta = rj(d / "metadata.json")
        md = ""
        if (d / "AGENT.md").exists():
            for line in (d / "AGENT.md").read_text().split("\n"):
                if line.startswith("# ") and not line.startswith("# NICE"):
                    md = line.replace("# ","").strip()
                    break
        res[name] = {
            "nome": meta.get("label") or md or name.capitalize(),
            "cache": cache,
        }
    return res

def build_state():
    ezra = rj(EZRA_FILE)
    nice = rj(NICE_FILE)
    daily = read_daily_agents()

    return {
        "bridges": {
            "ezra": {
                "status": ezra.get("status","offline"),
                "uptime": ezra.get("uptime",0),
                "last_msg": ezra.get("last_msg",""),
                "last_resp": ezra.get("last_resp",""),
                "active_agent": ezra.get("active_agent",""),
                "active_label": ezra.get("active_label",""),
                "phase": ezra.get("phase",""),
                "timestamp": ezra.get("timestamp",""),
            },
            "nice": {
                "status": nice.get("status","offline"),
                "uptime": nice.get("uptime",0),
                "last_msg": nice.get("last_msg",""),
                "last_resp": nice.get("last_resp",""),
                "threshold": nice.get("threshold",""),
                "timestamp": nice.get("timestamp",""),
            },
        },
        "daily": daily,
        "timestamp": time.strftime("%H:%M:%S"),
        "agents_total": len(DAILY_AGENTS),
    }

async def broadcast():
    global CLIENTS
    while True:
        if CLIENTS:
            data = json.dumps(build_state())
            dead = set()
            for ws in CLIENTS:
                try: await ws.send(data)
                except: dead.add(ws)
            CLIENTS -= dead
        await asyncio.sleep(0.5)

async def handler(websocket):
    global CLIENTS
    CLIENTS.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        CLIENTS.discard(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print(f"WS malha real em ws://0.0.0.0:8765")
        await broadcast()

asyncio.run(main())
