#!/usr/bin/env python3
"""
[BR-EZRA-001] temporal_loop.py — Ezra's Memory + Self-Improvement Daemon

Runs in background (screen/launchd). Every N seconds:
  1. Reads context_memory.json + schedule_progress.json (own files only)
  2. Writes heartbeat.json — checkpoint between sessions
  3. Scans all worklogs for new entries since last heartbeat
  4. Checks schedule for mismatches
  5. Every HERMES_CYCLE cycles: runs Hermes consolidation (self-improvement)
  6. Logs pulse, sleeps

Token economy: reads ONLY Ezra's files. Never reads other agent contexts.
When Ezra starts a new session: reads heartbeat.json -> knows exactly where left off.
"""

import json, os, time, datetime, glob, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))
HERMES_DIR = os.path.join(BASE, "hermes_agent")
CONTEXT_FILE = os.path.join(BASE, "context_memory.json")
SCHEDULE_FILE = os.path.join(BASE, "schedule_progress.json")
HEARTBEAT_FILE = os.path.join(BASE, "heartbeat.json")
WORKLOG_FILE = os.path.join(BASE, "worklog.jsonl")

INTERVAL_SEC = int(os.environ.get("EZRA_LOOP_INTERVAL", "300"))
HERMES_CYCLE = int(os.environ.get("EZRA_HERMES_CYCLE", "12"))  # every 12 pulses (~1h)
AGENTS_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))


def now_iso():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).isoformat()


def read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def read_worklogs_since(since_ts):
    """Scan ALL agent worklogs for entries newer than `since_ts`. Returns list."""
    new_entries = []
    pattern = os.path.join(AGENTS_ROOT, "*", "*", "worklog.jsonl")
    for fpath in glob.glob(pattern):
        try:
            with open(fpath) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        if entry.get("ts", "") > since_ts:
                            entry["_file"] = fpath
                            new_entries.append(entry)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            continue
    return new_entries


def push_mem0_snapshot(context, schedule, last_heartbeat):
    """Push a compact context snapshot to mem0 via API call."""
    summary = {
        "event": "temporal_loop_heartbeat",
        "timestamp": now_iso(),
        "context_updated": context.get("updated_at", ""),
        "schedule_day": schedule.get("current_day", 0),
        "schedule_month": schedule.get("current_month", 0),
        "days_completed": schedule.get("days_completed", []),
        "mode": schedule.get("mode", ""),
        "blockers": context.get("blockers", []),
        "last_heartbeat": last_heartbeat,
    }
    agent_data = json.dumps({
        "agent_id": "BR-EZRA-001",
        "text": f"[BR-EZRA-001] Temporal loop heartbeat. Schedule: Month {summary['schedule_month']} Day {summary['schedule_day']}. Completed: {summary['days_completed']}. Blockers: {len(summary['blockers'])}.",
        "user_id": "ezra-brachat",
        "metadata": summary
    })
    pass  # mem0 push via API not available in daemon context; heartbeat.json serves as local checkpoint
    return summary


