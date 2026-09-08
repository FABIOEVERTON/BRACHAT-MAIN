"""Dashboard de execução: lê os logs JSONL e resume métricas do agente."""

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import config  # noqa: E402


def load_records(log_dir: Path) -> list[dict]:
    """Carrega todos os registros válidos dos arquivos JSONL de queries."""
    records: list[dict] = []

    for path in sorted(log_dir.glob("queries_*.jsonl")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue

        for line in lines:
            line = line.strip()

            if not line:
                continue

            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return records


def main() -> None:
    """Executa o dashboard no terminal."""
    log_dir = Path(config.LOG_DIR)
    records = load_records(log_dir)

    if not records:
        print(f"Sem registros em {log_dir}")
        return

    total = len(records)

    found = sum(
        1
        for record in records
        if record.get("found") is True
    )

    not_found = total - found

    latencies = [
        float(record.get("latency_ms", 0))
        for record in records
        if record.get("latency_ms") is not None
    ]

    avg_latency = (
        sum(latencies) / len(latencies)
        if latencies
        else 0.0
    )

    fallbacks = [
        record
        for record in records
        if record.get("fallback")
    ]

    providers = Counter(
        record.get("provider", "-")
        for record in records
    )

    feedbacks = [
        record
        for record in records
        if record.get("feedback")
    ]

    negative_feedback = [
        record
        for record in feedbacks
        if record.get("feedback") == "negativo"
    ]

    positive_feedback = [
        record
        for record in feedbacks
        if record.get("feedback") == "positivo"
    ]

    print("==== EZRA_CURATOR — DASHBOARD ====")
    print()
    print(f"Total de perguntas : {total}")
    print(
        f"Respondidas        : "
        f"{found} ({found / total:.0%})"
    )
    print(
        f"Não encontradas    : "
        f"{not_found} ({not_found / total:.0%})"
    )
    print(f"Latência média     : {avg_latency:.0f} ms")
    print(f"Usaram fallback    : {len(fallbacks)}")
    print(f"Provedores         : {dict(providers)}")
    print(
        f"Feedbacks          : {len(feedbacks)} "
        f"(positivos: {len(positive_feedback)}, "
        f"negativos: {len(negative_feedback)})"
    )

    if not_found:
        print("\nPerguntas sem resposta:")

        for record in records:
            if not record.get("found"):
                print(
                    f"  - {record.get('question', '?')}"
                )

    if negative_feedback:
        print("\nPerguntas com feedback negativo:")

        for record in negative_feedback:
            print(
                f"  - {record.get('question', '?')}"
            )

    if fallbacks:
        print("\nFallbacks acionados (últimos 5):")

        for record in fallbacks[-5:]:
            print(
                f"  - provider={record.get('provider', '-')}, "
                f"model={record.get('model', '-')}, "
                f"fallback={record.get('fallback', '-')}"
            )


if __name__ == "__main__":
    main()