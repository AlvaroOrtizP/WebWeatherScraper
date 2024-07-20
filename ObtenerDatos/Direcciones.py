import os
import sys
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
import re

# Agregar el path al módulo de conexión
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'conexion')))
from conexion_mysql import conectar

# Obtener el directorio actual del script
script_dir = os.path.dirname(__file__)

# Construir la ruta completa al directorio donde están los archivos
ruta_direccionesClimatologicas_txt = os.path.join(script_dir, '..', 'data_buceo', 'WindWuru')

# Obtener el nombre del archivo en la ruta
nombre_archivo = [f for f in os.listdir(ruta_direccionesClimatologicas_txt) if re.match(r'direccionesClimatologicas\d+\.txt', f)][0]
ruta_completa = os.path.join(ruta_direccionesClimatologicas_txt, nombre_archivo)

# Extraer el id_playa del nombre del archivo
id_playa = re.search(r'direccionesClimatologicas(\d+)\.txt', nombre_archivo).group(1)

# Función para limpiar caracteres no deseados
def limpiar_dato(dato):
    return dato.replace('�', '')  # Reemplazar � con vacío

# Función para separar las letras y los números de una dirección
def separar_direccion(direccion):
    match = re.match(r'([A-Z]+) \((\d+)\)', direccion)
    if match:
        return match.group(1), match.group(2)
    return None, None

# Leer el contenido del archivo
try:
    print("------------------------------------------------------------------------------------------------")
    print("Comienza el proceso de Direcciones")
    with open(ruta_completa, 'r', encoding='utf-8', errors='replace') as archivo:
        contenido = archivo.read()

    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(contenido, 'html.parser')

    # Encontrar los <tr> con id "tabid_0_0_SMER", "tabid_0_0_DIRPW" y "tabid_0_0_dates"
    tr_smer = soup.find('tr', id='tabid_0_0_SMER') #viento
    tr_dirpw = soup.find('tr', id='tabid_0_0_DIRPW') #olas
    tr_dates = soup.find('tr', id='tabid_0_0_dates') 

    # Crear una lista para almacenar los resultados
    resultados = []

    # Extraer el contenido de los elementos <span> encontrados en tr_dates
    horas = []
    dias = []
    if tr_dates:
        tds_dates = tr_dates.find_all('td', class_='tcell')
        for td in tds_dates:
            # Verificar que el <td> tenga al menos 4 elementos
            if len(td.contents) >= 4:
                dia_mes = td.contents[2].strip().replace('.', '')
                hora = td.contents[4].strip().replace('h', '')
                horas.append(hora)
                dias.append(int(dia_mes))
                resultados.append(f"DATE: {dia_mes} - HOUR: {hora}")

    # Extraer el contenido de los elementos <span> encontrados en tr_smer
    smer_datos = []
    if tr_smer:
        spans_smer = tr_smer.find_all('span', title=True)
        for span in spans_smer:
            dato_limpio = limpiar_dato(span['title'])
            smer_datos.append(dato_limpio)
            resultados.append(f"SMER: {dato_limpio}")

    # Extraer el contenido de los elementos <span> encontrados en tr_dirpw
    dirpw_datos = []
    if tr_dirpw:
        spans_dirpw = tr_dirpw.find_all('span', title=True)
        for span in spans_dirpw:
            dato_limpio = limpiar_dato(span['title'])
            dirpw_datos.append(dato_limpio)
            resultados.append(f"DIRPW: {dato_limpio}")

    # Conectar a la base de datos
    conn = conectar()
    if conn is None:
        exit()

    # Obtener el cursor
    cursor = conn.cursor()

    # Escribir los resultados en el archivo (sobrescribirlo)
    with open(ruta_completa, 'w', encoding='utf-8') as archivo:
        for resultado in resultados:
            archivo.write(f"{resultado}\n")

    print("El archivo ha sido sobrescrito con los datos extraídos.")

    # Obtener la fecha actual
    hoy = datetime.date.today()

    # Imprimir los datos requeridos e insertar en la base de datos
    if horas and smer_datos and dirpw_datos:
        print(f"Fecha actual: {hoy}")
        current_date = hoy
        for i in range(min(len(horas), len(smer_datos), len(dirpw_datos))):
            current_date = current_date.replace(day=dias[i])
            # Verificar si se ha de cambiar el mes/año
            if i > 0 and dias[i] < dias[i - 1]:
                # Si el día actual es menor que el anterior, incrementar el mes
                current_date += relativedelta(months=1)

            smer_letras, smer_numeros = separar_direccion(smer_datos[i])
            dirpw_letras, dirpw_numeros = separar_direccion(dirpw_datos[i])

            #print(f"ID_PLAYA: {id_playa}, YEAR: {current_date.year}, MONTH: {current_date.month}, DAY: {current_date.day}, HOUR: {horas[i]}, SMER: {smer_letras} {smer_numeros}, DIRPW: {dirpw_letras} {dirpw_numeros}")

            # Completa tu sentencia SQL correctamente aquí
            sql = "UPDATE wind_conditions SET wind_direction=%s, wind_direction_nm=%s, wave_direction=%s, wave_direction_nm=%s WHERE year=%s AND month=%s AND day=%s AND site=%s AND time_of_day= %s"
            val = ( smer_numeros, smer_letras, dirpw_numeros, dirpw_letras, current_date.year, current_date.month, current_date.day, id_playa, horas[i])
            
            #print(sql)
            #print(val)
            cursor.execute(sql, val)
        conn.commit()  # Confirmar cambios en la base de datos
        
        print("Finaliza el proceso de Direcciones")
        print("------------------------------------------------------------------------------------------------")
        
        # Eliminar el archivo
        os.remove(ruta_completa)
        print(f"Archivo {ruta_completa} eliminado correctamente.")
except FileNotFoundError:
    print(f"El archivo {ruta_completa} no fue encontrado.")
except Exception as e:
    print(f"Ocurrió un error al procesar el archivo: {str(e)}")
finally:
    cursor.close()  # Cerrar el cursor
    conn.close()  # Cerrar la conexión a la base de datos"WHERE year=%s AND month=%s AND day=%s AND site=%s AND time_of_day > '14'"WHERE year=%s AND month=%s AND day=%s AND site=%s AND time_of_day > '14'
