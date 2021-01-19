from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from notes.models import Note


class ModelOne(models.Model):
    name = models.CharField(max_length=16)
    notes = GenericRelation(Note)

    def __str__(self):
        return self.name


class ModelTwo(models.Model):
    name = models.CharField(max_length=16)
    notes = GenericRelation(Note)

    def __str__(self):
        return self.name
