#!/usr/bin/env python3
"""
[BR-EZRA-001] Darwinian Evolver
Maintains a population of solutions and prompts, applies targeted mutations
to failures identified in logs, and filters best variants by fitness.
Part of Hermes Agent self-evolution.
"""
import json, sys, os, random, hashlib
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent
HERMES_DIR = AGENT_DIR / "hermes_agent"
POP_FILE = HERMES_DIR / "population" / "darwinian_pop.json"
STATE_FILE = AGENT_DIR / "state.json"
LEDGER_FILE = Path(os.environ.get("HOME")) / "brachat-main" / ".opencode" / "governance-ledger.jsonl"


class DarwinianEvolver:
    def __init__(self):
        self.population = []
        self.generation = 0
        self.mutation_rate = 0.3
        self.pop_size = 8
        HERMES_DIR.mkdir(parents=True, exist_ok=True)
        (HERMES_DIR / "population").mkdir(exist_ok=True)
        self._load()

    def _load(self):
        if POP_FILE.exists():
            try:
                data = json.loads(POP_FILE.read_text())
                self.population = data.get("population", [])
                self.generation = data.get("generation", 0)
                self.mutation_rate = data.get("mutation_rate", 0.3)
            except (json.JSONDecodeError, KeyError):
                self.population = []

    def _save(self):
        POP_FILE.write_text(json.dumps({
            "generation": self.generation,
            "population": self.population,
            "mutation_rate": self.mutation_rate,
            "updated_at": datetime.now().isoformat(),
        }, indent=2) + "\n")

    def _id(self):
        h = hashlib.md5(str(random.getrandbits(64)).encode()).hexdigest()[:8]
        return f"d{self.generation}-{h}"

    def seed(self, domains=None):
        if self.population:
            return
        domains = domains or ["dispatch", "email", "study", "gate", "ssh"]
        for d in domains:
            self.population.append({
                "id": self._id(),
                "domain": d,
                "solution": f"Default solution for {d}",
                "fitness": 0.5,
                "generation": 0,
                "attempts": 0,
                "successes": 0,
                "failures": 0,
                "parent": None,
            })
        self._save()

    def record_outcome(self, domain, success=True):
        for v in self.population:
            if v["domain"] == domain:
                v["attempts"] += 1
                if success:
                    v["successes"] += 1
                else:
                    v["failures"] += 1
                v["fitness"] = v["successes"] / max(v["attempts"], 1)
                self._save()
                return
        self.population.append({
            "id": self._id(),
            "domain": domain,
            "solution": f"Evolved solution for {domain}",
            "fitness": 0.8 if success else 0.2,
            "generation": self.generation,
            "attempts": 1,
            "successes": 1 if success else 0,
            "failures": 0 if success else 1,
            "parent": None,
        })
        self._save()

    def load_log_failures(self):
        failures = []
        if not LEDGER_FILE.exists():
            return failures
        with open(LEDGER_FILE) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("state") in ("DENY", "REJECT"):
                        failures.append(entry)
                except json.JSONDecodeError:
                    continue
        return failures[-10:]

    def evolve(self):
        self.generation += 1

        for v in self.population:
            v["fitness"] = v["successes"] / max(v["attempts"], 1)

        self.population.sort(key=lambda x: x["fitness"])
        bottom = self.population[:2]

        failures = self.load_log_failures()
        for v in bottom:
            fail_context = ""
            if failures:
                f = random.choice(failures)
                fail_context = f.get("evidence", "")[:100]
            v["solution"] = f"Evolved: {v['domain']} (mutated gen{self.generation})"
            if fail_context:
                v["solution"] += f" | context: {fail_context}"
            v["generation"] = self.generation
            v["parent"] = v["id"]
            v["id"] = self._id()
            v["attempts"] = 0
            v["successes"] = 0
            v["failures"] = 0
            v["fitness"] = 0.0

        if len(self.population) < self.pop_size:
            for i in range(min(2, self.pop_size - len(self.population))):
                parent = random.choice(self.population[i:] or self.population)
                self.population.append({
                    "id": self._id(),
                    "domain": parent["domain"],
                    "solution": f"Offspring of {parent['domain']} (gen{self.generation})",
                    "fitness": 0.3,
                    "generation": self.generation,
                    "attempts": 0,
                    "successes": 0,
                    "failures": 0,
                    "parent": parent["id"],
                })

        self.mutation_rate = min(0.8, self.mutation_rate + 0.05)
        self._save()

        print(f"DARWINIAN GEN {self.generation}: pop={len(self.population)} rate={self.mutation_rate:.2f}")
        for v in sorted(self.population, key=lambda x: x["fitness"], reverse=True)[:3]:
            print(f"  {v['id']} [{v['domain']}] fitness={v['fitness']:.2f} attempts={v['attempts']}")
        return len(self.population)


def main():
    evolver = DarwinianEvolver()
    evolver.seed()

    if len(sys.argv) > 2 and sys.argv[1] == "--record":
        evolver.record_outcome(sys.argv[2], success=True)
        print(f"Recorded success for domain: {sys.argv[2]}")
        return 0

    count = evolver.evolve()
    print(f"\nDarwinian evolution cycle complete. Population: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
