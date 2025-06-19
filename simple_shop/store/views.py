# store/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login # Added login import
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .models import Product
from .forms import ProductForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in directly after signup
            return redirect('product_list') # Redirect to product list or home
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

# We will use Django's built-in LoginView and LogoutView,
# but we might need to customize them later via URLs or settings.

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
