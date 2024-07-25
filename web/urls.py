
from django.urls import path,include
from .views import index,registro,perfil,modificar_perfil,get_comunas,formulario_view

urlpatterns = [
   
    path("", index, name= 'index'),
    path('registro/', registro, name='registro'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/modificar/', modificar_perfil, name='modificar_perfil'),
    path('formulario/', formulario_view, name='formulario'),
    path('get_comunas/', get_comunas, name='get_comunas'),
    path('accounts/', include('django.contrib.auth.urls')),
   
    
]
