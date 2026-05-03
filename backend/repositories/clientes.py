from database import get_connection
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError

def get_all():
    """
    Obtiene todos los clientes.

    Returns:
        list: Lista de clientes.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM cliente ORDER BY id_cliente")
        return cur.fetchall()
    except DatabaseError as e:
        print(f"Error de base de datos en get_all cliente: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def get_active():
    """
    Obtiene los clientes activos.

    Returns:
        list: Lista de clientes activos.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT id_cliente
            FROM cliente
            WHERE id_cliente IN (
                SELECT DISTINCT id_cliente
                FROM venta
                WHERE fecha >= CURRENT_DATE - INTERVAL '1 month'
            )
            ORDER BY id_cliente
        """)
        rows = cur.fetchall()
        return [row["id_cliente"] for row in rows]
    except DatabaseError as e:
        print(f"Error de base de datos en get_active cliente: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def create(nombre: str, email: str):
    """
    Crea un nuevo cliente.

    Args:
        nombre (str): Nombre del cliente.
        email (str): Correo electrónico del cliente.

    Returns:
        dict: Cliente creado con su ID asignado.

    Raises:
        DatabaseError: Si ocurre un error al crear el cliente.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("INSERT INTO cliente (nombre, email) VALUES (%s, %s) RETURNING *", (nombre, email))
        cliente = cur.fetchone()
        conn.commit()
        return cliente
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en create cliente: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def update(id: int, nombre: str, email: str):
    """
    Actualiza un cliente existente.

    Args:
        id (int): ID del cliente a actualizar.
        nombre (str): Nuevo nombre del cliente.
        email (str): Nuevo correo electrónico del cliente.

    Returns:
        dict: Cliente actualizado.

    Raises:
        DatabaseError: Si ocurre un error al actualizar el cliente.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("UPDATE cliente SET nombre = %s, email = %s WHERE id_cliente = %s RETURNING *", (nombre, email, id))
        cliente = cur.fetchone()
        conn.commit()
        return cliente
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en update cliente: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def delete(id: int):
    """
    Elimina un cliente por su ID.

    Args:
        id (int): ID del cliente a eliminar.

    Returns:
        dict: Cliente eliminado.

    Raises:
        DatabaseError: Si ocurre un error al eliminar el cliente.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE FROM cliente WHERE id_cliente = %s RETURNING *", (id,))
        cliente = cur.fetchone()
        conn.commit()
        return cliente
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en delete cliente: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()    
