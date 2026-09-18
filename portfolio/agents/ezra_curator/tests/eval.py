import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.rag import answer_question


def run(items: list[dict]) -> list[dict]:
    results = []

    for i, item in enumerate(items, 1):
        question = item["question"]

        print(f"[{i}/{len(items)}] {question}")

        try:
            result = answer_question(question)

            got_found = result.found
            got_sources = sorted(
                {
                    source["source"]
                    for source in result.sources
                    if source.get("source")
                }
            )

            expected_found = item["expected_found"]
            expected_sources = sorted(item["expected_sources"])

            ok_found = got_found == expected_found

            if expected_sources:
                ok_sources = set(expected_sources) <= set(got_sources)
            else:
                ok_sources = True

            ok = ok_found and ok_sources

            results.append(
                {
                    "question": question,
                    "found": got_found,
                    "sources": got_sources,
                    "expected_found": expected_found,
                    "expected_sources": expected_sources,
                    "ok": ok,
                }
            )

            print(
                f"    -> found={got_found} "
                f"sources={got_sources} "
                f"ok={ok}"
            )

        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "question": question,
                    "ok": False,
                    "error": str(exc),
                }
            )

            print(f"    -> ERROR {exc}")

        time.sleep(0.5)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Eval do agente PEGASUS"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Executa apenas os N primeiros itens (0 = todos)",
    )

    args = parser.parse_args()

    path = ROOT / "tests" / "eval_set.json"

    if not path.exists():
        print(f"Arquivo de avaliação não encontrado: {path}")
        sys.exit(1)

    items = json.loads(
        path.read_text(encoding="utf-8")
    )

    if not isinstance(items, list):
        print("Erro: eval_set.json deve conter uma lista de questões.")
        sys.exit(1)

    if args.limit:
        items = items[: args.limit]

    if not items:
        print("Nenhum item para avaliar.")
        sys.exit(1)

    results = run(items)

    ok_count = sum(
        1
        for result in results
        if result["ok"]
    )

    total = len(results)

    accuracy = ok_count / total

    print("\n==== RESUMO ====")
    print(
        f"Acurácia: {ok_count}/{total} "
        f"({accuracy:.0%})"
    )

    report = (
        ROOT
        / "logs"
        / f"eval_{time.strftime('%Y%m%d_%H%M%S')}.json"
    )

    report.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report.write_text(
        json.dumps(
            results,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Relatório: {report}")

    sys.exit(
        0 if ok_count == total else 1
    )


if __name__ == "__main__":
    main()