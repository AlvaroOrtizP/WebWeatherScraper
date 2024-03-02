import requests
import xml.etree.ElementTree as ET
import json
import datetime
import sys  

def obtener_datos_aemet(url):
    # Realizar la solicitud GET para obtener el contenido XML
    respuesta = requests.get(url)
    
    
    
    #https://www.aemet.es/es/eltiempo/prediccion/municipios/noja-id39047
    #Hacer tambien de esta
    
    
    
    # Verificar si la solicitud fue exitosa (código 200)
    if respuesta.status_code == 200:
        # Parsear el contenido XML
        arbol = ET.fromstring(respuesta.text)
        
        # Inicializar lista para almacenar datos de cada día
        datos_por_dia = []
        
        # Iterar sobre los elementos "dia"
        for dia_elem in arbol.findall(".//dia"):
            # Obtener la fecha del día
            fecha = dia_elem.attrib.get("fecha", "")
            
            # Obtener los datos necesarios para cada día
            t_agua = dia_elem.find(".//t_agua").attrib.get("valor1", "")
            
            estado_cielo = dia_elem.find(".//estado_cielo")
            estado_cielo_data = {
                "f1": estado_cielo.attrib.get("f1", ""),
                "descripcion1": estado_cielo.attrib.get("descripcion1", ""),
                "f2": estado_cielo.attrib.get("f2", ""),
                "descripcion2": estado_cielo.attrib.get("descripcion2", "")
            }
            
            # Crear un diccionario con los datos para cada día
            datos_dia = {
                "fecha": fecha,
                "t_agua": t_agua,
                "estado_cielo": estado_cielo_data
            }
            
            # Agregar los datos del día a la lista
            datos_por_dia.append(datos_dia)
        
        return datos_por_dia
    else:
        # Imprimir mensaje de error si la solicitud no fue exitosa
        print(f"Error al obtener datos: {respuesta.status_code}")
        return None

def guardar_json(datos, nombre_archivo):
    # Guardar los datos en un archivo JSON
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)

print("------------------------------------------------------------------------------------------------")
print("TEMPERATURA LOGGER")
# URL del XML de AEMET
url_aemet = "https://www.aemet.es/xml/playas/play_v2_3900602.xml"

# Obtener la ruta del directorio proporcionada por el usuario (si está disponible)
ruta_guardado = sys.argv[1] if len(sys.argv) > 1 else ""

# Obtener los datos de AEMET para cada día
datos_aemet_por_dia = obtener_datos_aemet(url_aemet)

# Obtener la fecha actual
fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d")

# Construir el nombre del archivo con la fecha y la ruta proporcionada
nombre_archivo = f"{ruta_guardado}data_buceo/Aemet/datos_aemet_{fecha_actual}.json"

# Guardar los datos en un archivo JSON
if datos_aemet_por_dia:
    guardar_json(datos_aemet_por_dia, nombre_archivo)
    print(f"TEMPERATURA_LOGGER: Datos guardados correctamente en {nombre_archivo}")
print("------------------------------------------------------------------------------------------------")
