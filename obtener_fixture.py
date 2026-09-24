import requests

url = "https://sports.core.api.espn.com/v2/sports/soccer/leagues/chi.1/seasons/2026/teams"

r = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

print("STATUS:", r.status_code)

print(r.text)
