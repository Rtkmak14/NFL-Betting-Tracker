from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .services import fetch_team_schedule, extract_game_locations, enrich_games_with_geocodes,enrich_games_with_home_coords,compute_home_travel_distances,TEAM_HOME_COORDS
from .forms import SearchForm, NoteForm
from django.contrib.auth.decorators import login_required



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
    fields = ['team', 'game_date', 'location', 'home_away', 'opponent', 'team_score', 'opponent_score', 'margin', 'days_between_games', 'travel_miles']

    template_name = 'notes/note_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin,UpdateView):
    model=Note
    fields = ['team', 'game_date', 'location', 'home_away', 'opponent', 'team_score', 'opponent_score', 'margin', 'days_between_games', 'travel_miles']
    template_name='notes/note_form.html'

class NoteDeleteView(LoginRequiredMixin,DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')


@login_required
def team_stats_view(request):
    parsed_games = None
    form = SearchForm()

    if request.method == "POST":
        if "save_game" in request.POST:
            note_form = NoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.user = request.user
                note.save()
                return redirect("team_stats")
            else:
                print("Failed to save game!")

        elif "choices" in request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                team_id = int(form.cleaned_data["choices"])
                team_name = dict(form.fields["choices"].choices).get(team_id)

                schedule_data = fetch_team_schedule(team_id=team_id)
                games = extract_game_locations(schedule_data)
                games = enrich_games_with_geocodes(games)
                games = enrich_games_with_home_coords(games, team_name)
                parsed_games = compute_home_travel_distances(games)

                for game in parsed_games:
                    initial_data = {
                        'team': team_name,
                        'game_date': game['display_date'],
                        'location': game['location'],
                        'home_away': game['homeAway'],
                        'opponent': game['opponent'],
                        'team_score': game['team_score'],
                        'opponent_score': game['opp_score'],
                        'margin': game['margin'],
                        'days_between_games': game['days_since_last_game'],
                        'travel_miles': game['travel_from_home_miles'],
                    }
                    game['note_form'] = NoteForm(initial=initial_data)

    return render(request, 'stats.html', {
        'form': form,
        'games': parsed_games,
    })




