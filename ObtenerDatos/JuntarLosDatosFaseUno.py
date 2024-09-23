import os
import json
import datetime
import shutil
import re  # Para usar expresiones regulares al extraer números de SMER

def cargar_datos_json(ruta_json):
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_datos_texto(ruta_txt):
    with open(ruta_txt, 'r', encoding='utf-8') as f:
        return f.readlines()

def encontrar_linea(datos_txt, palabra):
    for i, linea in enumerate(datos_txt):
        if palabra in linea:
            return i
    return -1

def ajustar_fecha(fecha_actual, incremento_dias):
    nueva_fecha = fecha_actual + datetime.timedelta(days=incremento_dias)
    return nueva_fecha

def procesar_archivos(codigo_playa):
    carpeta = "./data_buceo/WindWuru/"
    carpeta_res = "./data_buceo/res/"
    carpeta_errores = "./data_buceo/ficherosErrores/"
    
    fecha_actual = datetime.datetime.now()
    anno = fecha_actual.year
    dia_ano = fecha_actual.strftime("%j")
    
    ruta_json = os.path.join(carpeta, f"datos_{codigo_playa}_{fecha_actual.strftime('%Y_%m_%d')}.json")
    ruta_txt = os.path.join(carpeta, f"direccionesClimatologicas_{fecha_actual.strftime('%Y_%m_%d')}_{codigo_playa}.txt")
    
    try:
        datos_json = cargar_datos_json(ruta_json)
        print(f"Datos del archivo JSON cargados: {ruta_json}")

        datos_txt = cargar_datos_texto(ruta_txt)
        print(f"Datos del archivo de texto cargados: {ruta_txt}")

        linea_smer = encontrar_linea(datos_txt, "SMER:")
        linea_dirpw = encontrar_linea(datos_txt, "DIRPW:")

        if linea_smer == -1 or linea_dirpw == -1:
            print("No se encontró SMER o DIRPW en el archivo de texto.")
            raise ValueError("Faltan datos en el archivo de texto")

        resultado_combinado = []
        incremento_dias = 0
        hora_anterior = None
        momentos_dia = {
            "anno": str(anno),
            "dia_ano": dia_ano,
            "momentos": []
        }

        for i in range(len(datos_txt) // 2):
            smer_linea = linea_smer + i
            dirpw_linea = linea_dirpw + i

            if smer_linea < len(datos_txt) and dirpw_linea < len(datos_txt):
                smer = datos_txt[smer_linea].strip().split(":")[1].strip() if "SMER:" in datos_txt[smer_linea] else "No disponible"
                dirpw = datos_txt[dirpw_linea].strip().split(":")[1].strip() if "DIRPW:" in datos_txt[dirpw_linea] else "No disponible"

                # Extraer la dirección del viento y el valor numérico de SMER
                match = re.search(r'([A-Z]+)\s*\((\d+)', smer)
                if match:
                    wind_direction_nm = match.group(1)  # OSO
                    wind_direction = match.group(2)     # 258
                else:
                    wind_direction_nm = "No disponible"
                    wind_direction = "No disponible"
                    
                # Extraer la dirección de las olas y el valor numérico de DIRPW
                match_dirpw = re.search(r'([A-Z]+)\s*\((\d+)', dirpw)
                if match_dirpw:
                    wave_direction_nm = match_dirpw.group(1)  # NO
                    wave_direction = match_dirpw.group(2)     # 310
                else:
                    wave_direction_nm = "No disponible"
                    wave_direction = "No disponible"

                fecha_hora = list(datos_json.keys())[i]
                dia, hora = fecha_hora.split(".")
                
                # Eliminar ceros a la izquierda en la hora
                hora = hora.strip().replace("h", "").replace('"', '').replace("'", "").lstrip('0') or '0'
                hora_int = int(hora)

                if hora_anterior is not None and hora_int < hora_anterior:
                    incremento_dias += 1
                    resultado_combinado.append(momentos_dia)
                    
                    # Crear un nuevo momento para el siguiente día
                    nueva_fecha = ajustar_fecha(fecha_actual, incremento_dias)
                    momentos_dia = {
                        "anno": str(nueva_fecha.year),
                        "dia_ano": nueva_fecha.strftime("%j"),
                        "momentos": []
                    }

                momento = {
                    "hora": hora,
                    "id_playa": datos_json[fecha_hora]['id_playa'],
                    "viento": datos_json[fecha_hora]['viento'],
                    "rafagas": datos_json[fecha_hora]['rafagas'],
                    "olas_altura": datos_json[fecha_hora]['olas_altura'],
                    "periodo_olas": datos_json[fecha_hora]['periodo_olas'],
                    "temperatura_tierra": datos_json[fecha_hora]['temperatura_tierra'],
                    "windDirection": wind_direction,        # Valor numérico extraído
                    "windDirectionNM": wind_direction_nm,  # Dirección cardinal extraída
                    "waveDirection": wave_direction,        # Valor numérico extraído de DIRPW
                    "waveDirectionNM": wave_direction_nm   # Dirección cardinal extraída de DIRPW
                }
                momentos_dia["momentos"].append(momento)
                hora_anterior = hora_int

        # Agregar el último conjunto de momentos
        if momentos_dia["momentos"]:
            resultado_combinado.append(momentos_dia)

        fecha_formateada = fecha_actual.strftime("%Y_%m_%d")
        ruta_final_json = os.path.join(carpeta_res, f"FaseUno_{codigo_playa}_{fecha_formateada}.json")
        
        # Guardar los resultados combinados en el nuevo archivo JSON
        with open(ruta_final_json, 'w', encoding='utf-8') as f:
            json.dump(resultado_combinado, f, ensure_ascii=False, indent=4)

        print(f"Datos guardados en: {ruta_final_json}")

        # Si todo fue exitoso, borrar los archivos de entrada
        carpeta_historico = "./data_buceo/historico/"
        shutil.move(ruta_json, os.path.join(carpeta_historico, os.path.basename(ruta_json)))
        shutil.move(ruta_txt, os.path.join(carpeta_historico, os.path.basename(ruta_txt)))
        print("Archivos de entrada movidos a la carpeta histórico.")
    except Exception as e:
        print(f"Error al procesar los archivos: {e}")
        # Crear la carpeta de errores si no existe
        if not os.path.exists(carpeta_errores):
            os.makedirs(carpeta_errores)
        
        # Mover los archivos de entrada a la carpeta de errores
        shutil.move(ruta_json, os.path.join(carpeta_errores, os.path.basename(ruta_json)))
        shutil.move(ruta_txt, os.path.join(carpeta_errores, os.path.basename(ruta_txt)))
        print("Archivos de entrada movidos a la carpeta de errores.")

if __name__ == "__main__":
    codigo_playa = "487006"
    procesar_archivos(codigo_playa)
