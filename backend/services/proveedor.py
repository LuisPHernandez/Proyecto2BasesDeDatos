from repositories import proveedor as repo
from fastapi import HTTPException
from psycopg2 import DatabaseError

def get_all():
    """
    Obtiene todos los proveedores.

    Returns:
        list: Lista de proveedores.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_all()
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener los proveedores"
        )

def create(nombre: str, email: str):
    """
    Crea un nuevo proveedor.

    Args:
        nombre (str): Nombre del proveedor.
        email (str): Correo electrónico del proveedor.

    Returns:
        dict: Proveedor creado con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error en la creación (500).
    """
    try:
        return repo.create(nombre, email)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al crear el proveedor"
        )

def update(id: int, nombre: str, email: str):
    """
    Actualiza un proveedor existente.

    Args:
        id (int): ID del proveedor a actualizar.
        nombre (str): Nuevo nombre del proveedor.
        email (str): Nuevo correo electrónico del proveedor.

    Returns:
        dict: Proveedor actualizado.

    Raises:
        HTTPException: Si el proveedor no existe (404).
        HTTPException: Si ocurre un error en la actualización (500).
    """
    try:
        p = repo.update(id, nombre, email)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al actualizar el proveedor"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return p

def delete(id: int):
    """
    Elimina un proveedor por su ID.

    Args:
        id (int): ID del proveedor a eliminar.

    Raises:
        HTTPException: Si el proveedor no existe (404).
        HTTPException: Si ocurre un error en la eliminación (500).
    """
    try:
        p = repo.delete(id)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al eliminar el proveedor"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")