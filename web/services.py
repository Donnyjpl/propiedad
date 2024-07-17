from .models import Usuario, Propiedad, ImagenPropiedad, SolicitudArriendo, Region, Comuna, Direccion

# Funciones CRUD para Usuario
def crear_usuario(username, first_name, last_name, RUT, telefono_personal, tipo_usuario, direccion_id=None):
    usuario = Usuario.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        RUT=RUT,
        telefono_personal=telefono_personal,
        tipo_usuario=tipo_usuario,
        direccion_id=direccion_id
    )
    return usuario

def listar_usuarios():
    return Usuario.objects.all()

def obtener_usuario_por_id(id):
    return Usuario.objects.get(id=id)

def actualizar_usuario(id, username=None, first_name=None, last_name=None, RUT=None, telefono_personal=None, tipo_usuario=None, direccion_id=None):
    usuario = Usuario.objects.get(id=id)
    if username:
        usuario.username = username
    if first_name:
        usuario.first_name = first_name
    if last_name:
        usuario.last_name = last_name
    if RUT:
        usuario.RUT = RUT
    if telefono_personal:
        usuario.telefono_personal = telefono_personal
    if tipo_usuario:
        usuario.tipo_usuario = tipo_usuario
    if direccion_id:
        usuario.direccion_id = direccion_id
    usuario.save()
    return usuario

def borrar_usuario(id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()


# Funciones CRUD para Propiedad
def crear_propiedad(nombre, descripcion, m2_construidos, m2_terreno, num_estacionamientos, num_habitaciones, num_banos, direccion_id, tipo_inmueble, precio_mensual, arrendador_id):
    propiedad = Propiedad.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        m2_construidos=m2_construidos,
        m2_terreno=m2_terreno,
        num_estacionamientos=num_estacionamientos,
        num_habitaciones=num_habitaciones,
        num_banos=num_banos,
        direccion_id=direccion_id,
        tipo_inmueble=tipo_inmueble,
        precio_mensual=precio_mensual,
        arrendador_id=arrendador_id
    )
    return propiedad

def listar_propiedades():
    return Propiedad.objects.all()

def obtener_propiedad_por_id(id):
    return Propiedad.objects.get(id=id)

def actualizar_propiedad(id, nombre=None, descripcion=None, m2_construidos=None, m2_terreno=None, num_estacionamientos=None, num_habitaciones=None, num_banos=None, direccion_id=None, tipo_inmueble=None, precio_mensual=None, arrendador_id=None, arrendatario_id=None):
    propiedad = Propiedad.objects.get(id=id)
    if nombre:
        propiedad.nombre = nombre
    if descripcion:
        propiedad.descripcion = descripcion
    if m2_construidos:
        propiedad.m2_construidos = m2_construidos
    if m2_terreno:
        propiedad.m2_terreno = m2_terreno
    if num_estacionamientos:
        propiedad.num_estacionamientos = num_estacionamientos
    if num_habitaciones:
        propiedad.num_habitaciones = num_habitaciones
    if num_banos:
        propiedad.num_banos = num_banos
    if direccion_id:
        propiedad.direccion_id = direccion_id
    if tipo_inmueble:
        propiedad.tipo_inmueble = tipo_inmueble
    if precio_mensual:
        propiedad.precio_mensual = precio_mensual
    if arrendador_id:
        propiedad.arrendador_id = arrendador_id
    if arrendatario_id is not None:
        propiedad.arrendatario_id = arrendatario_id
    propiedad.save()
    return propiedad

def borrar_propiedad(id):
    propiedad = Propiedad.objects.get(id=id)
    propiedad.delete()


# Funciones CRUD para ImagenPropiedad
def crear_imagen_propiedad(propiedad_id, imagen, descripcion=''):
    imagen_propiedad = ImagenPropiedad.objects.create(
        propiedad_id=propiedad_id,
        imagen=imagen,
        descripcion=descripcion
    )
    return imagen_propiedad

def listar_imagenes_propiedad(propiedad_id):
    return ImagenPropiedad.objects.filter(propiedad_id=propiedad_id)

def obtener_imagen_propiedad_por_id(id):
    return ImagenPropiedad.objects.get(id=id)

def actualizar_imagen_propiedad(id, descripcion=None):
    imagen_propiedad = ImagenPropiedad.objects.get(id=id)
    if descripcion:
        imagen_propiedad.descripcion = descripcion
    imagen_propiedad.save()
    return imagen_propiedad

def borrar_imagen_propiedad(id):
    imagen_propiedad = ImagenPropiedad.objects.get(id=id)
    imagen_propiedad.delete()


# Funciones CRUD para SolicitudArriendo
def crear_solicitud_arriendo(propiedad_id, usuario_id, estado='pendiente'):
    solicitud = SolicitudArriendo.objects.create(
        propiedad_id=propiedad_id,
        usuario_id=usuario_id,
        estado=estado
    )
    return solicitud

def listar_solicitudes_arriendo():
    return SolicitudArriendo.objects.all()

def obtener_solicitud_arriendo_por_id(id):
    return SolicitudArriendo.objects.get(id=id)

def actualizar_solicitud_arriendo(id, estado=None):
    solicitud = SolicitudArriendo.objects.get(id=id)
    if estado:
        solicitud.estado = estado
    solicitud.save()
    return solicitud

def borrar_solicitud_arriendo(id):
    solicitud = SolicitudArriendo.objects.get(id=id)
    solicitud.delete()


# Funciones CRUD para Region
def crear_region(nombre):
    region = Region.objects.create(nombre=nombre)
    return region

def listar_regiones():
    return Region.objects.all()

def obtener_region_por_id(id):
    return Region.objects.get(id=id)

def actualizar_region(id, nombre):
    region = Region.objects.get(id=id)
    region.nombre = nombre
    region.save()
    return region

def borrar_region(id):
    region = Region.objects.get(id=id)
    region.delete()


# Funciones CRUD para Comuna
def crear_comuna(nombre, region_id):
    comuna = Comuna.objects.create(nombre=nombre, region_id=region_id)
    return comuna

def listar_comunas():
    return Comuna.objects.all()

def obtener_comuna_por_id(id):
    return Comuna.objects.get(id=id)

def actualizar_comuna(id, nombre, region_id):
    comuna = Comuna.objects.get(id=id)
    comuna.nombre = nombre
    comuna.region_id = region_id
    comuna.save()
    return comuna

def borrar_comuna(id):
    comuna = Comuna.objects.get(id=id)
    comuna.delete()


# Funciones CRUD para Direccion
def crear_direccion(calle, numero, comuna_id, punto_referencia=None):
    direccion = Direccion.objects.create(
        calle=calle,
        numero=numero,
        comuna_id=comuna_id,
        punto_referencia=punto_referencia
    )
    return direccion

def listar_direcciones():
    return Direccion.objects.all()

def obtener_direccion_por_id(id):
    return Direccion.objects.get(id=id)

def actualizar_direccion(id, calle=None, numero=None, comuna_id=None, punto_referencia=None):
    direccion = Direccion.objects.get(id=id)
    if calle:
        direccion.calle = calle
    if numero:
        direccion.numero = numero
    if comuna_id:
        direccion.comuna_id = comuna_id
    if punto_referencia:
        direccion.punto_referencia = punto_referencia
    direccion.save()
    return direccion

def borrar_direccion(id):
    direccion = Direccion.objects.get(id=id)
    direccion.delete()
