from django.contrib import admin
from .models import Usuario

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'es_admin', 'is_staff')
    list_filter = ('es_admin', 'is_staff')
