import requests
from django.http import JsonResponse
from datetime import datetime
from zoneinfo import ZoneInfo
import os
from math import radians, sin, cos, sqrt, atan2

TEAM_HOME_COORDS = {
    "Arizona Cardinals": {"lat": 33.5276, "lng": -112.2626},  # State Farm Stadium
    "Atlanta Falcons": {"lat": 33.7554, "lng": -84.4008},     # Mercedes-Benz Stadium
    "Baltimore Ravens": {"lat": 39.2779, "lng": -76.6227},    # M&T Bank Stadium
    "Buffalo Bills": {"lat": 42.7738, "lng": -78.7868},       # Highmark Stadium
    "Carolina Panthers": {"lat": 35.2251, "lng": -80.8529},   # Bank of America Stadium
    "Chicago Bears": {"lat": 41.8625, "lng": -87.6166},       # Soldier Field
    "Cincinnati Bengals": {"lat": 39.0955, "lng": -84.5160},  # Paycor Stadium
    "Cleveland Browns": {"lat": 41.5061, "lng": -81.6995},    # Cleveland Browns Stadium
    "Dallas Cowboys": {"lat": 32.7473, "lng": -97.0945},      # AT&T Stadium
    "Denver Broncos": {"lat": 39.7439, "lng": -105.0201},     # Empower Field at Mile High
    "Detroit Lions": {"lat": 42.3389, "lng": -83.0458},       # Ford Field
    "Green Bay Packers": {"lat": 44.5013, "lng": -88.0622},   # Lambeau Field
    "Houston Texans": {"lat": 29.6847, "lng": -95.4107},      # NRG Stadium
    "Indianapolis Colts": {"lat": 39.7601, "lng": -86.1638},  # Lucas Oil Stadium
    "Jacksonville Jaguars": {"lat": 30.3239, "lng": -81.6375},# EverBank Stadium
    "Kansas City Chiefs": {"lat": 39.0489, "lng": -94.4839},  # GEHA Field at Arrowhead Stadium
    "Las Vegas Raiders": {"lat": 36.0906, "lng": -115.1839},  # Allegiant Stadium
    "Los Angeles Chargers": {"lat": 33.9535, "lng": -118.3390},# SoFi Stadium
    "Los Angeles Rams": {"lat": 33.9535, "lng": -118.3390},   # SoFi Stadium
    "Miami Dolphins": {"lat": 25.9581, "lng": -80.2389},      # Hard Rock Stadium
    "Minnesota Vikings": {"lat": 44.9740, "lng": -93.2580},   # U.S. Bank Stadium
    "New England Patriots": {"lat": 42.0910, "lng": -71.2640},# Gillette Stadium
    "New Orleans Saints": {"lat": 29.9508, "lng": -90.0811},  # Caesars Superdome
    "New York Giants": {"lat": 40.8135, "lng": -74.0744},     # MetLife Stadium
    "New York Jets": {"lat": 40.8135, "lng": -74.0744},       # MetLife Stadium
    "Philadelphia Eagles": {"lat": 39.9008, "lng": -75.1675}, # Lincoln Financial Field
    "Pittsburgh Steelers": {"lat": 40.4467, "lng": -80.0158}, # Acrisure Stadium
    "San Francisco 49ers": {"lat": 37.4030, "lng": -121.9700},# Levi's Stadium
    "Seattle Seahawks": {"lat": 47.5952, "lng": -122.3316},   # Lumen Field
    "Tampa Bay Buccaneers": {"lat": 27.9758, "lng": -82.5033},# Raymond James Stadium
    "Tennessee Titans": {"lat": 36.1664, "lng": -86.7714},    # Nissan Stadium
    "Washington Commanders": {"lat": 38.9078, "lng": -76.8644}# Commanders Field
}

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

def get_geocodes(address):
    key = os.getenv("GOOGLE_MAPS_API_KEY")
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


def enrich_games_with_geocodes(games):
    for game in games:
        lat, lng = get_geocodes(game["location"])
        game["lat"]=lat
        game["lng"]=lng
    return games

def enrich_games_with_home_coords(games,team_name):
    home = TEAM_HOME_COORDS.get(team_name)
    for game in games:
        game["home_lat"]=home["lat"]
        game["home_lng"]=home["lng"]
    return games

def haversine(lat1, lng1, lat2, lng2):
    R = 3958.8  # Earth radius in miles
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def compute_home_travel_distances(games):
    for game in games:
        if game["homeAway"]=="away":
            distance= haversine(
                game["home_lat"],game["home_lng"],
                game["lat"],game["lng"]
            )
            game["travel_from_home_miles"]=round(distance,1)
        else:
            game["travel_from_home_miles"]=0
    
    return games