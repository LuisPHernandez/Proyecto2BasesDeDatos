from repositories import categorias as repo
from fastapi import HTTPException, Depends # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError # pyrefly: ignore [missing-import]
from database import get_db

def get_all(db: Session = Depends(get_db)):
    """
    Obtiene todas las categorías.

    Returns:
        list: Lista de categorías.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_all(db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener las categorías"
        )

def get_income(db: Session = Depends(get_db)):
    """
    Obtiene las categorías con sus ingresos.

    Returns:
        list: Lista de categorías con sus ingresos.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_income(db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener las categorías con sus ingresos"
        )

def create(nombre: str, db: Session = Depends(get_db)):
    """
    Crea una nueva categoría.

    Args:
        nombre (str): Nombre de la categoría.

    Returns:
        dict: Categoría creada con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error en la creación (500).
    """
    try:
        return repo.create(nombre, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al crear la categoría"
        )

def update(id: int, nombre: str, db: Session = Depends(get_db)):
    """
    Actualiza una categoría existente.

    Args:
        id (int): ID de la categoría a actualizar.
        nombre (str): Nuevo nombre de la categoría.

    Returns:
        dict: Categoría actualizada.

    Raises:
        HTTPException: Si la categoría no existe (404).
        HTTPException: Si ocurre un error en la actualización (500).
    """
    try:
        p = repo.update(id, nombre, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al actualizar la categoría"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return p

def delete(id: int, db: Session = Depends(get_db)):
    """
    Elimina una categoría por su ID.

    Args:
        id (int): ID de la categoría a eliminar.

    Raises:
        HTTPException: Si la categoría no existe (404).
        HTTPException: Si ocurre un error en la eliminación (500).
    """
    try:
        p = repo.delete(id, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al eliminar la categoría"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")