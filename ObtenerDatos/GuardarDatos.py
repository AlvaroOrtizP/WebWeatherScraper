import os
import json
import re
import datetime
import sys
import shutil  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion.conexion_mysql import conectar
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from dotenv import load_dotenv


def obtener_mes_por_dia(año, dia_del_año):
    año = int(año)
    dia_del_año = int(dia_del_año)
    fecha = datetime.datetime(año, 1, 1) + datetime.timedelta(days=dia_del_año - 1)
    return fecha.month

def obtener_dia_por_dia(año, dia_del_año):
    año = int(año)
    dia_del_año = int(dia_del_año)
    fecha = datetime.datetime(año, 1, 1) + datetime.timedelta(days=dia_del_año - 1)
    return fecha.day
def enviar_correo(asunto, mensaje, adjuntos=None):
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()
    remitente = os.getenv("MAIL_USERNAME")
    destinatario = os.getenv("TO_MAIL_USERNAME")
    contraseña = os.getenv("MAIL_PASSWORD") 
    print(f"MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
    print(f"TO_MAIL_USERNAME: {os.getenv('TO_MAIL_USERNAME')}")
    print(f"MAIL_PASSWORD: {'*' * len(os.getenv('MAIL_PASSWORD', ''))}")  
    
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'plain'))

     # Adjuntar archivos
    if adjuntos:
        for adjunto in adjuntos:
            with open(adjunto, 'rb') as f:
                parte_adjunto = MIMEApplication(f.read(), Name=os.path.basename(adjunto))
                parte_adjunto['Content-Disposition'] = f'attachment; filename="{os.path.basename(adjunto)}"'
                msg.attach(parte_adjunto)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(remitente, contraseña)
            servidor.sendmail(remitente, destinatario, msg.as_string())
            print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        
def obtener_archivos(carpeta):
    """Obtiene todos los archivos de una carpeta."""
    if os.path.exists(carpeta):
        return [os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, archivo))]
    return []


def eliminar_archivos(carpeta):
    """Elimina todos los archivos de una carpeta."""
    if os.path.exists(carpeta):
        for archivo in os.listdir(carpeta):
            ruta_archivo = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)     
        
