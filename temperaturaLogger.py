import requests
import xml.etree.ElementTree as ET
import json
import datetime
import sys  

def obtener_datos_aemet(url, id_playa):
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        arbol = ET.fromstring(respuesta.text)
        datos_por_dia = []
        
        for dia_elem in arbol.findall(".//dia"):
            
            fecha = dia_elem.attrib.get("fecha", "")
            t_agua = dia_elem.find(".//t_agua").attrib.get("valor1", "")
            
            estado_cielo = dia_elem.find(".//estado_cielo")
            estado_cielo_data = {
                "f1": estado_cielo.attrib.get("f1", ""),
                "descripcion1": estado_cielo.attrib.get("descripcion1", ""),
                "f2": estado_cielo.attrib.get("f2", ""),
                "descripcion2": estado_cielo.attrib.get("descripcion2", "")
            }
            
            datos_dia = {
                "id_playa" : id_playa,
                "fecha": fecha,
                "t_agua": t_agua,
                "estado_cielo": estado_cielo_data
            }
            
            datos_por_dia.append(datos_dia)
        
        return datos_por_dia
    else:
        print(f"Error al obtener datos: {respuesta.status_code}")
        return [{"error": f"Error al obtener datos: {respuesta.status_code}"}]

def guardar_json(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporciona el ID de la playa.")
        sys.exit(1)

    print("------------------------------------------------------------------------------------------------")
    print("TEMPERATURA LOGGER")

    id_playa = sys.argv[1]

    url_aemet = f"https://www.aemet.es/xml/playas/{id_playa}.xml"

    ruta_guardado = sys.argv[2] if len(sys.argv) > 2 else ""

    datos_aemet_por_dia = obtener_datos_aemet(url_aemet, id_playa)

    fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d")
    nombre_archivo = f"{ruta_guardado}data_buceo/Aemet/datos_aemet_{fecha_actual}.json"

    if datos_aemet_por_dia:
        guardar_json(datos_aemet_por_dia, nombre_archivo)
        print(f"TEMPERATURA_LOGGER: Datos guardados correctamente en {nombre_archivo}")
    print("------------------------------------------------------------------------------------------------")
