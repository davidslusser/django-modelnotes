from django.contrib import admin

# import models
from notes.models import (Note)


def set_private(modeladmin, request, queryset):
    for item in queryset:
        item.scope = 'private'
        item.save()


def set_public(modeladmin, request, queryset):
    for item in queryset:
        item.scope = 'public'
        item.save()


set_private.short_description = 'set scope to private'
set_public.short_description = 'set scope to public'


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'scope', 'permissions', 'content', 'created_at', 'updated_at', 'content_type', 'object_id', 'object_repr']
    search_fields = ['title', 'scope', 'permissions', 'content', 'object_id', 'object_repr']
    list_filter = ['author', 'scope', 'permissions', 'content_type']
    actions = [set_private, set_public]


# register models
admin.site.register(Note, NoteAdmin)
