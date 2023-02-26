from django.conf import settings

from django.shortcuts import render
from django.views.generic import (ListView, View)

from handyhelpers.views import HandyHelperListView

from test_app.models import Order


# class ListOrders(HandyHelperListView):
#     """ list available Order entries """
#     queryset = Order.objects.all().select_related('product').prefetch_related('notes')
#     title = 'Orders'
#     page_description = ''
#     table = 'test_app/table/orders.htm'
#     modals = 'modelnotes/form/create_note.htm'

    # need to add the create_update modal and js for modal controls and toast

from modelnotes.forms import NoteForm

class ListOrders(View):
    base_template = getattr(settings, 'BASE_TEMPLATE', 'handyhelpers/handyhelpers_base_bs5.htm')
    template_name = 'modelnotes/generic_list_view.html'
    form_template = 'modelnotes/form/note_form.htm'
    model = Order

    def get(self, request, *args, **kwargs):
        print('in ListOrders get()')
        context = dict()
        form = NoteForm(request.GET)
        context['title'] = 'Orders'
        context['subtitle'] = 'all orders'
        # context['form'] = form
        # context['modal_id'] = 'create_update_modal'
        # context['modal_size'] = 'modal-lg'
        # context['modal_action'] = 'Create'
        # context['modal_title'] = f'Create: <span class="font-italic text-secondary">{self.model._meta.model_name.title()}</span>'
        # context['form_template'] = self.form_template
        context['table'] = 'test_app/table/orders.htm'
        context['queryset'] = self.model.objects.all()
        return render(request, self.template_name, context)
