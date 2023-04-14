from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime
import time
import re
import json


# ID de los elementos HTML que se van a buscar en la página
DOM_CABECERA = 'tabid_0_0_dates'
DOM_V_VIENTO = 'tabid_0_0_WINDSPD'
DOM_RAFAGAS_VIENTO = 'tabid_0_0_GUST'
DOM_OLA_ALTURA = 'tabid_0_0_HTSGW'
DOM_DIRECCION = 'tabid_0_0_SMER'
DOM_PERIODO_OLAS = 'tabid_0_0_PERPW'
DOM_DIRECCION_OLAS = ''
DOM_TEMPERATURA_TIERRA = 'tabid_0_0_TMPE'

def configurar_navegador():
# Configura el navegador para ejecutarse en modo headless y establece el tamaño de la ventana
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1200')
    return webdriver.Chrome(options=options)


def cargar_pagina(driver, url):
# Carga la página y espera hasta que aparezca un elemento en el DOM
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    div = wait.until(EC.presence_of_element_located((By.ID, 'forecasts-page')))
    time.sleep(3)
    return driver.execute_script("return document.documentElement.outerHTML")


def encontrar_div(html):
# Busca el div que contiene los datos relevantes
    soup = BeautifulSoup(html, 'html.parser')
    
    return soup.find('div', {'id': 'tabid_0_content_div'})


def obtener_datos_cabecera(tr):
# Extrae los datos de la cabecera de la tabla
    datos = tr.find_all('td')
    resultados = []
    for dato in datos:
        # Extrae el número de punto y la hora a partir del texto de cada celda
        numero_punto = re.findall(r'\d+\.', dato.get_text())[0]
        numero_h = re.findall(r'\d+h', dato.get_text())[0]
        resultados.append(f"{numero_punto} {numero_h}")
    return resultados


def guardar_cabecera_en_archivo(tr):
    # Guarda la cabecera de la tabla en un archivo de texto
    now = datetime.datetime.now()
    filename = f"DOM_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(tr.prettify())

def obtener_body(tr):
    # Extrae los datos del cuerpo de la tabla
    datos = tr.find_all('td')
    return [dato.get_text() for i, dato in enumerate(datos) if i < 110]




def crear_json_padre(datos):
    # Crea un objeto JSON a partir de los datos extraídos de la página
    horas = datos[0]
    vientos = datos[1]
    rafagas = datos[2]
    olas_altura_datos = datos[3]
    periodo_olas = datos[4]
    temperaturas_tierra = datos[5]
    resultado = {}
    for i in range(len(horas)):
        hora = horas[i]
        viento = vientos[i]
        rafaga = rafagas[i]
        ola_altura = olas_altura_datos[i] 
        periodo_ola = periodo_olas[i] 
        temperatura_tierra = temperaturas_tierra[i]
        resultado[json.dumps({"hora" : hora})] = {"viento": viento, "rafagas": rafaga, "olas_altura": ola_altura, "periodo_olas": periodo_ola, "temperatura_tierra": temperatura_tierra}

    return json.dumps(resultado)





def main():
    driver = configurar_navegador()
    url = 'https://www.windguru.cz/179761'
    html = cargar_pagina(driver, url)
    div = encontrar_div(html)
    tr = div.find('tr', {'id': DOM_CABECERA})
    resultados = obtener_datos_cabecera(tr)    
    
    guardar_cabecera_en_archivo(div.find('tr', {'id': DOM_DIRECCION}))
    
    datos = []
    datos.append(resultados)
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_V_VIENTO})))
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_RAFAGAS_VIENTO})))
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_OLA_ALTURA})))
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_PERIODO_OLAS})))
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_TEMPERATURA_TIERRA})))
    
    
    print(crear_json_padre(datos))
    driver.quit()


if __name__ == '__main__':
    main()
