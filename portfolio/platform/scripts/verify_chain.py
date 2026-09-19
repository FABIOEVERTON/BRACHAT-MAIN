#!/usr/bin/env python3
"""Verificação externa da cadeia SHA-256 (PRD §3.4, ADR-004, F0-24).

Uso:
  python3 scripts/verify_chain.py <tenant_id> <content_hash> <expected_chain_hash> [previous_chain_hash]

Sem previous → valida âncora: expected == SHA256(content + tenant_id).
Com previous → valida encadeamento: expected == SHA256(content + previous).

Exit 0 = cadeia íntegra; exit 1 = quebra (perito consegue provar violação).
"""

import hashlib
import sys


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def main() -> int:
    args = sys.argv[1:]
    if len(args) not in (3, 4):
        print("uso: verify_chain.py <tenant_id> <content_hash> <expected_chain_hash> [previous_chain_hash]")
        return 2

    tenant_id, content_hash, expected = args[0], args[1], args[2]
    previous = args[3] if len(args) == 4 else None

    anchor = previous if previous else tenant_id
    computed = sha256(f"{content_hash}{anchor}")

    if computed == expected:
        print(f"OK  — cadeia íntegra: {computed}")
        return 0
    print(f"VIOLACAO — esperado {expected}, calculado {computed}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())