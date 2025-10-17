from django.urls import path
from . import views
from .views import NoteListView, NoteDetailView, NoteCreateView


urlpatterns = [
    path('',views.home,name='home'),
    path('notes/', NoteListView.as_view(), name='note_list'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('notes/new/', NoteCreateView.as_view(), name='note_create'),
]
