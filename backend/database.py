import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Crea y retorna una conexión a la base de datos PostgreSQL.

    La conexión se configura a partir de variables de entorno:
    - DB_HOST
    - DB_PORT
    - DB_NAME
    - DB_USER
    - DB_PASSWORD

    Returns:
        connection: Objeto de conexión a la base de datos.

    Raises:
        psycopg2.DatabaseError: Si ocurre un error al establecer la conexión.
    """
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
    except psycopg2.DatabaseError as e:
        print(f"Error al conectarse a la base de datos: {e}")
        raise e