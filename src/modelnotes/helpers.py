from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from modelnotes.models import Note


def get_user_notes(user: User) -> QuerySet:
    """
    Return a queryset of Notes where provided user is the auther

    Args:
        user: django User object

    Returns:
        filtered queryset of Notes
    """
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
    return Note.objects.filter(
            Q(author=user) |
            Q(groups__user=user, scope__name='group') |
            Q(scope__name='public')
        ).distinct().order_by('-updated_at')\
            .select_related('author', 'scope', 'content_type')\
            .prefetch_related('public_permissions', 'groups', 'content_object')
