import requests
import datetime
import sys 
import json  
from Utils import BuscarGeolocalizacion


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

def main(lugar):
    api_key = "PFodxGivcZJFGhZdPSh9R9mwLWIGXMpH"
    latitud, longitud = BuscarGeolocalizacion.obtener_coordenadas_lugar(lugar)
    pronostico = obtener_pronostico_clima(latitud, longitud, api_key)
    if pronostico:
        print("Pronóstico del clima obtenido con éxito:")
        fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d")
        ruta_guardado = sys.argv[1] if len(sys.argv) > 1 else ""
        nombre_archivo = f"data_buceo/viento/datos_{fecha_actual}.json"
        print(f"ObtenerDireccionViento: Se adjunta nombre al archivo {nombre_archivo}")

        with open(nombre_archivo, "w") as f:
            json.dump(pronostico, f)  # Guardar como JSON

        print(f"WIND_WU_LOGGER: Datos guardados en el archivo {nombre_archivo}")
        print("------------------------------------------------------------------------------------------------") 
    else:
        print("No se pudo obtener el pronóstico del clima.")

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Por favor, proporciona el ID de la playa.")
        sys.exit(1)
    print("------------------------------------------------------------------------------------------------")
    print("Comienza el proceso de ObtenerDireccionViento")
    lugar = sys.argv[1]
    main(lugar)