def procesar_archivos():
    # Conectar a la base de datos
    conn = conectar()
    if conn is None:
        exit()
    cursor = conn.cursor()
    
    # Crear carpetas si no existen
    carpeta = "./data_buceo/res/"
    carpeta_errores = "./data_buceo/ficherosErrores/"
    carpeta_historico = "./data_buceo/historico/"
    carpeta_capturas = "./data_buceo/capturas/"
    if not os.path.exists(carpeta_errores):
        os.makedirs(carpeta_errores)

    # Listar todos los archivos en la carpeta que sean .json
    archivos = [archivo for archivo in os.listdir(carpeta) if archivo.endswith(".json")]
    archivos_procesados = []
    errores = []
    # Procesar cada archivo
    for archivo in archivos:
        try:
            # Extraer la fecha desde el nombre del archivo
            partes_nombre = archivo.split("_")
            if len(partes_nombre) < 3:
                print(f"Nombre de archivo no tiene el formato esperado: {archivo}")
                continue

            identificador = partes_nombre[1]
            fecha_str = partes_nombre[2].split(".")[0]  # Remover la extensión .json
            if len(fecha_str) != 8 or not fecha_str.isdigit():
                print(f"Formato de fecha no válido en el archivo {archivo}: {fecha_str}")
                continue

            año = int(fecha_str[:4])
            mes = int(fecha_str[4:6])
            dia = int(fecha_str[6:8])
            fecha_inicial = datetime.datetime(año, mes, dia)

            # Cargar el archivo JSON
            ruta_json = os.path.join(carpeta, archivo)
            with open(ruta_json, 'r') as f:
                datos_json = json.load(f)
                momentos_procesados = 0

                if isinstance(datos_json, list):
                    for dia_fase_uno in datos_json:
                        momentos = dia_fase_uno.get("momentos", [])
                        anno = dia_fase_uno.get("anno", None)
                        dia_ano = dia_fase_uno.get("dia_ano", None)

                        mes = obtener_mes_por_dia(anno, dia_ano)
                        dia_r = obtener_dia_por_dia(anno, dia_ano)

                        for momento in momentos:
                            if momentos_procesados >= 90:
                                break

                            hora = momento.get('hora', None)
                            site = momento.get('id_playa', None)
                            viento = momento.get('viento', None)
                            windDirection = momento.get('windDirection', None)
                            windDirectionNM = momento.get('windDirectionNM', None)
                            rafagas = momento.get('rafagas', None)
                            olas_altura = momento.get('olas_altura', None)
                            periodo_olas = momento.get('periodo_olas', None)
                            waveDirection = momento.get('waveDirection', None)
                            waveDirectionNM = momento.get('waveDirectionNM', None)
                            temperatura_tierra = momento.get('temperatura_tierra', None)
                            t_agua = momento.get('t_agua', None)
                            f = momento.get('f', None)
                            descripcion = momento.get('descripcion', None)

                            # Limpiamos olas_altura y periodo_olas para evitar caracteres no deseados
                            # Primero eliminamos cualquier carácter no numérico o punto decimal
                            olas_altura = re.sub(r"[^\d.]", "", olas_altura) if olas_altura else "0"
                            periodo_olas = re.sub(r"[^\d.]", "", periodo_olas) if periodo_olas else "0"

                            # Luego, si quedaron vacíos después de la limpieza, asignamos "0"
                            olas_altura = "0" if olas_altura == "" else olas_altura
                            periodo_olas = "0" if periodo_olas == "" else periodo_olas

                            # Imprimimos los valores después de la limpieza para verificar
                            #print(f"Valores después de limpieza: olas_altura={olas_altura}, periodo_olas={periodo_olas}")





                            if None in [hora, site, viento, rafagas, olas_altura, periodo_olas, temperatura_tierra, waveDirection, waveDirectionNM]:
                                print(f"Datos incompletos en el archivo {archivo}, saltando momento: {momento}")
                                continue

                            sql = ("INSERT INTO wind_conditions (year, month, day, site, time_of_day, wind, wind_direction, "
                                   "wind_direction_nm, gusts_of_wind, wave_height, wave_period, wave_direction, wave_direction_nm, "
                                   "earth_temperature, water_temperature, condition_code, condition_description, day_of_year) "
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                                   "ON DUPLICATE KEY UPDATE year=VALUES(year), month=VALUES(month), day=VALUES(day), "
                                   "site=VALUES(site), time_of_day=VALUES(time_of_day), wind=VALUES(wind), "
                                   "wind_direction=VALUES(wind_direction), wind_direction_nm=VALUES(wind_direction_nm), "
                                   "gusts_of_wind=VALUES(gusts_of_wind), wave_height=VALUES(wave_height), "
                                   "wave_period=VALUES(wave_period), wave_direction=VALUES(wave_direction), "
                                   "wave_direction_nm=VALUES(wave_direction_nm), earth_temperature=VALUES(earth_temperature), "
                                   "water_temperature=VALUES(water_temperature), condition_code=VALUES(condition_code), "
                                   "condition_description=VALUES(condition_description), day_of_year=VALUES(day_of_year)")

                            val = (
                                anno, mes, dia_r, site, hora, viento, windDirection,
                                windDirectionNM, rafagas, olas_altura, periodo_olas, waveDirection, waveDirectionNM,
                                temperatura_tierra, t_agua, f, descripcion, dia_ano
                            )
                            
                            #print(f"Insertando en la base de datos: {val}")
                            cursor.execute(sql, val)

                            momentos_procesados += 1
                            if momentos_procesados >= 190:
                                break
                else:
                    print(f"Estructura inesperada en el archivo {archivo}, no es una lista.")
                    continue

            conn.commit()
            print(f"Procesamiento y guardado de {archivo} completado.")
            # Mover el archivo después de procesarlo
             # Si se procesa correctamente
            archivos_procesados.append(archivo)
            # Mover el archivo después de procesarlo
            archivo_historico = os.path.join(carpeta_historico, archivo)
            shutil.move(os.path.join(carpeta, archivo), archivo_historico)

        
        except Exception as e:
            print(f"Error procesando el archivo {archivo}: {str(e)}")
            # Mover archivo con error a la carpeta de errores
            archivo_error = os.path.join(carpeta_errores, archivo)
            shutil.move(os.path.join(carpeta, archivo), archivo_error)

            print(f"Archivo {archivo} movido a la carpeta de errores.")
     # Archivos de las carpetas
    adjuntos_historico = obtener_archivos(carpeta_historico)
    adjuntos_capturas = obtener_archivos(carpeta_capturas)
    adjuntos_errores = obtener_archivos(carpeta_errores)

    # Enviar correos según el resultado
    if errores:
        mensaje_error = (
            f"Se procesaron algunos archivos con errores.\n\nErrores:\n" +
            "\n".join(errores)
        )
        enviar_correo(
            "Errores en el procesamiento de archivos",
            mensaje_error,
            adjuntos=adjuntos_historico + adjuntos_capturas + adjuntos_errores
        )
    else:
        mensaje_exito = (
            "Todos los archivos fueron procesados exitosamente.\n\n" +
            f"Archivos procesados:\n" + "\n".join(archivos_procesados)
        )
        enviar_correo(
            "Reporte diario - exitoso",
            mensaje_exito,
            adjuntos=adjuntos_historico + adjuntos_capturas
        )

    eliminar_archivos(carpeta_historico)
    eliminar_archivos(carpeta_capturas)
    #eliminar_archivos(carpeta_errores)
    cursor.close()
    conn.close()
    
def eliminar_archivos(carpeta):
    """Elimina todos los archivos de una carpeta."""
    if os.path.exists(carpeta):  # Verifica que la carpeta exista
        for archivo in os.listdir(carpeta):  # Recorre todos los archivos dentro de la carpeta
            ruta_archivo = os.path.join(carpeta, archivo)  # Construye la ruta completa
            if os.path.isfile(ruta_archivo):  # Asegura que es un archivo y no un directorio
                os.remove(ruta_archivo)  # Elimina el archivo

if __name__ == "__main__":
    procesar_archivos()
