from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .services import fetch_team_schedule, extract_game_locations,fetch_all_nfl_teams
from .forms import SearchForm

from .models import Note

# Create your views here.

class Home(LoginView):
    template_name = 'home.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('note_list')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    

class NoteListView(LoginRequiredMixin,ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('game_date')

class NoteDetailView(LoginRequiredMixin,DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'


class NoteCreateView(LoginRequiredMixin,CreateView):
    model = Note
    fields = ['team', 'game_date', 'spread', 'total', 'moneyline', 'prior_week_winning_margin', 'travel_miles']
    template_name = 'notes/note_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin,UpdateView):
    model=Note
    fields = ['team', 'game_date', 'spread', 'total', 'moneyline', 'prior_week_winning_margin', 'travel_miles']
    template_name='notes/note_form.html'

class NoteDeleteView(LoginRequiredMixin,DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

def team_stats_view(request):
    team_id = int(request.GET.get("team_id", 3))
    form = SearchForm(request.POST)

    if form.is_valid():
        team_id=form.cleaned_data["choices"]
    else:
        print(form.errors)

    # all_teams = fetch_all_nfl_teams()
    schedule_data = fetch_team_schedule(team_id=team_id)
    parsed_games = extract_game_locations(schedule_data)
    
    return render(request, 'stats.html',{'form':form,'games':parsed_games})

