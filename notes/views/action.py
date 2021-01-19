from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import View, DeleteView, UpdateView
from braces.views import LoginRequiredMixin

# import models
from django.contrib.auth.models import Group
from notes.models import Note


def check_managability(user, note, action):
    """
    Determine if user can edit or delete this note. This note can be edited or deleted if at least one of the
    following criteria is met:
        - user is an admin
        - user is the author of the note
        - user is member of a group in groups AND note is proper permission is set
        - note is public and proper permission is set

    Args:
        user: django User object
        note: Note object
        action: (str) name of action to check for (edit or delete)

    Returns (bool):
        True if this note can be managed by the provided user
        False if this note can not be managed by the provided user
    """
    if action not in 'editdelete':
        return False
    if user.is_superuser:
        return True
    if note.author == user:
        return True
    if note.scope == 'group' and \
            any(i in user.groups.all() for i in note.groups.all()) and \
            action in note.permissions:
        return True
    if note.scope == 'public' and action in note.permissions:
        return True
    return False


class EditNote(LoginRequiredMixin, View):
    """ edit a note """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        obj_id = self.request.GET.dict().get('id', None)
        title = self.request.GET.dict().get('title', None)
        scope = self.request.GET.dict().get('scope', None)
        groups = self.request.GET.dict().get('groups', None)
        permissions = self.request.GET.dict().get('permissions', None)
        content = self.request.GET.dict().get('content', None)
        new_groups = Group.objects.filter(name__in=groups.split(','))
        try:
            note = Note.objects.get_object_or_none(id=obj_id)
            if check_managability(request.user, note, 'edit'):
                note.title = title
                note.scope = scope
                note.permissions = permissions
                note.content = content
                if scope == 'private':
                    note.groups.remove(*new_groups)
                for group in new_groups:
                    if group not in note.groups.all():
                        note.groups.add(group)
                for group in note.groups.all():
                    if group not in new_groups:
                        note.groups.remove(group)
                note.save()
                messages.add_message(self.request, messages.INFO, 'note successfully updated', extra_tags='alert-info')
            else:
                messages.add_message(self.request, messages.ERROR, f'This note can not be updated by {request.user}',
                                     extra_tags='alert-danger')
        except Exception as err:
            messages.add_message(request, messages.ERROR, err, extra_tags='alert-danger')
        return redirect(self.request.META.get('HTTP_REFERER'))


class DeleteNote(LoginRequiredMixin, DeleteView):
    """ delete a note (by pk) and return to the referring page """
    def delete(self, request, *args, **kwargs):
        note = Note.objects.get(**kwargs)
        if check_managability(request.user, note, 'delete'):
            note.delete()
            messages.add_message(self.request, messages.INFO, 'note successfully deleted', extra_tags='alert-info')
        else:
            messages.add_message(self.request, messages.ERROR, f'This note can not be deleted by {request.user}',
                                 extra_tags='alert-danger')
        return redirect(self.request.META.get('HTTP_REFERER'))
