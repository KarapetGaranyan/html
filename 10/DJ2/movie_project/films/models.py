# films/models.py
from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название фильма')
    description = models.TextField(verbose_name='Описание фильма')
    review = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title