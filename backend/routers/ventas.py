from fastapi import APIRouter
from pydantic import BaseModel
from services import ventas as service
from typing import List
from datetime import datetime

router = APIRouter()

class VentaSummary(BaseModel):
    """
    Modelo que se devuelve para tabla de ventas.

    Attributes:
        id_venta (int): ID de la venta.
        nombre_empleado (str): Nombre del empleado.
        email_cliente (str): Email del cliente.
        nombre_cliente (str): Nombre del cliente.
        fecha (datetime): Fecha de la venta.
        total (float): Total de la venta.
    """
    id_venta: int
    nombre_empleado: str
    email_cliente: str
    nombre_cliente: str
    fecha: datetime
    total: float

class VentaProducto(BaseModel):
    """
    Modelo que se devuelve para mostrar los productos de una venta en el detalle.

    Attributes:
        id_producto (int): ID del producto.
        nombre_producto (str): Nombre del producto.
        precio_unitario (float): Precio unitario del producto.
        cantidad (int): Cantidad del producto.
    """
    id_producto: int
    nombre_producto: str
    precio_unitario: float
    cantidad: int

class DetalleVentaInput(BaseModel):
    """
    Modelo base para los productos que se reciben en una creación de ventas.

    Attributes:
        id_producto (int): ID del producto.
        cantidad (int): Cantidad del producto.
        precio_unitario (float): Precio unitario del producto.
    """
    id_producto: int
    cantidad: int
    precio_unitario: float

class VentaCreateInput(BaseModel):
    """
    Modelo base que se recibe en una creación de ventas.

    Attributes:
        id_cliente (int): ID del cliente.
        id_empleado (int): ID del empleado.
        fecha (datetime): Fecha de la venta.
        productos (List[DetalleVentaInput]): Lista de productos de la venta.
    """
    id_cliente: int
    id_empleado: int
    fecha: datetime
    productos: List[DetalleVentaInput]

@router.get(
    "/",
    status_code=200,
    response_model=List[VentaSummary],
    summary="Obtener todas las ventas realizadas en un rango de fechas",
    description="Devuelve una lista de todas las ventas realizadas en un rango de fechas."
)
def get_all(fecha_inicio: datetime, fecha_fin: datetime):
    """
    Obtiene todas las ventas realizadas en un rango de fechas.

    Args:
        fecha_inicio (datetime): Fecha inicial del rango.
        fecha_fin (datetime): Fecha final del rango.

    Returns:
        List[VentaSummary]: Lista de ventas.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_all(fecha_inicio, fecha_fin)

@router.get(
    "/{id}",
    status_code=200,
    response_model=VentaSummary,
    summary="Obtener una venta por ID",
    description="Devuelve una venta con todos su información básica."
)
def get_by_id(id: int):
    """
    Obtiene una venta por ID.

    Args:
        id (int): ID de la venta.

    Returns:
        VentaSummary: Venta con su información básica.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_by_id(id)

@router.get(
    "/{id}/productos",
    status_code=200,
    response_model=List[VentaProducto],
    summary="Obtener los productos de una venta por ID",
    description="Devuelve una lista de productos de una venta."
)
def get_productos_by_id(id: int):
    """
    Obtiene los productos de una venta por ID.

    Args:
        id (int): ID de la venta.

    Returns:
        List[VentaProducto]: Lista de productos de la venta.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_productos_by_id(id)

@router.post(
    "/",
    status_code=201,
    response_model=VentaSummary,
    summary="Crear una venta con sus productos",
    description="Crea una nueva venta con todos sus productos en una transacción."
)
def create(v: VentaCreateInput):
    """
    Crea una nueva venta.

    Args:
        venta (VentaCreateInput): Venta a crear.

    Returns:
        VentaSummary: Venta creada.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.create(v.id_cliente, v.id_empleado, v.fecha, v.productos)

@router.delete(
    "/{id}",
    status_code=204,
    summary="Eliminar una venta",
    description="Elimina una venta por ID."
)
def delete(id: int):
    """
    Elimina una venta por ID.

    Args:
        id (int): ID de la venta.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    service.delete(id)
