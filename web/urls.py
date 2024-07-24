
from django.urls import path,include
from .views import index,registro,perfil,modificar_perfil

urlpatterns = [
   
    path("", index, name= 'index'),
    path('registro/', registro, name='registro'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/modificar/', modificar_perfil, name='modificar_perfil'),
    path('accounts/', include('django.contrib.auth.urls')),
   
]
