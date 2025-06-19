# news/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class News_post(models.Model):
    title = models.CharField('Название новости', max_length=200)
    short_description = models.CharField('Краткое описание новости', max_length=300)
    text = models.TextField('Текст новости')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', default=1)
    pub_date = models.DateTimeField('Дата публикации', default=timezone.now)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-pub_date']