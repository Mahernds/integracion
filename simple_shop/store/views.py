from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User  
from .models import Product, Compra, DetalleCompra
from .forms import ProductForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django import forms
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

@login_required
def bodeguero_dashboard(request):
    if not request.user.is_staff:
        return redirect('product_list')
    if request.method == "POST":
        if "delete_product" in request.POST:
            product_id = request.POST.get("product_id")
            if product_id:
                Product.objects.filter(id=product_id).delete()
        else:
            product_id = request.POST.get("product_id")
            new_stock = request.POST.get("new_stock")
            if product_id and new_stock is not None:
                try:
                    product = Product.objects.get(id=product_id)
                    product.stock = int(new_stock)
                    product.save()
                except (Product.DoesNotExist, ValueError):
                    pass
        return redirect('bodeguero_dashboard')
    products = Product.objects.all()
    return render(request, 'store/bodeguero_dashboard.html', {'products': products})

def carrito(request):
    return render(request, 'store/carrito.html')

@csrf_exempt
def registrar_compra(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        print("Datos recibidos:", data)

        compra = Compra.objects.create(
            usuario=request.user,
            total=data['total'],
            nombre=data['nombre'],
            correo=data['correo'],
            telefono=data['telefono'],
            region=data['region'],
            comuna=data['comuna'],
            direccion=data['direccion'],
        )
        for item in data['items']:
            DetalleCompra.objects.create(
                compra=compra,
                producto=item['nombre'],
                precio=item['precio'],
                cantidad=item['cantidad'],
            )
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)

@login_required
def perfil_usuario(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'store/perfil.html', {'compras': compras})

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('user', 'Usuario'),
        ('bodeguero', 'Bodeguero'),
        ('admin', 'Administrador'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rol')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    users = User.objects.all().order_by('-date_joined')
    mensaje = None
    edit_user = None
    form = CustomUserCreationForm()  # <-- Siempre inicializa el form

    # Eliminar usuario
    if request.method == 'POST' and 'delete_user' in request.POST:
        user_id = request.POST.get('delete_user')
        if user_id:
            try:
                user_to_delete = User.objects.get(id=user_id)
                if not user_to_delete.is_superuser:
                    user_to_delete.delete()
                    mensaje = f'Usuario eliminado correctamente.'
                else:
                    mensaje = 'No puedes eliminar un superusuario.'
            except User.DoesNotExist:
                mensaje = 'Usuario no encontrado.'

    # Editar usuario
    elif request.method == 'POST' and 'edit_user' in request.POST:
        user_id = request.POST.get('edit_user')
        try:
            edit_user = User.objects.get(id=user_id)
            form = CustomUserCreationForm(instance=edit_user)
        except User.DoesNotExist:
            mensaje = 'Usuario no encontrado.'
    # Guardar edición
    elif request.method == 'POST' and 'save_edit' in request.POST:
        user_id = request.POST.get('save_edit')
        try:
            edit_user = User.objects.get(id=user_id)
            form = CustomUserCreationForm(request.POST, instance=edit_user)
            if form.is_valid():
                user = form.save(commit=False)
                role = form.cleaned_data['role']
                if role == 'admin':
                    user.is_staff = True
                    user.is_superuser = True
                elif role == 'bodeguero':
                    user.is_staff = True
                    user.is_superuser = False
                else:
                    user.is_staff = False
                    user.is_superuser = False
                user.save()
                mensaje = f'Usuario "{user.username}" editado correctamente.'
                edit_user = None
                form = CustomUserCreationForm()
        except User.DoesNotExist:
            mensaje = 'Usuario no encontrado.'
    # Crear usuario nuevo
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            elif role == 'bodeguero':
                user.is_staff = True
                user.is_superuser = False
            else:
                user.is_staff = False
                user.is_superuser = False
            user.save()
            mensaje = f'Usuario "{user.username}" creado correctamente como {role}.'
            form = CustomUserCreationForm()  # Limpiar el formulario

    return render(request, 'store/admin_panel.html', {
        'users': users,
        'form': form,
        'mensaje': mensaje,
        'edit_user': edit_user,
    })