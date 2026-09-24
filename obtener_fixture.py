import requests
import json

torneos = [
    "chi.1",
    "chi.copa_chi",
    "chi.super_cup",
    "conmebol.libertadores",
    "conmebol.sudamericana"
]

for torneo in torneos:

    url = (
        f"https://sports.core.api.espn.com/v2/"
        f"sports/soccer/leagues/{torneo}/"
        f"seasons/2026/teams/2688/events"
    )

    r = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    print("\n------------------")
    print(torneo)
    print("STATUS:", r.status_code)

    try:
        data = r.json()
        print("COUNT:", data.get("count"))
    except Exception:
        print("SIN JSON")
