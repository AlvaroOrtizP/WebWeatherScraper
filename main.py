import sys
import subprocess
import time

wait_time = 15

# Verificar si se proporcionó una ruta como argumento de línea de comandos
#if len(sys.argv) < 2:
 #   print("Por favor, proporciona la ruta donde deseas guardar los datos.")
  #  sys.exit(1)

# Obtener la ruta proporcionada como argumento
#ruta_guardado = sys.argv[1]

# Función para ejecutar un programa y manejar excepciones
def ejecutar_programa(programa, *args):
    try:
        subprocess.run(["python", programa] + list(args), check=True)
        time.sleep(wait_time)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {programa}: {e}")

# Ejecutar WindWuLogger.py
ejecutar_programa("WindWuLogger.py")

# Ejecutar TomarCapturaWindWuru.py
ejecutar_programa("TomarCapturaWindWuru.py")

# Ejecutar TemperaturaLogger.py 
ejecutar_programa("TemperaturaLogger.py")

# Ejecutar Mezclar.py 
#ejecutar_programa("Mezclar.py")
