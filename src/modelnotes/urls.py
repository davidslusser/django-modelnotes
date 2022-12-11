from django.urls import path
from modelnotes.views import gui
from modelnotes.views import action

app_name = 'modelnotes'

urlpatterns = [
    # list views
    path('list_my_notes/', gui.ListMyNotes.as_view(), name='list_my_notes'),
    path('list_group_notes/', gui.ListGroupNotes.as_view(), name='list_group_notes'),
    path('list_readable_notes/', gui.ListReadableNotes.as_view(), name='list_readable_notes'),
    path('list_all_notes/', gui.ListAllNotes.as_view(), name='list_all_notes'),

    # action views
    path('update_note/', action.UpdateNote.as_view(), name='update_note'),
    path('delete_note/<int:pk>', action.DeleteNote.as_view(), name='delete_note'),

]
