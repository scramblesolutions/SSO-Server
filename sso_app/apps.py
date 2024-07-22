from django.apps import AppConfig


class SsoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sso_app'

    def ready(self):
        import sso_app.signals
