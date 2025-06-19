from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Пользовательский бэкенд аутентификации, который позволяет пользователям
    входить в систему используя либо email, либо имя пользователя
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')

        if username is None or password is None:
            return None

        try:
            # Попытка найти пользователя по email или username
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            # Запускаем дефолтный hasher, чтобы избежать timing attacks
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # В случае нескольких пользователей с одинаковым username/email
            # берем первого найденного
            user = User.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()

        # Проверяем пароль и активность пользователя
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def get_user(self, user_id):
        """
        Получение пользователя по ID
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None