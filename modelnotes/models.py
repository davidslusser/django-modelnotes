from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.apps import apps
from django.conf import settings
from handyhelpers.models import HandyHelperBaseModel
if 'auditlog' in settings.INSTALLED_APPS:
    from auditlog.registry import auditlog
    from auditlog.models import AuditlogHistoryField


SCOPE_CHOICES = (
    ('public', 'public'),
    ('group', 'group'),
    ('private', 'private'),
)
PERMISSION_CHOICES = (
    ('read', 'read'),
    ('read, edit', 'read, edit'),
    ('read, edit, delete', 'read, edit, delete'),
    ('read, delete', 'read, delete'),
)


class Note(HandyHelperBaseModel):
    """
    if scope is group, any member of the group can perform actions as set in permissions
    """
    title = models.CharField(max_length=32, help_text='title for this note')
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                               help_text='user who created this note')
    groups = models.ManyToManyField(Group, blank=True, help_text='if group scoped, groups who can view this note')
    scope = models.CharField(max_length=8, choices=SCOPE_CHOICES, default='public',
                             help_text='sets access to this note')
    permissions = models.CharField(max_length=32, choices=PERMISSION_CHOICES, default='read',
                                   help_text='operations allowed on this note')
    content = models.TextField(help_text='the actual content of this note')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=128, blank=True, null=True,
                                   help_text='string representation of an object instance')
    content_object = GenericForeignKey('content_type', 'object_id')
    if 'auditlog' in settings.INSTALLED_APPS:
        history = AuditlogHistoryField()

    def clean(self):
        """ runs validations before saving """
        def verify_object_instance_exists():
            """ Check that the instance of an object, as identified by object_id, exists. If not, do not allow
            note to be attached. """
            try:
                content_type_object = ContentType.objects.get(id=self.content_type_id)
                model_class = apps.get_model(app_label=content_type_object.app_label,
                                             model_name=content_type_object.model)
            except Exception as err:
                raise ValidationError({'object_id': f'Failed to attach note: {err}'})
            try:
                model_class.objects.get(id=self.object_id)
            except model_class.DoesNotExist:
                raise ValidationError({'object_id': 'Can not attach a note to an instance that does not exists'})

        def set_obj_repr():
            """ set the object_repr """
            try:
                content_type_object = ContentType.objects.get(id=self.content_type_id)
                model_class = apps.get_model(app_label=content_type_object.app_label,
                                             model_name=content_type_object.model)
                content_instance = model_class.objects.get(id=self.object_id)
                self.object_repr = str(content_instance)
            except Exception as err:
                pass

        verify_object_instance_exists()
        set_obj_repr()

    def __str__(self):
        return self.title


if 'auditlog' in settings.INSTALLED_APPS:
    auditlog.register(Note)
