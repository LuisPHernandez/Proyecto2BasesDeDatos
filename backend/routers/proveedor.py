from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services import proveedor as service

router = APIRouter()

class ProveedorBase(BaseModel):
    """
    Modelo base que se recibe en una creación o actualización de proveedores.

    Attributes:
        nombre (str): Nombre del proveedor.
        email (str): Correo electrónico del proveedor.
    """
    nombre: str
    email: str

class Proveedor(ProveedorBase):
    """
    Modelo con identificador que se devuelve en una creación o actualización de proveedor.

    Extiende ProveedorBase agregando el ID del proveedor.

    Attributes:
        id_proveedor (int): Identificador único del proveedor.
    """
    id_proveedor: int

@router.get(
    "/",
    status_code=200,
    response_model=List[Proveedor],
    summary="Obtener todos los proveedores",
    description="Devuelve una lista de todos los proveedores disponibles."
)
def get_all():
    """
    Obtiene todos los proveedores.

    Returns:
        List[Proveedor]: Lista de proveedores.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_all()

@router.post(
    "/",
    status_code=201,
    response_model=Proveedor,
    summary="Crear proveedor",
    description="Crea un nuevo proveedor."
)
def create(p: ProveedorBase):
    """
    Crea un nuevo proveedor.

    Args:
        p (ProveedorBase): Datos del proveedor a crear.

    Returns:
        Proveedor: Proveedor creado con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.create(p.nombre, p.email)

@router.put(
    "/{id}",
    status_code=200,
    response_model=Proveedor,
    summary="Actualizar proveedor",
    description="Actualiza la información de un proveedor existente."
)
def update(id: int, p: ProveedorBase):
    """
    Actualiza un proveedor existente.

    Args:
        id (int): ID del proveedor a actualizar.
        p (ProveedorBase): Nuevos datos del proveedor.

    Returns:
        Proveedor: Proveedor actualizado con su identificador.

    Raises:
        HTTPException: Si el proveedor no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    return service.update(id, p.nombre, p.email)

@router.delete(
    "/{id}",
    status_code=204,
    summary="Eliminar proveedor",
    description="Elimina un proveedor del sistema."
)
def delete(id: int):
    """
    Elimina un proveedor por su ID.

    Args:
        id (int): ID del proveedor a eliminar.

    Raises:
        HTTPException: Si el proveedor no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    service.delete(id)
