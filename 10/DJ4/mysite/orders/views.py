from django.shortcuts import render

# Create your views here.
def login(request):
    return HttpResponse('login')

def register(request):
    return HttpResponse('register')