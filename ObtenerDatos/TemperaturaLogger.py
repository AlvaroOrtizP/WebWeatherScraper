import requests
import xml.etree.ElementTree as ET
import json
import datetime
import sys  
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion.conexion_mysql import conectar

class ProcesadorDatos:
    def __init__(self):
        self.conn = conectar()
        if self.conn is None:
            exit()

    @staticmethod
    def obtener_datos_aemet(url, id_playa, id_lugar):
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
                    "id_lugar" : id_lugar,
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

    @staticmethod
    def guardar_json(datos, nombre_archivo):
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
            
    def procesar_aemet(self):
        cursor = self.conn.cursor()

        directorio = "./data_buceo/Aemet/"
        if len(sys.argv) > 3:
            ruta = sys.argv[3]
            directorio = f"{ruta}/data_buceo/Aemet/"   

        try:
            self.procesar_directorio_aemet(cursor, directorio)
            cursor.close()
            return "OK"  # Retorna éxito si se procesa sin errores
        except Exception as e:
            cursor.close()
            return f"NOK: Error en procesar_aemet: {str(e)}"  # Retorna el error si ocurre alguno

    def procesar_directorio_aemet(self, cursor, directorio):
        for filename in os.listdir(directorio):
            if filename.endswith(".json"):
                ruta_json = os.path.join(directorio, filename)
                                
                with open(ruta_json) as f:
                    datos = json.load(f)
                    for dato in datos:
                        id_playa = dato["id_playa"]
                        fecha_json = dato["fecha"]
                        año = fecha_json[:4]
                        mes = fecha_json[4:6]
                        dia = fecha_json[6:8]
                        t_agua = dato["t_agua"]
                        estado_cielo = dato["estado_cielo"]
                        f1 = estado_cielo["f1"]
                        descripcion1 = estado_cielo["descripcion1"]
                        f2 = estado_cielo["f2"]
                        descripcion2 = estado_cielo["descripcion2"]
                        id_lugar = dato["id_lugar"]
                        
                        # En caso de ser anterior o igual a las 14 horas se guardara el f1 y su descripcion
                        sql = ("UPDATE wind_conditions SET water_temperature=%s, condition_code=%s, condition_description=%s "
                               "WHERE year=%s AND month=%s AND day=%s AND site=%s AND time_of_day <= '14'")
                        val = (t_agua, f1, descripcion1, año, mes.lstrip("0"), dia.lstrip("0"), id_lugar)

                        cursor.execute(sql, val)

                        # En caso de ser posterior a las 14 horas se guardara el f2 y su descripcion
                        sql = ("UPDATE wind_conditions SET water_temperature=%s, condition_code=%s, condition_description=%s "
                               "WHERE year=%s AND month=%s AND day=%s AND site=%s AND time_of_day > '14'")
                        val = (t_agua, f2, descripcion2, año, mes.lstrip("0"), dia.lstrip("0"), id_lugar)

                        cursor.execute(sql, val)
                
                self.conn.commit()
                #os.remove(ruta_json)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Por favor, proporciona el ID de la playa y el ID del lugar.")
        sys.exit(1)

    print("------------------------------------------------------------------------------------------------")
    print("TEMPERATURA LOGGER")

    id_playa = sys.argv[1]
    id_lugar = sys.argv[2]

    url_aemet = f"https://www.aemet.es/xml/playas/{id_playa}.xml"
    datos_aemet_por_dia = ProcesadorDatos.obtener_datos_aemet(url_aemet, id_playa, id_lugar)

    if datos_aemet_por_dia:
        fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d")
        ruta_guardado = sys.argv[3] if len(sys.argv) > 3 else ""
        nombre_archivo = f"{ruta_guardado}data_buceo/Aemet/datos_aemet_{id_lugar}_{fecha_actual}.json"    

        ProcesadorDatos.guardar_json(datos_aemet_por_dia, nombre_archivo)
        print(f"TEMPERATURA_LOGGER: Datos guardados correctamente en {nombre_archivo}")
        procesador = ProcesadorDatos()
        resultado_aemet = procesador.procesar_aemet()
        print(resultado_aemet)
        print("------------------------------------------------------------------------------------------------")
