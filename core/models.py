from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

# Create your models here.
class USER(models.Model):
    ROL_CHOICES = (
        (1, 'Usuario'),
        (2, 'Administrador'),
    )

    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    born_date = models.DateField()
    adress = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    rol = models.IntegerField(choices=ROL_CHOICES, default=1)

    def __str__(self):
        return self.email
    
class CATEGORY(models.Model):
    cod_category = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class GAME(models.Model):
    cod_game = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=100)
    game_description = models.TextField()
    game_price = models.IntegerField()
    game_picture = models.ImageField(upload_to='caratulas/', blank=False, null=False)
    cod_category = models.ForeignKey(CATEGORY, on_delete=models.CASCADE)

    def __str__(self):
        return self.game_name   
    
class MEDIO_PAGO(models.Model):
    cod_medio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class BOLETA(models.Model):
    cod_boleta = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()
    user = models.ForeignKey('USER', on_delete=models.CASCADE)
    medio_pago = models.ForeignKey('MEDIO_PAGO', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Boleta #{self.cod_boleta} - {self.user.email}'

class DETALLE_BOLETA(models.Model):
    boleta = models.ForeignKey('BOLETA', on_delete=models.CASCADE, related_name='detalles')
    game = models.ForeignKey('GAME', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    subtotal = models.IntegerField()

    def __str__(self):
        return f'{self.cantidad} x {self.game.game_name} (Boleta #{self.boleta.cod_boleta})'