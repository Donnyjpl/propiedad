# Importar Django y configurar el entorno
import os
import django

# Configurar la ruta de tu proyecto Django y cargar la configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'propiedad.settings')
django.setup()

# Importar los modelos necesarios
from web.models import Propiedad, Comuna

# Función para obtener y guardar los inmuebles por comunas en un archivo de texto
def guardar_inmuebles_por_comunas():
    # Abrir archivo de texto para escritura
    with open('inmuebles_por_comunas.txt', 'w', encoding='utf-8') as archivo:
        # Obtener todas las comunas
        comunas = Comuna.objects.all()
        
        # Iterar sobre cada comuna
        for comuna in comunas:
            archivo.write(f"Comuna: {comuna.nombre}\n\n")
            
            # Obtener todas las propiedades en la comuna actual
            propiedades = Propiedad.objects.filter(direccion__comuna=comuna)
            
            # Iterar sobre cada propiedad y escribir nombre y descripción en el archivo
            for propiedad in propiedades:
                archivo.write(f"Nombre: {propiedad.nombre}\n")
                archivo.write(f"Descripción: {propiedad.descripcion}\n")
                archivo.write("\n")
                
            archivo.write("\n\n")

# Llamar a la función principal para guardar los inmuebles por comunas
if __name__ == "__main__":
    guardar_inmuebles_por_comunas()
    print("Datos de inmuebles por comunas guardados en 'inmuebles_por_comunas.txt'")
