from .models import Usuario, Propiedad, ImagenPropiedad, SolicitudArriendo, Region, Comuna, Direccion

# Funciones para Usuario

def crear_usuario(data):
    return Usuario.objects.create(**data)

def obtener_usuarios():
    return Usuario.objects.all()

def obtener_usuario_por_id(id):
    return Usuario.objects.get(pk=id)

def actualizar_usuario(id, data):
    usuario = Usuario.objects.get(pk=id)
    for key, value in data.items():
        setattr(usuario, key, value)
    usuario.save()
    return usuario

def eliminar_usuario(id):
    usuario = Usuario.objects.get(pk=id)
    usuario.delete()


# Funciones para Propiedad

def crear_propiedad(data):
    return Propiedad.objects.create(**data)

def obtener_propiedades():
    return Propiedad.objects.all()

def obtener_propiedad_por_id(id):
    return Propiedad.objects.get(pk=id)

def actualizar_propiedad(id, data):
    propiedad = Propiedad.objects.get(pk=id)
    for key, value in data.items():
        setattr(propiedad, key, value)
    propiedad.save()
    return propiedad

def eliminar_propiedad(id):
    propiedad = Propiedad.objects.get(pk=id)
    propiedad.delete()


# Funciones para ImagenPropiedad

def crear_imagen_propiedad(propiedad, imagen, descripcion=''):
    return ImagenPropiedad.objects.create(propiedad=propiedad, imagen=imagen, descripcion=descripcion)

def obtener_imagenes_propiedad(propiedad):
    return propiedad.imagenes.all()

def obtener_imagen_propiedad_por_id(id):
    return ImagenPropiedad.objects.get(pk=id)

def actualizar_imagen_propiedad(id, data):
    imagen_propiedad = ImagenPropiedad.objects.get(pk=id)
    for key, value in data.items():
        setattr(imagen_propiedad, key, value)
    imagen_propiedad.save()
    return imagen_propiedad

def eliminar_imagen_propiedad(id):
    imagen_propiedad = ImagenPropiedad.objects.get(pk=id)
    imagen_propiedad.delete()


# Funciones para SolicitudArriendo

def crear_solicitud_arriendo(propiedad, usuario, estado='pendiente'):
    return SolicitudArriendo.objects.create(propiedad=propiedad, usuario=usuario, estado=estado)

def obtener_solicitudes_arriendo():
    return SolicitudArriendo.objects.all()

def obtener_solicitud_arriendo_por_id(id):
    return SolicitudArriendo.objects.get(pk=id)

def actualizar_solicitud_arriendo(id, data):
    solicitud_arriendo = SolicitudArriendo.objects.get(pk=id)
    for key, value in data.items():
        setattr(solicitud_arriendo, key, value)
    solicitud_arriendo.save()
    return solicitud_arriendo

def eliminar_solicitud_arriendo(id):
    solicitud_arriendo = SolicitudArriendo.objects.get(pk=id)
    solicitud_arriendo.delete()


# Funciones para Region

def crear_region(nombre):
    return Region.objects.create(nombre=nombre)

def obtener_regiones():
    return Region.objects.all()

def obtener_region_por_id(id):
    return Region.objects.get(pk=id)

def actualizar_region(id, nombre):
    region = Region.objects.get(pk=id)
    region.nombre = nombre
    region.save()
    return region

def eliminar_region(id):
    region = Region.objects.get(pk=id)
    region.delete()


# Funciones para Comuna

def crear_comuna(nombre, region):
    return Comuna.objects.create(nombre=nombre, region=region)

def obtener_comunas():
    return Comuna.objects.all()

def obtener_comuna_por_id(id):
    return Comuna.objects.get(pk=id)

def actualizar_comuna(id, nombre, region):
    comuna = Comuna.objects.get(pk=id)
    comuna.nombre = nombre
    comuna.region = region
    comuna.save()
    return comuna

def eliminar_comuna(id):
    comuna = Comuna.objects.get(pk=id)
    comuna.delete()


# Funciones para Direccion

def crear_direccion(calle, numero, comuna, punto_referencia=None):
    return Direccion.objects.create(calle=calle, numero=numero, comuna=comuna, punto_referencia=punto_referencia)

def obtener_direcciones():
    return Direccion.objects.all()

def obtener_direccion_por_id(id):
    return Direccion.objects.get(pk=id)

def actualizar_direccion(id, calle, numero, comuna, punto_referencia=None):
    direccion = Direccion.objects.get(pk=id)
    direccion.calle = calle
    direccion.numero = numero
    direccion.comuna = comuna
    direccion.punto_referencia = punto_referencia
    direccion.save()
    return direccion

def eliminar_direccion(id):
    direccion = Direccion.objects.get(pk=id)
    direccion.delete()

# Nuevas funciones para listar

# Función para listar todos los usuarios
def listar_usuarios():
    usuarios = Usuario.objects.all()
    resultado = "Usuarios:\n"
    for usuario in usuarios:
        resultado += f"{usuario.id} - {usuario.username} {usuario.last_name}\n"
    return resultado

# Función para listar todas las propiedades
def listar_propiedades():
    propiedades = Propiedad.objects.all()
    resultado = "Propiedades:\n"
    for propiedad in propiedades:
        resultado += f"{propiedad.id} - {propiedad.nombre} de tipo {propiedad.tipo_inmueble}\n"
    return resultado

# Función para listar todas las imágenes de propiedades
def listar_imagenes_propiedades():
    imagenes = ImagenPropiedad.objects.all()
    resultado = "Imágenes de Propiedades:\n"
    for imagen in imagenes:
        resultado += f"{imagen.id} - Imagen de '{imagen.propiedad.nombre}'\n"
    return resultado

# Función para listar todas las solicitudes de arriendo
def listar_solicitudes_arriendo():
    solicitudes = SolicitudArriendo.objects.all()
    resultado = "Solicitudes de Arriendo:\n"
    for solicitud in solicitudes:
        resultado += f"{solicitud.id} - Solicitud de {solicitud.usuario.username} para {solicitud.propiedad.nombre}, estado: {solicitud.estado}\n"
    return resultado

# Función para listar todas las regiones
def listar_regiones():
    regiones = Region.objects.all()
    resultado = "Regiones:\n"
    for region in regiones:
        resultado += f"{region.id} - {region.nombre}\n"
    return resultado

# Función para listar todas las comunas
def listar_comunas():
    comunas = Comuna.objects.all()
    resultado = "Comunas:\n"
    for comuna in comunas:
        resultado += f"{comuna.id} - {comuna.nombre}, {comuna.region.nombre}\n"
    return resultado

# Función para listar todas las direcciones
def listar_direcciones():
    direcciones = Direccion.objects.all()
    resultado = "Direcciones:\n"
    for direccion in direcciones:
        if direccion.punto_referencia:
            resultado += f"{direccion.id} - {direccion.calle} {direccion.numero}, {direccion.punto_referencia}, {direccion.comuna.nombre}\n"
        else:
            resultado += f"{direccion.id} - {direccion.calle} {direccion.numero}, {direccion.comuna.nombre}\n"
    return resultado
