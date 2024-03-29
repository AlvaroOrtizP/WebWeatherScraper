from geopy.geocoders import Nominatim

def obtener_coordenadas_lugar(nombre_lugar):
    # Inicializar el geocoder con el proveedor Nominatim
    geolocator = Nominatim(user_agent="my_geocoder")
    
    # Realizar la solicitud de geocodificación
    location = geolocator.geocode(nombre_lugar)
    
    # Verificar si se obtuvieron resultados de geocodificación
    if location:
        latitud = location.latitude
        longitud = location.longitude
        return latitud, longitud
    else:
        print("No se encontraron coordenadas para el lugar especificado.")
        return None, None

