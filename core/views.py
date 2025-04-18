from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import USER
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.models import GAME
from core.cart import Cart
from django.shortcuts import render, get_object_or_404, redirect
from .models import GAME, CATEGORY
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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

@csrf_exempt
def profile(request):
    if 'usuario' not in request.session:
        return render(request, 'login.html', {'error': 'Debes iniciar sesión'})

    usuario = USER.objects.get(email=request.session['usuario'])
    user_rol = request.session.get('user_rol', None)
    return render(request, 'profile.html', {'user': usuario, 'user_rol': user_rol})

def catalogo(request):
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    return render(request, 'Catalogo.html', {'user_username': user_username, 'user_rol': user_rol})

def carrito(request):
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    return render(request, 'carrito.html', {'user_username': user_username, 'user_rol': user_rol})

def adventure(request):
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    return render(request, 'adventure.html', {'user_username': user_username, 'user_rol': user_rol})

def racing(request):
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    return render(request, 'racing.html', {'user_username': user_username, 'user_rol': user_rol})

def shooter(request):
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    return render(request, 'shooter.html', {'user_username': user_username, 'user_rol': user_rol})

def strategy(request):
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    return render(request, 'strategy.html', {'user_username': user_username, 'user_rol': user_rol})

def terror(request):
    user_username = request.session.get('user_username', None)
    user_rol = request.session.get('user_rol', None)
    return render(request, 'terror.html', {'user_username': user_username, 'user_rol': user_rol})

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

def close_session(request):
    request.session.flush()
    return redirect('index')

@require_POST
def cart_add(request, cod_game):
    cart = Cart(request)
    game = get_object_or_404(GAME, cod_game=cod_game)
    cart.add(game=game, quantity=1, override_quantity=False)
    return redirect('cart_detail')

@require_POST
def cart_remove(request, cod_game):
    cart = Cart(request)
    game = get_object_or_404(GAME, cod_game=cod_game)
    cart.remove(game)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        'subtotal': cart.get_subtotal(),
        'shipping': Decimal('5000'),
        'discount': Decimal('0'),
    }
    context['total'] = context['subtotal'] + context['shipping'] - context['discount']
    return render(request, 'store/cart_detail.html', context)

def gameAdministration(request):
    if 'user_email' not in request.session or request.session.get('user_rol') != 2:
        return redirect('login')
    
    user_username = request.session.get('user_username')
    user_rol = request.session.get('user_rol')
    
    return render(request, 'gameAdministration.html', {
        'user_username': user_username,
        'user_rol': user_rol
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
        return redirect('game_admin')

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
        return redirect('game_admin')

@csrf_exempt
def delete_game(request, cod_game):
    game = get_object_or_404(GAME, pk=cod_game)
    game.delete()
    return redirect('game_admin')