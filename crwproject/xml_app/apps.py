from django.apps import AppConfig


class XmlAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crwproject.xml_app'

    def ready(self):
        import crwproject.xml_app.signals
