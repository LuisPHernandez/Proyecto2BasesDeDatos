from database import get_connection
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError

def get_all():
    """
    Obtiene todos los empleados.

    Returns:
        list: Lista de empleados.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT e.id_empleado, e.nombre, COUNT(v.id_venta) AS ventas, SUM(v.total) AS ingresos
            FROM empleado e
            JOIN venta v ON e.id_empleado = v.id_empleado
            GROUP BY e.id_empleado, e.nombre
            HAVING SUM(v.total) > 1
            ORDER BY ingresos DESC
        """)
        return cur.fetchall()
    except DatabaseError as e:
        print(f"Error de base de datos en get_all empleado: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def create(nombre: str):
    """
    Crea un nuevo empleado.

    Args:
        nombre (str): Nombre del empleado.

    Returns:
        dict: Empleado creado con su ID asignado.

    Raises:
        DatabaseError: Si ocurre un error al crear el empleado.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("INSERT INTO empleado (nombre) VALUES (%s) RETURNING *", (nombre,))
        empleado = cur.fetchone()
        conn.commit()
        return empleado
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en create empleado: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def update(id: int, nombre: str):
    """
    Actualiza un empleado existente.

    Args:
        id (int): ID del empleado a actualizar.
        nombre (str): Nuevo nombre del empleado.

    Returns:
        dict: Empleado actualizado.

    Raises:
        DatabaseError: Si ocurre un error al actualizar el empleado.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("UPDATE empleado SET nombre = %s WHERE id_empleado = %s RETURNING *", (nombre, id))
        empleado = cur.fetchone()
        conn.commit()
        return empleado
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en update empleado: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def delete(id: int):
    """
    Elimina un empleado por su ID.

    Args:
        id (int): ID del empleado a eliminar.

    Returns:
        dict: Empleado eliminado.

    Raises:
        DatabaseError: Si ocurre un error al eliminar el empleado.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE FROM empleado WHERE id_empleado = %s RETURNING *", (id,))
        empleado = cur.fetchone()
        conn.commit()
        return empleado
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en delete empleado: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()    
