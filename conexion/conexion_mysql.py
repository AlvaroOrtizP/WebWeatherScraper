
import mysql.connector

def conectar():
    # Detalles de conexión
    host = "localhost"
    user = "deepdiverecord"
    password = "deepdiverecord"
    database = "deepdiverecord"

    # Conexión a la base de datos
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            print("Conexión exitosa a la base de datos")
        return conn
    except mysql.connector.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

