from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_sin_decimales', 'photo_url')

    @admin.display(description='Precio')
    def precio_sin_decimales(self, obj):
        return str(round(obj.price))

