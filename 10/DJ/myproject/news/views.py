# news/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import News_post
from .forms import NewsPostForm


def home(request):
    """Отображение всех новостей"""
    news = News_post.objects.all().order_by('-pub_date')
    return render(request, 'news/news.html', {'news': news})


def create_news(request):
    """Создание новой новости"""
    if request.method == 'POST':
        form = NewsPostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно добавлена!')
            return redirect('news_home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = NewsPostForm()

    return render(request, 'news/add_new_post.html', {'form': form})