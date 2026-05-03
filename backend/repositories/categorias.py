from database import get_connection
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError

def get_all():
    """
    Obtiene todas las categorías.

    Returns:
        list: Lista de categorías.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM categoria ORDER BY id_categoria")
        return cur.fetchall()
    except DatabaseError as e:
        print(f"Error de base de datos en get_all categoria: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def create(nombre: str):
    """
    Crea una nueva categoría.

    Args:
        nombre (str): Nombre de la categoría.

    Returns:
        dict: Categoría creada con su ID asignado.

    Raises:
        DatabaseError: Si ocurre un error al crear la categoría.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("INSERT INTO categoria (nombre) VALUES (%s) RETURNING *", (nombre))
        categoria = cur.fetchone()
        conn.commit()
        return categoria
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en create categoria: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def update(id: int, nombre: str):
    """
    Actualiza una categoría existente.

    Args:
        id (int): ID de la categoría a actualizar.
        nombre (str): Nuevo nombre de la categoría.

    Returns:
        dict: Categoría actualizada.

    Raises:
        DatabaseError: Si ocurre un error al actualizar la categoría.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("UPDATE categoria SET nombre = %s WHERE id_categoria = %s RETURNING *", (nombre, id))
        categoria = cur.fetchone()
        conn.commit()
        return categoria
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en update categoria: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def delete(id: int):
    """
    Elimina una categoría por su ID.

    Args:
        id (int): ID de la categoría a eliminar.

    Returns:
        dict: Categoría eliminada.

    Raises:
        DatabaseError: Si ocurre un error al eliminar la categoría.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE FROM categoria WHERE id_categoria = %s RETURNING *", (id,))
        categoria = cur.fetchone()
        conn.commit()
        return categoria
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en delete categoria: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()    
