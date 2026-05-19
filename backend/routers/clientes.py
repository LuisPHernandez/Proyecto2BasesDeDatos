from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from services import clientes as service

router = APIRouter()

class ClienteBase(BaseModel):
    """
    Modelo base que se recibe en una creación o actualización de clientes.

    Attributes:
        nombre (str): Nombre del cliente.
        email (str): Correo electrónico del cliente.
    """
    nombre: str
    email: str

class Cliente(ClienteBase):
    """
    Modelo con identificador que se devuelve en una creación o actualización de cliente.

    Extiende ClienteBase agregando el ID del cliente.

    Attributes:
        id_cliente (int): Identificador único del cliente.
    """
    id_cliente: int

@router.get(
    "/",
    status_code=200,
    response_model=List[Cliente],
    summary="Obtener todos los clientes",
    description="Devuelve una lista de todos los clientes disponibles."
)
def get_all(db: Session = Depends(get_db)):
    """
    Obtiene todos los clientes.

    Returns:
        List[Cliente]: Lista de clientes.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_all(db)

@router.get(
    "/activos",
    status_code=200,
    response_model=List[int],
    summary="Obtener clientes activos",
    description="Devuelve una lista de clientes que han realizado compras en el último mes."
)
def get_active(db: Session = Depends(get_db)):
    """
    Obtiene los clientes activos.

    Returns:
        List[int]: Lista de IDs de clientes que han realizado compras en el último mes.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_active(db)

@router.post(
    "/",
    status_code=201,
    response_model=Cliente,
    summary="Crear cliente",
    description="Crea un nuevo cliente."
)
def create(c: ClienteBase, db: Session = Depends(get_db)):
    """
    Crea un nuevo cliente.

    Args:
        c (ClienteBase): Datos del cliente a crear.

    Returns:
        Cliente: Cliente creado con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.create(c.nombre, c.email, db)

@router.put(
    "/{id}",
    status_code=200,
    response_model=Cliente,
    summary="Actualizar cliente",
    description="Actualiza la información de un cliente existente."
)
def update(id: int, c: ClienteBase, db: Session = Depends(get_db)):
    """
    Actualiza un cliente existente.

    Args:
        id (int): ID del cliente a actualizar.
        c (ClienteBase): Nuevos datos del cliente.

    Returns:
        Cliente: Cliente actualizado con su identificador.

    Raises:
        HTTPException: Si el cliente no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    return service.update(id, c.nombre, c.email, db)

@router.delete(
    "/{id}",
    status_code=204,
    summary="Eliminar cliente",
    description="Elimina un cliente del sistema."
)
def delete(id: int, db: Session = Depends(get_db)):
    """
    Elimina un cliente por su ID.

    Args:
        id (int): ID del cliente a eliminar.

    Raises:
        HTTPException: Si el cliente no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    service.delete(id, db)
