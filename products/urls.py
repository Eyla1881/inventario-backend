from django.urls import path
from . import views

"""
Archivo de enrutamiento (URLs) específico para la aplicación 'products'.
Aquí conectamos las URLs de la web con las funciones (vistas) que deben ejecutarse.
"""
urlpatterns = [
    # Ruta vacía (''). Significa que al entrar a /products/ se ejecutará product_list
    path('', views.product_list, name='product_list'),
    
    # Ruta 'create/'. Significa que al entrar a /products/create/ se ejecutará create_product
    path('create/', views.create_product, name='create_product'),
]
