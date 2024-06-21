import os
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys
from conexion.conexion_mysql import conectar

class ProcesadorDatos:
    def __init__(self):
        self.conn = conectar()
        if self.conn is None:
            exit()

    def procesar_lunar(self):
        cursor = self.conn.cursor()
        directorio = "./data_buceo/lunar/"
        if len(sys.argv) > 2:
            ruta = sys.argv[2]
            directorio = f"{ruta}/data_buceo/lunar/"   
        try:
            self.procesar_directorio_lunar(cursor, directorio)
            cursor.close()
            return "OK"  # Retorna éxito si se procesa sin errores
        except Exception as e:
            cursor.close()
            return f"NOK: Error en procesar_aemet: {str(e)}"  # Retorna el error si ocurre alguno

    
    def procesar_directorio_lunar(self, cursor, directorio):
        # Diccionario para mapear las fases lunares a sus valores numéricos
        fases_lunares = {
            "WANING_MOON": 1,
            "NEW_MOON": 2,
            "CRESCENT_MOON": 3,
            "FULL_MOON": 4  
        }
        for filename in os.listdir(directorio):
            if filename.endswith(".json"):
                ruta_json = os.path.join(directorio, filename)
                                
                with open(ruta_json) as f:
                    datos = json.load(f)
                    for dato in datos:
                        day = dato["day"]
                        month = dato["month"]         
                        year = dato["year"]                   
                        site = dato["site"]
                        
                        # Convertir la fase lunar a su valor numérico
                        lunarPhase = fases_lunares.get(dato["lunarPhase"], None)
                        if lunarPhase is None:
                            print(f"Fase lunar desconocida: {dato['lunarPhase']}")
                            continue
                        morningHighTideTime = dato["morningHighTideTime"]                   
                        morningHighTideHeight = dato["morningHighTideHeight"]
                        eveningHighTideTime = dato["eveningHighTideTime"]
                        eveningHighTideHeight = dato["eveningHighTideHeight"]
                        coefficient0H = dato["coefficient0H"]
                        coefficient12H = dato["coefficient12H"]
                        morningLowTideTime = dato["morningLowTideTime"]
                        morningLowTideHeight = dato["morningLowTideHeight"]
                        eveningLowTideTime = dato["eveningLowTideTime"]
                        eveningLowTideHeight = dato["eveningLowTideHeight"]
                        
                                                    

                        sql = "INSERT INTO tide_table (day, month, year, site, moon_phase,  morning_high_tide_time, morning_high_tide_height, afternoon_high_tide_time, afternoon_high_tide_height, coefficient0H, coefficient12H, morning_low_tide_time, morning_low_tide_height, afternoon_low_tide_time, afternoon_low_tide_height ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE year=VALUES(year), month=VALUES(month), day=VALUES(day), site=VALUES(site), moon_phase=VALUES(moon_phase), morning_high_tide_time=VALUES(morning_high_tide_time), morning_high_tide_height=VALUES(morning_high_tide_height), afternoon_high_tide_time=VALUES(afternoon_high_tide_time), afternoon_high_tide_height=VALUES(afternoon_high_tide_height), coefficient0H=VALUES(coefficient0H), coefficient12H=VALUES(coefficient12H), morning_low_tide_time=VALUES(morning_low_tide_time), morning_low_tide_height=VALUES(morning_low_tide_height), afternoon_low_tide_time=VALUES(afternoon_low_tide_time), afternoon_low_tide_height=VALUES(afternoon_low_tide_height)"
                        val = (day, month, year, site, lunarPhase, morningHighTideTime, morningHighTideHeight, eveningHighTideTime, eveningHighTideHeight, coefficient0H, coefficient12H, morningLowTideTime, morningLowTideHeight, eveningLowTideTime, eveningLowTideHeight)
                        # Imprimir la consulta SQL y los valores de los datos
                        #print("SQL:", sql)
                        #print("Datos:", val)
                        cursor.execute(sql, val)
                
                self.conn.commit()
                os.remove(ruta_json)    
   
# Uso de la clase
procesador = ProcesadorDatos()

resultado_lunar = procesador.procesar_lunar()

