import os
import mysql.connector
from dotenv import load_dotenv
def conectar():
    # Cargar .env
    load_dotenv()

    # Detalles de conexión
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

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

