from django import forms
from .services import fetch_all_nfl_teams
from .models import Note


class SearchForm(forms.Form):
    
    teams =[
        ("", "Select a team"),
        (22, "Arizona Cardinals"),
        (1, "Atlanta Falcons"),
        (33, "Baltimore Ravens"),
        (2, "Buffalo Bills"),
        (29, "Carolina Panthers"),
        (3, "Chicago Bears"),
        (4, "Cincinnati Bengals"),
        (5, "Cleveland Browns"),
        (6, "Dallas Cowboys"),
        (7, "Denver Broncos"),
        (8, "Detroit Lions"),
        (9, "Green Bay Packers"),
        (34, "Houston Texans"),
        (11, "Indianapolis Colts"),
        (30, "Jacksonville Jaguars"),
        (12, "Kansas City Chiefs"),
        (13, "Las Vegas Raiders"),
        (24, "Los Angeles Chargers"),
        (14, "Los Angeles Rams"),
        (15, "Miami Dolphins"),
        (16, "Minnesota Vikings"),
        (17, "New England Patriots"),
        (18, "New Orleans Saints"),
        (19, "New York Giants"),
        (20, "New York Jets"),
        (21, "Philadelphia Eagles"),
        (23, "Pittsburgh Steelers"),
        (25, "San Francisco 49ers"),
        (26, "Seattle Seahawks"),
        (27, "Tampa Bay Buccaneers"),
        (10, "Tennessee Titans"),
        (28, "Washington Commanders"),
    ]


    choices = forms.ChoiceField(
        choices=teams,
        required=True,
        )

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'team',
            'game_date',
            'location',
            'home_away',
            'opponent',
            'team_score',
            'opponent_score',
            'margin',
            'days_between_games',
            'travel_miles'
        ]
        widgets = {
            'team': forms.HiddenInput(),
            'game_date': forms.HiddenInput(),
            'location': forms.HiddenInput(),
            'home_away': forms.HiddenInput(),
            'opponent': forms.HiddenInput(),
            'team_score': forms.HiddenInput(),
            'opponent_score': forms.HiddenInput(),
            'margin': forms.HiddenInput(),
            'days_between_games': forms.HiddenInput(),
            'travel_miles': forms.HiddenInput()
        }
