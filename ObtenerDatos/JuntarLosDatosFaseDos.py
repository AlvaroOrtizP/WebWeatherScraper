import os
import json
import datetime
import shutil  # Importado para mover archivos

def cargar_datos_json(ruta_json):
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def obtener_fichero_mas_reciente(carpeta, codigo_playa):
    # Listar todos los archivos en la carpeta de AEMET que coincidan con el código de la playa
    archivos = [f for f in os.listdir(carpeta) if f.startswith(f"datos_aemet_{codigo_playa}_") and f.endswith(".json")]
    
    if not archivos:
        return None
    
    # Ordenar los archivos por fecha extraída del nombre (asumiendo que la fecha está en el formato YYYYMMDD)
    archivos.sort(reverse=True, key=lambda f: f.split('_')[-1].replace('.json', ''))
    
    # Devolver el archivo más reciente
    return os.path.join(carpeta, archivos[0])

def mover_archivos_a_errores(archivos):
    carpeta_errores = "./data_buceo/ficherosErrores/"
    
    if not os.path.exists(carpeta_errores):
        os.makedirs(carpeta_errores)
    
    for archivo in archivos:
        if os.path.exists(archivo):
            shutil.move(archivo, carpeta_errores)
            print(f"Archivo {archivo} movido a {carpeta_errores}")

def procesar_fase_dos(codigo_playa):
    carpeta_aemet = "./data_buceo/Aemet/"
    carpeta_res = "./data_buceo/res/"
    
    if not os.path.exists(carpeta_res):
        os.makedirs(carpeta_res)

    # Obtener el fichero más reciente de AEMET para la playa especificada
    ruta_aemet = obtener_fichero_mas_reciente(carpeta_aemet, codigo_playa)
    if ruta_aemet is None:
        print(f"No se encontró ningún archivo de AEMET para la playa con código {codigo_playa}.")
        #return
    
    print(f"Fichero AEMET más reciente: {ruta_aemet}")

    # Nombre del archivo de FaseUno
    fecha_actual = datetime.datetime.now()
    ruta_fase_uno = os.path.join(carpeta_res, f"FaseUno_{codigo_playa}_{fecha_actual.strftime('%Y_%m_%d')}.json")

    try:
        # Cargar datos de AEMET
        datos_aemet = cargar_datos_json(ruta_aemet)
        print(f"Datos AEMET cargados: {ruta_aemet}")

        # Cargar datos de Fase Uno
        datos_fase_uno = cargar_datos_json(ruta_fase_uno)
        print(f"Datos Fase Uno cargados: {ruta_fase_uno}")

        # Crear un diccionario para asociar las fechas de AEMET con sus datos
        aemet_por_fecha = {}
        for entrada in datos_aemet:
            fecha = entrada['fecha']  # Ejemplo: "20240922"
            aemet_por_fecha[fecha] = {
                't_agua': entrada['t_agua'],
                'f1': entrada['estado_cielo']['f1'],
                'descripcion1': entrada['estado_cielo']['descripcion1'],
                'f2': entrada['estado_cielo']['f2'],
                'descripcion2': entrada['estado_cielo']['descripcion2']
            }

        # Combinar los datos de Fase Uno con los de AEMET
        for dia_fase_uno in datos_fase_uno:
            dia_ano = int(dia_fase_uno['dia_ano'])  # Día del año en FaseUno
            fecha_fase_uno = datetime.datetime(int(dia_fase_uno['anno']), 1, 1) + datetime.timedelta(days=dia_ano - 1)
            fecha_fase_uno_str = fecha_fase_uno.strftime("%Y%m%d")  # Formato "20240922" para comparar con AEMET

            # Si encontramos datos de AEMET para la misma fecha, los añadimos
            if fecha_fase_uno_str in aemet_por_fecha:
                datos_aemet_dia = aemet_por_fecha[fecha_fase_uno_str]

                for momento in dia_fase_uno['momentos']:
                    # Añadir la temperatura del agua
                    momento['t_agua'] = datos_aemet_dia['t_agua']

                    # Añadir el estado del cielo según la hora
                    hora = int(momento['hora'])
                    if hora < 13:  # Si la hora es inferior a 13, usar f1 y descripcion1
                        momento['f'] = datos_aemet_dia['f1']
                        momento['descripcion'] = datos_aemet_dia['descripcion1']
                    else:  # Si la hora es 13 o mayor, usar f2 y descripcion2
                        momento['f'] = datos_aemet_dia['f2']
                        momento['descripcion'] = datos_aemet_dia['descripcion2']

        # Guardar el resultado combinado en un nuevo archivo FaseDos
        ruta_fase_dos = os.path.join(carpeta_res, f"FaseDos_{codigo_playa}_{fecha_actual.strftime('%Y%m%d')}.json")
        with open(ruta_fase_dos, 'w', encoding='utf-8') as f:
            json.dump(datos_fase_uno, f, ensure_ascii=False, indent=4)
        carpeta_historico = "./data_buceo/historico/"
        shutil.move(ruta_aemet, os.path.join(carpeta_historico, os.path.basename(ruta_aemet)))
        shutil.move(ruta_fase_uno, os.path.join(carpeta_historico, os.path.basename(ruta_fase_uno)))
        print(f"Datos combinados guardados en: {ruta_fase_dos}")

    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
        mover_archivos_a_errores([ruta_aemet, ruta_fase_uno])  # Mover ambos archivos en caso de error

    except Exception as e:
        print(f"Error al procesar los archivos: {e}")
        mover_archivos_a_errores([ruta_aemet, ruta_fase_uno])  # Mover ambos archivos en caso de error

if __name__ == "__main__":
    codigo_playa = "487006"  # Cambia este código según sea necesario
    procesar_fase_dos(codigo_playa)
