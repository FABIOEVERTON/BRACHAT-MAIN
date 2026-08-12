#!/usr/bin/env python3
"""Gera data/vendas.csv com dados de vendas de 2015 (prova suporte a CSV)."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

PRODUTOS = [
    ("Smartphone Pegasus X1", "Eletrônicos", 1899.00),
    ("Notebook Falcon Pro 14", "Eletrônicos", 4299.00),
    ("Fone Bluetooth AirBeat", "Eletrônicos", 299.00),
    ("Relógio SmartWatch S2", "Eletrônicos", 799.00),
    ("Cadeira Ergonômica Aura", "Móveis", 1249.00),
    ("Mesa Ajustável Nova", "Móveis", 1899.00),
    ("Cafeteira Premium Café", "Cozinha", 649.00),
    ("Liquidificador Turbo Mix", "Cozinha", 249.00),
    ("Air Fryer Crisp 5L", "Cozinha", 549.00),
    ("Tênis Corrida Volt", "Esporte", 399.00),
    ("Mochila Urban Pro", "Acessórios", 259.00),
    ("Monitor UltraView 27", "Eletrônicos", 1599.00),
]


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "data" / "vendas.csv"
    out.parent.mkdir(exist_ok=True)
    rows = []
    start = date(2015, 1, 1)
    end = date(2015, 12, 31)
    for i in range(600):
        produto, cat, preco = random.choice(PRODUTOS)
        d = start + timedelta(days=random.randint(0, (end - start).days))
        qtd = random.randint(1, 30)
        rows.append([
            i + 1,
            produto,
            cat,
            d.isoformat(),
            qtd,
            round(preco, 2),
            round(preco * qtd, 2),
        ])
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "produto", "categoria", "data_venda", "quantidade", "preco_unitario", "receita"])
        w.writerows(rows)
    print(f"Gerado {out} ({len(rows)} linhas)")


if __name__ == "__main__":
    main()
