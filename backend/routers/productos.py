from fastapi import APIRouter
from pydantic import BaseModel
from services import productos as service
from typing import List

router = APIRouter()

class ProductoBase(BaseModel):
    """
    Modelo base que se recibe en una creación o actualización de productos.

    Attributes:
        id_proveedor (int): ID del proveedor asociado al producto.
        nombre (str): Nombre del producto.
        unidades_disponibles (int): Cantidad disponible en inventario.
        precio_venta (float): Precio al que se vende el producto en la tienda.
        precio_compra (float): Precio al que se compró el producto al proveedor.
        id_categoria (int): ID de la categoría del producto.
    """
    id_proveedor: int
    nombre: str
    unidades_disponibles: int
    precio_venta: float
    precio_compra: float
    id_categoria: int

class Producto(ProductoBase):
    """
    Modelo con identificador que se devuelve en una creación o actualización de 
    producto.

    Extiende ProductoBase agregando el ID del producto.

    Attributes:
        id_producto (int): Identificador único del producto.
    """
    id_producto: int

class ProductoDetailed(Producto):
    """
    Modelo detallado de producto.

    Incluye información adicional relacionada al proveedor y categoría del producto.

    Attributes:
        proveedor (str): Nombre del proveedor.
        categoria (str): Categoría del producto.
    """
    proveedor: str
    categoria: str

@router.get(
    "/",
    status_code=200,
    response_model=List[ProductoDetailed],
    summary="Obtener todos los productos",
    description="Devuelve una lista de todos los productos con información detallada, incluyendo proveedor y categoría."
)
def get_all():
    """
    Obtiene todos los productos disponibles.

    Returns:
        List[ProductoDetailed]: Lista de productos con información detallada.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_all()

@router.get(
    "/{id}",
    status_code=200,
    response_model=ProductoDetailed,
    summary="Obtener producto por ID",
    description="Devuelve la información detallada de un producto específico utilizando su identificador."
)
def get_by_id(id: int):
    """
    Obtiene un producto por su ID.

    Args:
        id (int): Identificador del producto.

    Returns:
        ProductoDetailed: Producto encontrado con información detallada.

    Raises:
        HTTPException: Si el producto no existe (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    return service.get_by_id(id)

@router.post(
    "/",
    status_code=201,
    response_model=Producto,
    summary="Crear producto",
    description="Crea un nuevo producto."
)
def create(p: ProductoBase):
    """
    Crea un nuevo producto.

    Args:
        p (ProductoBase): Datos del producto a crear.

    Returns:
        Producto: Producto creado con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.create(p.id_proveedor, p.nombre, p.unidades_disponibles, p.precio_venta, p.precio_compra, p.id_categoria)

@router.put(
    "/{id}",
    status_code=200,
    response_model=Producto,
    summary="Actualizar producto",
    description="Actualiza la información de un producto existente."
)
def update(id: int, p: ProductoBase):
    """
    Actualiza un producto existente.

    Args:
        id (int): ID del producto a actualizar.
        p (ProductoBase): Nuevos datos del producto.

    Returns:
        Producto: Producto actualizado con su identificador.

    Raises:
        HTTPException: Si el producto no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    return service.update(id, p.id_proveedor, p.nombre, p.unidades_disponibles, p.precio_venta, p.precio_compra, p.id_categoria)

@router.delete(
    "/{id}",
    status_code=204,
    summary="Eliminar producto",
    description="Elimina un producto del sistema."
)
def delete(id: int):
    """
    Elimina un producto por su ID.

    Args:
        id (int): Identificador del producto a eliminar.

    Raises:
        HTTPException: Si el producto no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    service.delete(id)