"""Dashboard de execução: lê os logs JSONL e resume métricas do agente."""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import config  # noqa: E402


def load_records(log_dir: Path) -> list[dict]:
    records = []
    for p in sorted(log_dir.glob("queries_*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def main():
    log_dir = Path(config.LOG_DIR)
    records = load_records(log_dir)
    if not records:
        print(f"Sem registros em {log_dir}")
        return

    total = len(records)
    found = sum(1 for r in records if r.get("found"))
    not_found = total - found
    latencies = [r.get("latency_ms", 0) for r in records]
    avg_lat = sum(latencies) / len(latencies) if latencies else 0
    fallbacks = [r.get("fallback") for r in records if r.get("fallback")]
    providers = Counter(r.get("provider", "-") for r in records)
    feedbacks = [r for r in records if r.get("feedback")]
    neg = [r for r in feedbacks if r.get("feedback") == "negativo"]

    print(f"Total de perguntas : {total}")
    print(f"Respondidas         : {found} ({found / total:.0%})")
    print(f"Não encontradas     : {not_found} ({not_found / total:.0%})")
    print(f"Latência média      : {avg_lat:.0f} ms")
    print(f"Usaram fallback     : {len(fallbacks)}")
    print(f"Provedores          : {dict(providers)}")
    print(f"Feedbacks           : {len(feedbacks)} (negativos: {len(neg)})")

    if not_found:
        print("\nPerguntas sem resposta:")
        for r in records:
            if not r.get("found"):
                print(f"  - {r.get('question', '?')}")
    if neg:
        print("\nPerguntas com feedback negativo:")
        for r in neg:
            print(f"  - {r.get('question', '?')}")
    if fallbacks:
        print("\nFallbacks acionados (últimos 5):")
        for r in fallbacks[-5:]:
            print(f"  - {r}")


if __name__ == "__main__":
    main()
