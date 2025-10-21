from django import forms
from .services import fetch_all_nfl_teams

class SearchForm(forms.Form):
    teams =[(3,"Chicago Bears"),(18,"Detroit Lions")]

    choices = forms.ChoiceField(
        choices=teams,
        required=True,
        )