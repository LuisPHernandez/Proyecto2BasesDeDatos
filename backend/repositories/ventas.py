from sqlalchemy import text  # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session  # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError  # pyrefly: ignore [missing-import]
from models import Venta, DetalleVenta, Producto, Empleado, Cliente
from datetime import datetime

def get_all(fecha_inicio: datetime, fecha_fin: datetime, db: Session):
    """
    Obtiene todas las ventas en un rango de fechas usando la vista venta_detallada.
    Usa SQL explícito por el uso de la vista.

    Args:
        fecha_inicio (datetime): Fecha inicial del rango.
        fecha_fin (datetime): Fecha final del rango.

    Returns:
        list[dict]: Lista de ventas.

    Raises:
        SQLAlchemyError: Si ocurre un error en la base de datos.
    """
    try:
        sql = text("""
            SELECT *
            FROM venta_detallada
            WHERE fecha BETWEEN :fecha_inicio AND :fecha_fin
            ORDER BY fecha DESC
        """)
        rows = db.execute(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin}).mappings().all()
        return [dict(row) for row in rows]
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_all ventas: {e}")
        raise

def get_by_id(id: int, db: Session):
    """
    Obtiene una venta por su ID con datos de empleado y cliente.
    Usa SQL explícito por el JOIN multi-tabla.

    Args:
        id (int): ID de la venta.

    Returns:
        dict | None: Venta con datos de empleado y cliente, o None si no existe.

    Raises:
        SQLAlchemyError: Si ocurre un error en la base de datos.
    """
    try:
        row = (
            db.query(
                Venta.id_venta,
                Venta.fecha,
                Venta.total,
                Empleado.nombre.label("nombre_empleado"),
                Cliente.email.label("email_cliente"),
                Cliente.nombre.label("nombre_cliente"),
            )
            .join(Empleado, Venta.id_empleado == Empleado.id_empleado)
            .join(Cliente, Venta.id_cliente == Cliente.id_cliente)
            .filter(Venta.id_venta == id)
            .first()
        )

        if row is None:
            return None

        return {
            "id_venta": row.id_venta,
            "fecha": row.fecha,
            "total": row.total,
            "nombre_empleado": row.nombre_empleado,
            "email_cliente": row.email_cliente,
            "nombre_cliente": row.nombre_cliente,
        }

    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_by_id ventas: {e}")
        raise

def get_productos_by_id(id: int, db: Session):
    """
    Obtiene los productos de una venta por su ID.
    Usa SQL explícito por el JOIN entre detalle_venta y producto.

    Args:
        id (int): ID de la venta.

    Returns:
        list[dict]: Lista de productos de la venta.

    Raises:
        SQLAlchemyError: Si ocurre un error en la base de datos.
    """
    try:
        sql = text("""
            SELECT p.id_producto, p.nombre AS nombre_producto,
                   dv.precio_unitario, dv.cantidad
            FROM detalle_venta dv
            JOIN producto p ON dv.id_producto = p.id_producto
            WHERE dv.id_venta = :id
        """)
        rows = db.execute(sql, {"id": id}).mappings().all()
        return [dict(row) for row in rows]
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_productos_by_id ventas: {e}")
        raise

def create(id_cliente: int, id_empleado: int, fecha: datetime, productos: list, db: Session):
    """
    Crea una nueva venta con su detalle y descuenta el stock.
    Transacción explícita con ROLLBACK ante stock insuficiente o error de BD.

    Args:
        id_cliente (int): ID del cliente.
        id_empleado (int): ID del empleado.
        fecha (datetime): Fecha de la venta.
        productos (list): Lista de dicts con id_producto, precio_unitario y cantidad.

    Returns:
        dict: Venta creada con datos de empleado y cliente.

    Raises:
        ValueError: Si el stock de algún producto es insuficiente.
        SQLAlchemyError: Si ocurre un error en la base de datos.
    """
    try:
        total = sum(p["precio_unitario"] * p["cantidad"] for p in productos)

        sql_venta = text("""
            CALL sp_crear_venta(
                :id_cliente,
                :id_empleado,
                :fecha,
                :total,
                NULL
            )
        """)
        result = db.execute(sql_venta, {
            "id_cliente": id_cliente,
            "id_empleado": id_empleado,
            "fecha": fecha,
            "total": total,
        })

        id_venta = result.scalar()

        sql_detalle = text("""
            CALL sp_insertar_detalle_venta(
                :id_venta,
                :id_producto,
                :cantidad,
                :precio_unitario
            )
        """)
        for p in productos:
            db.execute(sql_detalle, {
                "id_venta": id_venta,
                "id_producto": p["id_producto"],
                "cantidad": p["cantidad"],
                "precio_unitario": p["precio_unitario"],
            })

        db.commit()
        return get_by_id(id_venta, db)
    except Exception as e:
        db.rollback()
        print(f"Error en create ventas: {e}")
        raise

def delete(id: int, db: Session):
    """
    Elimina una venta por su ID.

    Args:
        id (int): ID de la venta.

    Returns:
        Venta | None: Venta eliminada o None si no existe.

    Raises:
        SQLAlchemyError: Si ocurre un error en la base de datos.
    """
    try:
        venta = db.query(Venta).filter(Venta.id_venta == id).first()

        if venta is None:
            return None

        sql = text("""
            CALL sp_eliminar_venta(:id_venta)
        """)
        db.execute(sql, {"id_venta": id})
        db.commit()

        return venta
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos en delete ventas: {e}")
        raise