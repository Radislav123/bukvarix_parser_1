from django.contrib import admin

from service import register_models
from . import models


class CoreAdmin(admin.ModelAdmin):
    model: models.CoreModel


class ParsingAdmin(CoreAdmin):
    model = models.Parsing
    list_display = ("start_time", "id", "parser_name", "current", "capacity")


register_models(CoreAdmin, models.CoreModel)
