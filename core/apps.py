from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Application principale'
    
    def ready(self):
        import core.signals  # Import des signaux
