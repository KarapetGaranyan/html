from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def data_page(request):
    return HttpResponse("Добро пожаловать на страницу данных! 📊")

def test_page(request):
    return HttpResponse("Тестовая страница! ✅")