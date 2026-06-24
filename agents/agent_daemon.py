#!/usr/bin/env python3
"""
[BR-AGENT-DAEMON] agent_daemon.py — Generic Agent Background Runtime

Usage:
  python3 agent_daemon.py --agent artur [--interval 60]
  python3 agent_daemon.py --agent aisio --once

Each daemon reads ONLY its own context_memory.json.
Uses LiteLLM (port 4001) for LLM calls.
Writes to its own worklog, receipts, state.
"""

import json, os, sys, time, argparse, glob, datetime, uuid, urllib.request

AGENTS_ROOT = os.path.dirname(os.path.abspath(__file__))
PORTFOLIO_ROOT = os.path.join(os.path.dirname(AGENTS_ROOT), "portfolio")
LITELLM_URL = "http://localhost:4001/v1/chat/completions"
LITELLM_MODEL = "command-r-plus"  # big-pickle is opencode-proprietary, unavailable via LiteLLM API. Fallback per context_memory.json.
DEFAULT_INTERVAL = 120


def find_agent_path(name):
    for root, dirs, files in os.walk(AGENTS_ROOT):
        if name in dirs:
            ctx = os.path.join(root, name, "context_memory.json")
            if os.path.exists(ctx):
                return os.path.join(root, name)
    pf = os.path.join(PORTFOLIO_ROOT, name)
    ctx = os.path.join(pf, "context_memory.json")
    if os.path.exists(ctx):
        return pf
    return None


def now_iso():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).isoformat()


def read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except: return {}


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def llm_call(system_prompt, user_prompt, max_tokens=500):
    payload = json.dumps({
        "model": LITELLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0,
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(LITELLM_URL, data=payload,
        headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[LLM_ERROR] {e}"


def check_pending_work(agent_path, agent_name, agent_id):
    worklog = os.path.join(agent_path, "worklog.jsonl")
    state = read_json(os.path.join(agent_path, "state.json"))
    ctx = read_json(os.path.join(agent_path, "context_memory.json"))
    if not ctx:
        return []
    tasks_dir = os.path.join(AGENTS_ROOT, "orchestrator_agents", "ezra", "tasks")
    pending = []
    if os.path.exists(tasks_dir):
        for fname in os.listdir(tasks_dir):
            if not fname.endswith(".json"):
                continue
            task = read_json(os.path.join(tasks_dir, fname))
            assigned = task.get("assigned_executor", "") or task.get("assigned_architect", "")
            if assigned == agent_name and task.get("status") in ("dispatched", "dispatched_to_artur"):
                pending.append(task)
    return pending


def write_receipt(agent_path, agent_name, agent_id, rtype, action_desc, status, files_created):
    seq = len(glob.glob(os.path.join(agent_path, "receipts", "*.json"))) + 1
    day = datetime.date.today().strftime("%Y%m%d")
    rid = f"RCP-{agent_name.upper()}-{day}-{seq:04d}"
    receipt = {
        "receipt_id": rid,
        "agent_id": agent_id,
        "agent_name": agent_name,
        "type": rtype,
        "timestamp": now_iso(),
        "action": {"description": action_desc, "target": "daemon_auto"},
        "outcome": {"status": status, "summary": action_desc[:200]},
        "evidence": {"files_created": files_created, "files_modified": [], "output": ""},
    }
    rpath = os.path.join(agent_path, "receipts", f"{rid.lower()}.json")
    write_json(rpath, receipt)
    return rid, rpath


def append_worklog(agent_path, agent_name, rtype, action, status, receipt_path, duration):
    wl = os.path.join(agent_path, "worklog.jsonl")
    entry = json.dumps({
        "ts": now_iso(),
        "agent": agent_name,
        "type": rtype,
        "action": action[:200],
        "status": status,
        "receipt": receipt_path,
        "duration_sec": duration,
        "error": None,
    })
    with open(wl, "a") as f:
        f.write(entry + "\n")


def process_agent(agent_name, once=False):
    apath = find_agent_path(agent_name)
    if not apath:
        print(f"[DAEMON] Agent '{agent_name}' not found")
        return False
    ctx = read_json(os.path.join(apath, "context_memory.json"))
    if not ctx:
        print(f"[DAEMON] No context for {agent_name}")
        return False
    agent_id = ctx.get("agent", {}).get("id", f"BR-{agent_name.upper()}-000")
    rtype = ctx.get("receipt_type", "task")
    pending = check_pending_work(apath, agent_name, agent_id)
    if not pending:
        return False
    for task in pending[:1]:
        tstart = time.time()
        system_p = f"You are {agent_name} ({agent_id}). {ctx.get('persona','')}"
        user_p = f"Task: {task.get('title','')}\n{task.get('description','')}\nProcess this task and report what you did."
        result = llm_call(system_p, user_p)
        rid, rpath = write_receipt(apath, agent_name, agent_id, rtype, f"Processed {task['task_id']}: {result[:100]}", "success", [])
        append_worklog(apath, agent_name, rtype, f"Auto-processed {task['task_id']}", "success", rpath, int(time.time()-tstart))
        task["status"] = "completed_by_daemon"
        task["evidence"]["daemon_receipt"] = rid
        task_path = os.path.join(AGENTS_ROOT, "orchestrator_agents", "ezra", "tasks", f"{task['task_id']}.json")
        write_json(task_path, task)
        print(f"[DAEMON] {agent_name} completed {task['task_id']} -> {rid}")
    return True


def daemon_loop(agent_name, interval):
    cycle = 0
    while True:
        try:
            ok = process_agent(agent_name)
            cycle += 1
        except Exception as e:
            print(f"[DAEMON] {agent_name} error cycle {cycle}: {e}")
        time.sleep(interval)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True)
    ap.add_argument("--interval", type=int, default=DEFAULT_INTERVAL)
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()
    if args.once:
        process_agent(args.agent)
    else:
        daemon_loop(args.agent, args.interval)


if __name__ == "__main__":
    main()
