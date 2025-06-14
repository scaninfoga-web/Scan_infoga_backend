from django.apps import AppConfig


class LeakDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leak_data'
    
    def ready(self):
        from . import utils
        utils.initialize_dynamodb_clients()