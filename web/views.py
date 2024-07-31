from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UsuarioUpdateForm,UsuarioForm,LoginForm,PropiedadForm,ImagenForm
from .forms import ImagenFormSet,PropiedadUpdateForm, ImagenUpdateFormSet,PropiedadFilterForm
from .models import Usuario,Comuna,Region,Propiedad,ImagenPropiedad,Direccion
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from django.core.paginator import Paginator


# Create your views here.

def index(request):
    return render(request, 'base.html')

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Redireccionar a algún lugar después del registro exitoso
            return redirect('index')
    else:
        form = UsuarioForm()
    
    context = {
        'form': form,
    }
    return render(request, 'registrar.html', context)

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('perfil')  # Cambia 'home' por el nombre de tu URL de página principal
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def perfil(request):
    usuario = request.user
    return render(request, 'perfil.html', {'usuario': usuario})


@login_required
def modificar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige al perfil después de guardar los cambios
    else:
        form = UsuarioUpdateForm(instance=usuario)
    return render(request, 'modificar_perfil.html', {'form': form})

def formulario_view(request):
    regions = Region.objects.all()
    return render(request, 'form.html', {'regions': regions})

def obtener_comunas(request):
    region_id = request.GET.get('region_id')
    print("Region ID:", region_id)
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'nombre')
    print("Comunas:", list(comunas))
    return JsonResponse(list(comunas), safe=False)

@login_required
def agregar_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        formset = ImagenFormSet(request.POST, request.FILES)
        
        print("Form is valid:", form.is_valid())
        print("Form errors:", form.errors)
        print("Formset is valid:", formset.is_valid())
        print("Formset errors:", formset.errors)

        if form.is_valid() and formset.is_valid():
            propiedad = form.save(commit=False)
            propiedad.arrendador = request.user
            propiedad.save()
            print("Propiedad saved:", propiedad)

            # Guardar la dirección
            direccion = Direccion.objects.create(
                comuna=form.cleaned_data['comuna'],
                calle=form.cleaned_data['direccion_calle'],
                numero=form.cleaned_data['direccion_numero'],
                punto_referencia=form.cleaned_data.get('direccion_punto_referencia', '')
            )
            propiedad.direccion = direccion
            propiedad.save()

            # Guardar las imágenes
            for imagen_form in formset:
                if imagen_form.is_valid() and imagen_form.cleaned_data:
                    imagen = imagen_form.cleaned_data.get('imagen')
                    descripcion = imagen_form.cleaned_data.get('descripcion', '')
                    if imagen:  # Verificar si la imagen está presente
                        ImagenPropiedad.objects.create(
                            propiedad=propiedad,
                            imagen=imagen,
                            descripcion=descripcion
                        )
            
            return redirect('listar')
    else:
        form = PropiedadForm()
        formset = ImagenFormSet()

    return render(request, 'propiedad/agregar.html', {'form': form, 'formset': formset})


@login_required
def editar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id, arrendador=request.user)
    
    if request.method == 'POST':
        form = PropiedadUpdateForm(request.POST, request.FILES, instance=propiedad, user=request.user)
        formset = ImagenUpdateFormSet(request.POST, request.FILES, instance=propiedad)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('detalle_propiedad', propiedad_id=propiedad.id)
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = PropiedadUpdateForm(instance=propiedad, user=request.user)
        formset = ImagenUpdateFormSet(instance=propiedad)
    context = {
        'form': form,
        'formset': formset,
        'propiedad': propiedad,
    }
    
    return render(request, 'propiedad/actualizar.html',context )

@login_required
def borrar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    
    # Verifica que el usuario sea el propietario de la propiedad
    if propiedad.arrendador != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar esta propiedad.")
    
    if request.method == 'POST':
        propiedad.delete()
        return redirect('listar_propiedad')

    return render(request, 'propiedad/eliminar.html', {'propiedad': propiedad})

@login_required
def listar_propiedades_usuario(request):
    # Obtener el usuario que está actualmente logeado
    usuario = request.user
    
    # Filtrar las propiedades del usuario logeado
    propiedades = Propiedad.objects.filter(arrendador=usuario)
    
    # Configurar el paginador
    paginator = Paginator(propiedades, 9)  # Mostrar 10 propiedades por página
    total_propiedades = propiedades.count()
    # Obtener la página actual
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        
        'page_obj': page_obj,
        'total_propiedades': total_propiedades  # Agrega el conteo al contexto
    }
    # Pasar el objeto de la página al contexto
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

    # Contar el número total de propiedades después de aplicar los filtros
    total_propiedades = propiedades.count()

    # Paginación
    paginator = Paginator(propiedades, 8)  # Muestra 9 propiedades por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'total_propiedades': total_propiedades  # Agrega el conteo al contexto
    }
    return render(request, 'propiedad/listar_propiedades.html', context)