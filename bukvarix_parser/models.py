from django.db import models

from core import models as core_models


class BukvarixModel(core_models.CoreModel):
    class Meta:
        abstract = True


class Domain(BukvarixModel):
    name = models.CharField("Домен", max_length = 256)
    parsing = models.ForeignKey(core_models.Parsing, on_delete = models.CASCADE)
    average_position = models.IntegerField("Средняя позиция")
    requests_top_10 = models.IntegerField("Запросов в ТОП 10")
    requests_top_3 = models.IntegerField("Запросов в ТОП 3")
    frequency_sum_top_10 = models.IntegerField("Сумма частотности ТОП 10")
    frequency_sum_top_3 = models.IntegerField("Сумма частотности ТОП 3")


class DomainsParsingList(core_models.DomainsParsingListModel):
    pass
