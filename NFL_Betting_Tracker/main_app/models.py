from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Note(models.Model):
    team = models.CharField(max_length=100)
    game_date = models.DateField()
    spread = models.CharField(max_length=100)
    total = models.CharField(max_length=100)  
    moneyline = models.CharField(max_length=100)
    prior_week_winning_margin = models.CharField(max_length=100)  
    travel_miles = models.CharField(max_length=100) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.team}-{self.game_date}"
    
    def get_absolute_url(self):
        return reverse('note_detail',kwargs={'pk':self.id})


