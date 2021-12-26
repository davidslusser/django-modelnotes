from django.db import models
from modelnotes.models import ModelNoteField


class ModelOne(models.Model):
    name = models.CharField(max_length=16)
    notes = ModelNoteField()

    def __str__(self):
        return self.name


class ModelTwo(models.Model):
    name = models.CharField(max_length=16)
    notes = ModelNoteField()

    def __str__(self):
        return self.name
