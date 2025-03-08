import json
import os
import sys
import re
import datetime
from bs4 import BeautifulSoup
from Utils import ObtenerDatosWeb
# Agregar el path al módulo de conexión
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'conexion')))
from conexion_mysql import conectar

class ProcesadorDatos:
    def __init__(self):
        pass        

    def guardar_contenido_en_archivo(self, contenido, nombre_archivo):
        try:
            ruta_guardado = sys.argv[2] if len(sys.argv) > 2 else ""
            nombre_archivo = f"{ruta_guardado}data_buceo/WindWuru/{nombre_archivo}"
            with open(nombre_archivo, "w", encoding='utf-8') as f:
                f.write(contenido)
            print(f"Contenido guardado en el archivo {nombre_archivo}")
        except Exception as e:
            print(f"Error al guardar el contenido en el archivo {nombre_archivo}: {e}")

def crear_json_padre(datos, id_playa):
    horas, vientos, rafagas, olas_altura_datos, periodo_olas, temperaturas_tierra = datos
    resultado = {}
    
    for i in range(len(horas)):
        hora = horas[i]
        viento = vientos[i]
        rafaga = rafagas[i]
        ola_altura = olas_altura_datos[i] 
        periodo_ola = periodo_olas[i] 
        temperatura_tierra = temperaturas_tierra[i]

        resultado[json.dumps(hora)] = {
            "id_playa": id_playa,
            "fecha": hora,
            "viento": viento,
            "rafagas": rafaga,
            "olas_altura": ola_altura,
            "periodo_olas": periodo_ola,
            "temperatura_tierra": temperatura_tierra
        }

    return json.dumps(resultado)

def limpiar_dato(dato):
    # Reemplazar caracteres no deseados con un '0' si se encuentran
    dato = dato.replace('Â', '').replace('\xa0', '').strip()
    return dato if dato else '0'  # Si el dato queda vacío, devuelve '0'


def separar_direccion(direccion):
    match = re.match(r'([A-Z]+) \((\d+)\)', direccion)
    if match:
        return match.group(1), match.group(2)
    return None, None

def main(id_playa):
    driver = ObtenerDatosWeb.configurar_navegador()
    url = f'https://www.windguru.cz/{id_playa}'
    print("Comienza la llamada")
    
    try:
        html = ObtenerDatosWeb.cargar_pagina(driver, url)
        div = ObtenerDatosWeb.encontrar_div(html)
        
        procesador = ProcesadorDatos()
        
        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d")
        ruta_guardado = sys.argv[2] if len(sys.argv) > 2 else ""
        nombre_archivo = f"direccionesClimatologicas_{fecha_actual}_{id_playa}.txt"
        procesador.guardar_contenido_en_archivo(str(div), nombre_archivo)
        
        # Extraer datos
        tr = div.find('tr', {'id': 'tabid_0_0_dates'})
        resultados = ObtenerDatosWeb.obtener_datos_cabecera(tr)

        datos = [resultados]
        filas = ['tabid_0_0_WINDSPD', 'tabid_0_0_GUST', 'tabid_0_0_HTSGW', 'tabid_0_0_PERPW', 'tabid_0_0_TMPE']
        for f in filas:
            datos.append(ObtenerDatosWeb.obtener_body(tr.find_next('tr', {'id': f})))

        driver.quit()
        resultado_json = crear_json_padre(datos, id_playa)

        # Leer y procesar archivo
        script_dir = os.path.dirname(__file__)
        ruta_direccionesClimatologicas_txt = os.path.join(script_dir, '..', 'data_buceo', 'WindWuru')
        ruta_completa = os.path.join(ruta_direccionesClimatologicas_txt, nombre_archivo)

        print("------------------------------------------------------------------------------------------------")
        print("Comienza el proceso de Direcciones")
        with open(ruta_completa, 'r', encoding='utf-8', errors='replace') as archivo:
            contenido = archivo.read()

        # Parsear el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(contenido, 'html.parser')
        tr_smer = soup.find('tr', id='tabid_0_0_SMER')
        tr_dirpw = soup.find('tr', id='tabid_0_0_DIRPW')
        tr_dates = soup.find('tr', id='tabid_0_0_dates')

        # Crear una lista para almacenar los resultados
        resultados = []
        horas = []
        dias = []

        if tr_dates:
            tds_dates = tr_dates.find_all('td', class_='tcell')
            for td in tds_dates:
                if len(td.contents) >= 4:
                    dia_mes = td.contents[2].strip().replace('.', '')
                    hora = td.contents[4].strip().replace('h', '')
                    horas.append(hora)
                    dias.append(int(dia_mes))
                    resultados.append(f"DATE: {dia_mes} - HOUR: {hora}")

        smer_datos = []
        if tr_smer:
            spans_smer = tr_smer.find_all('span', title=True)
            for span in spans_smer:
                dato_limpio = limpiar_dato(span['title'])
                smer_datos.append(dato_limpio)
                resultados.append(f"SMER: {dato_limpio}")

        dirpw_datos = []
        if tr_dirpw:
            spans_dirpw = tr_dirpw.find_all('span', title=True)
            for span in spans_dirpw:
                dato_limpio = limpiar_dato(span['title'])
                dirpw_datos.append(dato_limpio)
                resultados.append(f"DIRPW: {dato_limpio}")

        # Escribir los resultados en el archivo (sobrescribirlo)
        with open(ruta_completa, 'w', encoding='utf-8') as archivo:
            for resultado in resultados:
                archivo.write(f"{resultado}\n")

        print("El archivo ha sido sobrescrito con los datos extraídos.")

        # Guardar el resultado JSON en un archivo
        nombre_json = f"{ruta_guardado}data_buceo/WindWuru/datos_{id_playa}_{fecha_actual}.json"
        
        with open(nombre_json, "w", encoding='utf-8') as f:
            f.write(resultado_json)
        
        print(f"Datos guardados en el archivo {nombre_json}")

    except Exception as e:
        print(f"Error al obtener los datos web: {e}")
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporciona el ID de la playa.")
        sys.exit(1)

    id_playa = sys.argv[1]
    main(id_playa)
