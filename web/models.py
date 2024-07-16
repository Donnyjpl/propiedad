from django.db import models
from django.contrib.auth.models import AbstractUser

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

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    RUT = models.CharField(max_length=12, unique=True)
    telefono_personal = models.CharField(max_length=15)
    tipo_usuario_choices = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    ]
    tipo_usuario = models.CharField(max_length=12, choices=tipo_usuario_choices)
    direccion = models.ForeignKey('Direccion', on_delete=models.SET_NULL, null=True)
    propiedades = models.ManyToManyField(Propiedad, related_name='usuarios', blank=True)
    
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
        return f"{self.first_name} {self.last_name}"
    
    

    
class Direccion(models.Model):
    calle = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    punto_referencia = models.CharField(max_length=255, blank=True, null=True)
    comuna = models.CharField(max_length=100)

    def __str__(self):
        if self.punto_referencia:
            return f"{self.calle} {self.numero}, {self.punto_referencia}, {self.comuna}"
        else:
            return f"{self.calle} {self.numero}, {self.comuna}"