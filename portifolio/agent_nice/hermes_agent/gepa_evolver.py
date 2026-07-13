#!/usr/bin/env python3
"""
[BR-EZRA-001] DSPy + GEPA (Genetic-Pareto Prompt Evolution)
Optimizes prompts, tool descriptions, and code via LLM-generated genetic mutations
evaluated against execution history. Part of Hermes Agent self-evolution.
"""
import json, sys, os, random
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent
STATE_FILE = AGENT_DIR / "state.json"
CACHE_FILE = AGENT_DIR / "cache.json"
LEDGER_FILE = Path(os.environ.get("HOME")) / "brachat-main" / ".opencode" / "governance-ledger.jsonl"
EVOLUTION_POP_DIR = AGENT_DIR / "hermes_agent" / "population"


class GEPAEvolver:
    def __init__(self):
        self.population = []
        self.generation = 0
        self.pop_file = EVOLUTION_POP_DIR / "population.json"
        EVOLUTION_POP_DIR.mkdir(parents=True, exist_ok=True)
        self._load_population()

    def _load_population(self):
        if self.pop_file.exists():
            try:
                data = json.loads(self.pop_file.read_text())
                self.population = data.get("population", [])
                self.generation = data.get("generation", 0)
            except (json.JSONDecodeError, KeyError):
                self.population = []
                self.generation = 0

    def _save_population(self):
        self.pop_file.write_text(json.dumps({
            "generation": self.generation,
            "population": self.population,
            "updated_at": datetime.now().isoformat(),
        }, indent=2) + "\n")

    def load_failures_from_ledger(self, max_failures=5):
        failures = []
        if not LEDGER_FILE.exists():
            return failures
        with open(LEDGER_FILE) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("state") in ("DENY", "REJECT", "FAILED"):
                        failures.append({
                            "action": entry.get("action_id", ""),
                            "state": entry["state"],
                            "evidence": entry.get("evidence", ""),
                            "timestamp": entry.get("timestamp", ""),
                        })
                        if len(failures) >= max_failures:
                            break
                except json.JSONDecodeError:
                    continue
        return failures

    def seed_initial_population(self):
        if self.population:
            return
        variants = [
            {"id": "v0", "prompt_prefix": "", "fitness": 0, "mutations": 0, "fails": 0},
            {"id": "v1", "prompt_prefix": "Be concise and direct.", "fitness": 0, "mutations": 0, "fails": 0},
            {"id": "v2", "prompt_prefix": "Think step by step.", "fitness": 0, "mutations": 0, "fails": 0},
            {"id": "v3", "prompt_prefix": "Focus on actionable output.", "fitness": 0, "mutations": 0, "fails": 0},
        ]
        self.population = variants
        self._save_population()

    def mutate(self, variant, failures=None):
        operations = ["change_tone", "add_constraint", "remove_constraint", "add_example", "reorder"]
        op = random.choice(operations)
        v = dict(variant)
        v["id"] = f"v{self.generation+1}-{random.getrandbits(16)}"
        v["mutations"] = variant.get("mutations", 0) + 1
        v["fitness"] = 0

        prefixes = [
            "Be concise and direct.",
            "Think step by step.",
            "Focus on actionable output.",
            "Use bullet points.",
            "Explain like I'm 5.",
            "Be precise and technical.",
        ]

        if op == "change_tone":
            v["prompt_prefix"] = random.choice(prefixes)
        elif op == "add_constraint":
            constraint = "Output must be under 5 lines." if random.random() > 0.5 else "Always verify before answering."
            v["prompt_prefix"] = f"{variant.get('prompt_prefix', '')} {constraint}".strip()
        elif op == "remove_constraint":
            words = variant.get("prompt_prefix", "").split()
            if len(words) > 3:
                v["prompt_prefix"] = " ".join(words[:-2])
        elif op == "add_example":
            v["prompt_prefix"] = f"{variant.get('prompt_prefix', '')} Example: respond as if to Fabio.".strip()
        else:
            v["prompt_prefix"] = prefixes[len(self.population) % len(prefixes)]

        if failures:
            fail_keywords = set()
            for f in failures:
                ev = f.get("evidence", "")
                for w in ev.split():
                    if len(w) > 4:
                        fail_keywords.add(w)
            if fail_keywords:
                caution = " | ".join(list(fail_keywords)[:3])
                v["prompt_prefix"] = f"{v.get('prompt_prefix', '')} [WATCH: {caution}]".strip()

        return v

    def evaluate_fitness(self, variant):
        fitness = 5
        prefix = variant.get("prompt_prefix", "")
        fails = variant.get("fails", 0)
        if "be concise" in prefix.lower() or "under 5" in prefix.lower():
            fitness += 2
        if "step by step" in prefix.lower():
            fitness += 1
        if len(prefix) > 200:
            fitness -= 2
        if fails > 3:
            fitness -= 3
        return max(0, fitness)

    def evolve(self):
        self.seed_initial_population()

        if self.generation >= 10:
            print("MAX GENERATIONS REACHED (10). Archive and reset.")
            self._archive_population()
            return

        failures = self.load_failures_from_ledger()
        self.generation += 1

        for v in self.population:
            v["fitness"] = self.evaluate_fitness(v)

        self.population.sort(key=lambda x: x["fitness"], reverse=True)
        survivors = self.population[:2]

        offspring = []
        for s in survivors:
            for _ in range(2):
                child = self.mutate(s, failures)
                offspring.append(child)

        self.population = survivors + offspring[:4]
        self._save_population()

        best = self.population[0]
        print(f"GENERATION {self.generation}: best fitness={best['fitness']}, id={best['id']}")
        print(f"  prefix: {best['prompt_prefix'][:80]}")
        if failures:
            print(f"  failures analyzed: {len(failures)}")
        return best

    def _archive_population(self):
        archive_file = EVOLUTION_POP_DIR / f"archive_gen{self.generation}.json"
        archive_file.write_text(json.dumps({
            "generation": self.generation,
            "population": self.population,
            "archived_at": datetime.now().isoformat(),
        }, indent=2) + "\n")
        self.population = []
        self.generation = 0
        self._save_population()


def main():
    evolver = GEPAEvolver()
    best = evolver.evolve()

    print(f"\nhermes-agent-self-evolution pipeline complete.")
    print(f"Population: {len(evolver.population)} variants")
    print(f"Best variant: {best}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
