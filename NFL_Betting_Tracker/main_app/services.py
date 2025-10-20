import requests
from django.http import JsonResponse
from datetime import datetime

def fetch_team_schedule(team_id=3):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


