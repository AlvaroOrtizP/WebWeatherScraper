import os
import json
import datetime
from dateutil.relativedelta import relativedelta
from conexion.conexion_mysql import conectar

class ProcesadorDatos:
    def __init__(self):
        self.conn = conectar()
        if self.conn is None:
            exit()

    def procesar_windwuru(self):
        cursor = self.conn.cursor()

        directorio = "./data_buceo/WindWuru/"
        self.procesar_directorio_windwuru(cursor, directorio)

        cursor.close()

    def procesar_aemet(self):
        cursor = self.conn.cursor()

        directorio = "./data_buceo/Aemet/"
        self.procesar_directorio_aemet(cursor, directorio)

        cursor.close()

    def procesar_directorio_windwuru(self, cursor, directorio):
        for filename in os.listdir(directorio):
            if filename.endswith(".json"):
                ruta_json = os.path.join(directorio, filename)

                nombre_archivo = os.path.basename(filename)
                partes_nombre = nombre_archivo.split("_")

                año = partes_nombre[1]
                mes = partes_nombre[2].lstrip("0")
                dia = partes_nombre[3].split(".")[0]
                horaAuxiliar = 0
                fecha_inicial = datetime.datetime(int(año), int(mes), int(dia))

                with open(ruta_json) as f:
                    datos = json.load(f)
                    print("ruta json: " + ruta_json)
                    for clave, dato in datos.items():
                        fecha = dato["fecha"]
                        partes_fecha = fecha.split(".")
                        hora = partes_fecha[1].split("h")[0]
                        #Aumento de dia
                        if horaAuxiliar > int(hora):
                            # Si la hora actual es menor que la hora anterior, se aumenta el día
                            fecha_inicial += relativedelta(days=1)

                        horaAuxiliar = int(hora)
                        #Aumento de mes
                        if int(dia) > int(partes_fecha[0]):
                            
                            fecha_inicial += relativedelta(months=1)
                            fecha_inicial = fecha_inicial.replace(day=1)


                        site  = dato["id_playa"]    
                        dia = partes_fecha[0]
                        hora = partes_fecha[1].split("h")[0]
                        viento = dato["viento"]
                        rafagas = dato["rafagas"]
                        olas_altura = dato["olas_altura"]
                        periodo_olas = dato["periodo_olas"]
                        temperatura_tierra = dato["temperatura_tierra"]
                        
                        sql = "INSERT INTO windconditions (year, month, day, site, time_of_day,  wind, gusts_of_wind, wave_height, wave_period, earth_temperature) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE year=VALUES(year), month=VALUES(month), day=VALUES(day), site=VALUES(site), time_of_day=VALUES(time_of_day), wind=VALUES(wind), gusts_of_wind=VALUES(gusts_of_wind), wave_height=VALUES(wave_height), wave_period=VALUES(wave_period), earth_temperature=VALUES(earth_temperature)"
                        val = (fecha_inicial.year, fecha_inicial.month, fecha_inicial.day, site, hora, viento, rafagas, olas_altura, periodo_olas, temperatura_tierra)
                        cursor.execute(sql, val)
                
                self.conn.commit()
                os.remove(ruta_json)

    def procesar_directorio_aemet(self, cursor, directorio):
        for filename in os.listdir(directorio):
            if filename.endswith(".json"):
                ruta_json = os.path.join(directorio, filename)
                                
                with open(ruta_json) as f:
                    datos = json.load(f)
                    for dato in datos:
                        id_playa = dato["id_playa"]
                        fecha_json = dato["fecha"]         
                        año = fecha_json[:4]
                        mes = fecha_json[4:6].lstrip("0")
                        dia = fecha_json[6:].lstrip("0")                        
                        t_agua = dato["t_agua"]
                        estado_cielo = dato["estado_cielo"]
                        f1 = estado_cielo["f1"]
                        descripcion1 = estado_cielo["descripcion1"]
                        f2 = estado_cielo["f2"]
                        descripcion2 = estado_cielo["descripcion2"]
                            
                        sql = "INSERT INTO weatherdata (year, month, day, site, water_termperature, f1, descripcion1, f2, descripcion2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE year=VALUES(year), month=VALUES(month), day=VALUES(day), site=VALUES(site), water_termperature=VALUES(water_termperature), f1=VALUES(f1), descripcion1=VALUES(descripcion1), f2=VALUES(f2), descripcion2=VALUES(descripcion2)"
                        val = (año, mes, dia, id_playa, t_agua, f1, descripcion1, f2, descripcion2)                            
                        cursor.execute(sql, val)
                
                self.conn.commit()
                os.remove(ruta_json)

        self.conn.close()

# Uso de la clase
procesador = ProcesadorDatos()
procesador.procesar_windwuru()
procesador.procesar_aemet()
