from django.contrib import admin

from . import models


class ProjectAdmin(admin.ModelAdmin):
    model: models.ProjectModel


class ParsingAdmin(ProjectAdmin):
    model = models.Parsing
    list_display = ("start_time", "current", "all")


def register_models():
    models_with_admin_page = ProjectAdmin.__subclasses__()

    for admin_model in models_with_admin_page:
        admin.site.register(admin_model.model, admin_model)

    for model in [x for x in models.ProjectModel.__subclasses__() if
                  x not in [y.model for y in models_with_admin_page]]:
        admin.site.register(model)


register_models()
