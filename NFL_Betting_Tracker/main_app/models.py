from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.CharField(max_length=100)
    game_date = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    home_away = models.CharField(max_length=100)
    opponent = models.CharField(max_length=100)
    team_score = models.CharField(max_length=100)
    opponent_score = models.CharField(max_length=100)
    margin = models.CharField(max_length=100)
    days_between_games = models.CharField(max_length=100)
    travel_miles = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.team} vs {self.opponent} on {self.game_date}"

    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'pk': self.id})



