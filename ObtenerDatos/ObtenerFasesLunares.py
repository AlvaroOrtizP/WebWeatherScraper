import requests
from bs4 import BeautifulSoup
import os
import datetime
import sys 
import json 

def obtener_fase_lunar(nombre_archivo):
    if 'M' in nombre_archivo:
        return "WANING_MOON"
    elif 'N' in nombre_archivo:
        return "NEW_MOON"
    elif 'C' in nombre_archivo:
        return "CRESCENT_MOON"
    elif 'LL' in nombre_archivo:
        return "FULL_MOON"
    else:
        return "UNKNOWN"

def obtener_contenido_tabla(url, lugar):
    # Obtener el HTML de la página web
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        # Analizar el HTML con BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        # Encontrar la etiqueta <tbody>
        tbody = soup.find('tbody')
        if tbody:
            contenido = []
            # Recorrer todas las filas de la tabla
            for fila in tbody.find_all('tr'):
                # Obtener el texto de cada celda en la fila
                datos_celda = [celda.get_text(strip=True) for celda in fila.find_all(['td', 'th'])]
               # Reemplazar comas por puntos en los números si es necesario
                datos_celda = [dato.replace(',', '.') if all(caracter.isdigit() or caracter == ',' or caracter == ':' for caracter in dato) else dato for dato in datos_celda]
    
                # Comprobar si la fila tiene datos
                if datos_celda:
                    contenido.append(datos_celda)
                # Comprobar si hay imágenes en la fila
                imagenes = fila.find_all('img')
                if imagenes:
                    for img in imagenes:
                        img_src = img.get('src')
                        img_filename = os.path.basename(img_src)
                        contenido.append(["Imagen", img_filename])
            return contenido
        else:
            print("No se pudo encontrar la etiqueta <tbody> en la página.")
            return None
    else:
        print("Error al obtener la página:", response.status_code)
        return None

def guardar_en_archivo(contenido, ruta_guardado, lugar):
    fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d")
    nombre_archivo = f"{ruta_guardado}data_buceo/lunar/datos_lunares_{fecha_actual}.json"
    datos_json = []
    fase_lunar = ""
    dia= ""
    mes= ""
    anno = ""
    anno = ""
    site= ""
    morningHighTideTime = ""
    morningHighTideHeight = ""
    eveningHighTideTime = ""
    eveningHighTideHeight= ""
    coefficient0H = ""
    coefficient12H = ""
    morningLowTideTime= ""
    morningLowTideHeight= ""
    eveningLowTideTime= ""
    eveningLowTideHeight= ""
    contador = 0
    for fila in contenido:
        if fila[0] == "Imagen":
            contador= contador+1
            fase_lunar = obtener_fase_lunar(fila[1])
        else:
            contador = contador+1
            dia, mes, anno = fila[1].split('/')
            anno = "20"+anno
            site = lugar
            morningHighTideTime = fila[3]
            morningHighTideHeight = fila[4]
            eveningHighTideTime = fila[5]
            eveningHighTideHeight = fila[6]
            coefficient0H = int(fila[7])
            coefficient12H = int(fila[8])
            morningLowTideTime= fila[9]
            morningLowTideHeight = fila[10]
            eveningLowTideTime = fila[11]
            eveningLowTideHeight = fila[12]
        if(contador == 2):  

            contador = 0  
            datos_json.append({
                    "day": dia,
                    "month": mes,
                    "year": anno,
                    "site": site,
                    "lunarPhase": fase_lunar,
                    "morningHighTideTime": morningHighTideTime,
                    "morningHighTideHeight": morningHighTideHeight,
                    "eveningHighTideTime": eveningHighTideTime,
                    "eveningHighTideHeight": eveningHighTideHeight,
                    "coefficient0H": coefficient0H,
                    "coefficient12H": coefficient12H,
                    "morningLowTideTime": morningLowTideTime,
                    "morningLowTideHeight": morningLowTideHeight,
                    "eveningLowTideTime": eveningLowTideTime,
                    "eveningLowTideHeight":eveningLowTideHeight
                })   
    with open(nombre_archivo, 'w', encoding='utf-8') as file:
        json.dump(datos_json, file, indent=4)
    print("Contenido guardado en", nombre_archivo)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, error de numero de parametros ")
        sys.exit(1)
    lugar = sys.argv[1]
    ruta_guardado = sys.argv[2] if len(sys.argv) > 2 else ""
    url = "https://www.puertosantander.es/es/tabla-de-mareas"
    contenido_tabla = obtener_contenido_tabla(url, lugar)
    if contenido_tabla:
        guardar_en_archivo(contenido_tabla, ruta_guardado, lugar)
