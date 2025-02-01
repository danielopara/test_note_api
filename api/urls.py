from django.urls import path

from .views import NoteView, UserView

urlpatterns = [
    path('notes/', NoteView.get_notes, name="get notes"),
    path('notes', NoteView.create_note, name="create note"),
    path('note/<str:id>', NoteView.get_note_by_id, name="get note by id"),
    
    
    path('user/register', UserView.register_user, name="register user"),
    path('user/login', UserView.login, name="login user"),
]
