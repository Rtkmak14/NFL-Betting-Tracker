from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from .models import Note

# Create your views here.

def home(request):
    return render(request,'home.html')

class NoteListView(ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'


class NoteCreateView(CreateView):
    model = Note
    fields = ['team', 'game_date', 'spread', 'total', 'moneyline', 'prior_week_winning_margin', 'travel_miles']
    template_name = 'notes/note_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NoteUpdateView(UpdateView):
    model=Note
    fields = ['team', 'game_date', 'spread', 'total', 'moneyline', 'prior_week_winning_margin', 'travel_miles']
    template_name='notes/note_form.html'

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')
