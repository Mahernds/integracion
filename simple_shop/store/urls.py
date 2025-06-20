# store/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='product_list'), name='logout'),
    path('add_product/', views.add_product, name='add_product'),
    path('bodeguero/', views.bodeguero_dashboard, name='bodeguero_dashboard'),
    path('registrar-compra/', views.registrar_compra, name='registrar_compra'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('carrito/', views.carrito, name='carrito'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),

]
