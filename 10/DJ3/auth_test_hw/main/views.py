from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    """Главная страница"""
    return render(request, 'main/index.html')

@login_required
def profile(request):
    """Страница профиля (только для авторизованных пользователей)"""
    return render(request, 'main/profile.html')