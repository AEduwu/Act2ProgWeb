from django.db import models

# Create your models here.
class Usuario(models.Model):
    correo = models.EmailField(primary_key=True)
    contrasenya = models.CharField(max_length=128)
    nombre_completo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    direccion_despacho = models.CharField(max_length=200, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return self.nombre_completo
    
class Categoria(models.Model):
    cod_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Juego(models.Model):
    codjuego = models.AutoField(primary_key=True)
    nombre_juego = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    caratula = models.ImageField(upload_to='caratulas/', blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_juego