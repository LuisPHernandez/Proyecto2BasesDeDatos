from repositories import productos as repo
from fastapi import HTTPException # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError # pyrefly: ignore [missing-import]
from services.db_errors import db_error_detail

def get_all(db: Session):
    """
    Obtiene todos los productos.

    Returns:
        list: Lista de productos.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_all(db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener los productos"
        )

def get_low_stock(db: Session):
    """
    Obtiene los productos con bajo stock.

    Returns:
        list: Lista de productos con bajo stock.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_low_stock(db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener los productos con bajo stock"
        )

def get_top_mes(db: Session):
    """
    Obtiene los productos más vendidos del mes.

    Returns:
        list: Lista de productos con unidades vendidas e ingresos.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_top_mes(db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener los productos más vendidos"
        )

def get_by_id(id: int, db: Session):
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
        p = repo.get_by_id(id, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener el producto"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p

def create(id_proveedor: int, nombre: str, unidades_disponibles: int, precio_venta: float, precio_compra: float, id_categoria: int, db: Session):
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
        dict: Producto creado cons su ID asignado.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.create(id_proveedor, nombre, unidades_disponibles, precio_venta, precio_compra, id_categoria, db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=400,
            detail=db_error_detail(e, "Error de base de datos al crear el producto")
        )

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
        HTTPException: Si el producto no existe (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        p = repo.update(id, id_proveedor, nombre, unidades_disponibles, precio_venta, precio_compra, id_categoria, db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=400,
            detail=db_error_detail(e, "Error de base de datos al actualizar el producto")
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p

def delete(id: int, db: Session):
    """
    Elimina un producto por su ID.

    Args:
        id (int): Identificador del producto.

    Raises:
        HTTPException: Si el producto no existe (404).
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        p = repo.delete(id, db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=400,
            detail=db_error_detail(e, "Error de base de datos al eliminar el producto")
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
