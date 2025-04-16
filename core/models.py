from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

# Create your models here.
class USER(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    born_date = models.DateField()
    adress = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return self.correo
    
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
        return self.nombre_juego
    