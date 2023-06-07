from django.contrib.auth import get_user_model

# noinspection PyUnresolvedReferences
import configure_django


user = get_user_model()
if not user.objects.filter(username = "admin").exists():
    user.objects.create_superuser("admin", "", "admin")
