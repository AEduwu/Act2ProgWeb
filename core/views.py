from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import USER
from django.contrib.auth.hashers import make_password

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

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']

            if USER.objects.filter(email=email).exists():
                return JsonResponse({'error': 'El correo ya está registrado'}, status=400)
            
            if USER.objects.filter(username=data['username']).exists():
                return JsonResponse({'error': 'El nombre de usuario ya está en uso'}, status=400)

            user = USER.objects.create(
                name=data['name'],
                username=data['username'],
                email=email,
                password=make_password(data['password']),
                born_date=data['born_date'],
                adress=data.get('adress', '')
            )
            return JsonResponse({'mensaje': 'Usuario registrado correctamente'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)