from django.db import models

from core import models as core_models


class WebArchiveModel(core_models.CoreModel):
    class Meta:
        abstract = True


class Snapshot(WebArchiveModel):
    parsing = models.ForeignKey(core_models.Parsing, on_delete = models.CASCADE)
    domain = models.CharField("Домен", max_length = 256)
    title = models.TextField("Содержимое тега <title>", null = True)
    url = models.URLField("Ссылка на снимок")


class DomainsParsingList(core_models.DomainsParsingListModel):
    pass
