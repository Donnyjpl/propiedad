from django import forms
from .models import Usuario, Region, Comuna, Direccion,Propiedad,ImagenPropiedad,TipoPropiedad
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory
from django.forms import inlineformset_factory

class UsuarioUpdateForm(forms.ModelForm):
    direccion_calle = forms.CharField(max_length=255)
    direccion_numero = forms.CharField(max_length=10)
    direccion_punto_referencia = forms.CharField(max_length=255, required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Seleccionar región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), empty_label="Seleccionar comuna")

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'rut', 'email', 'telefono_personal', 'tipo_usuario', 'region', 'comuna']
        labels = {
            'first_name':'Nombre',
            'last_name': 'Apellido',
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'telefono_personal': 'Teléfono',
            'region': 'Región',
            'comuna': 'Comuna',
        }

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
        fields = ['first_name', 'last_name','username', 'rut', 'email', 'telefono_personal', 'region', 'comuna']
        labels = {
            'first_name':'Nombre',
            'last_name': 'Apellido',
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
                        'numero': '10',
                        'punto_referencia': 'Sin especificar'
                    }
                )
                user.direccion = direccion
                user.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )



class ImagenForm(forms.ModelForm):
    class Meta:
        model = ImagenPropiedad
        fields = ['imagen', 'descripcion']
        
        
        
        # Define el formset fuera del formulario
ImagenFormSet = formset_factory(ImagenForm, extra=5)  # Permitir hasta 5 imágenes

class PropiedadForm(forms.ModelForm):
    # Campos para la dirección
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Seleccionar región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), empty_label="Seleccionar comuna")
    direccion_calle = forms.CharField(max_length=255)
    direccion_numero = forms.CharField(max_length=10)
    direccion_punto_referencia = forms.CharField(max_length=255, required=False)
    imagen_formset = ImagenFormSet()  # Instanciamos el formset aquí
    
    class Meta:
        model = Propiedad
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_terreno', 'num_estacionamientos', 
                  'num_habitaciones', 'num_banos', 'tipo_propiedad', 'precio_mensual', 'region', 'comuna']
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'm2_construidos': 'Metros Construidos',
            'm2_terreno': 'Metros de Terreno',
            'num_estacionamientos': 'Número de Estacionamientos',
            'num_habitaciones': 'Número de Habitaciones',
            'num_banos': 'Número de Baños',
            'tipo_propiedad': 'Tipo de Propiedad',
            'precio_mensual': 'Precio Mensual',
            'region': 'Región',
            'comuna': 'Comuna',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user  # Guardamos el usuario

        # Filtrar las comunas basadas en la región seleccionada si hay datos en la solicitud POST
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['comuna'].queryset = Comuna.objects.none()
        elif self.instance and self.instance.pk and self.instance.direccion and self.instance.direccion.comuna:
            self.fields['region'].initial = self.instance.direccion.comuna.region
            self.fields['comuna'].queryset = Comuna.objects.filter(region=self.instance.direccion.comuna.region).order_by('nombre')

    def save(self, commit=True):
        propiedad = super().save(commit=False)

        if self.user:
            propiedad.arrendador = self.user

        if commit:
            propiedad.save()

            # Crear una nueva dirección
            direccion = Direccion.objects.create(
                comuna=self.cleaned_data['comuna'],
                calle=self.cleaned_data['direccion_calle'],
                numero=self.cleaned_data['direccion_numero'],
                punto_referencia=self.cleaned_data['direccion_punto_referencia']
            )

            # Asociar la nueva dirección a la propiedad
            propiedad.direccion = direccion
            propiedad.save()

            # Guardar imágenes si se han proporcionado
            imagen_formset = self.imagen_formset
            if imagen_formset:
                for form in imagen_formset:
                    if form.is_valid() and form.cleaned_data:
                        imagen = form.cleaned_data.get('imagen')
                        descripcion = form.cleaned_data.get('descripcion', '')
                        if imagen:
                            ImagenPropiedad.objects.create(
                                propiedad=propiedad,
                                imagen=imagen,
                                descripcion=descripcion
                            )
        return propiedad
    
    
