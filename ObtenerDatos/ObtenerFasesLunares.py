import requests
from bs4 import BeautifulSoup
import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion.conexion_mysql import conectar


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
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody')
        if tbody:
            contenido = []
            for fila in tbody.find_all('tr'):
                datos_celda = [celda.get_text(strip=True) for celda in fila.find_all(['td', 'th'])]
                datos_celda = [dato.replace(',', '.') if all(caracter.isdigit() or caracter == ',' or caracter == ':' for caracter in dato) else dato for dato in datos_celda]
                if datos_celda:
                    contenido.append(datos_celda)
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

def guardar_en_base_datos(contenido, lugar):
    conn = conectar()
    if conn is None:
        exit()

    cursor = conn.cursor()
    fases_lunares = {
        "WANING_MOON": 1,
        "NEW_MOON": 2,
        "CRESCENT_MOON": 3,
        "FULL_MOON": 4  
    }
    fase_lunar = ""
    dia = ""
    mes = ""
    anno = ""
    site = ""
    morningHighTideTime = ""
    morningHighTideHeight = ""
    eveningHighTideTime = ""
    eveningHighTideHeight = ""
    coefficient0H = ""
    coefficient12H = ""
    morningLowTideTime = ""
    morningLowTideHeight = ""
    eveningLowTideTime = ""
    eveningLowTideHeight = ""
    contador = 0

    for fila in contenido:
        if fila[0] == "Imagen":
            contador += 1
            fase_lunar = obtener_fase_lunar(fila[1])
        else:
            contador += 1
            dia, mes, anno = fila[1].split('/')
            anno = "20" + anno
            site = lugar
            morningHighTideTime = fila[3]
            morningHighTideHeight = fila[4]
            eveningHighTideTime = fila[5]
            eveningHighTideHeight = fila[6]
            coefficient0H = int(fila[7])
            coefficient12H = int(fila[8])
            morningLowTideTime = fila[9]
            morningLowTideHeight = fila[10]
            eveningLowTideTime = fila[11]
            eveningLowTideHeight = fila[12]
        if contador == 2:
            contador = 0
            lunarPhase = fases_lunares.get(fase_lunar, None)
            if lunarPhase is None:
                print(f"Fase lunar desconocida: {fase_lunar}")
                continue

            sql = "INSERT INTO tide_table (day, month, year, site, moon_phase,  morning_high_tide_time, morning_high_tide_height, afternoon_high_tide_time, afternoon_high_tide_height, coefficient0H, coefficient12H, morning_low_tide_time, morning_low_tide_height, afternoon_low_tide_time, afternoon_low_tide_height ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE year=VALUES(year), month=VALUES(month), day=VALUES(day), site=VALUES(site), moon_phase=VALUES(moon_phase), morning_high_tide_time=VALUES(morning_high_tide_time), morning_high_tide_height=VALUES(morning_high_tide_height), afternoon_high_tide_time=VALUES(afternoon_high_tide_time), afternoon_high_tide_height=VALUES(afternoon_high_tide_height), coefficient0H=VALUES(coefficient0H), coefficient12H=VALUES(coefficient12H), morning_low_tide_time=VALUES(morning_low_tide_time), morning_low_tide_height=VALUES(morning_low_tide_height), afternoon_low_tide_time=VALUES(afternoon_low_tide_time), afternoon_low_tide_height=VALUES(afternoon_low_tide_height)"

            val = (dia, mes, anno, site, lunarPhase, morningHighTideTime, morningHighTideHeight, eveningHighTideTime, eveningHighTideHeight, coefficient0H, coefficient12H, morningLowTideTime, morningLowTideHeight, eveningLowTideTime, eveningLowTideHeight)
            cursor.execute(sql, val)

    conn.commit()
    cursor.close()
    conn.close()
    print("Datos guardados en la base de datos")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, error de numero de parametros")
        sys.exit(1)
    lugar = sys.argv[1]
    ruta_guardado = sys.argv[2] if len(sys.argv) > 2 else ""
    url = "https://www.puertosantander.es/es/tabla-de-mareas"
    contenido_tabla = obtener_contenido_tabla(url, lugar)
    if contenido_tabla:
        guardar_en_base_datos(contenido_tabla, lugar)
