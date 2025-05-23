from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import USER, GAME, CATEGORY
from .cart import Cart
from decimal import Decimal
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GameSerializer, UserSerializer
import requests
from django.conf import settings


def index(request):
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    return render(request, 'index.html', {'user_username': user_username, 'user_rol': user_rol})

def login(request):
    return render(request, 'login.html')

def registration(request):
    return render(request, 'registration.html')

def forgot_password(request):
    return render(request, 'forgotPassword.html')

def catalogo(request):
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    return render(request, 'Catalogo.html', {'user_username': user_username, 'user_rol': user_rol})

def carrito(request):
    cart = Cart(request)
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    
    context = {
        'user_username': user_username,
        'user_rol': user_rol,
        'cart': cart,
        'subtotal': cart.get_subtotal(),
        'shipping': Decimal('5000'),
        'discount': Decimal('0'),
    }
    
    context['total'] = context['subtotal'] + context['shipping'] - context['discount']
    
    return render(request, 'carrito.html', context)

def adventure(request):
    user_username = request.session.get('user_username')
    user_rol = request.session.get('user_rol')

    juegos_adventure = GAME.objects.filter(cod_category_id=1)

    return render(request, 'adventure.html', {
        'user_username': user_username,
        'user_rol': user_rol,
        'juegos': juegos_adventure,
    })

def racing(request):
    user_username = request.session.get('user_username')
    user_rol = request.session.get('user_rol')

    juegos_racing = GAME.objects.filter(cod_category_id=3)

    return render(request, 'racing.html', {
        'user_username': user_username,
        'user_rol': user_rol,
        'juegos': juegos_racing,
    })

def shooter(request):
    user_username = request.session.get('user_username')
    user_rol = request.session.get('user_rol')

    juegos_shooter = GAME.objects.filter(cod_category_id=2)

    return render(request, 'shooter.html', {
        'user_username': user_username,
        'user_rol': user_rol,
        'juegos': juegos_shooter,
    })

def strategy(request):
    user_username = request.session.get('user_username')
    user_rol = request.session.get('user_rol')

    juegos_strategy = GAME.objects.filter(cod_category_id=5)

    return render(request, 'strategy.html', {
        'user_username': user_username,
        'user_rol': user_rol,
        'juegos': juegos_strategy,
    })

def terror(request):
    user_username = request.session.get('user_username')
    user_rol      = request.session.get('user_rol')

    juegos_terror = GAME.objects.filter(cod_category_id=4)

    return render(request, 'terror.html', {
        'user_username': user_username,
        'user_rol': user_rol,
        'juegos': juegos_terror,
    })

def close_session(request):
    request.session.flush()
    return redirect('index')

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

            rol = data.get('rol', 1)

            user = USER.objects.create(
                name=data['name'],
                username=data['username'],
                email=email,
                password=make_password(data['password']),
                born_date=data['born_date'],
                adress=data.get('adress', ''),
                rol=rol
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
            request.session['user_rol'] = usuario.rol
            return JsonResponse({'mensaje': 'Login exitoso'})
        else:
            return JsonResponse({'error': 'Contraseña incorrecta'}, status=401)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@require_POST
def cart_add(request, cod_game):
    cart = Cart(request)
    game = get_object_or_404(GAME, cod_game=cod_game)
    cart.add(game=game, quantity=1, override_quantity=False)
    return redirect('carrito')

@require_POST
def cart_down(request, cod_game):
    cart = Cart(request)
    game = get_object_or_404(GAME, cod_game=cod_game)
    
    if str(game.cod_game) in cart.cart:
        current_quantity = cart.cart[str(game.cod_game)]['quantity']
        if current_quantity > 1:
            cart.cart[str(game.cod_game)]['quantity'] -= 1
        else:
            cart.remove(game)
    cart.save()
    return redirect('carrito')

@require_POST
def cart_remove(request, cod_game):
    cart = Cart(request)
    game = get_object_or_404(GAME, cod_game=cod_game)
    cart.remove(game)
    return redirect('carrito')

def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        'subtotal': cart.get_subtotal(),
        'shipping': Decimal('5000'),
        'discount': Decimal('0'),
    }
    context['total'] = context['subtotal'] + context['shipping'] - context['discount']
    return render(request, 'carrito.html', context)


def gameAdministration(request):
    if 'user_email' not in request.session or request.session.get('user_rol') != 2:
        return redirect('login')
    
    user_username = request.session.get('user_username')
    user_rol = request.session.get('user_rol')

    juegos = GAME.objects.all()
    categorias = CATEGORY.objects.all()

    return render(request, 'gameAdministration.html', {
        'user_username': user_username,
        'user_rol': user_rol,
        'game': juegos,
        'categoriy': categorias,
    })

