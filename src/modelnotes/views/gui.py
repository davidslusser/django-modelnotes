from django.conf import settings

from braces.views import SuperuserRequiredMixin
from handyhelpers.views import HandyHelperListPlusCreateAndFilterView

from modelnotes.helpers import get_all_notes, get_group_notes, get_user_notes, get_readable_notes


class ListNotesBaseView(HandyHelperListPlusCreateAndFilterView):
    base_template = getattr(settings, 'BASE_TEMPLATE', 'handyhelpers/handyhelpers_base_bs5.htm')
    template = 'handyhelpers/generic/bs5/generic_list.html'


class ListMyNotes(ListNotesBaseView):
    """ get modelnotes where user is the author """
    title = 'Notes'
    page_description = 'my notes'
    table = 'modelnotes/table/notes.htm'

    def get(self, request, *args, **kwargs):
        self.queryset = get_user_notes(user=request.user)
        return super().get(request, *args, **kwargs)


class ListGroupNotes(ListNotesBaseView):
    """  get modelnotes with a scope of 'group' and authored by a member of a group user is also a member of """
    title = 'Notes'
    page_description = 'group'
    table = 'modelnotes/table/notes.htm'

    def get(self, request, *args, **kwargs):
        self.queryset = get_group_notes(user=request.user)
        return super().get(request, *args, **kwargs)



class ListReadableNotes(ListNotesBaseView):
    """ get modelnotes that current user can read:
        - authored by user
        - with a scope of 'group' and authored by a member of a group user is also a member of
        - with a scope of 'public'
    """
    title = 'Notes'
    page_description = 'readable'
    table = 'modelnotes/table/notes.htm'

    def get(self, request, *args, **kwargs):
        self.queryset = get_readable_notes(user=request.user)
        return super().get(request, *args, **kwargs)


class ListAllNotes(ListNotesBaseView, SuperuserRequiredMixin):
    """ get modelnotes all modelnotes (only available to superusers) """
    title = 'Notes'
    page_description = 'readable'
    table = 'modelnotes/table/notes.htm'

    def get(self, request, *args, **kwargs):
        self.queryset = get_all_notes(user=request.user)
        return super().get(request, *args, **kwargs)
