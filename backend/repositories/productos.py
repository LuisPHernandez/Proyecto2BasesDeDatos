from sqlalchemy import text # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError # pyrefly: ignore [missing-import]
from models import Producto, Proveedor, Categoria

def get_all(db: Session):
    """
    Obtiene todos los productos con proveedor y categoría.

    Returns:
        list[dict]: Lista de productos.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    try:
        rows = (
            db.query(Producto, Proveedor.nombre.label("proveedor"), Categoria.nombre.label("categoria"))
            .join(Proveedor, Producto.id_proveedor == Proveedor.id_proveedor)
            .join(Categoria, Producto.id_categoria == Categoria.id_categoria)
            .order_by(Producto.id_producto)
            .all()
        )

        return [
            {
                **producto.__dict__,
                "proveedor": proveedor,
                "categoria": categoria,
            }
            for producto, proveedor, categoria in rows
        ]
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_all productos: {e}")
        raise

def get_low_stock(db: Session):
    """
    Obtiene los productos con bajo stock que han sido vendidos al menos una vez.

    Returns:
        list: Lista de productos con bajo stock.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    try:
        sql = text("""
            SELECT DISTINCT id_producto
            FROM detalle_venta
            WHERE id_producto IN (
                SELECT id_producto
                FROM producto
                WHERE unidades_disponibles < 10
            );
        """)

        rows = db.execute(sql).mappings().all()

        return [row["id_producto"] for row in rows]

    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_low_stock_productos: {e}")
        raise

def get_top_mes(db: Session):
    """
    Obtiene los productos más vendidos del mes usando CTE.

    Returns:
        list[dict]: Lista de productos con unidades vendidas e ingresos.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    try:
        sql = text("""
            WITH ventas_mes AS (
                SELECT
                    dv.id_producto,
                    SUM(dv.cantidad) AS unidades_vendidas,
                    SUM(dv.cantidad * dv.precio_unitario) AS ingresos
                FROM detalle_venta dv
                JOIN venta v ON dv.id_venta = v.id_venta
                WHERE DATE_TRUNC('month', v.fecha) = DATE_TRUNC('month', CURRENT_DATE)
                GROUP BY dv.id_producto
            )
            SELECT
                p.id_producto,
                p.nombre,
                vm.unidades_vendidas,
                vm.ingresos
            FROM ventas_mes vm
            JOIN producto p ON p.id_producto = vm.id_producto
            ORDER BY vm.unidades_vendidas DESC
            LIMIT 5
        """)

        rows = db.execute(sql).mappings().all()

        return [dict(row) for row in rows]

    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_top_mes productos: {e}")
        raise

def get_by_id(id: int, db: Session):
    """
    Obtiene un producto por su ID.

    Args:
        id (int): Identificador del producto.

    Returns:
        dict: Producto encontrado.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """    
    try:
        row = (
            db.query(Producto, Proveedor.nombre.label("proveedor"), Categoria.nombre.label("categoria"))
            .join(Proveedor, Producto.id_proveedor == Proveedor.id_proveedor)
            .join(Categoria, Producto.id_categoria == Categoria.id_categoria)
            .filter(Producto.id_producto == id)
            .first()
        )

        if row is None:
            return None

        producto, proveedor, categoria = row
        return {
            **producto.__dict__,
            "proveedor": proveedor,
            "categoria": categoria,
        }
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_by_id productos: {e}")
        raise

def create(id_proveedor: int, nombre: str, unidades_disponibles: int, precio_venta: float, precio_compra: float, id_categoria: int, db: Session):
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
    try:
        sql = text("""
            CALL sp_crear_producto(
                :id_proveedor,
                :nombre,
                :unidades_disponibles,
                :precio_venta,
                :precio_compra,
                :id_categoria,
                NULL
            )
        """)

        result = db.execute(sql, {
            "id_proveedor": id_proveedor,
            "nombre": nombre,
            "unidades_disponibles": unidades_disponibles,
            "precio_venta": precio_venta,
            "precio_compra": precio_compra,
            "id_categoria": id_categoria
        })

        id_producto = result.scalar()
        db.commit()
        return get_by_id(id_producto, db)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos en create productos: {e}")
        raise

def update(id: int, id_proveedor: int, nombre: str, unidades_disponibles: int, precio_venta: float, precio_compra: float, id_categoria: int, db: Session):
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
    try:
        producto = db.query(Producto).filter(
            Producto.id_producto == id
        ).first()

        if producto is None:
            return None

        producto.id_proveedor = id_proveedor
        producto.nombre = nombre
        producto.precio_venta = precio_venta
        producto.precio_compra = precio_compra
        producto.id_categoria = id_categoria

        sql = text("""
            CALL sp_actualizar_stock(
                :id_producto,
                :unidades
            )
        """)

        db.execute(sql, {
            "id_producto": id,
            "unidades": unidades_disponibles
        })

        db.commit()
        db.refresh(producto)
        return producto
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos en update productos: {e}")
        raise

def delete(id: int, db: Session):
    """
    Elimina un producto por su ID.

    Args:
        id (int): Identificador del producto.

    Returns:
        dict: Producto eliminado.

    Raises:
        DatabaseError: Si ocurre un error al eliminar el producto.
    """
    try:
        producto = db.query(Producto).filter(Producto.id_producto == id).first()

        if producto is None:
            return None

        db.delete(producto)
        db.commit()
        return producto
    except SQLAlchemyError as e:
        print(f"Error de base de datos en delete productos: {e}")
        raise