def run_hermes_consolidation():
    """Run Hermes self-improvement pipeline every N cycles."""
    consolidate = os.path.join(HERMES_DIR, "consolidate_all.py")
    if not os.path.exists(consolidate):
        return "no_hermes_script"
    try:
        result = subprocess.run(
            [sys.executable, consolidate],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return "consolidated"
        return f"error: {result.stderr[:100]}"
    except Exception as e:
        return f"exception: {e}"


def check_daily_close(cycle, schedule):
    """Write daily_close.json if between 18:00-18:05 and not yet done today."""
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    close_file = os.path.join(BASE, "daily_close.json")
    if os.path.exists(close_file):
        try:
            prev_close = read_json(close_file)
            if prev_close.get("date") == today:
                return None  # already closed today
        except: pass
    if now.hour == 18 and now.minute < 5:
        # Gather all agent receipts for the day
        receipts_today = []
        for fpath in glob.glob(os.path.join(AGENTS_ROOT, "*", "*", "receipts", "*.json")):
            receipt = read_json(fpath)
            if receipt.get("timestamp","").startswith(today):
                receipts_today.append({
                    "agent": receipt.get("agent_name"),
                    "type": receipt.get("type"),
                    "id": receipt.get("receipt_id"),
                    "status": receipt.get("outcome",{}).get("status"),
                })
        close = {
            "date": today,
            "type": "daily_close",
            "timestamp": now_iso(),
            "agent": "ezra",
            "cycle": cycle,
            "schedule_day": schedule.get("current_day", 0),
            "schedule_month": schedule.get("current_month", 0),
            "days_completed": schedule.get("days_completed", []),
            "receipts_today": receipts_today,
            "note": "Daily close. Push this to mem0 when Ezra is in session.",
        }
        write_json(close_file, close)
        # Write consolidated worklog summary
        summary_file = os.path.join(BASE, "daily_summary.json")
        write_json(summary_file, {
            "date": today, "type": "daily_summary",
            "total_receipts": len(receipts_today),
            "agents_active": len(set(r["agent"] for r in receipts_today if r.get("agent"))),
            "receipts": receipts_today,
        })
        return close
    return None


def check_schedule(context, schedule):
    """Compare schedule with current time. Log if something is due."""
    now = datetime.datetime.now()
    day_name = now.strftime("%A")
    cert_map = {
        "Monday": "OCI Foundations Associate",
        "Tuesday": "OCI AI Foundations Associate",
        "Wednesday": "OCI Generative AI Professional",
        "Thursday": "OCI Architect Professional",
        "Friday": "OCI Multicloud Architect Professional",
        "Saturday": "AIGP",
    }
    findings = []
    if day_name in cert_map:
        cert = cert_map[day_name]
        track_idx = list(cert_map.values()).index(cert)
        expected_idx = schedule.get("certification_track_index", 0)
        if track_idx != expected_idx:
            findings.append(f"Cert mismatch: expected track {expected_idx}, today is {day_name}/{cert}")
    return findings


def pulse(last_heartbeat, cycle=0):
    context = read_json(CONTEXT_FILE)
    schedule = read_json(SCHEDULE_FILE)
    old_hb = read_json(HEARTBEAT_FILE)

    ts = now_iso()
    findings = check_schedule(context, schedule)
    new_logs = read_worklogs_since(old_hb.get("timestamp", ""))

    hermes_status = ""
    if cycle > 0 and cycle % HERMES_CYCLE == 0:
        hermes_status = run_hermes_consolidation()

    daily_close = check_daily_close(cycle, schedule)

    heartbeat = {
        "timestamp": ts,
        "cycle": cycle,
        "loop_interval_sec": INTERVAL_SEC,
        "agent": "ezra",
        "id": "BR-EZRA-001",
        "schedule_day": schedule.get("current_day", 0),
        "schedule_month": schedule.get("current_month", 0),
        "days_completed": schedule.get("days_completed", []),
        "new_worklog_entries": len(new_logs),
        "findings": findings,
        "hermes_status": hermes_status,
        "context_updated_at": context.get("updated_at", ""),
        "blockers": context.get("blockers", []),
        "daily_close": daily_close["date"] if daily_close else None,
    }

    write_json(HEARTBEAT_FILE, heartbeat)

    action = f"Cycle {cycle}. Logs: {len(new_logs)}, Findings: {len(findings)}"
    if hermes_status:
        action += f" | Hermes: {hermes_status}"

    log_line = json.dumps({
        "ts": ts, "agent": "ezra", "type": "temporal_pulse",
        "action": action, "status": "ok", "duration_sec": INTERVAL_SEC,
        "cycle": cycle, "hermes": hermes_status,
    })
    with open(WORKLOG_FILE, "a") as f:
        f.write(log_line + "\n")

    return heartbeat


def main():
    last_hb = {"timestamp": ""}
    cycle = 0
    while True:
        try:
            hb = pulse(last_hb, cycle)
            last_hb = hb
            cycle += 1
        except Exception as e:
            err_line = json.dumps({
                "ts": now_iso(), "agent": "ezra", "type": "temporal_error",
                "action": f"Loop error on cycle {cycle}", "status": "error",
                "error": str(e)
            })
            with open(WORKLOG_FILE, "a") as f:
                f.write(err_line + "\n")
        time.sleep(INTERVAL_SEC)


if __name__ == "__main__":
    main()
