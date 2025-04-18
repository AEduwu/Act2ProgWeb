from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.models import CATEGORY
        categorias = ['Adventure', 'Shooter', 'Racing', 'Terror', 'Strategy']
        for nombre in categorias:
            CATEGORY.objects.get_or_create(nombre=nombre)