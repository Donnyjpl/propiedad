# Importar Django y configurar el entorno
import os
import django

# Configurar la ruta de tu proyecto Django y cargar la configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'propiedad.settings')
django.setup()

# Importar los modelos necesarios
from web.models import Propiedad, Direccion, Comuna

# Función para obtener y guardar los inmuebles por comunas en un archivo de texto
def guardar_inmuebles_por_comunas():
    # Abrir archivo de texto para escritura
    with open('inmuebles_por_comunas.txt', 'w', encoding='utf-8') as archivo:
        # Consulta SQL para obtener las propiedades por comuna
        consulta_sql = """
            SELECT c.nombre AS comuna, p.nombre AS propiedad, p.descripcion 
            FROM web_propiedad AS p
            INNER JOIN web_direccion AS d ON p.direccion_id = d.id
            INNER JOIN web_comuna AS c ON d.comuna_id = c.id
            ORDER BY c.nombre, p.nombre
        """
        
        # Ejecutar la consulta SQL
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql)
            resultados = cursor.fetchall()
        
        # Escribir resultados en el archivo de texto
        for comuna, nombre_propiedad, descripcion in resultados:
            archivo.write(f"Comuna: {comuna}\n")
            archivo.write(f"Nombre: {nombre_propiedad}\n")
            archivo.write(f"Descripción: {descripcion}\n")
            archivo.write("\n")

# Llamar a la función principal para guardar los inmuebles por comunas
if __name__ == "__main__":
    guardar_inmuebles_por_comunas()
    print("Datos de propiedad por comunas guardados en 'propiedad_por_comunas.txt'")
