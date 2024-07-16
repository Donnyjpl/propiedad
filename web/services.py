from models import Usuario, Propiedad, Direccion

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
def crear_propiedad(nombre, descripcion, m2_construidos, m2_terreno, num_estacionamientos, num_habitaciones, num_banos, direccion_id, tipo_inmueble, precio_mensual):
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
        precio_mensual=precio_mensual
    )
    return propiedad

def listar_propiedades():
    return Propiedad.objects.all()

def actualizar_propiedad(id, nombre=None, descripcion=None, m2_construidos=None, m2_terreno=None, num_estacionamientos=None, num_habitaciones=None, num_banos=None, direccion_id=None, tipo_inmueble=None, precio_mensual=None):
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
    propiedad.save()
    return propiedad

def borrar_propiedad(id):
    propiedad = Propiedad.objects.get(id=id)
    propiedad.delete()


# Funciones CRUD para Direccion
def crear_direccion(calle, numero, comuna, punto_referencia=None):
    direccion = Direccion.objects.create(
        calle=calle,
        numero=numero,
        comuna=comuna,
        punto_referencia=punto_referencia
    )
    return direccion

def listar_direcciones():
    return Direccion.objects.all()

def actualizar_direccion(id, calle=None, numero=None, comuna=None, punto_referencia=None):
    direccion = Direccion.objects.get(id=id)
    if calle:
        direccion.calle = calle
    if numero:
        direccion.numero = numero
    if comuna:
        direccion.comuna = comuna
    if punto_referencia:
        direccion.punto_referencia = punto_referencia
    direccion.save()
    return direccion

def borrar_direccion(id):
    direccion = Direccion.objects.get(id=id)
    direccion.delete()




