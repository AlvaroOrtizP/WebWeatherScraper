import requests
import datetime
import sys 
import json  
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Utils import BuscarGeolocalizacion
from conexion.conexion_mysql import conectar

class ProcesadorDatos:
    def __init__(self):
        self.conn = conectar()
        if self.conn is None:
            exit()

    @staticmethod
    def obtener_pronostico_clima(latitud, longitud, api_key):
        url = f"https://api.tomorrow.io/v4/weather/forecast?location={latitud},{longitud}&apikey={api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                datos = response.json()
                return datos
            else:
                print("Error al obtener el pronóstico del clima. Código de estado:", response.status_code)
                return None
        except Exception as e:
            print("Error al conectarse a la API:", e)
            return None

    def procesar_directorio_viento(self, cursor, directorio):
        site = sys.argv[2]
        for filename in os.listdir(directorio):
            if filename.endswith(".json"):
                ruta_json = os.path.join(directorio, filename)
                with open(ruta_json) as f:
                    try:
                        datos = json.load(f)
                        if "timelines" in datos and "hourly" in datos["timelines"]:
                            hourly_data = datos["timelines"]["hourly"]
                            for hourly_entry in hourly_data:
                                time_value = hourly_entry["time"]
                                año = int(time_value[:4])
                                mes = int(time_value[5:7])
                                dia = int(time_value[8:10])
                                hora = int(time_value[11:13])
                                wind_direction = hourly_entry["values"]["windDirection"]

                                sql = ("UPDATE wind_conditions SET wind_direction = %s "
                                       "WHERE year = %s AND month = %s AND day = %s AND site = %s AND time_of_day = %s")
                                val = (wind_direction, año, mes, dia, site, hora)
                                #print(f"CONSULTA: {sql % val}")
                                cursor.execute(sql, val)

                    except Exception as e:
                        print("Error:", e)
                        continue  # Si hay un error, continuamos con el siguiente archivo

                    self.conn.commit()

                # Eliminar el archivo solo si no hay errores
                try:
                    os.remove(ruta_json)
                except Exception as e:
                    print(f"Error al eliminar el archivo {ruta_json}: {e}")

def main(lugar, ruta_guardado):
    api_key = "PFodxGivcZJFGhZdPSh9R9mwLWIGXMpH"
    latitud, longitud = BuscarGeolocalizacion.obtener_coordenadas_lugar(lugar)
    pronostico = ProcesadorDatos.obtener_pronostico_clima(latitud, longitud, api_key)
    if pronostico:
        print("Pronóstico del clima obtenido con éxito:")
        fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d")

        nombre_archivo = f"{ruta_guardado}data_buceo/viento/datos_viento_{fecha_actual}.json"

        print(f"ObtenerDireccionViento: Se adjunta nombre al archivo {nombre_archivo}")

        with open(nombre_archivo, "w") as f:
            json.dump(pronostico, f)  # Guardar como JSON

        print(f"WIND_WU_LOGGER: Datos guardados en el archivo {nombre_archivo}")
        print("------------------------------------------------------------------------------------------------") 
    else:
        print("No se pudo obtener el pronóstico del clima.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporciona el lugar del viento")
        sys.exit(1)
    print("------------------------------------------------------------------------------------------------")
    print("Comienza el proceso de ObtenerDireccionViento")
    lugar = sys.argv[1]
    ruta_guardado = sys.argv[3] if len(sys.argv) > 3 else ""
    
    main(lugar, ruta_guardado)
    procesador = ProcesadorDatos()
    resultado_viento = procesador.procesar_directorio_viento(procesador.conn.cursor(), f"{ruta_guardado}data_buceo/viento/")
