from database import get_connection
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError
from datetime import date

def get_all(fecha_inicio: date, fecha_fin: date):
    """
    Obtiene todas las ventas realizadas en un rango de fechas.

    Args:
        fecha_inicio (date): Fecha inicial del rango.
        fecha_fin (date): Fecha final del rango.

    Returns:
        list: Lista de ventas.

    Raises:
        DatabaseError: Si ocurre un error en la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT v.id_venta, v.fecha, v.total, e.nombre AS nombre_empleado, c.email AS email_cliente
            FROM venta v
            JOIN empleado e ON v.id_empleado = e.id_empleado
            JOIN cliente c ON v.id_cliente = c.id_cliente
            WHERE v.fecha BETWEEN %s AND %s
            ORDER BY v.id_venta
        """, (fecha_inicio, fecha_fin))
        return cur.fetchall()
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en get_all ventas: {e}")
        raise
    finally:
        cur.close()
        conn.close()

def get_by_id(id: int):
    """
    Obtiene una venta por su ID.

    Args:
        id (int): ID de la venta.

    Returns:
        dict: Venta.

    Raises:
        DatabaseError: Si ocurre un error en la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.executr("""
            SELECT v.id_venta, v.fecha, v.total, e.nombre AS nombre_empleado, c.email AS email_cliente
            FROM venta v
            JOIN empleado e ON v.id_empleado = e.id_empleado
            JOIN cliente c ON v.id_cliente = c.id_cliente
            WHERE v.id_venta = %s
        """, (id))
    except DatabaseError as e:
        print(f"Error de base de datos en get_by_id ventas: {e}")
        raise
    finally:
        cur.close()
        conn.close()

def get_productos_by_id(id: int):
    """
    Obtiene los productos de una venta por su ID.

    Args:
        id (int): ID de la venta.

    Returns:
        list: Lista de productos de la venta.

    Raises:
        DatabaseError: Si ocurre un error en la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.executr("""
            SELECT p.id_producto, p.nombre, dv.precio_unitario, dv.cantidad
            FROM detalle_venta dv
            JOIN producto p ON dv.id_producto = p.id_producto
            WHERE dv.id_venta = %s
        """, (id))
        return cur.fetchall()
    except DatabaseError as e:
        print(f"Error de base de datos en get_productos_by_id ventas: {e}")
        raise
    finally:
        cur.close()
        conn.close()

def create(id_cliente: int, id_empleado: int, fecha: date, total: float):
    """
    Crea una nueva venta.

    Args:
        id_cliente (int): ID del cliente.
        id_empleado (int): ID del empleado.
        fecha (date): Fecha de la venta.
        total (float): Total de la venta.

    Returns:
        dict: Venta creada.

    Raises:
        DatabaseError: Si ocurre un error en la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            INSERT INTO venta (id_cliente, id_empleado, fecha, total) VALUES (%s, %s, %s, %s) RETURNING *
        """, (id_cliente, id_empleado, fecha, total))
        venta = cur.fetchone()
        conn.commit()
        return venta
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en create ventas: {e}")
        raise
    finally:
        cur.close()
        conn.close()

def delete(id: int):
    """
    Elimina una venta.

    Args:
        id (int): ID de la venta.

    Returns:
        dict: Venta eliminada.

    Raises:
        DatabaseError: Si ocurre un error en la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            DELETE FROM venta WHERE id_venta = %s RETURNING *
        """, (id))
        venta = cur.fetchone()
        conn.commit()
        return venta
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en delete ventas: {e}")
        raise
    finally:
        cur.close()
        conn.close()