class ImagenUpdateForm(forms.ModelForm):
    class Meta:
        model = ImagenPropiedad
        fields = ['imagen', 'descripcion']

ImagenUpdateFormSet = inlineformset_factory(
    Propiedad, ImagenPropiedad, form=ImagenUpdateForm, extra=5, can_delete=True
)

class PropiedadUpdateForm(forms.ModelForm):
    # Campos para la dirección
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Seleccionar región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), empty_label="Seleccionar comuna")
    direccion_calle = forms.CharField(max_length=255)
    direccion_numero = forms.CharField(max_length=10)
    direccion_punto_referencia = forms.CharField(max_length=255, required=False)
    
    class Meta:
        model = Propiedad
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_terreno', 'num_estacionamientos',
                  'num_habitaciones', 'num_banos', 'tipo_propiedad', 'precio_mensual', 'region', 'comuna']
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'm2_construidos': 'Metros Construidos',
            'm2_terreno': 'Metros de Terreno',
            'num_estacionamientos': 'Número de Estacionamientos',
            'num_habitaciones': 'Número de Habitaciones',
            'num_banos': 'Número de Baños',
            'tipo_propiedad': 'Tipo de Propiedad',
            'precio_mensual': 'Precio Mensual',
            'region': 'Región',
            'comuna': 'Comuna',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        propiedad_instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        self.user = user  # Guardamos el usuario

        # Cargar las regiones disponibles en el formulario
        self.fields['region'].queryset = Region.objects.all()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass

        elif propiedad_instance and propiedad_instance.direccion and propiedad_instance.direccion.comuna:
            self.fields['region'].initial = propiedad_instance.direccion.comuna.region
            self.fields['comuna'].queryset = Comuna.objects.filter(region=propiedad_instance.direccion.comuna.region).order_by('nombre')

        # Inicializar el formset con las imágenes existentes si hay una instancia de propiedad
        if propiedad_instance:
            self.imagen_formset = ImagenUpdateFormSet(instance=propiedad_instance)
        else:
            self.imagen_formset = ImagenUpdateFormSet()

    def save(self, commit=True):
        propiedad = super().save(commit=False)

        # Asegurarse de que arrendador se asigna correctamente
        if self.user:
            propiedad.arrendador = self.user

        if commit:
            propiedad.save()

            # Crear o obtener la dirección
            comuna = self.cleaned_data['comuna']
            direccion, created = Direccion.objects.get_or_create(
                comuna=comuna,
                calle=self.cleaned_data['direccion_calle'],
                numero=self.cleaned_data['direccion_numero'],
                punto_referencia=self.cleaned_data['direccion_punto_referencia']
            )
            propiedad.direccion = direccion
            propiedad.save()

            # Guardar imágenes si se han proporcionado
            for form in self.imagen_formset:
                if form.is_valid() and form.cleaned_data:
                    imagen = form.cleaned_data['imagen']
                    descripcion = form.cleaned_data.get('descripcion', '')
                    ImagenPropiedad.objects.create(
                        propiedad=propiedad,
                        imagen=imagen,
                        descripcion=descripcion
                    )
        return propiedad

class PropiedadFilterForm(forms.Form):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, empty_label="Seleccionar región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), required=False, empty_label="Seleccionar comuna")
    tipo_propiedad = forms.ModelChoiceField(queryset=TipoPropiedad.objects.all(), required=False, empty_label="Seleccionar tipo de propiedad")
    precio_min = forms.DecimalField(required=False, decimal_places=2, max_digits=10)
    precio_max = forms.DecimalField(required=False, decimal_places=2, max_digits=10)
    m2_terreno_min = forms.DecimalField(required=False, decimal_places=2, max_digits=10)
    m2_terreno_max = forms.DecimalField(required=False, decimal_places=2, max_digits=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass