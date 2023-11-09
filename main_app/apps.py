from django.apps import AppConfig


# class MainAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'main_app'

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

    def ready(self):
        import main_app.signals