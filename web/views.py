from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from .forms import UsuarioUpdateForm, UsuarioForm, LoginForm, PropiedadForm, ImagenForm, PropiedadFilterForm
from .models import Usuario, Comuna, Region, Propiedad, ImagenPropiedad, Direccion

# Definición de un conjunto de formularios para las imágenes de la propiedad
ImagenFormSet = inlineformset_factory(Propiedad, ImagenPropiedad, fields=['imagen', 'descripcion'], extra=5, can_delete=True)

def index(request):
    return render(request, 'base.html')

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('index')
    else:
        form = UsuarioForm()
    
    return render(request, 'registrar.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('perfil')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def perfil(request):
    return render(request, 'perfil.html', {'usuario': request.user})

@login_required
def modificar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        form = UsuarioUpdateForm(instance=usuario)
    
    return render(request, 'modificar_perfil.html', {'form': form})

def formulario_view(request):
    regions = Region.objects.all()
    return render(request, 'form.html', {'regions': regions})

def obtener_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'nombre')
    return JsonResponse(list(comunas), safe=False)

@login_required
def agregar_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        formset = ImagenFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            propiedad = form.save(commit=False)
            propiedad.arrendador = request.user
            propiedad.save()

            # Crear y guardar la dirección
            direccion = Direccion.objects.create(
                comuna=form.cleaned_data['comuna'],
                calle=form.cleaned_data['direccion_calle'],
                numero=form.cleaned_data['direccion_numero'],
                punto_referencia=form.cleaned_data.get('direccion_punto_referencia', '')
            )

            # Asociar la dirección con la propiedad
            propiedad.direccion = direccion
            propiedad.save()

            # Guardar las imágenes
            for imagen_form in formset:
                if imagen_form.cleaned_data.get('imagen'):
                    ImagenPropiedad.objects.create(
                        propiedad=propiedad,
                        imagen=imagen_form.cleaned_data['imagen'],
                        descripcion=imagen_form.cleaned_data.get('descripcion', '')
                    )

            messages.success(request, 'Propiedad agregada exitosamente.')
            return redirect('listar')
    else:
        form = PropiedadForm()
        formset = ImagenFormSet()

    return render(request, 'propiedad/agregar.html', {'form': form, 'formset': formset})


class PropiedadUpdateView(UpdateView):
    model = Propiedad
    form_class = PropiedadForm
    template_name = 'propiedad/actualizar.html'
    success_url = reverse_lazy('listar')

    def get_object(self, queryset=None):
        return get_object_or_404(Propiedad, id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ImagenFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['formset'] = ImagenFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Propiedad actualizada exitosamente.')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

@login_required
def borrar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    
    if propiedad.arrendador != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar esta propiedad.")
    
    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, 'Propiedad eliminada exitosamente.')
        return redirect('listar')

    return render(request, 'propiedad/eliminar.html', {'propiedad': propiedad})

@login_required
def listar_propiedades_usuario(request):
    usuario = request.user
    propiedades = Propiedad.objects.filter(arrendador=usuario)
    paginator = Paginator(propiedades, 9)  # Muestra 9 propiedades por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_propiedades': propiedades.count()
    }
    return render(request, 'propiedad/listar.html', context)

def detalle_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, pk=propiedad_id)
    imagenes = ImagenPropiedad.objects.filter(propiedad=propiedad)
    return render(request, 'propiedad/detalle_propiedad.html', {'propiedad': propiedad, 'imagenes': imagenes})

def listar_propiedades(request):
    form = PropiedadFilterForm(request.GET or None)
    propiedades = Propiedad.objects.all()

    if form.is_valid():
        if form.cleaned_data['region']:
            propiedades = propiedades.filter(direccion__comuna__region=form.cleaned_data['region'])
        if form.cleaned_data['comuna']:
            propiedades = propiedades.filter(direccion__comuna=form.cleaned_data['comuna'])
        if form.cleaned_data['tipo_propiedad']:
            propiedades = propiedades.filter(tipo_propiedad=form.cleaned_data['tipo_propiedad'])
        if form.cleaned_data['precio_min']:
            propiedades = propiedades.filter(precio_mensual__gte=form.cleaned_data['precio_min'])
        if form.cleaned_data['precio_max']:
            propiedades = propiedades.filter(precio_mensual__lte=form.cleaned_data['precio_max'])
        if form.cleaned_data['m2_terreno_min']:
            propiedades = propiedades.filter(m2_terreno__gte=form.cleaned_data['m2_terreno_min'])
        if form.cleaned_data['m2_terreno_max']:
            propiedades = propiedades.filter(m2_terreno__lte=form.cleaned_data['m2_terreno_max'])

    total_propiedades = propiedades.count()
    paginator = Paginator(propiedades, 8)  # Muestra 8 propiedades por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'total_propiedades': total_propiedades
    }
    return render(request, 'propiedad/listar_propiedades.html', context)
