from django.contrib import admin
from django.urls import path
from bot.views import register_user

urlpatterns = [
    path('admin/', admin.site.urls),
]