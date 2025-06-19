# films/apps.py
from django.apps import AppConfig

class FilmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'films'
    verbose_name = 'Фильмы'