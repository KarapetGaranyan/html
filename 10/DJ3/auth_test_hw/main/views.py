from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import TemplateView
from django.urls import reverse_lazy


def index(request):
    """Главная страница"""
    return render(request, 'main/index.html')


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан! Теперь вы можете войти в систему.')
            return redirect('main:login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


@login_required
def profile(request):
    """Страница профиля (только для авторизованных пользователей)"""
    return render(request, 'main/profile.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    """Класс-представление для страницы профиля с LoginRequiredMixin"""
    template_name = 'main/profile.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Можно добавить дополнительный контекст если нужно
        context['page_title'] = 'Профиль пользователя'
        return context