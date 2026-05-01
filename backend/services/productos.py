from repositories import productos as repo
from fastapi import HTTPException
from psycopg2 import DatabaseError

def get_all():
    """
    Obtiene todos los productos.

    Returns:
        list: Lista de productos obtenidos desde el repositorio.

    Raises:
        HTTPException: Si ocurre un error la base de datos (500).
    """
    try:
        return repo.get_all()
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener los productos"
        )

def get_by_id(id: int):
    """
    Obtiene un producto por su ID.

    Args:
        id (int): Identificador del producto.

    Returns:
        dict: Producto encontrado.

    Raises:
        HTTPException: Si el producto no existe (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        p = repo.get_by_id(id)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener el producto"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p

def create(id_proveedor: int, nombre: str, unidades_disponibles: int, precio_venta: float, precio_compra: float, id_categoria: int):
    """
    Crea un nuevo producto.

    Args:
        id_proveedor (int): ID del proveedor asociado.
        nombre (str): Nombre del producto.
        unidades_disponibles (int): Cantidad disponible en inventario.
        precio_venta (float): Precio de venta.
        precio_compra (float): Precio de compra.
        id_categoria (int): ID de la categoría.

    Returns:
        dict: Producto creado.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.create(id_proveedor, nombre, unidades_disponibles, precio_venta, precio_compra, id_categoria)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al crear el producto"
        )

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
        HTTPException: Si el producto no existe (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    p = repo.update(id, id_proveedor, nombre, unidades_disponibles, precio_venta, precio_compra, id_categoria)
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p

def delete(id: int):
    """
    Elimina un producto por su ID.

    Args:
        id (int): Identificador del producto.

    Raises:
        HTTPException: Si el producto no existe (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    p = repo.delete(id)
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
