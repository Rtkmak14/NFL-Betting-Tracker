import requests
from django.http import JsonResponse
from datetime import datetime
from zoneinfo import ZoneInfo
import os


def fetch_all_nfl_teams():
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    teams = []
    for item in data.get("sports", [])[0].get("leagues", [])[0].get("teams", []):
        team_info = item.get("team", {})
        teams.append({
            "id": int(team_info.get("id")),
            "displayName": team_info.get("displayName")
        })

    return teams

def fetch_team_schedule(team_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


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
            game_date_local = game_date.astimezone(ZoneInfo("America/Chicago"))
            display_date = game_date_local.strftime("%Y-%m-%d %I:%M %p %Z")


            competitors = comp.get("competitors", [])
            home_away = None
            opponent = None

            for c in competitors:
                score_obj = c.get("score")
                score = int(score_obj["value"]) if score_obj and "value" in score_obj else 0
                
                if c["team"]["id"] == team_id:
                    home_away = c.get("homeAway")
                    team_score = score

                else:
                    opponent = c["team"].get("displayName")
                    opp_score = score
            
            margin = team_score - opp_score

  

            games.append({
                "date": game_date,
                "display_date":display_date,
                "location": location,
                "homeAway": home_away,
                "opponent": opponent,
                "team_score": team_score,
                "opp_score": opp_score,
                "margin": margin
            })

        except Exception as e:
            print(f"Skipping event due to error: {e}")
    
    for i in range(1,len(games)):
        prev_date=games[i-1]["date"]
        curr_date=games[i]["date"]
        games[i]["days_since_last_game"] = (curr_date - prev_date).days
    
    games[0]["days_since_last_game"] = 0

    return games

def get_geocodes():
    key = os.getenv("GOOGLE_MAPS_API_KEY")
    address = "Soldier Field, Chicago, IL"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": key}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if data["status"] == "OK" and data["results"]:
        coords = data["results"][0]["geometry"]["location"]
        return coords["lat"], coords["lng"]
    else:
        print("Geocoding failed:", data.get("status"), data.get("error_message"))
        return None, None




