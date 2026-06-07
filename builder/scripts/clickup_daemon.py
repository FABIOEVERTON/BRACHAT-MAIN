#!/usr/bin/env python3
"""ClickUp daemon — CRUD de tasks via Composio SDK."""

import json, time, logging, os, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

POLL_INTERVAL = int(os.getenv("CLICKUP_POLL_INTERVAL", "300"))
LIST_ID = os.getenv("CLICKUP_LIST_ID", "")
TEAM_ID = os.getenv("CLICKUP_TEAM_ID", "")
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
CACHE_PATH = Path(__file__).parent.parent / "cache" / "clickup.json"
Path(CACHE_PATH.parent).mkdir(parents=True, exist_ok=True)

_LOG_DIR = Path(__file__).parent.parent / "logs"
_LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(_LOG_DIR / "clickup_daemon.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("clickup")


def _init_tools():
    from composio.sdk import Composio
    c = Composio()
    return c


def _get_connected_account(tools) -> Optional[str]:
    from composio.sdk import ConnectedAccounts
    accounts = ConnectedAccounts.get(tool="clickup")
    for acc in accounts:
        if acc.status == "ACTIVE" and getattr(acc, "is_default", False):
            return acc.id
    for acc in accounts:
        if acc.status == "ACTIVE":
            return acc.id
    return None


def _exec(tools, slug: str, args: dict, account: Optional[str] = None):
    from composio.sdk import Tools
    kwargs = {"slug": slug, "arguments": args}
    if account:
        kwargs["connected_account_id"] = account
    resp = Tools.execute(**kwargs)
    data = getattr(resp, "data", resp)
    if hasattr(data, "model_dump"):
        return data.model_dump()
    if isinstance(data, dict):
        return data
    return {"raw": str(data)}


def get_tasks(tools, account: str, status_filter: Optional[str] = None):
    params = {"list_id": LIST_ID}
    if status_filter:
        params["status"] = status_filter
    return _exec(tools, "CLICKUP_GET_FILTERED_TEAM_TASKS", params, account)


def get_task(tools, account: str, task_id: str):
    return _exec(tools, "CLICKUP_GET_TASK", {"task_id": task_id}, account)


def create_task(tools, account: str, name: str, **kwargs):
    args = {"list_id": LIST_ID, "name": name, **kwargs}
    return _exec(tools, "CLICKUP_CREATE_TASK", args, account)


def update_task(tools, account: str, task_id: str, **kwargs):
    args = {"task_id": task_id, **kwargs}
    return _exec(tools, "CLICKUP_UPDATE_TASK", args, account)


def delete_task(tools, account: str, task_id: str):
    return _exec(tools, "CLICKUP_DELETE_TASK", {"task_id": task_id}, account)


def save_cache(tasks: list):
    CACHE_PATH.write_text(
        json.dumps({"updated_at": datetime.now(timezone.utc).isoformat(), "tasks": tasks}, indent=2, ensure_ascii=False)
    )


def load_cache() -> dict:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text())
    return {"tasks": []}


def poll_loop(tools, account: str):
    log.info("Polling ClickUp tasks (interval=%ss, list=%s)", POLL_INTERVAL, LIST_ID)
    while True:
        try:
            resp = get_tasks(tools, account)
            tasks = resp.get("tasks", [])
            log.info("Fetched %d tasks", len(tasks))
            save_cache(tasks)
        except Exception as e:
            log.error("Poll failed: %s", e)
        time.sleep(POLL_INTERVAL)


def interactive(tools, account: str):
    print("ClickUp daemon — modo interativo")
    print("Comandos: poll, list, get <id>, create <nome>, update <id> <campo>=<valor> [+...], delete <id>, help, quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()

        if cmd == "quit":
            break
        elif cmd == "help":
            print("poll           - fetch tasks and cache")
            print("list           - list cached tasks")
            print("get <id>       - fetch single task")
            print('create <nome>  - cria task (opcional: status="To Do" priority=3)')
            print("update <id> k=v [+ k=v] - atualiza campos")
            print("delete <id>    - deleta task")
        elif cmd == "poll":
            poll_loop(tools, account)
        elif cmd == "list":
            cached = load_cache()
            for t in cached.get("tasks", []):
                s = (t.get("status") or {}).get("status", "?")
                print(f'  [{s}] {t["id"]}  {t.get("name","?")}')
            print(f"Total: {len(cached.get('tasks',[]))} cached")
        elif cmd == "get" and len(parts) >= 2:
            r = get_task(tools, account, parts[1])
            print(json.dumps(r, indent=2, ensure_ascii=False))
        elif cmd == "create" and len(parts) >= 2:
            name = " ".join(parts[1:])
            r = create_task(tools, account, name)
            print(json.dumps(r, indent=2, ensure_ascii=False))
        elif cmd == "update" and len(parts) >= 3:
            task_id = parts[1]
            kwargs = {}
            for kv in parts[2:]:
                k, _, v = kv.partition("=")
                kwargs[k] = v
            r = update_task(tools, account, task_id, **kwargs)
            print(json.dumps(r, indent=2, ensure_ascii=False))
        elif cmd == "delete" and len(parts) >= 2:
            r = delete_task(tools, account, " ".join(parts[1:]))
            print(json.dumps(r, indent=2, ensure_ascii=False))
        else:
            print("Comando invalido. Digite help.")


def main():
    if not LIST_ID:
        log.error("Defina CLICKUP_LIST_ID no env ou config.json")
        sys.exit(1)

    tools = _init_tools()
    account = _get_connected_account(tools)
    if not account:
        log.error("Nenhuma conta ClickUp ativa encontrada. Execute: composio add clickup")
        sys.exit(1)
    log.info("Connected account: %s", account)

    if "--poll" in sys.argv:
        poll_loop(tools, account)
    elif "--once" in sys.argv:
        resp = get_tasks(tools, account)
        print(json.dumps(resp, indent=2, ensure_ascii=False))
    else:
        interactive(tools, account)


if __name__ == "__main__":
    main()
