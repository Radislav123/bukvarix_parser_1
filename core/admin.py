from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models as django_models
from django.http import HttpRequest

from run import Runner
from service import register_models
from . import models
from .app_settings import CoreSettings


class BaseParsingIdFilter(SimpleListFilter):
    title = "parsing ID"
    parameter_name = "parsing_id"
    parser_name: str

    def lookups(self, request, model_admin: "DomainsParsingListCoreAdmin"):
        lookups = [(x.id, x.id) for x in models.Parsing.objects.filter(parser_name = self.parser_name)]
        return lookups

    def queryset(self, request, queryset):
        if self.value() is not None:
            new_queryset = queryset.filter(parsing = self.value())
        else:
            new_queryset = queryset
        return new_queryset


# noinspection PyUnusedLocal
def run_parsing(
        admin_model: "DomainsParsingListCoreAdmin",
        request: HttpRequest,
        queryset: django_models.QuerySet
) -> None:
    Runner().run_from_code(admin_model.app_settings)


class CoreAdmin(admin.ModelAdmin):
    model: models.CoreModel
    app_settings_class = CoreSettings

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.app_settings = self.app_settings_class()


class ParsingAdmin(CoreAdmin):
    model = models.Parsing
    list_display = ("start_time", "id", "parser_name", "current", "capacity")
    list_filter = ("parser_name",)


class DomainsParsingListCoreAdmin(CoreAdmin):
    model: models.DomainsParsingListModel
    list_display = ("domains",)
    actions = (run_parsing,)


register_models(CoreAdmin, models.CoreModel, [DomainsParsingListCoreAdmin])
