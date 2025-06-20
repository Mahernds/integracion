from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    nombre = models.CharField("Nombre", max_length=200)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    photo_url = models.URLField("URL de la foto", max_length=2000)
    stock = models.PositiveIntegerField("Stock", default=0)
    

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    region = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f'Compra #{self.id} - {self.usuario.username}'

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.producto} x{self.cantidad}'