from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime
import time
import re


# Configurar el navegador para usar Chrome en modo headless
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1200')

# Iniciar el navegador y cargar la página
driver = webdriver.Chrome(options=options)
url = 'https://www.windguru.cz/179761'
driver.get(url)

# Esperar hasta que el elemento div se cargue en la página
wait = WebDriverWait(driver, 10)
div = wait.until(EC.presence_of_element_located((By.ID, 'forecasts-page')))

# Esperar 5 segundos adicionales para que la página se cargue completamente
time.sleep(3)

# Obtener el HTML completo de la página después de la carga completa
html = driver.execute_script("return document.documentElement.outerHTML")

# Analizar el HTML con BeautifulSoup y encontrar el elemento div necesario
soup = BeautifulSoup(html, 'html.parser')


#Guardamos el div con los datos en una variable

div = soup.find('div', {'id': 'tabid_0_content_div'})



#BUSCAR LOS DIAS
# busca el tr con el id especificado dentro del tbody
tr = div.find('tr', {'id': 'tabid_0_0_dates'})



tr = div.find('tr', {'id': 'tabid_0_0_dates'})
datos = tr.find_all('td')

# Obtener números que terminan en "."
numeros_punto = [re.findall(r'\d+\.', dato.get_text()) for dato in datos]

# Obtener números que terminan en "h"
numeros_h = [re.findall(r'\d+h', dato.get_text()) for dato in datos]

#Obtener el header en formato json
resultados = []
for dato in datos:
    numero_punto = re.findall(r'\d+\.', dato.get_text())[0]
    numero_h = re.findall(r'\d+h', dato.get_text())[0]
    resultados.append(f"{numero_punto} {numero_h}")
    
print("-----------------")
print("Cabecera con los dias / horas")
print(resultados)
print("-----------------")






now = datetime.datetime.now()
filename = f"DOM_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
# Escribir el DOM en un archivo de texto en el mismo directorio que el script
with open(filename, 'w', encoding='utf-8') as file:
    file.write(tr.prettify())
    
driver.quit()

