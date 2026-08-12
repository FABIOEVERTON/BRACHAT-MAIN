#!/usr/bin/env python3
"""
[BR-EZRA-001] _spawn_background_review
Initializes background subagents to analyze past conversations,
extract preferences, and consolidate learnings continuously.
Part of Hermes Agent self-evolution.
"""
import json, sys, os
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent
STATE_FILE = AGENT_DIR / "state.json"
CONTEXT_MEMORY = AGENT_DIR / "context_memory.json"
SKILLS_MEMORY = AGENT_DIR / "skills_memory.json"
CACHE_FILE = AGENT_DIR / "cache.json"
REVIEW_DIR = AGENT_DIR / "hermes_agent" / "reviews"
HERMES_DIR = AGENT_DIR / "hermes_agent"


class BackgroundReview:
    def __init__(self):
        REVIEW_DIR.mkdir(parents=True, exist_ok=True)
        self.review_log = REVIEW_DIR / "review_log.json"
        self._load()

    def _load(self):
        if self.review_log.exists():
            try:
                self.data = json.loads(self.review_log.read_text())
            except (json.JSONDecodeError, KeyError):
                self.data = {"reviews": [], "last_review_id": 0}
        else:
            self.data = {"reviews": [], "last_review_id": 0}

    def _save(self):
        self.review_log.write_text(json.dumps(self.data, indent=2) + "\n")

    def _next_id(self):
        self.data["last_review_id"] += 1
        return self.data["last_review_id"]

    def analyze_state(self):
        """Read current state and extract what needs review."""
        findings = []
        if STATE_FILE.exists():
            state = json.loads(STATE_FILE.read_text())
            blockers = state.get("blockers", [])
            hermes = state.get("hermes", {})
            insights = state.get("recent_insights", [])

            if blockers:
                findings.append(f"Blockers detected ({len(blockers)}): {blockers[0][:80]}")
            if hermes.get("blockers_found"):
                findings.append(f"Hermes blockers: {hermes['blockers_found'][0][:80]}")
            if insights:
                findings.append(f"Last insight: {insights[-1].get('insight', '')[:100]}")
        return findings

    def analyze_cache(self):
        findings = []
        if CACHE_FILE.exists():
            cache = json.loads(CACHE_FILE.read_text())
            daily = cache.get("daily_log", {})
            if daily:
                latest_day = max(daily.keys())
                entries = daily[latest_day]
                findings.append(f"Latest activity ({latest_day}): {len(entries)} entries")
        return findings

    def consolidate_preferences(self):
        """Extract user preferences from recent interactions logged in cache/state."""
        preferences = []
        if STATE_FILE.exists():
            state = json.loads(STATE_FILE.read_text())
            insights = state.get("recent_insights", [])
            for ins in insights:
                if "preference" in ins.get("insight", "").lower():
                    preferences.append(ins["insight"])
        if SKILLS_MEMORY.exists():
            skills = json.loads(SKILLS_MEMORY.read_text())
            for s in skills.get("learned_skills", []):
                if s.get("occurrence", 0) > 1:
                    preferences.append(f"Repeated pattern: {s['name']} (x{s['occurrence']})")
        return preferences

    def run_review(self):
        review_id = self._next_id()
        findings = []
        findings.extend(self.analyze_state())
        findings.extend(self.analyze_cache())
        preferences = self.consolidate_preferences()

        review = {
            "id": review_id,
            "timestamp": datetime.now().isoformat(),
            "findings": findings,
            "preferences": preferences,
            "summary": f"Review #{review_id}: {len(findings)} findings, {len(preferences)} preferences",
        }

        self.data["reviews"].append(review)

        if len(self.data["reviews"]) > 10:
            archive = REVIEW_DIR / f"reviews_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            archive.write_text(json.dumps(self.data, indent=2) + "\n")
            self.data["reviews"] = self.data["reviews"][-5:]

        self._save()

        if preferences:
            self._update_context_memory(preferences)

        return review

    def _update_context_memory(self, preferences):
        if not CONTEXT_MEMORY.exists():
            return
        try:
            ctx = json.loads(CONTEXT_MEMORY.read_text())
            if "learned_preferences" not in ctx:
                ctx["learned_preferences"] = []
            for p in preferences:
                if p not in ctx["learned_preferences"]:
                    ctx["learned_preferences"].append(p)
            ctx["learned_preferences"] = ctx["learned_preferences"][-20:]
            CONTEXT_MEMORY.write_text(json.dumps(ctx, indent=2) + "\n")
        except (json.JSONDecodeError, KeyError):
            pass

    def get_review_summary(self):
        if not self.data["reviews"]:
            return "No reviews yet."
        latest = self.data["reviews"][-1]
        return f"[Review #{latest['id']}] {latest['summary']}"


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "review"

    reviewer = BackgroundReview()

    if action == "review":
        review = reviewer.run_review()
        print(f"REVIEW #{review['id']} COMPLETE")
        for f in review["findings"]:
            print(f"  FINDING: {f}")
        for p in review.get("preferences", []):
            print(f"  PREFERENCE: {p}")
        print(f"  Summary: {review['summary']}")
    elif action == "summary":
        print(reviewer.get_review_summary())
    elif action == "consolidate":
        prefs = reviewer.consolidate_preferences()
        print(f"Preferences extracted: {len(prefs)}")
        for p in prefs:
            print(f"  - {p}")
    else:
        print(f"Unknown action: {action}")
        print("Usage: background_review.py [review|summary|consolidate]")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
