from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('user/<int:telegram_id>/', views.get_user_info, name='get_user_info'),
    path('register/', views.register_user, name='register_user'),
    path('health/', views.health_check, name='health_check'),
]