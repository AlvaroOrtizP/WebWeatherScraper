# Proyecto de Obtención de Datos Meteorológicos
Este proyecto tiene como objetivo recopilar datos meteorológicos de dos fuentes: [Windguru](https://www.windguru.cz/) y la Agencia Estatal de Meteorología [AEMET](https://www.aemet.es/). Además, realiza capturas de pantalla de la web Windguru.

# Ejecución

Ejecucion previa dentro del directorio donde se encuentra el archivo:
```bash
pip install .
```

Ejecución completa:
```bash
python .\Main.py <indicador windwuru> <identificador playa aemet>
```
```bash
python .\Main.py 487006 play_v2_3900602
```

Ejecuciones parciales:

```bash
python TemperaturaLogger.py <identificador playa aemet>
```


```bash
python TomarCapturaWindWuru.py <indicador windwuru>
```


```bash
python WindWuLogger.py <indicador windwuru>
```


# Datos Obtenidos
Ejemplo de JSON obtenido de Windguru:

 ```json
[
  "\"16. 19h\"": {
        "id_playa": "487006",
        "fecha": "16. 19h",
        "viento": "3",
        "rafagas": "4",
        "olas_altura": "0.9",
        "periodo_olas": "9",
        "temperatura_tierra": "16"
    },
    "\"16. 21h\"": {
        "id_playa": "487006",
        "fecha": "16. 21h",
        "viento": "4",
        "rafagas": "5",
        "olas_altura": "0.9",
        "periodo_olas": "9",
        "temperatura_tierra": "15"
    }
]
 ```


Ejemplo de JSON obtenido de AEMET:

 ```json
[
  {
    "id_playa": "play_v2_3900602",
    "fecha": "20240316",
    "t_agua": "13",
    "estado_cielo": {
      "f1": "120",
      "descripcion1": "muy nuboso",
      "f2": "120",
      "descripcion2": "muy nuboso"
    }
  },
  {
    "id_playa": "play_v2_3900602",
    "fecha": "20240317",
    "t_agua": "13",
    "estado_cielo": {
      "f1": "120",
      "descripcion1": "muy nuboso",
      "f2": "120",
      "descripcion2": "muy nuboso"
    }
  }
]
 ```


Ejemplo de JSON obtenido de tomorrow (viento):

 ```json
{
    "timelines": {
       "hourly": [
                  {
                "time": "2024-03-29T20:00:00Z",
                "values": {
                    "cloudBase": 0.15,
                    "cloudCeiling": 0.15,
                    "cloudCover": 100,
                    "dewPoint": 8.31,
                    "freezingRainIntensity": 0,
                    "humidity": 92,
                    "iceAccumulation": 0,
                    "iceAccumulationLwe": 0,
                    "precipitationProbability": 20,
                    "pressureSurfaceLevel": 993.84,
                    "rainAccumulation": 0.98,
                    "rainAccumulationLwe": 0.39,
                    "rainIntensity": 0.32,
                    "sleetAccumulation": 0,
                    "sleetAccumulationLwe": 0,
                    "sleetIntensity": 0,
                    "snowAccumulation": 0,
                    "snowAccumulationLwe": 0,
                    "snowIntensity": 0,
                    "temperature": 9.5,
                    "temperatureApparent": 9.5,
                    "uvHealthConcern": 0,
                    "uvIndex": 0,
                    "visibility": 6.35,
                    "weatherCode": 4000,
                    "windDirection": 235.38,
                    "windGust": 1.81,
                    "windSpeed": 0.88
                }
            },
 ```

Ejemplo de captura de pantalla
![Captura de Pantalla de Windguru](data_buceo/capturas/windguru_2024_03_29_16_25.png)

