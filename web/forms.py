from django import forms
from .models import Usuario, Region, Comuna, Direccion


class UsuarioUpdateForm(forms.ModelForm):
    direccion_calle = forms.CharField(max_length=255)
    direccion_numero = forms.CharField(max_length=10)
    direccion_punto_referencia = forms.CharField(max_length=255, required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Seleccionar región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), empty_label="Seleccionar comuna")

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'rut', 'email', 'telefono_personal', 'tipo_usuario', 'region', 'comuna']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance:
            # Verificar si la instancia tiene una región definida
            if hasattr(self.instance, 'direccion') and self.instance.direccion and self.instance.direccion.comuna:
                self.fields['direccion_calle'].initial = self.instance.direccion.calle
                self.fields['direccion_numero'].initial = self.instance.direccion.numero
                self.fields['direccion_punto_referencia'].initial = self.instance.direccion.punto_referencia
                self.fields['region'].initial = self.instance.direccion.comuna.region
                self.fields['comuna'].queryset = Comuna.objects.filter(region=self.instance.direccion.comuna.region).order_by('nombre')
            else:
                # Si no hay una región definida para la instancia, dejar el queryset vacío
                self.fields['comuna'].queryset = Comuna.objects.none()
        else:
            # Cuando se está creando un nuevo usuario, se deja el queryset de comuna vacío inicialmente
            self.fields['comuna'].queryset = Comuna.objects.none()

    def save(self, commit=True):
        usuario = super().save(commit=False)
        direccion_calle = self.cleaned_data['direccion_calle']
        direccion_numero = self.cleaned_data['direccion_numero']
        direccion_punto_referencia = self.cleaned_data['direccion_punto_referencia']
        region = self.cleaned_data['region']
        comuna = self.cleaned_data['comuna']

        # Buscar o crear la dirección
        direccion, created = Direccion.objects.get_or_create(
            calle=direccion_calle,
            numero=direccion_numero,
            punto_referencia=direccion_punto_referencia,
            comuna=comuna
        )

        usuario.direccion = direccion

        if commit:
            usuario.save()

        return usuario


class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Seleccionar región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), empty_label="Seleccionar comuna")
    
    class Meta:
        model = Usuario
        fields = ['username', 'rut', 'email', 'telefono_personal', 'region', 'comuna']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'telefono_personal': 'Teléfono',
            'region': 'Región',
            'comuna': 'Comuna',
        }
        error_messages = {
            'username': {
                'unique': 'Ya existe un usuario con ese nombre de usuario. Por favor, elige otro.',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar las regiones disponibles en el formulario
        self.fields['region'].queryset = Region.objects.all()

        # Si hay datos posteados (POST request), filtrar las comunas basadas en la región seleccionada
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # Si hay algún error al intentar obtener el ID de la región, no se filtra nada
        
        # Si ya existe una instancia de usuario (estamos en una actualización), cargar las opciones seleccionadas
        elif self.instance.pk and self.instance.direccion and self.instance.direccion.comuna:
            self.fields['region'].initial = self.instance.direccion.comuna.region
            self.fields['comuna'].queryset = Comuna.objects.filter(region=self.instance.direccion.comuna.region).order_by('nombre')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

            # Asignar la dirección al usuario si existe
            if 'region' in self.cleaned_data and 'comuna' in self.cleaned_data:
                region_id = self.cleaned_data['region'].id
                comuna_id = self.cleaned_data['comuna'].id
                direccion, created = Direccion.objects.get_or_create(
                    comuna_id=comuna_id,
                    defaults={
                        'calle': 'Sin especificar',
                        'numero': 'Sin especificar',
                        'punto_referencia': 'Sin especificar'
                    }
                )
                user.direccion = direccion
                user.save()

        return user

    
class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)