@csrf_exempt
def create_game(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        picture = request.FILES.get('picture')

        category = get_object_or_404(CATEGORY, pk=category_id)

        GAME.objects.create(
            game_name=name,
            game_description=description,
            game_price=price,
            game_picture=picture,
            cod_category=category
        )
        return redirect('index')

@csrf_exempt
def update_game(request, cod_game):
    game = get_object_or_404(GAME, pk=cod_game)

    if request.method == 'POST':
        game.game_name = request.POST.get('name')
        game.game_description = request.POST.get('description')
        game.game_price = request.POST.get('price')
        game.cod_category = get_object_or_404(CATEGORY, pk=request.POST.get('category'))

        if 'picture' in request.FILES:
            game.game_picture = request.FILES['picture']

        game.save()
        return redirect('index')

@csrf_exempt
def delete_game(request, cod_game):
    game = get_object_or_404(GAME, pk=cod_game)
    game.delete()
    return redirect('index')


@csrf_exempt
def recuperar_clave(request):
    if request.method == "POST":
        data = json.loads(request.body)
        correo = data.get('correo', '').strip().lower()
        try:
            usuario = USER.objects.get(email=correo)
        except USER.DoesNotExist:
            return JsonResponse({'error': 'Correo no encontrado'}, status=400)

        uidb64 = urlsafe_base64_encode(force_bytes(usuario.pk))
        reset_url = f'http://127.0.0.1:8000/restablecer/{uidb64}/'

        send_mail(
            'Restablecimiento de contraseña',
            f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}',
            'soporte@todojuegos.com',
            [correo]
        )

        return JsonResponse({'mensaje': 'Correo enviado con instrucciones para restablecer la contraseña'})
    
    return render(request, 'recuperar_clave.html')

@csrf_exempt
def restablecer(request, uidb64):
    try:
        correo = force_str(urlsafe_base64_decode(uidb64))
        usuario = USER.objects.get(email=correo)
    except (TypeError, ValueError, OverflowError, USER.DoesNotExist):
        return render(request, 'restablecer.html', {'error': 'Enlace inválido o expirado.'})

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'restablecer.html', {
                'error': 'Las contraseñas no coinciden.'
            })

        usuario.password = make_password(new_password)
        usuario.save()
        return redirect('login')

    return render(request, 'restablecer.html', {'uidb64': uidb64})

def profile(request):
    if 'user_email' in request.session:
        user_username = request.session.get('user_username')
        user_rol = request.session.get('user_rol')
        usuario = USER.objects.get(email=request.session['user_email'])

        return render(request, 'profile.html', {'user_username': user_username, 'user_rol': user_rol, 'usuario': usuario})
    else:
        return redirect('login')
    
@csrf_exempt
def editar_perfil(request):
    if request.method == 'POST':
        email = request.session.get('user_email')
        if not email:
            return JsonResponse({'error': 'No has iniciado sesión'}, status=403)

        usuario = get_object_or_404(USER, email=email)

        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        nueva_contrasena = request.POST.get('contrasena')
        foto = request.FILES.get('foto')

        if nombre:
            usuario.name = nombre
        if direccion:
            usuario.adress = direccion
        if nueva_contrasena:
            usuario.password = make_password(nueva_contrasena)
        if foto:
            usuario.profile_pic = foto

        usuario.save()
        return redirect('profile')

    return HttpResponseForbidden("Método no permitido")

class GameListAPIView(APIView):
    def get(self, request):
        games = GAME.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListAPIView(APIView):
    def get(self, request):
        users = USER.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def apisImportadas(request):
    juegos = []
    noticias = []

    try:
        url_juegos = f"https://api.rawg.io/api/games?key={settings.RAWG_API_KEY}&page_size=6"
        response_juegos = requests.get(url_juegos)
        if response_juegos.ok:
            juegos = response_juegos.json().get("results", [])
        else:
            print("Error", response_juegos.status_code)
    except Exception as e:
        print("Excepcion", e)

    try:
        url_noticias = f"https://gnews.io/api/v4/search?q=videojuegos&lang=es&token={settings.GNEWS_API_KEY}"
        response_noticias = requests.get(url_noticias)
        if response_noticias.ok:
            noticias = response_noticias.json().get("articles", [])
        else:
            print("Error", response_noticias.status_code)
    except Exception as e:
        print("Excepcion", e)

    return render(request, 'index.html', {
        'juegos': juegos,
        'noticias': noticias,
    })