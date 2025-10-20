import requests
from django.http import JsonResponse
from datetime import datetime

def fetch_team_schedule(team_id=3):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


from datetime import datetime

def extract_game_locations(schedule_data):
    team_id = schedule_data.get("team", {}).get("id")
    events = schedule_data.get("events", [])
    games = []

    for event in events:
        try:
            comp = event["competitions"][0]
            venue_info = comp.get("venue", {})
            address = venue_info.get("address", {})
            stadium = venue_info.get("fullName", "")
            city = address.get("city", "")
            state = address.get("state", "")
            location = f"{stadium}, {city}, {state}"

            date_str = event["date"]
            game_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

            competitors = comp.get("competitors", [])
            home_away = None
            opponent = None

            for c in competitors:
                if c["team"]["id"] == team_id:
                    home_away = c.get("homeAway")
                else:
                    opponent = c["team"].get("displayName")

            games.append({
                "date": game_date.isoformat(),
                "location": location,
                "homeAway": home_away,
                "opponent": opponent
            })

        except Exception as e:
            print(f"Skipping event due to error: {e}")

    return games


