import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import (ListView, View)
from django.contrib.contenttypes.models import ContentType

# import models
from modelnotes.models import Note, Permission

from modelnotes.views.action import check_managability
from modelnotes.forms import NoteForm

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
        context['name'] = None

        if scope == '2':
            context['field'] = 'groups'
            context['option_list'] = request.user.groups.all()
            if instance:
                context['selected_list'] = instance.groups.all()
            if action:
                context['select_id'] = f'id_{action}_group_select'
            else:
                context['select_id'] = 'id_group_select'
            context['multiple'] = True
            context['name'] = 'groups'
        elif scope == '3':
            context['field'] = 'Permissions'
            context['option_list'] = Permission.objects.all()
            if instance:
                context['selected_list'] = instance.public_permissions.all()
            if action:
                context['select_id'] = f'id_{action}_permission_select'
            else:
                context['select_id'] = 'id_permission_select'
            context['multiple'] = True
            context['name'] = 'public_permissions'
        return render(request, template_name='modelnotes/snippet/select_options.htm', context=context)


class BuildEditNoteModal(View):
    """ get groups or permissions based on scope and build dropdown for create/edit modelnote form """
    def get(self, request, *args, **kwargs):
        context = dict()
        instance_id = request.GET.get('id', None)
        instance = Note.objects.get_object_or_none(id=instance_id)
        if instance:
            context['object'] = instance
            if not check_managability(request.user, instance, 'edit'):
                context['object'] = None
                context['message'] = f'{request.user} is not authorized to update this note'
        else:
            context['object'] = None
        context['permissions'] = Permission.objects.all()
        return render(request, template_name='modelnotes/snippet/edit_modal.htm', context=context)



#########

class CreateNote(View):
    """
    ** need to get the model name and object_id; probably best to add to the url '{% url 'modelnotes:create_note' %}?model={{ object|label }}&id={{ object.id }}'
    """
    model = Note
    form = NoteForm
    form_template = 'modelnotes/form/note_form.htm'
    template_name = 'modelnotes/htmx/generic_modal.htm'

    """ create a note """

    def post(self, request, *args, **kwargs):
        print('in CreateNote post()')

        print(request.GET)
        print(request.POST)

        nodel_label = self.request.GET.dict().get('model_label', None)
        object_id = self.request.GET.dict().get('object_id', None)
        app, model_name = nodel_label.split('.')
        print(app, model_name)

        form = self.form(request.POST)
        context = dict()
        context['form'] = form

        if form.is_valid():
            print('TEST: groups = ', getattr(form.cleaned_data, 'groups', None))
            print(form.data)
            print(form.cleaned_data)
            instance = form.save(commit=False)
            instance.author = request.user
            instance.content_type = ContentType.objects.get(app_label=app,
                                                            model=model_name)
            ContentType.objects.get(app_label='test_app', model='order')
            instance.object_id = int(object_id)
            instance.save()
            form.save_m2m()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "instanceListChanged": None,
                        "showMessage": f"{instance} created"
                    })
                })
        else:
            print('ERROR: form is not valid')
            print(form.errors)
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        print('in CreateNote get()')
        print(request.GET)
        model_label = self.request.GET.dict().get('model_label', None)
        object_id = self.request.GET.dict().get('object_id', None)

        context = dict()
        form = NoteForm(request.GET)
        context['form'] = form
        context['modal_id'] = 'create_update_modal'
        context['modal_size'] = 'modal-lg'
        context['modal_action'] = 'Create'
        context['modal_title'] = f'Create: <span class="font-italic text-secondary">{self.model._meta.model_name.title()}</span>'
        context['form_template'] = self.form_template
        context['hx_post'] = f'/modelnotes/create_note?model_label={model_label}&object_id={object_id}'
        return render(request, self.template_name, context)


class RetrieveNotes(ListView):
    model = Note
    template_name = "modelnotes/table/list_notes_two.htm"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_modal_id'] = 'delete_confirmation_modal'
        context['create_update_modal_id'] = 'create_update_modal'
        return context


class UpdateNote(View):
    """ update a note """
    model = Note
    form = NoteForm
    form_template = 'modelnotes/form/note_form.htm'
    template_name = 'modelnotes/htmx/generic_modal.htm'

    def post(self, request, *args, **kwargs):
        print('TEST: in UpdateNote post()')
        note = get_object_or_404(Note, **kwargs)
        form = self.form(request.POST, instance=note)
        context = dict()
        context['form'] = form
        context['action'] = 'Update'
        context['object'] = note
        context['path'] = f'/modelnotes/update_note/{kwargs["pk"]}/'
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "instanceListChanged": None,
                        "showMessage": f"{note.title} updated"
                    })
                })
        else:
            print('ERROR: form is not valid')
            print(form.errors)
        return render(request, 'modelnotes/form/note_form.htm', context)

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(self.model, **kwargs)
        form = self.form(instance=instance)
        context = dict()
        context['object'] = instance
        context['form'] = form
        context['modal_id'] = 'create_update_modal'
        context['modal_size'] = 'modal-lg'
        context['modal_action'] = 'Update'
        context['modal_title'] = f'Update: <span class="font-italic text-secondary">{instance}</span>'
        context['form_template'] = self.form_template
        return render(request, self.template_name, context)


class DeleteNote(View):
    model = Note
    template_name = 'modelnotes/htmx/generic_modal.htm'

    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(self.model, **kwargs)
        # instance.delete()

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "instanceListChanged": None,
                    "showMessage": f"{instance} deleted"
                })
            })

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(self.model, **kwargs)
        context = dict()
        request.htmx_method = 'hx-delete'
        context['modal_id'] = 'delete_confirmation_modal'
        context['modal_size'] = 'modal-md'
        context['modal_action'] = 'Delete'
        context['modal_title'] = f'Delete Note: <span class="font-italic text-secondary">{instance}</span>'
        context[
            'modal_body'] = f'<span class="font-italic text-secondary">{instance}</span> will be permanently deleted. Do you wish to continue?'
        return render(request, self.template_name, context)

