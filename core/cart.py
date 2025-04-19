# store/cart.py
from decimal import Decimal
from django.conf import settings
from core.models import GAME
from django.shortcuts import redirect
from django.contrib import messages

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, game, quantity=1, override_quantity=False):
        game_cod = str(game.cod_game)
        if game_cod in self.cart:
            if override_quantity:
                self.cart[game_cod]['quantity'] = quantity
            else:
                self.cart[game_cod]['quantity'] += quantity
        else:
            self.cart[game_cod] = {'quantity': quantity, 'price': str(game.game_price), 'game': game_cod}
        self.save()

    def remove(self, game):
        game_cod = str(game.cod_game)
        if game_cod in self.cart:
            del self.cart[game_cod]
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        game_ids = self.cart.keys()
        games = GAME.objects.filter(cod_game__in=game_ids)
        for game in games:
            self.cart[str(game.cod_game)]['game'] = game
            yield self.cart[str(game.cod_game)]

    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self, request):
        self.cart.clear()
        self.save()
        messages.success(request, 'Compra exitosa')
        return redirect('cart:summary')
