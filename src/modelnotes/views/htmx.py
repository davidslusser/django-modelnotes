import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import (ListView, View)
from django.contrib.contenttypes.models import ContentType

# import models
from modelnotes.models import Note, Permission

from modelnotes.views.action import check_managability
from modelnotes.forms import NoteForm
from modelnotes.helpers import get_all_notes

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


class CreateNote(View):
    """
    Create a Note instance via htmx. The Get method builds the form and modal. The post method creates the
    instance and triggers a confirmation via Bootstrap toast.

    Example usage in a template:
        <a href="#" hx-get="{% url 'modelnotes:create_note' %}?model_label={{ row|label }}&object_id={{ object.id }}" hx-target="#create_update_modal_wrapper">
            add note
        </a>

    To utilize the create form and modal, the modal, modal wrapper, and javascript for controlling the modal must be
    included in your template. It should look something like this:
        <div id="create_update_modal_wrapper">
        {% with 'create_update_modal' as modal_id %}
        {% include 'modelnotes/htmx/generic_modal.htm' %}
        {% include 'modelnotes/htmx/generic_modal_js.htm' %}
        {% endwith %}
        </div>
    """
    model = Note
    form = NoteForm
    form_template = 'modelnotes/form/note_form.htm' # this is the template for the note form
    template_name = 'modelnotes/htmx/generic_modal.htm' # this is the template for the modal that houses the form

    def post(self, request, *args, **kwargs):
        """ create a Note instance and confirm update via Bootstrap 'toast' """
        if not request.META.get('HTTP_HX_REQUEST'):
            return HttpResponse('Invalid request', status=400)

        nodel_label = self.request.GET.dict().get('model_label', None)
        object_id = self.request.GET.dict().get('object_id', None)
        app, model_name = nodel_label.split('.')

        form = self.form(request.POST)
        context = dict()
        context['form'] = form

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.content_type = ContentType.objects.get(app_label=app,
                                                            model=model_name)
            instance.object_id = int(object_id)
            instance.save()
            form.save_m2m()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "instanceListChanged": None,
                        "showSuccess": f"{instance} created"
                    })
                })
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        """ construct the modal content required for creating a new note """
        if not request.META.get('HTTP_HX_REQUEST'):
            return HttpResponse('Invalid request', status=400)
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
    """ List view used to dynamically get a list ot Note instances via htmx

    Example usage in a template:
        <div hx-trigger="load, instanceListChanged from:body"
             hx-get="{% url 'modelnotes:retrieve_notes' %}" hx-target="this">
        </div>

    To include create option (via Bootstrap modal) include something like in your template:
        <a href="#" hx-get="{% url 'modelnotes:create_note' %}" hx-target="#create_update_modal_wrapper">
            <i class="fas fa-add"></i>
        </a>

    To include create/update and/or delete confirmation modals include the following in your template:
        <!-- wrapper for the create/update note form modal -->
        <div id="create_update_modal_wrapper">
        {% with 'create_update_modal' as modal_id %}
        {% include 'modelnotes/htmx/generic_modal.htm' %}
        {% include 'modelnotes/htmx/generic_modal_js.htm' %}
        {% endwith %}
        </div>

        <!-- wrapper for the delete confirmation modal -->
        <div id="delete_confirmation_modal_wrapper">
        {% with 'delete_confirmation_modal' as modal_id %}
        {% include 'modelnotes/htmx/generic_modal.htm' %}
        {% include 'modelnotes/htmx/generic_modal_js.htm' %}
        {% endwith %}
        </div>
    """
    model = Note
    template_name = 'modelnotes/table/list_notes.htm'

    def get(self, request, *args, **kwargs):
        if not request.META.get('HTTP_HX_REQUEST'):
            return HttpResponse('Invalid request', status=400)
        context = dict()
        context['delete_modal_id'] = 'delete_confirmation_modal'
        context['create_update_modal_id'] = 'create_update_modal'
        context['note_list'] = get_all_notes(request.user)
        return render(request, self.template_name, context=context)


