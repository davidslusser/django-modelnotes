from django.urls import path
from .views import gui
from .views import htmx
from .views import ajax

app_name = 'modelnotes'

urlpatterns = [
    # list views
    path('list_my_notes/', gui.ListMyNotes.as_view(), name='list_my_notes'),
    path('list_group_notes/', gui.ListGroupNotes.as_view(), name='list_group_notes'),
    path('list_readable_notes/', gui.ListReadableNotes.as_view(), name='list_readable_notes'),
    path('list_all_notes/', gui.ListAllNotes.as_view(), name='list_all_notes'),

    # ajax views
    path('get_note_details', ajax.get_note_details, name='get_note_details'),
    path('get_note_auditlog', ajax.get_note_auditlog, name='get_note_auditlog'),

    # htmx views
    path('create_note', htmx.CreateNote.as_view(), name='create_note'),
    path('retrieve_notes', htmx.RetrieveNotes.as_view(), name='retrieve_notes'),
    path('update_note/<int:pk>/', htmx.UpdateNote.as_view(), name='update_note'),
    path('delete_note/<int:pk>/', htmx.DeleteNote.as_view(), name='delete_note'),
    path('get_scope_fields/', htmx.GetScopeFields.as_view(), name='get_scope_fields'),
    path('get_scope_fields/<int:pk>', htmx.GetScopeFields.as_view(), name='get_scope_fields'),
    path('get_notes_for_instance/', htmx.GetNotesForInstance.as_view(), name='get_notes_for_instance'),


]
