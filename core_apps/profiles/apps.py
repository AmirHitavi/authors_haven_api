from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.profiles"

    def ready(self):
        from core_apps.profiles import signals
