from django.contrib import admin

# import models
from notes.models import (Note)


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'scope', 'permissions', 'content', 'created_at', 'updated_at', 'content_type', 'object_id', 'object_repr']
    search_fields = ['title', 'scope', 'permissions', 'content', 'object_id', 'object_repr']
    list_filter = ['author', 'scope', 'permissions', 'content_type']


# register models
admin.site.register(Note, NoteAdmin)
