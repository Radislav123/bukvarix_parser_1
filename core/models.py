from django.db import models


class CoreModel(models.Model):
    class Meta:
        abstract = True


class DomainsParsingListModel(CoreModel):
    class Meta:
        abstract = True
        verbose_name_plural = "Domains Parsing List"

    domains = models.TextField("Домены для парсинга")

    def save(self, *args, **kwargs):
        self.id = 0
        super().save(*args, **kwargs)


class Parsing(CoreModel):
    parser_name = models.CharField("Название парсера", max_length = 100)
    current = models.IntegerField("Текущий шаг", default = 0)
    capacity = models.IntegerField("Общее количество шагов")
    start_time = models.DateTimeField("Время начала парсинга", auto_now = True)

    def __str__(self) -> str:
        return str(self.start_time)
