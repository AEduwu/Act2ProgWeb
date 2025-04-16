from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def registration(request):
    return render(request, 'registration.html')

def forgot_password(request):
    return render(request, 'forgotPassword.html')

def profile(request):
    return render(request, 'profile.html')

def catalogo(request):
    return render(request, 'Catalogo.html')

def carrito(request):
    return render(request, 'carrito.html')

def adventure(request):
    return render(request, 'adventure.html')

def racing(request):
    return render(request, 'racing.html')

def shooter(request):
    return render(request, 'shooter.html')

def strategy(request):
    return render(request, 'strategy.html')

def terror(request):
    return render(request, 'terror.html')