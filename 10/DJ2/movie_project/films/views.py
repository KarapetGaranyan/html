# films/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Film
from .forms import FilmForm


def add_film(request):
    """Представление для добавления фильма"""
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фильм успешно добавлен!')
            return redirect('film_list')
    else:
        form = FilmForm()

    return render(request, 'films/add_film.html', {'form': form})


def film_list(request):
    """Представление для отображения списка фильмов"""
    films = Film.objects.all()
    return render(request, 'films/film_list.html', {'films': films})


# films/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.film_list, name='film_list'),
    path('add/', views.add_film, name='add_film'),
]