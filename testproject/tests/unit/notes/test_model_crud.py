import sys
import environ
import os
import django
from model_bakery import baker
sys.path.append(str(environ.Path(__file__) - 4))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproject.settings')
django.setup()

from django.test import TestCase

# import models
from auditlog.models import LogEntry
from notes.models import (Scope, Permission, Note, GroupPermission)


class ScopeTests(TestCase):
    """ test CRUD operations on Scope """
    def setUp(self):
        self.model = Scope
        self.to_bake = f'notes.{self.model.__name__}'
        self.field_to_update = 'name'

    def test_create(self):
        """ verify object can be created """
        row = baker.make(self.to_bake)
        self.assertTrue(isinstance(row, self.model))
        self.assertEqual(row.__str__(), getattr(row, self.field_to_update))

    def test_read(self):
        """ verify object can be read """
        row = baker.make(self.to_bake)
        entry = self.model.objects.get(id=row.id)
        self.assertTrue(isinstance(entry, self.model))
        self.assertEqual(row.id, entry.id)

    def test_update(self):
        """ verify object can be updated """
        row = baker.make(self.to_bake)
        updated = 'updated value'
        setattr(row, self.field_to_update, updated)
        row.save()
        self.assertEqual(getattr(row, self.field_to_update), updated)

    def test_delete(self):
        """ verify object can be deleted """
        row = baker.make(self.to_bake)
        row_id = row.id
        row.delete()
        queryset = self.model.objects.get_object_or_none(id=row_id)
        self.assertIsNone(queryset)


class PermissionTests(TestCase):
    """ test CRUD operations on Permission """
    def setUp(self):
        self.model = Permission
        self.to_bake = f'notes.{self.model.__name__}'
        self.field_to_update = 'name'

    def test_create(self):
        """ verify object can be created """
        row = baker.make(self.to_bake)
        self.assertTrue(isinstance(row, self.model))
        self.assertEqual(row.__str__(), getattr(row, self.field_to_update))

    def test_read(self):
        """ verify object can be read """
        row = baker.make(self.to_bake)
        entry = self.model.objects.get(id=row.id)
        self.assertTrue(isinstance(entry, self.model))
        self.assertEqual(row.id, entry.id)

    def test_update(self):
        """ verify object can be updated """
        row = baker.make(self.to_bake)
        updated = 'updated value'
        setattr(row, self.field_to_update, updated)
        row.save()
        self.assertEqual(getattr(row, self.field_to_update), updated)

    def test_delete(self):
        """ verify object can be deleted """
        row = baker.make(self.to_bake)
        row_id = row.id
        row.delete()
        queryset = self.model.objects.get_object_or_none(id=row_id)
        self.assertIsNone(queryset)


class NoteTests(TestCase):
    """ test CRUD operations on Note """
    def setUp(self):
        self.model = Note
        self.to_bake = f'notes.{self.model.__name__}'
        self.field_to_update = 'title'

    def test_create(self):
        """ verify object can be created """
        row = baker.make(self.to_bake)
        self.assertTrue(isinstance(row, self.model))
        self.assertEqual(row.__str__(), getattr(row, self.field_to_update))

    def test_read(self):
        """ verify object can be read """
        row = baker.make(self.to_bake)
        entry = self.model.objects.get(id=row.id)
        self.assertTrue(isinstance(entry, self.model))
        self.assertEqual(row.id, entry.id)

    def test_update(self):
        """ verify object can be updated """
        row = baker.make(self.to_bake)
        updated = 'updated value'
        setattr(row, self.field_to_update, updated)
        row.save()
        self.assertEqual(getattr(row, self.field_to_update), updated)

    def test_delete(self):
        """ verify object can be deleted """
        row = baker.make(self.to_bake)
        row_id = row.id
        row.delete()
        queryset = self.model.objects.get_object_or_none(id=row_id)
        self.assertIsNone(queryset)


class GroupPermissionTests(TestCase):
    """ test CRUD operations on GroupPermission """
    def setUp(self):
        self.model = GroupPermission
        self.to_bake = f'notes.{self.model.__name__}'
        for perm in ['read', 'edit', 'delete']:
            Permission.objects.get_or_create(name=perm)

    def test_create(self):
        """ verify object can be created """
        row = baker.make(self.to_bake)
        row.permissions.add(Permission.objects.get_random_row())
        self.assertTrue(isinstance(row, self.model))

    def test_read(self):
        """ verify object can be read """
        row = baker.make(self.to_bake)
        entry = self.model.objects.get(id=row.id)
        self.assertTrue(isinstance(entry, self.model))
        self.assertEqual(row.id, entry.id)

    def test_update(self):
        """ verify object can be updated """
        row = baker.make(self.to_bake)
        new_permission = Permission.objects.get_or_create(name='test')[0]
        row.permissions.add(new_permission)
        self.assertIn(new_permission, row.permissions.all())

    def test_delete(self):
        """ verify object can be deleted """
        row = baker.make(self.to_bake)
        row_id = row.id
        row.delete()
        queryset = self.model.objects.get_object_or_none(id=row_id)
        self.assertIsNone(queryset)
