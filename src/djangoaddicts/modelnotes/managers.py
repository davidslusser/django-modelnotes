from handyhelpers.managers import HandyHelperModelManager

from .helpers import get_readable_notes
from .models import Note


class ReadableNotesManager(HandyHelperModelManager):

    def readable_notes(self, *args, **kwargs):
        print('TEST: in readable_notes()')
        user = kwargs.get('user', None)
        if not user:
            return Note.objects.none()
        print('TEST: got a user: ', user)
        print(self)
        print(dir(self.model._meta))
        print(self.model._meta.related_objects)
        return get_readable_notes(user=user)
