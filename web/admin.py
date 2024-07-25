from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'telefono_personal', 'tipo_usuario']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['tipo_usuario']