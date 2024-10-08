import sys
import subprocess
import time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion.conexion_mysql import conectar

# Función para crear directorios si no existen
def crear_directorios():
    carpetas = ["data_buceo/WindWuru", "data_buceo/Aemet", "data_buceo/capturas", "data_buceo/viento"]
    for carpeta in carpetas:
        ruta_carpeta = os.path.join(carpeta)
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
            print(f"Directorio creado: {ruta_carpeta}")

# Función para obtener todos los valores desde la base de datos
def obtener_valores_de_bd():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ID_WINDWURU, ID_AEMET FROM configuration_data where active = 1")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            if result:
                return result
            else:
                print("No se encontraron registros en la tabla configuration_data.")
                sys.exit(1)
        except Exception as e:
            print("Error al ejecutar la consulta:", e)
            sys.exit(1)
    else:
        print("No se pudo establecer la conexión con la base de datos.")
        sys.exit(1)

wait_time = 15
ruta_ejecucion = ""
# Verificar el número de argumentos proporcionados
if len(sys.argv) == 4:
    # Obtener los valores específicos proporcionados como argumentos
    valores_especificos = [(sys.argv[1], sys.argv[2])]
else:
    # Obtener todos los valores de la base de datos
    valores_especificos = obtener_valores_de_bd()
    if len(sys.argv) == 2:
        ruta_ejecucion = sys.argv[1];
        print("La ruta de ejecucion es" + ruta_ejecucion)

# Comprobar y crear directorios si no existen
crear_directorios()

# Función para ejecutar un programa y manejar excepciones
def ejecutar_programa(programa, *args):
    try:
        # Convertir todos los argumentos a cadenas antes de pasarlos a subprocess.run
        args = [str(arg) for arg in args]
        subprocess.run(["python", programa] + list(args), check=True)
        time.sleep(wait_time)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {programa}: {e}")

# Ejecutar programas para cada conjunto de valores específicos
for valores in valores_especificos:
    valor_especifico_windwulogger, valor_especifico_temperaturalogger = valores        
    
    print("Parte 1: obtener ficheros, captura y fases lunares")
    
    #Generamos los ficheros de todos los datos y los datos de direcciones
    ejecutar_programa(ruta_ejecucion +"ObtenerDatos/WindWuLogger.py", valor_especifico_windwulogger)
    # Ejecutar TemperaturaLogger.py con el valor específico proporcionado
    ejecutar_programa(ruta_ejecucion +"ObtenerDatos/TemperaturaLogger.py", valor_especifico_temperaturalogger, valor_especifico_windwulogger)
    #Tomamos la captura
    ejecutar_programa(ruta_ejecucion +"ObtenerDatos/TomarCapturaWindWuru.py", valor_especifico_windwulogger)
    
    ejecutar_programa(ruta_ejecucion +"ObtenerDatos/ObtenerFasesLunares.py", valor_especifico_windwulogger)
    
    #Se juntan los ficheros de windwuru generales con los datos de windwuru direcciones
    ejecutar_programa(ruta_ejecucion +"ObtenerDatos/JuntarLosDatosFaseUno.py")
    #Se juntan los ficheros de fase uno con los datos de aemet
    ejecutar_programa(ruta_ejecucion +"ObtenerDatos/JuntarLosDatosFaseDos.py")

    #Se guardan los datos en la base de datos
    ejecutar_programa(ruta_ejecucion +"ObtenerDatos/GuardarDatos.py")
    print("OK")