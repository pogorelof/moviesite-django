from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    #как будет отображаться название приложения
    verbose_name = 'Фильмы'


