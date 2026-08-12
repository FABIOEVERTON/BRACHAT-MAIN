import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.rag import answer_question


def run(items):
    results = []
    for i, item in enumerate(items, 1):
        q = item["question"]
        print(f"[{i}/{len(items)}] {q}")
        try:
            r = answer_question(q)
            got_found = r.found
            got_sources = sorted({s["source"] for s in r.sources})
            exp_found = item["expected_found"]
            exp_sources = sorted(item["expected_sources"])

            ok_found = got_found == exp_found
            ok_sources = ok_found and set(exp_sources) <= set(got_sources) if exp_sources else True
            ok = ok_found and (not exp_sources or ok_sources)
            results.append(
                {
                    "question": q,
                    "found": got_found,
                    "sources": got_sources,
                    "expected_found": exp_found,
                    "expected_sources": exp_sources,
                    "ok": ok,
                }
            )
            print(f"    -> found={got_found} sources={got_sources} ok={ok}")
        except Exception as exc:
            results.append({"question": q, "ok": False, "error": str(exc)})
            print(f"    -> ERROR {exc}")
        time.sleep(0.5)
    return results


def main():
    parser = argparse.ArgumentParser(description="Eval do agente PEGASUS")
    parser.add_argument("--limit", type=int, default=0, help="executa apenas os N primeiros itens (0 = todos)")
    args = parser.parse_args()

    path = ROOT / "tests" / "eval_set.json"
    items = json.loads(path.read_text())
    if args.limit:
        items = items[: args.limit]

    results = run(items)
    ok_count = sum(1 for r in results if r["ok"])
    total = len(results)
    print("\n==== RESUMO ====")
    print(f"Acurácia: {ok_count}/{total} ({ok_count / total:.0%})")
    report = ROOT / "logs" / f"eval_{time.strftime('%Y%m%d_%H%M%S')}.json"
    report.parent.mkdir(exist_ok=True)
    report.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"Relatório: {report}")
    sys.exit(0 if ok_count == total else 1)


if __name__ == "__main__":
    main()
