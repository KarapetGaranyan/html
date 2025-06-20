from django.contrib import admin
from django.urls import path
from bot.views import register_user, get_user_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register_user),
    path('api/user/<int:user_id>/', get_user_info),  # Новый URL
]