class UpdateNote(View):
    """
    Update a Note instance via htmx. The Get method creates the update form and modal. The post method updates the
    instance and triggers a confirmation via Bootstrap toast.

    Example usage in a template:
        <a href="#" hx-get="{% url 'modelnotes:update_note' pk=object.pk %}" hx-target="#{% if create_update_modal_id %}{{ create_update_modal_id }}{% else %}create_update_modal_id{% endif %}_wrapper">
            <i class="fas fa-edit"></i>
        </a>

    To utilize the update form and modal, the modal, modal wrapper, and javascript for controlling the modal must be
    included in your template. It should look something like this:
        <div id="create_update_modal_wrapper">
        {% with 'create_update_modal' as modal_id %}
        {% include 'modelnotes/htmx/generic_modal.htm' %}
        {% include 'modelnotes/htmx/generic_modal_js.htm' %}
        {% endwith %}
        </div>
    """
    model = Note
    form = NoteForm
    form_template = 'modelnotes/form/note_form.htm' # this is the template for the note form
    template_name = 'modelnotes/htmx/generic_modal.htm' # this is the template for the modal that houses the form

    def post(self, request, *args, **kwargs):
        """ update a Note instance and confirm update via Bootstrap 'toast' """
        if not request.META.get('HTTP_HX_REQUEST'):
            return HttpResponse('Invalid request', status=400)
        instance = get_object_or_404(Note, *args, **kwargs)
        if not check_managability(request.user, instance, 'delete'):
            return HttpResponse(
                status=403,
                headers={
                    'HX-Trigger': json.dumps({
                        'instanceListChanged': None,
                        'showError': f'{request.user} can not update {instance}'
                    })
                })

        form = self.form(request.POST, instance=instance)
        context = dict()
        context['form'] = form
        context['action'] = 'Update'
        context['object'] = instance
        context['path'] = f'/modelnotes/update_note/{kwargs["pk"]}/'
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        'instanceListChanged': None,
                        'showSuccess': f'{instance.title} updated'
                    })
                })
        return render(request, 'modelnotes/form/note_form.htm', context)

    def get(self, request, *args, **kwargs):
        """ build the modal and form used for editing an existing instance of a Note """
        if not request.META.get('HTTP_HX_REQUEST'):
            return HttpResponse('Invalid request', status=400)
        instance = get_object_or_404(self.model, *args, **kwargs)
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
    """
    Delete a Note instance via htmx. The Get method creates a confirmation modal. The delete method deletes the
    instance and triggers a confirmation via Bootstrap toast.

    Example usage in a template:
        <a href="#"
            hx-get="{% url 'modelnotes:delete_note' pk=note.pk %}"
            hx-target="#{% if delete_modal_id %}{{ delete_modal_id }}{% else %}id_delete_modal{% endif %}_wrapper">
            <i class="fas fa-trash"></i>
        </a>

    To utilize the delete confirmation, the modal, modal wrapper, and javascript for controlling the modal must be
    included in your template. It should look something like this:
        <!-- wrapper for the delete confirmation modal -->
        <div id="delete_confirmation_modal_wrapper">
        {% with 'delete_confirmation_modal' as modal_id %}
        {% include 'modelnotes/htmx/generic_modal.htm' %}
        {% include 'modelnotes/htmx/generic_modal_js.htm' %}
        {% endwith %}
        </div>

    """
    model = Note
    template_name = 'modelnotes/htmx/generic_modal.htm'

    def delete(self, request, *args, **kwargs):
        """ delete a Note instance and confirm delete via Bootstrap 'toast' """
        if not request.META.get('HTTP_HX_REQUEST'):
            return HttpResponse('Invalid request', status=400)

        instance = get_object_or_404(self.model, *args, **kwargs)
        if not check_managability(request.user, instance, 'delete'):
            return HttpResponse(
                status=403,
                headers={
                    'HX-Trigger': json.dumps({
                        'instanceListChanged': None,
                        'showError': f'{request.user} can not delete {instance}'
                    })
                })
        instance.delete()

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    'instanceListChanged': None,
                    'showSuccess': f'{instance} deleted'
                })
            })

    def get(self, request, *args, **kwargs):
        """ build modal for confirming delete of a Note instance """
        if not request.META.get('HTTP_HX_REQUEST'):
            return HttpResponse('Invalid request', status=400)

        instance = get_object_or_404(self.model, *args, **kwargs)
        context = dict()
        request.htmx_method = 'hx-delete'
        context['modal_id'] = 'delete_confirmation_modal'
        context['modal_size'] = 'modal-md'
        context['modal_action'] = 'Delete'
        context['modal_title'] = f'Delete Note: <span class="font-italic text-secondary">{instance}</span>'
        context['modal_body'] = f'<span class="font-italic text-secondary">{instance}</span> will be permanently ' \
                                f'deleted. Do you wish to continue?'
        return render(request, self.template_name, context)
