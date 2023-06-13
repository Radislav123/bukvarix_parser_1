from django.contrib import admin


# todo: copy to parsing_helper
def register_models(base_admin_class: type = None, base_model_class: type = None):
    models_with_admin_page = base_admin_class.__subclasses__()

    for admin_model in models_with_admin_page:
        admin.site.register(admin_model.model, admin_model)

    for model in [x for x in base_model_class.__subclasses__() if x not in [y.model for y in models_with_admin_page]]:
        if "Model" not in model.__name__:
            admin.site.register(model)
