import requests

url = "https://site.api.espn.com/apis/site/v2/sports/soccer/chi.1/teams"

r = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

print("STATUS:", r.status_code)

data = r.json()

for team in data["sports"][0]["leagues"][0]["teams"]:

    nombre = team["team"]["displayName"]
    team_id = team["team"]["id"]

    print(team_id, "-", nombre)
