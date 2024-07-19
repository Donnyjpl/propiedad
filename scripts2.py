# consulta_inmuebles.py

import os
import django
from django.db import connection

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'propiedad.settings')
django.setup()

# Función para ejecutar la consulta SQL
def consultar_inmuebles_por_regiones():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT r.nombre AS region, p.nombre AS propiedad, p.descripcion 
            FROM web_propiedad AS p
            INNER JOIN web_direccion AS d ON p.direccion_id = d.id
            INNER JOIN web_comuna AS c ON d.comuna_id = c.id
            INNER JOIN web_region AS r ON c.region_id = r.id
            ORDER BY r.nombre, p.nombre
        ''')

        # Obtener todos los resultados
        resultados = cursor.fetchall()

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
    resultados = consultar_inmuebles_por_regiones()
    guardar_resultados_en_archivo(resultados)
    print('Consulta finalizada. Los resultados han sido guardados en inmuebles_por_regiones.txt')
