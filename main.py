import sys
import subprocess
import time
import os

# Función para crear directorios si no existen
def crear_directorios(ruta):
    carpetas = ["data_buceo/WindWuru", "data_buceo/Aemet", "data_buceo/capturas"]
    for carpeta in carpetas:
        ruta_carpeta = os.path.join(ruta, carpeta)
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
            print(f"Directorio creado: {ruta_carpeta}")
            

wait_time = 15

# Verificar si se proporcionó una ruta y valores específicos como argumentos de línea de comandos
if len(sys.argv) < 4:
    print("Por favor, proporciona la ruta donde deseas guardar los datos y los valores específicos.")
    sys.exit(1)

# Obtener la ruta proporcionada como argumento
ruta_guardado = sys.argv[1]

# Comprobar y crear directorios si no existen
crear_directorios(ruta_guardado)

# Obtener los valores específicos proporcionados como argumentos
valor_especifico_windwulogger = sys.argv[2]
valor_especifico_temperaturalogger = sys.argv[3]

# Función para ejecutar un programa y manejar excepciones
def ejecutar_programa(programa, *args):
    try:
        subprocess.run(["python", programa] + list(args), check=True)
        time.sleep(wait_time)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {programa}: {e}")

# Ejecutar WindWuLogger.py con el valor específico proporcionado
ejecutar_programa("WindWuLogger.py", valor_especifico_windwulogger, ruta_guardado)

# Ejecutar TemperaturaLogger.py con el valor específico proporcionado
ejecutar_programa("TemperaturaLogger.py", valor_especifico_temperaturalogger, ruta_guardado)


# Ejecutar TomarCapturaWindWuru.py
ejecutar_programa("TomarCapturaWindWuru.py", valor_especifico_windwulogger, ruta_guardado)
