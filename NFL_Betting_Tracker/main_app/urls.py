from django.urls import path
from . import views
from .views import NoteListView, NoteDetailView, NoteCreateView, NoteUpdateView, NoteDeleteView



urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('notes/', NoteListView.as_view(), name='note_list'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('notes/new/', NoteCreateView.as_view(), name='note_create'),
    path('notes/<int:pk>/update', NoteUpdateView.as_view(), name='note_update'),
    path('notes/<int:pk>/delete', NoteDeleteView.as_view(), name='note_delete'),
]
