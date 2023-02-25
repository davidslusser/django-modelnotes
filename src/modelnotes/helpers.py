from django.apps import apps
from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.models import User


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
    if action not in 'readeditdelete':
        return False
    if user.is_superuser:
        return True
    if note.author == user:
        return True
    if note.scope.name == 'group' and \
            any(i in user.groups.all() for i in note.groups.all()) and \
            action in [i.name for i in note.public_permissions.all()]:
        return True
    if note.scope.name == 'public' and action in [i.name for i in note.public_permissions.all()]:
        return True
    return False


def get_user_notes(user: User) -> QuerySet:
    """
    Return a queryset of Notes where provided user is the auther

    Args:
        user: django User object

    Returns:
        filtered queryset of Notes
    """
    Note = apps.get_model('modelnotes', 'Note')
    return Note.objects.filter(author=user).distinct().order_by('-updated_at')\
        .select_related('author', 'scope', 'content_type')\
        .prefetch_related('public_permissions', 'groups', 'content_object')


def get_group_notes(user: User) -> QuerySet:
    """
    Return a queryset of Notes with a scope of 'group' and authored by a member of a group the
    provided user is also a member of

    Args:
        user: django User object

    Returns:
        filtered queryset of Notes
    """
    Note = apps.get_model('modelnotes', 'Note')
    return Note.objects.filter(groups__user=user, scope__name='group').distinct()\
            .order_by('-updated_at')\
            .select_related('author', 'scope', 'content_type')\
            .prefetch_related('public_permissions', 'groups', 'content_object')


def get_readable_notes(user: User) -> QuerySet:
    """
    Return a queryset of Notes that the provided user can read:
        - authored by user
        - with a scope of 'group' and authored by a member of a group user is also a member of
        - with a scope of 'public'

    Args:
        user: django User object

    Returns:
        filtered queryset of Notes
    """
    Note = apps.get_model('modelnotes', 'Note')
    return Note.objects.filter(
            Q(author=user) |
            Q(groups__user=user, scope__name='group') |
            Q(scope__name='public')
        ).distinct().order_by('-updated_at')\
            .select_related('author', 'scope', 'content_type')\
            .prefetch_related('public_permissions', 'groups', 'content_object')


def get_all_notes(user: User) -> QuerySet:
    """
    Return a queryset of Notes that the provided user can read:
        - authored by user
        - with a scope of 'group' and authored by a member of a group user is also a member of
        - with a scope of 'public'
         or all notes if user is superuser

    Args:
        user: django User object

    Returns:
        filtered queryset of Notes
    """
    Note = apps.get_model('modelnotes', 'Note')
    if user.is_superuser:
        return Note.objects.all()
    return get_readable_notes(user)
