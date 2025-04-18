from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import USER
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.
def index(request):
    user_username = request.session.get('user_username', None)
    return render(request, 'index.html', {'user_username': user_username})

def login(request):
    return render(request, 'login.html')

def registration(request):
    return render(request, 'registration.html')

def forgot_password(request):
    return render(request, 'forgotPassword.html')

@login_required
def profile(request):
    if 'usuario' not in request.session:
        return render(request, 'login.html', {'error': 'Debes iniciar sesión'})

    usuario = USER.objects.get(email=request.session['usuario'])
    return render(request, 'profile.html', {'user': usuario})

def catalogo(request):
    user_username = request.session.get('user_username', None)
    return render(request, 'Catalogo.html', {'user_username': user_username})

def carrito(request):
    user_username = request.session.get('user_username', None)
    return render(request, 'carrito.html', {'user_username': user_username})

def adventure(request):
    user_username = request.session.get('user_username', None)
    return render(request, 'adventure.html', {'user_username': user_username})

def racing(request):
    user_username = request.session.get('user_username', None)
    return render(request, 'racing.html', {'user_username': user_username})

def shooter(request):
    user_username = request.session.get('user_username', None)
    return render(request, 'shooter.html', {'user_username': user_username})

def strategy(request):
    user_username = request.session.get('user_username', None)
    return render(request, 'strategy.html', {'user_username': user_username})

def terror(request):
    user_username = request.session.get('user_username', None)
    return render(request, 'terror.html', {'user_username': user_username})

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

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('correo')
        password = data.get('clave')

        try:
            usuario = USER.objects.get(email=email)
        except USER.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        if check_password(password, usuario.password):
            request.session['user_email'] = usuario.email
            request.session['user_username'] = usuario.username
            return JsonResponse({'mensaje': 'Login exitoso'})
        else:
            return JsonResponse({'error': 'Contraseña incorrecta'}, status=401)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def close_session(request):
    request.session.flush()
    return redirect('index')