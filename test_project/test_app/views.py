from django.conf import settings

from django.shortcuts import render
from django.views.generic import (DetailView, ListView, View)

from handyhelpers.views import HandyHelperListView

from test_app.models import Order
from djangoaddicts.modelnotes.helpers import get_all_notes


# class ListOrders(HandyHelperListView):
#     """ list available Order entries """
#     queryset = Order.objects.all().select_related('product').prefetch_related('notes')
#     title = 'Orders'
#     page_description = ''
#     table = 'test_app/table/orders.htm'
#     modals = 'modelnotes/form/create_note.htm'

    # need to add the create_update modal and js for modal controls and toast

from djangoaddicts.modelnotes.forms import NoteForm

class ListOrders(View):
    base_template = getattr(settings, 'BASE_TEMPLATE', 'handyhelpers/handyhelpers_base_bs5.htm')
    template_name = 'modelnotes/generic_list_view.html'
    form_template = 'modelnotes/form/note_form.htm'
    model = Order

    def get(self, request, *args, **kwargs):
        print('TEST: in ListOrders()')
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


class DetailOrder(DetailView):
    model = Order
    base_template = getattr(settings, 'BASE_TEMPLATE', 'handyhelpers/handyhelpers_base_bs5.htm')
    template_name = "test_app/detail/detail_order.html"

    def get_context_data(self, **kwargs):
        # print(self.object.notes.readable_notes(self.request.user))
        # print(self.object)
        # print(self.object.notes.all())
        context = super(DetailOrder, self).get_context_data(**kwargs)
        context['base_template'] = self.base_template
        # context['readable_notes'] = get_all_notes(user=self.request.user, instance=self.object)
        context['readable_notes'] = self.object.notes.filter(user=self.request.user)#, title='n7')
        return context
