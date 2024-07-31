from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import index,registro,perfil,modificar_perfil,obtener_comunas,formulario_view,listar_propiedades_usuario
from .views import agregar_propiedad,editar_propiedad,borrar_propiedad,listar_propiedades,detalle_propiedad

urlpatterns = [
   
    path("", index, name= 'index'),
    path('registro/', registro, name='registro'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/modificar/', modificar_perfil, name='modificar_perfil'),
    path('formulario/', formulario_view, name='formulario'),
    path('obtener_comunas/', obtener_comunas, name='obtener_comunas'),
    
    path('propiedades/agregar/', agregar_propiedad, name='agregar_propiedad'),
    path('propiedades/<int:propiedad_id>/editar/', editar_propiedad, name='editar_propiedad'),
    path('propiedades/<int:propiedad_id>/borrar/', borrar_propiedad, name='borrar_propiedad'),
    path('propiedades/usuario/', listar_propiedades_usuario, name='listar'),
    path('propiedades/<int:propiedad_id>/', detalle_propiedad, name='detalle_propiedad'),
    path('propiedades/', listar_propiedades, name='listar_propiedades'),
    
    
    path('accounts/', include('django.contrib.auth.urls')),
   
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
