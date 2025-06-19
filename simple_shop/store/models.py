from django.db import models

class Product(models.Model):
    nombre = models.CharField("Nombre", max_length=200)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    photo_url = models.URLField("URL de la foto", max_length=2000)

    def __str__(self):
        return self.nombre
