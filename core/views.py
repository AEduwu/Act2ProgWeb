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

def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            USER = USER.objects.create(
                nombre=data['nombre'],
                username=data['usuario'],
                correo=data['correo'],
                contrasena=make_password(data['contrasena']),
                fecha_nacimiento=data['fechaNacimiento'],
                direccion=data.get('direccion', '')
            )
            return JsonResponse({'mensaje': 'Usuario registrado correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
