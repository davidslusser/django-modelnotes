from django.conf import settings
from django.shortcuts import redirect, render, reverse
from django.views.generic import (View, ListView)
from django.db.models import Q

from braces.views import LoginRequiredMixin
from handyhelpers.mixins.view_mixins import FilterByQueryParamsMixin

# import models
from django.contrib.auth.models import Group
from notes.models import Note


class ListNotesBaseView(LoginRequiredMixin, FilterByQueryParamsMixin, ListView):
    base_template = getattr(settings, 'BASE_TEMPLATE', 'handyhelpers/handyhelpers_base.htm')
    template = 'handyhelpers/generic/generic_list.html'


class ListMyNotes(ListNotesBaseView):
    """ get notes where user is the author of """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = Note.objects.filter(author=request.user).distinct().order_by('-updated_at')
        context['base_template'] = self.base_template
        context['queryset'] = self.filter_by_query_params()
        context['title'] = 'Notes'
        context['subtitle'] = request.user.username
        context['table'] = 'notes/table/list_notes.htm'
        context['modals'] = 'notes/form/edit_note.htm'
        return render(request, self.template, context=context)


class ListGroupNotes(ListNotesBaseView):
    """ get notes with a scope of 'group' and authored by a member of a group user is also a member of """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = Note.objects.filter(groups__user=request.user, scope='group').distinct().order_by('-updated_at')
        context['base_template'] = self.base_template
        context['queryset'] = self.filter_by_query_params()
        context['title'] = 'Notes'
        context['subtitle'] = request.user.username + '\'s groups'
        context['table'] = 'notes/table/list_notes.htm'
        context['modals'] = 'notes/form/edit_note.htm'
        return render(request, self.template, context=context)


class ListReadableNotes(ListNotesBaseView):
    """ get notes user can read:
        - authored by user
        - with a scope of 'group' and authored by a member of a group user is also a member of
        - with a scope of 'public'
    """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = Note.objects.filter(
            Q(author=request.user) |
            Q(groups__user=request.user, scope='group') |
            Q(scope='public')
        ).distinct().order_by('-updated_at')
        context['base_template'] = self.base_template
        context['queryset'] = self.filter_by_query_params()
        context['title'] = 'Notes'
        context['subtitle'] = None
        context['table'] = 'notes/table/list_notes.htm'
        context['modals'] = 'notes/form/edit_note.htm'
        context['groups'] = Group.objects.all()
        return render(request, self.template, context=context)
