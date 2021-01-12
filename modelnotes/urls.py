from django.urls import path
from notes.views import gui
from notes.views import action

app_name = 'notes'

urlpatterns = [
    # list views
    path('list_my_notes/', gui.ListMyNotes.as_view(), name='list_my_notes'),
    path('list_group_notes/', gui.ListGroupNotes.as_view(), name='list_group_notes'),
    path('list_readable_notes/', gui.ListReadableNotes.as_view(), name='list_readable_notes'),

    # action views
    path('edit_note/', action.EditNote.as_view(), name='edit_note'),
    path('delete_note/<int:pk>', action.DeleteNote.as_view(), name='delete_note'),

]
