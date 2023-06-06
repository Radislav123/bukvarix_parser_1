from django.db import models


class ProjectModel(models.Model):
    class Meta:
        abstract = True


class Parsing(ProjectModel):
    current = models.IntegerField("Текущий шаг парсинга")
    all = models.IntegerField("Общее количество шагов парсинга")
    start_time = models.DateTimeField("Время начала парсинга", auto_now = True)

    def __str__(self) -> str:
        return str(self.start_time)


class Domain(ProjectModel):
    name = models.CharField("Домен", primary_key = True)
    average_position = models.IntegerField("Средняя позиция")
    requests_top_10 = models.IntegerField("Запросов в ТОП 10")
    requests_top_3 = models.IntegerField("Запросов в ТОП 3")
    frequency_sum_top_10 = models.IntegerField("Сумма частотности ТОП 10")
    frequency_sum_top_3 = models.IntegerField("Сумма частотности ТОП 3")
