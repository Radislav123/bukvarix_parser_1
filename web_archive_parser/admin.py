from django.utils.html import format_html

from core import admin as core_admin
from service import register_models
from . import models
from .app_settings import WebArchiveSettings


class ParsingIdFilter(core_admin.BaseParsingIdFilter):
    parser_name = "WebArchiveParser"


class WebArchiveAdmin(core_admin.CoreAdmin):
    model: models.WebArchiveModel
    app_settings_class = WebArchiveSettings


class SnapshotAdmin(WebArchiveAdmin):
    model = models.Snapshot
    list_display = ("domain", "title", "clickable_url", "parsing_id")
    list_filter = (ParsingIdFilter,)

    def clickable_url(self, obj: model):
        return format_html(f'<a target="_blank" href="{obj.url}">{obj.url}</a>')

    # noinspection PyProtectedMember
    clickable_url.short_description = model._meta.get_field("url").verbose_name

    # noinspection PyMethodMayBeStatic
    def parsing_id(self, obj: model):
        return obj.parsing.id


class DomainsParsingListAdmin(WebArchiveAdmin, core_admin.DomainsParsingListCoreAdmin):
    model = models.DomainsParsingList


register_models(WebArchiveAdmin, models.WebArchiveModel)
