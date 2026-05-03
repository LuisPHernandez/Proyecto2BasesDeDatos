from database import get_connection
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError

def get_all():
    """
    Obtiene todos los proveedores.

    Returns:
        list: Lista de proveedores.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM proveedor ORDER BY id_proveedor")
        return cur.fetchall()
    except DatabaseError as e:
        print(f"Error de base de datos en get_all proveedor: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def create(nombre: str, email: str):
    """
    Crea un nuevo proveedor.

    Args:
        nombre (str): Nombre del proveedor.
        email (str): Correo electrónico del proveedor.

    Returns:
        dict: Proveedor creado con su ID asignado.

    Raises:
        DatabaseError: Si ocurre un error al crear el proveedor.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("INSERT INTO proveedor (nombre, email) VALUES (%s, %s) RETURNING *", (nombre, email))
        proveedor = cur.fetchone()
        conn.commit()
        return proveedor
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en create proveedor: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def update(id: int, nombre: str, email: str):
    """
    Actualiza un proveedor existente.

    Args:
        id (int): ID del proveedor a actualizar.
        nombre (str): Nuevo nombre del proveedor.
        email (str): Nuevo correo electrónico del proveedor.

    Returns:
        dict: Proveedor actualizado.

    Raises:
        DatabaseError: Si ocurre un error al actualizar el proveedor.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("UPDATE proveedor SET nombre = %s, email = %s WHERE id_proveedor = %s RETURNING *", (nombre, email, id))
        proveedor = cur.fetchone()
        conn.commit()
        return proveedor
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en update proveedor: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def delete(id: int):
    """
    Elimina un proveedor por su ID.

    Args:
        id (int): ID del proveedor a eliminar.

    Returns:
        dict: Proveedor eliminado.

    Raises:
        DatabaseError: Si ocurre un error al eliminar el proveedor.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE FROM proveedor WHERE id_proveedor = %s RETURNING *", (id,))
        proveedor = cur.fetchone()
        conn.commit()
        return proveedor
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en delete proveedor: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()    
