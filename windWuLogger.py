import json
from io import BytesIO
import Utils.GeneradorImagen
import Utils.ObtenerDatosWeb
import datetime
import sys 

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
    driver = Utils.ObtenerDatosWeb.configurar_navegador()
    url = f'https://www.windguru.cz/{id_playa}'
    print("Comienza la llamada")
    try:
        html = Utils.ObtenerDatosWeb.cargar_pagina(driver, url)
        div = Utils.ObtenerDatosWeb.encontrar_div(html)
        tr = div.find('tr', {'id': DOM_CABECERA})
   
        resultados = Utils.ObtenerDatosWeb.obtener_datos_cabecera(tr)    

        datos = [resultados]
        filas = [DOM_V_VIENTO, DOM_RAFAGAS_VIENTO, DOM_OLA_ALTURA, DOM_PERIODO_OLAS, DOM_TEMPERATURA_TIERRA]
        for f in filas:
            datos.append(Utils.ObtenerDatosWeb.obtener_body(tr.find_next('tr', {'id': f})))

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
        print("------------------------------------------------------------------------------------------------") 
