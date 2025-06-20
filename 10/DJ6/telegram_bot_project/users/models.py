from django.db import models
from django.utils import timezone

class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Фамилия')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    last_seen = models.DateTimeField(auto_now=True, verbose_name='Последняя активность')

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} (@{self.username})"

    @property
    def full_name(self):
        """Возвращает полное имя пользователя"""
        parts = [self.first_name, self.last_name]
        return ' '.join(part for part in parts if part)

    def to_dict(self):
        """Преобразует объект в словарь для API"""
        return {
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_seen': self.last_seen.isoformat(),
        }