from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import datetime
import time

CANTIDAD_JSON = 100

def configurar_navegador():
    """
    Configura el navegador para ejecutarse en modo headless y establece el tamaño de la ventana.

    Returns:
    - webdriver.Chrome: Objeto del navegador configurado.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1200')
    return webdriver.Chrome(options=options)

def cargar_pagina(driver, url):
    """
    Carga la página y espera hasta que aparezca un elemento en el DOM.

    Parameters:
    - driver (webdriver.Chrome): Objeto del navegador.
    - url (str): URL de la página.

    Returns:
    - str: HTML de la página cargada.
    """
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    div = wait.until(EC.presence_of_element_located((By.ID, 'forecasts-page')))
    time.sleep(3)
    return driver.execute_script("return document.documentElement.outerHTML")

def encontrar_div(html):
    """
    Busca el div que contiene los datos relevantes.

    Parameters:
    - html (str): HTML de la página.

    Returns:
    - BeautifulSoup.Tag: Objeto de sopa con el div encontrado.
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('div', {'id': 'tabid_0_content_div'})

def obtener_datos_cabecera(tr):
    """
    Extrae los datos de la cabecera de la tabla.

    Parameters:
    - tr (BeautifulSoup.Tag): Objeto de sopa con la fila de la cabecera.

    Returns:
    - list: Lista de datos de la cabecera.
    """
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
    """
    Guarda la cabecera de la tabla en un archivo de texto.

    Parameters:
    - tr (BeautifulSoup.Tag): Objeto de sopa con la fila de la cabecera.

    Returns:
    - None
    """
    now = datetime.datetime.now()
    filename = f"DOM_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(tr.prettify())

def obtener_body(tr):
    """
    Extrae los datos del cuerpo de la tabla.

    Parameters:
    - tr (BeautifulSoup.Tag): Objeto de sopa con la fila del cuerpo.

    Returns:
    - list: Lista de datos del cuerpo.
    """
    datos = tr.find_all('td')
    return [dato.get_text() for i, dato in enumerate(datos) if i < CANTIDAD_JSON]
