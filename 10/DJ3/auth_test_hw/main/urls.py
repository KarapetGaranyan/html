from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'main'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post']), name='logout'),
    path('register/', views.register, name='register'),

    # Профиль пользователя (функция-представление)
    path('profile/', views.profile, name='profile'),

    # Альтернативный профиль с LoginRequiredMixin (класс-представление)
    path('profile-class/', views.ProfileView.as_view(), name='profile_class'),
]