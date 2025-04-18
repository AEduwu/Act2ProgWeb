# store/cart.py
from decimal import Decimal
from django.conf import settings
from core.models import GAME

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, game, quantity=1, override_quantity=False):

        game_id = str(game.cod_game)
        if game_id not in self.cart:
            self.cart[game_id] = {
                'quantity': 0,
                'price': str(game.game_price)
            }
        if override_quantity:
            self.cart[game_id]['quantity'] = quantity
        else:
            self.cart[game_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, game):

        game_id = str(game.cod_game)
        if game_id in self.cart:
            del self.cart[game_id]
            self.save()

    def __iter__(self):

        game_ids = self.cart.keys()
        games = GAME.objects.filter(cod_game__in=game_ids)
        for game in games:
            item = self.cart[str(game.cod_game)]
            item['game'] = game
            item['price'] = Decimal(item['price'])
            item['subtotal'] = item['price'] * item['quantity']
            yield item

    def __len__(self):

        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()