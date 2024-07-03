import json
from io import BytesIO
from Utils import ObtenerDatosWeb
import datetime
import sys 
from dateutil.relativedelta import relativedelta
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion.conexion_mysql import conectar

class ProcesadorDatos:
    def __init__(self):
        self.conn = conectar()
        if self.conn is None:
            exit()
    
    def procesar_directorio_windwuru(self, cursor, directorio):
        for filename in os.listdir(directorio):
            if filename.endswith(".json"):
                ruta_json = os.path.join(directorio, filename)

                nombre_archivo = os.path.basename(filename)
                partes_nombre = nombre_archivo.split("_")

                año = partes_nombre[1]
                mes = partes_nombre[2].lstrip("0")
                dia = partes_nombre[3].split(".")[0]
                horaAuxiliar = 0
                fecha_inicial = datetime.datetime(int(año), int(mes), int(dia))

                with open(ruta_json) as f:
                   
                    datos = json.load(f)
                    for clave, dato in datos.items():

                        fecha = dato["fecha"]
                        partes_fecha = fecha.split(".")
                        hora = partes_fecha[1].split("h")[0]

                        #Aumento de dia
                        if horaAuxiliar > int(hora):
                            # Si la hora actual es menor que la hora anterior, se aumenta el día
                            fecha_inicial += relativedelta(days=1)

                        horaAuxiliar = int(hora)
                        #Aumento de mes
                        if int(dia) > int(partes_fecha[0]):
                            fecha_inicial += relativedelta(months=0)
                            fecha_inicial = fecha_inicial.replace(day=1)

                        site = dato["id_playa"]    
                        dia = partes_fecha[0]
                        hora = partes_fecha[1].split("h")[0]
                        viento = dato["viento"]
                        rafagas = dato["rafagas"]
                        olas_altura = dato["olas_altura"]
                        periodo_olas = dato["periodo_olas"]
                        temperatura_tierra = dato["temperatura_tierra"]
            
                        sql = ("INSERT INTO wind_conditions (year, month, day, site, time_of_day, wind, gusts_of_wind, "
                               "wave_height, wave_period, earth_temperature) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                               "ON DUPLICATE KEY UPDATE year=VALUES(year), month=VALUES(month), day=VALUES(day), "
                               "site=VALUES(site), time_of_day=VALUES(time_of_day), wind=VALUES(wind), "
                               "gusts_of_wind=VALUES(gusts_of_wind), wave_height=VALUES(wave_height), "
                               "wave_period=VALUES(wave_period), earth_temperature=VALUES(earth_temperature)")
                        val = (fecha_inicial.year, fecha_inicial.month, fecha_inicial.day, site, hora, viento, rafagas,
                               olas_altura, periodo_olas, temperatura_tierra)
                        cursor.execute(sql, val)
                        print("se hace insert")

                self.conn.commit()
                os.remove(ruta_json)

    def procesar_windwuru(self):
        cursor = self.conn.cursor()

        directorio = "./data_buceo/WindWuru/"
        if len(sys.argv) > 2:
            ruta = sys.argv[2]
            directorio = f"{ruta}/data_buceo/WindWuru/"   

        try:
            self.procesar_directorio_windwuru(cursor, directorio)
            cursor.close()
            return "OK"  # Retorna éxito si se procesa sin errores
        except Exception as e:
            cursor.close()
            return f"NOK: Error en procesar_windwuru: {str(e)}"  # Retorna el error si ocurre alguno

def crear_json_padre(datos, id_playa):
    # Crea un objeto JSON a partir de los datos extraídos de la página
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
            "id_playa" : id_playa,
            "fecha": hora,
            "viento": viento,
            "rafagas": rafaga,
            "olas_altura": ola_altura,
            "periodo_olas": periodo_ola,
            "temperatura_tierra": temperatura_tierra
        }

    return json.dumps(resultado)

# ID de los elementos HTML que se van a buscar en la página
DOM_CABECERA = 'tabid_0_0_dates'
DOM_V_VIENTO = 'tabid_0_0_WINDSPD'
DOM_RAFAGAS_VIENTO = 'tabid_0_0_GUST'
DOM_OLA_ALTURA = 'tabid_0_0_HTSGW'
DOM_PERIODO_OLAS = 'tabid_0_0_PERPW'
DOM_TEMPERATURA_TIERRA = 'tabid_0_0_TMPE'

def main(id_playa):
    driver = ObtenerDatosWeb.configurar_navegador()
    url = f'https://www.windguru.cz/{id_playa}'
    print("Comienza la llamada")
    try:
        html = ObtenerDatosWeb.cargar_pagina(driver, url)
        div = ObtenerDatosWeb.encontrar_div(html)
        tr = div.find('tr', {'id': DOM_CABECERA})

        resultados = ObtenerDatosWeb.obtener_datos_cabecera(tr)    

        datos = [resultados]
        filas = [DOM_V_VIENTO, DOM_RAFAGAS_VIENTO, DOM_OLA_ALTURA, DOM_PERIODO_OLAS, DOM_TEMPERATURA_TIERRA]
        for f in filas:
            datos.append(ObtenerDatosWeb.obtener_body(tr.find_next('tr', {'id': f})))

        driver.quit()
        return crear_json_padre(datos, id_playa)
    except Exception as e:
        print(f"Error al obtener los datos web: {e}")
        driver.quit()
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporciona el ID de la playa.")
        sys.exit(1)

    print("------------------------------------------------------------------------------------------------")
    print("Comienza el proceso de WindWuLogger")
    
    id_playa = sys.argv[1]
    resultado_json = main(id_playa)
    
    if resultado_json:
        fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d")
        ruta_guardado = sys.argv[2] if len(sys.argv) > 2 else ""
        nombre_archivo = f"{ruta_guardado}data_buceo/WindWuru/datos_{fecha_actual}.json"
        print(f"WindWuLogger: Se adjunta nombre al archivo {nombre_archivo}")

        with open(nombre_archivo, "w") as f:
            print("WindWuLogger se guarda el archivo")
            f.write(resultado_json)

        print(f"WIND_WU_LOGGER: Datos guardados en el archivo {nombre_archivo}")
        procesador = ProcesadorDatos()
        resultado_windwuru = procesador.procesar_windwuru()
        print("------------------------------------------------------------------------------------------------")
