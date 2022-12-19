import requests
from django.shortcuts import render
from django.views.generic import (View)

# import models
from modelnotes.models import Note, Permission


class GetScopeFields(View):
    """ get groups or permissions based on scope and build dropdown for create/edit modelnote form """
    def get(self, request, *args, **kwargs):
        context = dict()
        scope = request.GET.get('scope', None)
        action = request.GET.get('action', None)
        pk = kwargs.get('pk', None)
        if pk:
            instance = Note.objects.get_object_or_none(pk=pk)
        else: instance = None
        context['object'] = instance

        # set defaults
        context['option_list'] = None
        context['selected_list'] = None
        context['field'] = None
        context['multiple'] = None

        if scope == 'group':
            context['field'] = 'Groups'
            context['option_list'] = request.user.groups.all()
            if instance:
                context['selected_list'] = instance.groups.all()
            if action:
                context['select_id'] = f'id_{action}_group_select'
            else:
                context['select_id'] = 'id_group_select'
            context['multiple'] = True
        elif scope == 'public':
            context['field'] = 'Permissions'
            context['option_list'] = Permission.objects.all()
            if instance:
                context['selected_list'] = instance.public_permissions.all()
            if action:
                context['select_id'] = f'id_{action}_permission_select'
            else:
                context['select_id'] = 'id_permission_select'
            context['multiple'] = True
        return render(request, template_name='modelnotes/snippet/select_options.htm', context=context)


class BuildEditNoteModal(View):
    """ get groups or permissions based on scope and build dropdown for create/edit modelnote form """
    def get(self, request, *args, **kwargs):
        context = dict()
        id = request.GET.get('id', None)
        if id:
            context['object'] = Note.objects.get_object_or_none(id=id)
        else:
            context['object'] = None
        context['permissions'] = Permission.objects.all()
        return render(request, template_name='modelnotes/snippet/edit_modal.htm', context=context)
