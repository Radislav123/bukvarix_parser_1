from io import BytesIO

import xlsxwriter
from django.db import models as django_models
from django.http import HttpRequest, HttpResponse

from core import admin as core_admin
from service import register_models
from . import models
from .app_settings import BukvarixSettings


class ParsingIdFilter(core_admin.BaseParsingIdFilter):
    parser_name = "BukvarixParser"


# noinspection PyUnusedLocal
def download_excel(
        admin_model: "DomainAdmin",
        request: HttpRequest,
        queryset: django_models.QuerySet
) -> HttpResponse:
    model_name = f"{admin_model.model.__name__}"
    stream = BytesIO()
    book = xlsxwriter.Workbook(stream, {"remove_timezone": True})
    sheet = book.add_worksheet(model_name)

    # noinspection PyUnresolvedReferences,PyProtectedMember
    header = [
        models.Domain._meta.get_field("name").verbose_name,
        models.Domain._meta.get_field("average_position").verbose_name,
        models.Domain._meta.get_field("requests_top_10").verbose_name,
        models.Domain._meta.get_field("requests_top_3").verbose_name,
        models.Domain._meta.get_field("frequency_sum_top_10").verbose_name,
        models.Domain._meta.get_field("frequency_sum_top_3").verbose_name
    ]
    for row_number, column_name in enumerate(header):
        sheet.write(0, row_number, column_name)
    for row_number, data in enumerate(queryset, 1):
        data: admin_model.model
        sheet.write(row_number, 0, data.name)
        sheet.write(row_number, 1, data.average_position)
        sheet.write(row_number, 2, data.requests_top_10)
        sheet.write(row_number, 3, data.requests_top_3)
        sheet.write(row_number, 4, data.frequency_sum_top_10)
        sheet.write(row_number, 5, data.frequency_sum_top_3)
    sheet.autofit()
    book.close()

    stream.seek(0)
    response = HttpResponse(stream.read(), content_type = admin_model.app_settings.DOWNLOAD_EXCEL_CONTENT_TYPE)
    response["Content-Disposition"] = f"attachment;filename={model_name}.xlsx"
    return response


class BukvarixAdmin(core_admin.CoreAdmin):
    model: models.BukvarixModel
    app_settings_class = BukvarixSettings


class DomainAdmin(BukvarixAdmin):
    model = models.Domain
    list_display = (
        "name",
        "average_position",
        "requests_top_10",
        "requests_top_3",
        "frequency_sum_top_10",
        "frequency_sum_top_3",
        "parsing_id"
    )
    list_filter = (ParsingIdFilter,)
    actions = (download_excel,)

    # noinspection PyMethodMayBeStatic
    def parsing_id(self, obj: model):
        return obj.parsing.id


class DomainsParsingListAdmin(BukvarixAdmin, core_admin.DomainsParsingListCoreAdmin):
    model = models.DomainsParsingList


register_models(BukvarixAdmin, models.BukvarixModel)
