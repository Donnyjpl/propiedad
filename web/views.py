from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UsuarioUpdateForm

# Create your views here.

def index(request):
    return render(request, 'base.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('perfil')  # Redirige al perfil del usuario después del registro
    else:
        form = UserCreationForm()
    return render(request, 'registrar.html', {'form': form})


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
            return redirect('perfil')  # Redirige al perfil después de la actualización
    else:
        form = UsuarioUpdateForm(instance=usuario)
    return render(request, 'modificar_perfil.html', {'form': form})