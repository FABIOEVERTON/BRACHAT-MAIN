from amadeus import Client

amadeus = Client(
    client_id="SUA_API_KEY",
    client_secret="SEU_API_SECRET"
)

response = amadeus.shopping.flight_offers_search.get(
    originLocationCode="GIG",
    destinationLocationCode="MAD",
    departureDate="2026-09-05",
    adults=1
)

print(response.data)
