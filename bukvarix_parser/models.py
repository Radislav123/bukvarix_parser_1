from django.db import models

from core.models import CoreModel, Parsing


class BukvarixModel(CoreModel):
    class Meta:
        abstract = True


class Domain(BukvarixModel):
    name = models.CharField("Домен", max_length = 254)
    parsing = models.ForeignKey(Parsing, on_delete = models.CASCADE)
    average_position = models.IntegerField("Средняя позиция")
    requests_top_10 = models.IntegerField("Запросов в ТОП 10")
    requests_top_3 = models.IntegerField("Запросов в ТОП 3")
    frequency_sum_top_10 = models.IntegerField("Сумма частотности ТОП 10")
    frequency_sum_top_3 = models.IntegerField("Сумма частотности ТОП 3")


class DomainsParsingList(BukvarixModel):
    class Meta:
        verbose_name_plural = "Domains Parsing List"

    domains = models.TextField("Домены для парсинга")

    def save(self, *args, **kwargs):
        self.id = 0
        super().save(*args, **kwargs)
