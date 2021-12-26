from django.contrib import admin

# import models
from testapp.models import (ModelOne, ModelTwo)


class ModelOneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = []


class ModelTwoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = []


# register models
admin.site.register(ModelOne, ModelOneAdmin)
admin.site.register(ModelTwo, ModelTwoAdmin)
