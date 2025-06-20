from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import TelegramUser


@api_view(['GET'])
def get_user_info(request, telegram_id):
    """
    Получение информации о пользователе по Telegram ID
    """
    try:
        user = TelegramUser.objects.get(telegram_id=telegram_id)
        return Response({
            'success': True,
            'user': user.to_dict()
        }, status=status.HTTP_200_OK)

    except TelegramUser.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Пользователь не найден',
            'message': 'Пользователь с указанным Telegram ID не зарегистрирован в системе'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'success': False,
            'error': 'Внутренняя ошибка сервера',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def register_user(request):
    """
    Регистрация нового пользователя
    """
    try:
        data = request.data
        telegram_id = data.get('telegram_id')

        if not telegram_id:
            return Response({
                'success': False,
                'error': 'Отсутствует Telegram ID'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли пользователь
        user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': data.get('username'),
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
            }
        )

        if created:
            return Response({
                'success': True,
                'message': 'Пользователь успешно зарегистрирован',
                'user': user.to_dict()
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': True,
                'message': 'Пользователь уже существует',
                'user': user.to_dict()
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'success': False,
            'error': 'Ошибка при регистрации',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def health_check(request):
    """
    Проверка работоспособности API
    """
    return Response({
        'status': 'OK',
        'message': 'API работает корректно'
    })