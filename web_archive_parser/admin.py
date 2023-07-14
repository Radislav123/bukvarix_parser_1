from io import BytesIO

import xlsxwriter
from django.db import models as django_models
from django.http import HttpRequest, HttpResponse
from django.utils.html import format_html

from core import admin as core_admin
from service import register_models
from . import models
from .app_settings import WebArchiveSettings


class ParsingIdFilter(core_admin.BaseParsingIdFilter):
    parser_name = "WebArchiveParser"


# noinspection PyUnusedLocal
def download_excel(
        admin_model: "SnapshotAdmin",
        request: HttpRequest,
        queryset: django_models.QuerySet
) -> HttpResponse:
    model_name = f"{admin_model.model.__name__}"
    stream = BytesIO()
    book = xlsxwriter.Workbook(stream, {"remove_timezone": True})
    sheet = book.add_worksheet(model_name)

    # noinspection PyUnresolvedReferences,PyProtectedMember
    header = [
        models.Snapshot._meta.get_field("domain").verbose_name,
        models.Snapshot._meta.get_field("title").verbose_name,
        models.Snapshot._meta.get_field("url").verbose_name,
        models.Snapshot._meta.get_field("exists_in_archive").verbose_name,
    ]
    for row_number, column_name in enumerate(header):
        sheet.write(0, row_number, column_name)
    for row_number, data in enumerate(queryset, 1):
        data: admin_model.model
        sheet.write(row_number, 0, data.domain)
        sheet.write(row_number, 1, data.title)
        sheet.write(row_number, 2, data.url)
        sheet.write(row_number, 3, data.exists_in_archive)
    sheet.autofit()
    book.close()

    stream.seek(0)
    response = HttpResponse(stream.read(), content_type = admin_model.app_settings.DOWNLOAD_EXCEL_CONTENT_TYPE)
    response["Content-Disposition"] = f"attachment;filename={model_name}.xlsx"
    return response


class WebArchiveAdmin(core_admin.CoreAdmin):
    model: models.WebArchiveModel
    app_settings_class = WebArchiveSettings


class SnapshotAdmin(WebArchiveAdmin):
    model = models.Snapshot
    list_display = ("domain", "title", "clickable_url", "exists_in_archive", "parsing_id")
    list_filter = (ParsingIdFilter, "exists_in_archive")
    actions = (download_excel,)

    def clickable_url(self, obj: model):
        return format_html(f'<a target="_blank" href="{obj.url}">{obj.url}</a>')

    # noinspection PyProtectedMember
    clickable_url.short_description = model._meta.get_field("url").verbose_name

    # noinspection PyMethodMayBeStatic
    def parsing_id(self, obj: model):
        return obj.parsing.id

    def get_queryset(self, request: HttpRequest) -> django_models.QuerySet:
        queryset: django_models.QuerySet = super().get_queryset(request)
        new_queryset = queryset.order_by("-exists_in_archive")
        return new_queryset


class DomainsParsingListAdmin(WebArchiveAdmin, core_admin.DomainsParsingListCoreAdmin):
    model = models.DomainsParsingList


register_models(WebArchiveAdmin, models.WebArchiveModel)
