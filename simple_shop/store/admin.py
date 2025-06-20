from django.contrib import admin
from .models import Product, Compra, DetalleCompra




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'price', 'photo_url')

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total', 'nombre', 'correo')
    search_fields = ('usuario__username', 'nombre', 'correo')
    list_filter = ('fecha', 'region', 'comuna')

@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('compra', 'producto', 'precio', 'cantidad')
    search_fields = ('producto',)
    list_filter = ('compra',)