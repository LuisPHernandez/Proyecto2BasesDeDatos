from repositories import clientes as repo
from fastapi import HTTPException
from psycopg2 import DatabaseError

def get_all():
    """
    Obtiene todos los clientes.

    Returns:
        list: Lista de clientes.

    Raises:
        HTTPException: Si ocurre un error en la base de datos (500).
    """
    try:
        return repo.get_all()
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al obtener los clientes"
        )

def create(nombre: str, email: str):
    """
    Crea un nuevo cliente.

    Args:
        nombre (str): Nombre del cliente.
        email (str): Correo electrónico del cliente.

    Returns:
        dict: Cliente creado con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error en la creación (500).
    """
    try:
        return repo.create(nombre, email)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al crear el cliente"
        )

def update(id: int, nombre: str, email: str):
    """
    Actualiza un cliente existente.

    Args:
        id (int): ID del cliente a actualizar.
        nombre (str): Nuevo nombre del cliente.
        email (str): Nuevo correo electrónico del cliente.

    Returns:
        dict: Cliente actualizado.

    Raises:
        HTTPException: Si el cliente no existe (404).
        HTTPException: Si ocurre un error en la actualización (500).
    """
    try:
        p = repo.update(id, nombre, email)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al actualizar el cliente"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return p

def delete(id: int):
    """
    Elimina un cliente por su ID.

    Args:
        id (int): ID del cliente a eliminar.

    Raises:
        HTTPException: Si el cliente no existe (404).
        HTTPException: Si ocurre un error en la eliminación (500).
    """
    try:
        p = repo.delete(id)
    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al eliminar el cliente"
        )
    if p is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")