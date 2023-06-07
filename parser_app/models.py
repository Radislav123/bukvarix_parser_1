from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from run import Runner
from . import settings


class ProjectModel(models.Model):
    class Meta:
        abstract = True


class Parsing(ProjectModel):
    current = models.IntegerField("Текущий шаг", default = 0)
    capacity = models.IntegerField("Общее количество шагов")
    start_time = models.DateTimeField("Время начала парсинга", auto_now = True)

    def __str__(self) -> str:
        return str(self.start_time)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # noinspection PyUnresolvedReferences
        instances_to_delete = Parsing.objects.order_by("start_time")[settings.PARSING_HISTORY_DEPTH:]
        # noinspection PyUnresolvedReferences
        Parsing.objects.filter(id__in = [x.id for x in instances_to_delete]).delete()


# noinspection PyUnusedLocal
# @receiver(post_save, sender = Parsing)
def remove_old_parsings(*args, **kwargs):
    pass


class Domain(ProjectModel):
    name = models.CharField("Домен", max_length = 254)
    # noinspection PyUnresolvedReferences,PyProtectedMember
    parsing = models.ForeignKey(
        Parsing, on_delete = models.CASCADE, verbose_name = Parsing._meta.get_field("start_time").verbose_name
    )
    average_position = models.IntegerField("Средняя позиция")
    requests_top_10 = models.IntegerField("Запросов в ТОП 10")
    requests_top_3 = models.IntegerField("Запросов в ТОП 3")
    frequency_sum_top_10 = models.IntegerField("Сумма частотности ТОП 10")
    frequency_sum_top_3 = models.IntegerField("Сумма частотности ТОП 3")


class DomainsParsingList(ProjectModel):
    class Meta:
        verbose_name_plural = "Domains Parsing List"

    domains = models.TextField("Домены для парсинга")

    def save(self, *args, **kwargs):
        self.id = 0
        super().save(*args, **kwargs)


# noinspection PyUnusedLocal
@receiver(post_save, sender = DomainsParsingList)
def run_parsing(*args, **kwargs):
    Runner().run_from_code([])
