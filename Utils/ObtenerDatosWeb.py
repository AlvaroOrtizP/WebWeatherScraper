from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import datetime
import time

CANTIDAD_JSON = 200

def configurar_navegador():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1200')
    return webdriver.Chrome(options=options)

def cargar_pagina(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    div = wait.until(EC.presence_of_element_located((By.ID, 'forecasts-page')))
    time.sleep(3)
    return driver.execute_script("return document.documentElement.outerHTML")

def encontrar_div(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('div', {'id': 'tabid_0_content_div'})

def obtener_datos_cabecera(tr):
    datos = tr.find_all('td')
    resultados = []
    contador = 0  # Agregar contador

    for dato in datos:
        # Salir del bucle si ya se han obtenido 50 resultados
        if contador == CANTIDAD_JSON:
            break

        # Extrae el número de punto y la hora a partir del texto de cada celda
        numero_punto = re.findall(r'\d+\.', dato.get_text())[0]
        numero_h = re.findall(r'\d+h', dato.get_text())[0]
        resultados.append(f"{numero_punto} {numero_h}")
        contador += 1  # Incrementar contador

    return resultados

def guardar_cabecera_en_archivo(tr):
    now = datetime.datetime.now()
    filename = f"DOM_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(tr.prettify())

def obtener_body(tr):
    datos = tr.find_all('td')
    
    return [dato.get_text() for i, dato in enumerate(datos) if i < CANTIDAD_JSON]
