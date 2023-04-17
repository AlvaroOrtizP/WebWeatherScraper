
import json
import prettytable as pt
from telegram import ParseMode
import telegram
from telegram.ext import CommandHandler, Updater
import generadorImagen
import obtenerDatosWeb
from io import BytesIO
import yaml

#INICIO BOT 

# Definir token del bot
with open('config.yaml') as f:
    config = yaml.safe_load(f)

TOKEN = config['bot_token']

# Inicializar bot
bot = telegram.Bot(token=TOKEN)

# Funciones para los comandos
def saludar(update, context):
    message = "¡Hola! ¿Cómo estás?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def tiempo(update, context):

    img = generadorImagen.crear_imagen(json.loads(main()))
    # Convertimos la imagen a bytes para poder enviarla
    imagen_bytes = BytesIO()
    img.save(imagen_bytes, format='PNG')
    imagen_bytes.seek(0)
    
    # Enviamos la imagen al usuario
    bot = context.bot
    bot.send_photo(chat_id=update.effective_chat.id, photo=imagen_bytes)
    
    # Cerramos la imagen
    imagen_bytes.close()
    
    

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



# ID de los elementos HTML que se van a buscar en la página
DOM_CABECERA = 'tabid_0_0_dates'
DOM_V_VIENTO = 'tabid_0_0_WINDSPD'
DOM_RAFAGAS_VIENTO = 'tabid_0_0_GUST'
DOM_OLA_ALTURA = 'tabid_0_0_HTSGW'
DOM_DIRECCION = 'tabid_0_0_SMER'
DOM_PERIODO_OLAS = 'tabid_0_0_PERPW'
DOM_DIRECCION_OLAS = ''
DOM_TEMPERATURA_TIERRA = 'tabid_0_0_TMPE'


def main():
    driver = obtenerDatosWeb.configurar_navegador()
    url = 'https://www.windguru.cz/179761'
    try:
        html = obtenerDatosWeb.cargar_pagina(driver, url)
        div = obtenerDatosWeb.encontrar_div(html)
        tr = div.find('tr', {'id': DOM_CABECERA})
        resultados = obtenerDatosWeb.obtener_datos_cabecera(tr)    

        datos = [resultados]
        filas = [DOM_V_VIENTO,DOM_RAFAGAS_VIENTO,DOM_OLA_ALTURA,DOM_PERIODO_OLAS,DOM_TEMPERATURA_TIERRA]
        for f in filas:
            datos.append(obtenerDatosWeb.obtener_body(tr.find_next('tr', {'id': f})))

        driver.quit()
        return crear_json_padre(datos)
    except Exception as e:
        print(f"Error al obtener los datos web: {e}")
        driver.quit()
        return None
