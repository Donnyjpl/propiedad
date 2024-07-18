from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    RUT = models.CharField(max_length=12, unique=True)
    telefono_personal = models.CharField(max_length=15)
    tipo_usuario_choices = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    ]
    tipo_usuario = models.CharField(max_length=12, choices=tipo_usuario_choices)
    direccion = models.ForeignKey('Direccion', on_delete=models.SET_NULL, null=True)
    
     # Define related_name único para los campos ManyToManyField
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',  # Ejemplo de related_name único
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',  # Ejemplo de related_name único
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return f"{self.username} {self.last_name}"
class Propiedad(models.Model):
    TIPO_INMUEBLE_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela'),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    m2_construidos = models.DecimalField(max_digits=10, decimal_places=2)
    m2_terreno = models.DecimalField(max_digits=10, decimal_places=2)
    num_estacionamientos = models.IntegerField()
    num_habitaciones = models.IntegerField()
    num_banos = models.IntegerField()
    direccion = models.ForeignKey('Direccion', on_delete=models.SET_NULL, null=True)
    tipo_inmueble = models.CharField(max_length=20, choices=TIPO_INMUEBLE_CHOICES)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    arrendador = models.ForeignKey(Usuario, related_name='propiedades_arrendadas', on_delete=models.CASCADE)
    arrendatario = models.ForeignKey(Usuario, related_name='propiedades_arrendadas_a_mi', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre}y el tipo {self.tipo_inmueble}"
    
    
class ImagenPropiedad(models.Model):
    propiedad = models.ForeignKey(Propiedad, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='propiedades/')
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Imagen de '{self.propiedad.nombre}'"    



class SolicitudArriendo(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Solicitud de arriendo de {self.usuario} para {self.propiedad}"
class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    # Otros campos relevantes para la región

    def __str__(self):
        return self.nombre
    
class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.region}"   
     
class Direccion(models.Model):
    calle = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    punto_referencia = models.CharField(max_length=255, blank=True, null=True)
    comuna = models.ForeignKey('Comuna', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.punto_referencia:
            return f"{self.calle} {self.numero}, {self.punto_referencia}, {self.comuna}, {self.region}"
        else:
            return f"{self.calle} {self.numero}, {self.comuna}, {self.region}"