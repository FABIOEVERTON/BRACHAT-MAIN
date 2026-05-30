import os
import requests
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

ORIGIN = "GIG"

DESTINATIONS = ["MAD", "AMS", "MXP"]

DATES = [
    "2026-09-03",
    "2026-09-04",
    "2026-09-05",
    "2026-09-06"
]

# baseline aproximado realista
BASELINE = {
    "MAD": 5200,
    "AMS": 5600,
    "MXP": 5800
}

# recomendação de emissão por rota
EMISSION = {
    "MAD": "Iberia (https://www.iberia.com)",
    "AMS": "KLM (https://www.klm.com)",
    "MXP": "Lufthansa ou TAP (https://www.lufthansa.com / https://www.flytap.com)"
}


# -----------------------------
# SEARCH
# -----------------------------

def fetch_price(dest, date):
    try:
        r = requests.get(
            "https://serpapi.com/search",
            params={
                "engine": "google_flights",
                "departure_id": ORIGIN,
                "arrival_id": dest,
                "outbound_date": date,
                "type": "2",
                "stops": "any",
                "currency": "BRL",
                "adults": 1,
                "api_key": SERPAPI_KEY
            },
            timeout=30
        )

        data = r.json()

        flights = data.get("best_flights") or data.get("other_flights") or []

        prices = [
            int(f["price"])
            for f in flights
            if "price" in f
        ]

        return min(prices) if prices else None

    except Exception as e:
        logging.error(f"Erro {dest} {date}: {e}")
        return None


# -----------------------------
# SCORE ENGINE
# -----------------------------

def score(price, base):
    if not price or not base:
        return 0

    return (base - price) / base * 100


def decision(avg_score):
    if avg_score >= 12:
        return "🟢 COMPRAR AGORA"
    elif avg_score >= 5:
        return "🟡 MONITORAR (até 48h)"
    else:
        return "🔴 ESPERAR"


# -----------------------------
# ENGINE
# -----------------------------

def run():
    results = {}

    for dest in DESTINATIONS:
        logging.info(f"\n=== {ORIGIN} → {dest} ===")

        prices = []
        scores = []

        for date in DATES:
            price = fetch_price(dest, date)

            if not price:
                logging.info(f"Sem dados {date}")
                continue

            base = BASELINE.get(dest, 5500)
            s = score(price, base)

            prices.append((date, price))
            scores.append(s)

            logging.info(f"{date} | R$ {price:,} | score {s:.1f}%")

        if not prices:
            continue

        best = min(prices, key=lambda x: x[1])
        avg_score = sum(scores) / len(scores)

        action = decision(avg_score)

        results[dest] = {
            "best_date": best[0],
            "best_price": best[1],
            "score": avg_score,
            "action": action
        }

    # -----------------------------
    # OUTPUT FINAL
    # -----------------------------

    print("\n==============================")
    print("🔥 DECISÃO FINAL DE COMPRA")
    print("==============================\n")

    for dest, data in results.items():
        print(f"{ORIGIN} → {dest}")
        print(f"Melhor data: {data['best_date']}")
        print(f"Preço: R$ {data['best_price']:,}")
        print(f"Score médio: {data['score']:.1f}%")
        print(f"DECISÃO: {data['action']}")
        print(f"EMISSÃO: {EMISSION[dest]}")
        print("----------------------")


if __name__ == "__main__":
    run()