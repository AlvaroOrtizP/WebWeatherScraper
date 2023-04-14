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
import requests
import prettytable as pt
from telegram import ParseMode
import telegram
from telegram.ext import CommandHandler, Updater


#INICIO BOT 

# Definir token del bot
TOKEN = "6025769421:AAFxAQwC6nsGsKOYIjCzW5vNaFiounc8tTU"

# Inicializar bot
bot = telegram.Bot(token=TOKEN)

# Funciones para los comandos
def saludar(update, context):
    message = "¡Hola! ¿Cómo estás?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def tiempo(update, context):
    data = json.loads(main())  # json_string es la variable que contiene tu JSON
    table_data = []
    for hora, info in data.items():
        viento = info['viento']
        rafagas = info['rafagas']
        altura_olas = info['olas_altura']
        periodo_olas = info['periodo_olas']
        temp_tierra = info['temperatura_tierra']
        table_data.append((hora, viento, rafagas, altura_olas, periodo_olas, temp_tierra))
    table = pt.PrettyTable(['Hora', 'Viento', 'Ráfagas', 'Altura de olas', 'Periodo de olas', 'Temperatura tierra'], hrules=pt.ALL)
    table.align['Hora'] = 'l'
    table.align['Viento'] = 'r'
    table.align['Ráfagas'] = 'r'
    table.align['Altura de olas'] = 'r'
    table.align['Periodo de olas'] = 'r'
    table.align['Temperatura tierra'] = 'r'
    table.field_names = table.field_names
    for row in table_data:
        table.add_row(row)
    update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)
    
    

    
    



# Manejadores de comandos
saludar_handler = CommandHandler('saludar', saludar)
tiempo_handler = CommandHandler('tiempo', tiempo)

# Inicializar Updater y agregar manejadores
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(saludar_handler)
dispatcher.add_handler(tiempo_handler)

# Iniciar bot
updater.start_polling()


#FIN BOT


# ID de los elementos HTML que se van a buscar en la página
DOM_CABECERA = 'tabid_0_0_dates'
DOM_V_VIENTO = 'tabid_0_0_WINDSPD'
DOM_RAFAGAS_VIENTO = 'tabid_0_0_GUST'
DOM_OLA_ALTURA = 'tabid_0_0_HTSGW'
DOM_DIRECCION = 'tabid_0_0_SMER'
DOM_PERIODO_OLAS = 'tabid_0_0_PERPW'
DOM_DIRECCION_OLAS = ''
DOM_TEMPERATURA_TIERRA = 'tabid_0_0_TMPE'


CANTIDAD_JSON = 20


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
    # Guarda la cabecera de la tabla en un archivo de texto
    now = datetime.datetime.now()
    filename = f"DOM_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(tr.prettify())

def obtener_body(tr):
    # Extrae los datos del cuerpo de la tabla
    datos = tr.find_all('td')
    return [dato.get_text() for i, dato in enumerate(datos) if i < CANTIDAD_JSON]




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
        resultado[json.dumps(hora)] = {"viento": viento, "rafagas": rafaga, "olas_altura": ola_altura, "periodo_olas": periodo_ola, "temperatura_tierra": temperatura_tierra}

    return json.dumps(resultado)





def main():
    driver = configurar_navegador()
    url = 'https://www.windguru.cz/179761'
    html = cargar_pagina(driver, url)
    div = encontrar_div(html)
    tr = div.find('tr', {'id': DOM_CABECERA})
    resultados = obtener_datos_cabecera(tr)    
    
    #guardar_cabecera_en_archivo(div.find('tr', {'id': DOM_DIRECCION}))
    
    datos = []
    datos.append(resultados)
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_V_VIENTO})))
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_RAFAGAS_VIENTO})))
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_OLA_ALTURA})))
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_PERIODO_OLAS})))
    datos.append(obtener_body(tr.find_next('tr', {'id': DOM_TEMPERATURA_TIERRA})))
    
    
    print(crear_json_padre(datos))
    driver.quit()
    return crear_json_padre(datos)

"""""
if __name__ == '__main__':
    main()"""""
