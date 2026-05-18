from repositories import empleados as repo
from fastapi import HTTPException, Depends # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError # pyrefly: ignore [missing-import]
from database import get_db

def get_all(db: Session = Depends(get_db)):
    """
    Obtiene todos los empleados.

    Returns:
        list: Lista de empleados.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_all(db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener los empleados"
        )

def create(nombre: str, db: Session = Depends(get_db)):
    """
    Crea un nuevo empleado.

    Args:
        nombre (str): Nombre del empleado.

    Returns:
        dict: Empleado creado con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error en la creación (500).
    """
    try:
        return repo.create(nombre, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al crear el empleado"
        )

def update(id: int, nombre: str, db: Session = Depends(get_db)):
    """
    Actualiza un empleado existente.

    Args:
        id (int): ID del empleado a actualizar.
        nombre (str): Nuevo nombre del empleado.

    Returns:
        dict: Empleado actualizado.

    Raises:
        HTTPException: Si el empleado no existe (404).
        HTTPException: Si ocurre un error en la actualización (500).
    """
    try:
        p = repo.update(id, nombre, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al actualizar el empleado"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return p

def delete(id: int, db: Session = Depends(get_db)):
    """
    Elimina un empleado por su ID.

    Args:
        id (int): ID del empleado a eliminar.

    Raises:
        HTTPException: Si el empleado no existe (404).
        HTTPException: Si ocurre un error en la eliminación (500).
    """
    try:
        p = repo.delete(id, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al eliminar el empleado"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")