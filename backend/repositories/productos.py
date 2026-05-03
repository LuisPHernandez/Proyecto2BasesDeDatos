from database import get_connection
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError

def get_all():
    """
    Obtiene todos los productos con proveedor y categoría.

    Returns:
        list[dict]: Lista de productos.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT pr.*, pv.nombre as proveedor, c.nombre as categoria
            FROM producto pr
            JOIN proveedor pv ON pr.id_proveedor = pv.id_proveedor
            JOIN categoria c ON pr.id_categoria = c.id_categoria
            ORDER BY pr.id_producto
        """)
        return cur.fetchall()
    except DatabaseError as e:
        print(f"Error de base de datos en get_all productos: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def get_low_stock():
    """
    Obtiene los productos con bajo stock que han sido vendidos al menos una vez.

    Returns:
        list: Lista de productos con bajo stock.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT DISTINCT id_producto
            FROM detalle_venta
            WHERE id_producto IN (
                SELECT id_producto FROM producto WHERE unidades_disponibles < 10
            );
        """)
        rows = cur.fetchall()
        return [row["id_producto"] for row in rows]
    except DatabaseError as e:
        print(f"Error de base de datos en get_low_stock productos: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def get_by_id(id: int):
    """
    Obtiene un producto por su ID.

    Args:
        id (int): Identificador del producto.

    Returns:
        dict: Producto encontrado.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """    
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT pr.*, pv.nombre as proveedor, c.nombre as categoria
            FROM producto pr
            JOIN proveedor pv ON pr.id_proveedor = pv.id_proveedor
            JOIN categoria c ON pr.id_categoria = c.id_categoria
            WHERE pr.id_producto = %s
        """, (id,))
        return cur.fetchone()
    except DatabaseError as e:
        print(f"Error de base de datos en get_by_id productos: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def create(id_proveedor: int, nombre: str, unidades_disponibles: int, precio_venta: float, precio_compra: float, id_categoria: int):
    """
    Crea un nuevo producto.

    Args:
        id_proveedor (int): ID del proveedor.
        nombre (str): Nombre del producto.
        unidades_disponibles (int): Cantidad disponible en inventario.
        precio_venta (float): Precio de venta.
        precio_compra (float): Precio de compra.
        id_categoria (int): ID de la categoría.

    Returns:
        dict: Producto creado.

    Raises:
        DatabaseError: Si ocurre un error al crear el producto.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            INSERT INTO producto (id_proveedor, nombre, unidades_disponibles, precio_venta, precio_compra, id_categoria) 
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING *
        """, (id_proveedor, nombre, unidades_disponibles, precio_venta, precio_compra, id_categoria))
        producto = cur.fetchone()
        conn.commit()
        return producto
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en create productos: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def update(id: int, id_proveedor: int, nombre: str, unidades_disponibles: int, precio_venta: float, precio_compra: float, id_categoria: int):
    """
    Actualiza un producto existente.

    Args:
        id (int): ID del producto.
        id_proveedor (int): ID del proveedor.
        nombre (str): Nombre del producto.
        unidades_disponibles (int): Cantidad disponible en inventario.
        precio_venta (float): Precio de venta.
        precio_compra (float): Precio de compra.
        id_categoria (int): ID de la categoría.

    Returns:
        dict: Producto actualizado.

    Raises:
        DatabaseError: Si ocurre un error al actualizar el producto.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            UPDATE producto 
            SET id_proveedor = %s, nombre = %s, unidades_disponibles = %s, precio_venta = %s, precio_compra = %s, id_categoria = %s
            WHERE id_producto = %s
            RETURNING *
        """, (id_proveedor, nombre, unidades_disponibles, precio_venta, precio_compra, id_categoria, id))
        producto = cur.fetchone()
        conn.commit()
        return producto
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en update productos: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def delete(id: int):
    """
    Elimina un producto por su ID.

    Args:
        id (int): Identificador del producto.

    Returns:
        dict: Producto eliminado.

    Raises:
        DatabaseError: Si ocurre un error al eliminar el producto.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            DELETE FROM producto WHERE id_producto = %s RETURNING *
        """, (id,))
        producto = cur.fetchone()
        conn.commit()
        return producto
    except DatabaseError as e:
        conn.rollback()
        print(f"Error de base de datos en delete productos: {e}")
        raise
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()