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
