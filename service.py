from django.contrib import admin


# todo: copy to parsing_helper
def register_models(base_admin_class: type = None, base_model_class: type = None, exclude: list[type] = None):
    if exclude is None:
        exclude = []
    models_with_admin_page = [x for x in base_admin_class.__subclasses__() if x not in exclude]

    for admin_model in [x for x in models_with_admin_page if x not in exclude]:
        admin.site.register(admin_model.model, admin_model)

    for model in [x for x in base_model_class.__subclasses__()
                  if x not in exclude and x not in [y.model for y in models_with_admin_page]]:
        if "Model" not in model.__name__:
            admin.site.register(model)
