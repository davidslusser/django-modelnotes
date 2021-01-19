from django.contrib import admin

# import models
from notes.models import (Scope, Permission, Note, GroupPermission, PublicPermission)


def set_private(modeladmin, request, queryset):
    for item in queryset:
        item.scope = Scope.objects.get(name='private')
        item.save()


def set_group(modeladmin, request, queryset):
    for item in queryset:
        item.scope = Scope.objects.get(name='group')
        item.save()


def set_public(modeladmin, request, queryset):
    for item in queryset:
        item.scope = Scope.objects.get(name='public')
        item.save()


set_private.short_description = 'set scope to private'
set_group.short_description = 'set scope to group'
set_public.short_description = 'set scope to public'


class ScopeAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'name', 'description']
    search_fields = ['name', 'description']
    list_filter = []


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'name', 'description']
    search_fields = ['name', 'description']
    list_filter = []


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'title', 'author', 'scope', 'content', 'content_type', 'object_id', 'object_repr']
    search_fields = ['title', 'content', 'object_id', 'object_repr']
    list_filter = ['author', 'scope', 'content_type']
    actions = [set_private, set_group, set_public]


class GroupPermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'note', 'group']
    search_fields = []
    list_filter = ['note', 'group']


class PublicPermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'note', 'permissions']
    search_fields = []
    list_filter = ['note', 'permissions']


# register models
admin.site.register(Scope, ScopeAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(GroupPermission, GroupPermissionAdmin)
admin.site.register(PublicPermission, PublicPermissionAdmin)
