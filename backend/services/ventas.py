from repositories import ventas as repo
from fastapi import HTTPException
from psycopg2 import DatabaseError
from datetime import datetime

def get_all(fecha_inicio: datetime, fecha_fin: datetime):
    """
    Obtiene todas las ventas realizadas en un rango de fechas.

    Args:
        fecha_inicio (datetime): Fecha inicial del rango.
        fecha_fin (datetime): Fecha final del rango.

    Returns:
        list: Lista de ventas.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_all(fecha_inicio, fecha_fin)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener las ventas"
        )

def get_by_id(id: int):
    """
    Obtiene una venta por ID.

    Args:
        id (int): ID de la venta.

    Returns:
        dict: Venta con su información básica.

    Raises:
        HTTPException: Si la venta no existe (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        v = repo.get_by_id(id)
    except DatabaseError:   
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener la venta"
        )
    if v is None:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return v

def get_productos_by_id(id: int):
    """
    Obtiene los productos de una venta por ID.

    Args:
        id (int): ID de la venta.

    Returns:
        list: Lista de productos de la venta.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_productos_by_id(id)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener los productos de la venta"
        )

def create(id_cliente: int, id_empleado: int, fecha: datetime, productos: list):
    """
    Crea una nueva venta.

    Args:
        id_cliente (int): ID del cliente.
        id_empleado (int): ID del empleado.
        fecha (datetime): Fecha de la venta.
        productos (list): Lista de productos de la venta.

    Returns:
        dict: Venta creada con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error en la creación (500).
    """
    try:
        return repo.create(id_cliente, id_empleado, fecha, [producto.dict() for producto in productos])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Error de base de datos al crear la venta")

def delete(id: int):
    """
    Elimina una venta por su ID.

    Args:
        id (int): ID de la venta a eliminar.

    Raises:
        HTTPException: Si la venta no existe (404).
        HTTPException: Si ocurre un error en la eliminación (500).
    """
    try:
        v = repo.delete(id)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al eliminar la venta"
        )
    if v is None:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
