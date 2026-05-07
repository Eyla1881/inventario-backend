from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Producto.
    Permite visualizar, buscar y filtrar productos desde /admin/
    """
    list_display = ('name', 'price', 'stock') # Columnas a mostrar
    search_fields = ('name',)                 # Barra de búsqueda por nombre
    list_filter = ('price',)                  # Filtro lateral por precio
