from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UsuarioUpdateForm,UsuarioForm,LoginForm
from .models import Usuario

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