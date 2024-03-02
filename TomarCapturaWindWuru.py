from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
import sys 
import json

def capture_website_screenshot(url, screenshot_path, scroll_percent=15, wait_time=1):
    print("Iniciando captura de pantalla...")
    
    # Configuración de Selenium con un navegador (por ejemplo, Chrome)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo sin cabeza (sin interfaz gráfica)
    
    # Inicializar el navegador
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Abrir la página
        print(f"Cargando página: {url}")
        driver.get(url)

        # Esperar unos segundos para que la página se cargue completamente
        time.sleep(wait_time)

        # Calcular la posición de desplazamiento en píxeles
        total_height = int(driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"))
        scroll_height = int(total_height * (scroll_percent / 100))

        # Desplazar la página hacia abajo
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")

        # Captura de pantalla
        print(f"Capturando pantalla y guardando en: {screenshot_path}")
        driver.save_screenshot(screenshot_path)

        print("Captura de pantalla exitosa.")
    except Exception as e:
        print(f"Error al capturar la pantalla: {e}")
        return json.dumps({"error": str(e)})
    finally:
        # Cerrar el navegador, incluso si ocurre una excepción
        driver.quit()
        print("Navegador cerrado.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporciona el ID de la playa.")
        sys.exit(1)
        
    print("------------------------------------------------------------------------------------------------")
    print("TOMAR CAPTURA WIND WURU")
    
    id_playa = sys.argv[1]
    
    # URL de la página web que deseas capturar
    target_url = f'https://www.windguru.cz/{id_playa}'
    
    # Obtener la fecha y hora actual
    fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")

    # Obtener la ruta del directorio proporcionada por el usuario (si está disponible)
    ruta_guardado = sys.argv[2] if len(sys.argv) > 2 else ""

    # Construir el nombre del archivo con la fecha y hora
    nombre_archivo = f"{ruta_guardado}data_buceo/capturas/windguru_{fecha_actual}.png"

    # Porcentaje de desplazamiento hacia abajo (ajustable)
    scroll_percent = 15

    # Capturar la pantalla de la web con desplazamiento hacia abajo
    resultado = capture_website_screenshot(target_url, nombre_archivo, scroll_percent)
    if resultado:
        print("Error al capturar la pantalla.")
        with open(nombre_archivo.replace(".png", ".json"), "w") as f:
            f.write(resultado)
    else:
        print(f"TOMAR_CAPTURA: Datos guardados correctamente en {nombre_archivo}")
    print("------------------------------------------------------------------------------------------------")
