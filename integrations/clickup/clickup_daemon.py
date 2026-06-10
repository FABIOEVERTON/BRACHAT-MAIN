#!/usr/bin/env python3
"""ClickUp daemon — CRUD de tasks via ClickUp API REST nativa."""

import json
import time
import logging
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

POLL_INTERVAL = int(os.getenv("CLICKUP_POLL_INTERVAL", "300"))
TOKEN = os.getenv("CLICKUP_TOKEN", "")
LIST_ID = os.getenv("CLICKUP_LIST_ID", "")
TEAM_ID = os.getenv("CLICKUP_TEAM_ID", "")

CACHE_PATH = Path(__file__).parent / "cache" / "clickup.json"
Path(CACHE_PATH.parent).mkdir(parents=True, exist_ok=True)

_LOG_DIR = Path(__file__).parent / "logs"
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


def _req(url: str, method: str = "GET", data: Optional[dict] = None) -> dict:
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except Exception as e:
        if hasattr(e, "read"):
            try:
                err_body = e.read().decode()
                log.error(f"ClickUp API Error ({method} {url}): {e} - Response: {err_body}")
            except:
                log.error(f"ClickUp API Error ({method} {url}): {e}")
        else:
            log.error(f"ClickUp API Connection Error ({method} {url}): {e}")
        raise e


def get_tasks(status_filter: Optional[str] = None) -> dict:
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    if status_filter:
        url += f"?status={status_filter}"
    return _req(url, "GET")


def get_task(task_id: str) -> dict:
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    return _req(url, "GET")


def create_task(name: str, **kwargs) -> dict:
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    payload = {"name": name, **kwargs}
    return _req(url, "POST", payload)


def update_task(task_id: str, **kwargs) -> dict:
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    return _req(url, "PUT", kwargs)


def delete_task(task_id: str) -> dict:
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    return _req(url, "DELETE")


def save_cache(tasks: list):
    CACHE_PATH.write_text(
        json.dumps({"updated_at": datetime.now(timezone.utc).isoformat(), "tasks": tasks}, indent=2, ensure_ascii=False)
    )


def load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text())
        except:
            pass
    return {"tasks": []}


def poll_loop():
    log.info("Polling ClickUp tasks (interval=%ss, list=%s)", POLL_INTERVAL, LIST_ID)
    while True:
        try:
            resp = get_tasks()
            tasks = resp.get("tasks", [])
            log.info("Fetched %d tasks", len(tasks))
            save_cache(tasks)
        except Exception as e:
            log.error("Poll failed: %s", e)
        time.sleep(POLL_INTERVAL)


def main():
    if not TOKEN:
        log.error("Defina CLICKUP_TOKEN no env")
        sys.exit(1)
    if not LIST_ID:
        log.error("Defina CLICKUP_LIST_ID no env")
        sys.exit(1)

    log.info("ClickUp Daemon iniciado nativamente. Monitorando lista: %s", LIST_ID)

    if "--poll" in sys.argv:
        poll_loop()
    else:
        try:
            resp = get_tasks()
            print(json.dumps(resp, indent=2, ensure_ascii=False))
        except Exception as e:
            sys.exit(1)


if __name__ == "__main__":
    main()
