from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nombre', 'price', 'photo_url']

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('user', 'Usuario'),
        ('bodeguero', 'Bodeguero'),
        ('admin', 'Administrador'),
    )
    email = forms.EmailField(label='Correo electrónico', required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rol')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
        labels = {
            'username': 'Nombre de usuario',
        }
        help_texts = {
            'username': '',  # Quita las indicaciones del username
            'email': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: juanperez'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }
