from django import forms

from modelnotes.models import Note


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['title', 'content', 'scope', 'groups', 'public_permissions']
