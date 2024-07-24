# consulta para obtener los inmuebles por regiones

import os
import django

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'propiedad.settings')
django.setup()

# Importar modelos necesarios
from web.models import Propiedad, Direccion, Comuna, Region

# Función para consultar inmuebles por regiones utilizando el ORM de Django
def consultar_inmuebles_por_regiones():
    # Obtener todas las propiedades y sus detalles relacionados
    propiedades = Propiedad.objects.select_related('direccion__comuna__region').all()
    
    resultados = []
    for propiedad in propiedades:
        region = propiedad.direccion.comuna.region.nombre
        nombre_propiedad = propiedad.nombre
        descripcion = propiedad.descripcion
        resultados.append((region, nombre_propiedad, descripcion))
    
    return resultados

# Función para guardar resultados en un archivo de texto
def guardar_resultados_en_archivo(resultados):
    with open('inmuebles_por_regiones.txt', 'w', encoding='utf-8') as archivo:
        region_actual = None
        for fila in resultados:
            region, propiedad, descripcion = fila
            if region != region_actual:
                archivo.write(f'\n=== Región: {region} ===\n')
                region_actual = region
            archivo.write(f'Propiedad: {propiedad}\n')
            archivo.write(f'Descripción: {descripcion}\n\n')

if __name__ == '__main__':
    # Ejecutar la consulta para obtener los inmuebles por regiones
    resultados = consultar_inmuebles_por_regiones()
    guardar_resultados_en_archivo(resultados)
    print('Consulta finalizada. Los resultados han sido guardados en inmuebles_por_regiones.txt')
