import json
from io import BytesIO
import generadorImagen
import obtenerDatosWeb
#INICIO BOT 


def crear_json_padre(datos):
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

def main():
    driver = obtenerDatosWeb.configurar_navegador()
    url = 'https://www.windguru.cz/487006'
    print("Comienza la llamada")
    try:
        html = obtenerDatosWeb.cargar_pagina(driver, url)
        div = obtenerDatosWeb.encontrar_div(html)
        tr = div.find('tr', {'id': DOM_CABECERA})
        resultados = obtenerDatosWeb.obtener_datos_cabecera(tr)    

        datos = [resultados]
        filas = [DOM_V_VIENTO, DOM_RAFAGAS_VIENTO, DOM_OLA_ALTURA, DOM_PERIODO_OLAS, DOM_TEMPERATURA_TIERRA]
        for f in filas:
            datos.append(obtenerDatosWeb.obtener_body(tr.find_next('tr', {'id': f})))

        driver.quit()
        return crear_json_padre(datos)
    except Exception as e:
        print(f"Error al obtener los datos web: {e}")
        driver.quit()
        return None

if __name__ == "__main__":
    # Ejecutar la función main y hacer algo con el resultado (por ejemplo, guardar en un archivo)
    resultado_json = main()
    print("1")
    
    if resultado_json:
        with open("datos.json", "w") as f:
            f.write(resultado_json)