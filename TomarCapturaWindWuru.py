from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime

def capture_website_screenshot(url, screenshot_path, scroll_percent=15, wait_time=5):
    # Configuración de Selenium con un navegador (por ejemplo, Chrome)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo sin cabeza (sin interfaz gráfica)
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Abrir la página
        driver.get(url)

        # Esperar unos segundos para que la página se cargue completamente
        time.sleep(wait_time)

        # Calcular la posición de desplazamiento en píxeles
        total_height = int(driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"))
        scroll_height = int(total_height * (scroll_percent / 100))

        # Desplazar la página hacia abajo
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")

        # Esperar un breve momento después de desplazar la página
        time.sleep(2)

        # Captura de pantalla
        driver.save_screenshot(screenshot_path)

    finally:
        # Cerrar el navegador, incluso si ocurre una excepción
        driver.quit()

if __name__ == "__main__":
    # URL de la página web que deseas capturar
    target_url = "https://www.windguru.cz/487006"
    
    fecha_actual = datetime.datetime.now().strftime("%Y_%m_%d")
    
    # Construir el nombre del archivo con la fecha
    nombre_archivo = f"capturas/windguru_{fecha_actual}.png"

    # Porcentaje de desplazamiento hacia abajo (ajustable)
    scroll_percent = 15

    # Tiempo de espera antes de tomar la captura (ajustable)
    wait_time = 3

    # Capturar la pantalla de la web con desplazamiento hacia abajo
    capture_website_screenshot(target_url, nombre_archivo, scroll_percent, wait_time)
