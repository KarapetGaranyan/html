from django.http import HttpResponse
# Create your views here.
def login(request):
    return HttpResponse('login')

def register(request):
    return HttpResponse('register')