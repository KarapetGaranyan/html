# myapp/views.py
from django.shortcuts import render

def home(request):
    """Home page view"""
    context = {
        'title': 'Главная страница',
        'content': 'Добро пожаловать на наш сайт!'
    }
    return render(request, 'myapp/home.html', context)

def about(request):
    """About page view"""
    context = {
        'title': 'О нас',
        'content': 'Информация о нашей компании'
    }
    return render(request, 'myapp/about.html', context)

def services(request):
    """Services page view"""
    services_list = [
        'Веб-разработка',
        'Мобильные приложения',
        'SEO оптимизация',
        'Дизайн интерфейсов'
    ]
    context = {
        'title': 'Наши услуги',
        'services': services_list
    }
    return render(request, 'myapp/services.html', context)

def contact(request):
    """Contact page view"""
    context = {
        'title': 'Контакты',
        'phone': '+7 (999) 123-45-67',
        'email': 'info@example.com',
        'address': 'г. Москва, ул. Примерная, д. 123'
    }
    return render(request, 'myapp/contact.html', context)