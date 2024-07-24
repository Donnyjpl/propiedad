from .models import Usuario
from django import forms

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono_personal', 'tipo_usuario', 'direccion']