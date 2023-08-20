from django.apps import AppConfig


class RefsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'refs'

    def ready(self):
        import refs.signals
