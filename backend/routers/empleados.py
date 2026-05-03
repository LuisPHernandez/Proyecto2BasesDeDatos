from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services import empleados as service

router = APIRouter()

class EmpleadoBase(BaseModel):
    """
    Modelo base que se recibe en una creación o actualización de empleados.

    Attributes:
        nombre (str): Nombre del empleado.
    """
    nombre: str

class Empleado(EmpleadoBase):
    """
    Modelo con identificador que se devuelve en una creación o actualización de empleado.

    Extiende EmpleadoBase agregando el ID del empleado.

    Attributes:
        id_empleado (int): Identificador único del empleado.
    """
    id_empleado: int

class EmpleadoSales(Empleado):
    """
    Modelo con identificador que se devuelve al obtener empleados con ventas.

    Extiende Empleado.

    Attributes:
        ventas (int): Número total de ventas realizadas por el empleado.
        ingresos (float): Total de ingresos generados por el empleado.
    """
    ventas: int
    ingresos: float

@router.get(
    "/",
    status_code=200,
    response_model=List[EmpleadoSales],
    summary="Obtener todos los empleados",
    description="Devuelve una lista de todos los empleados disponibles y su total de ventas e ingresos generado."
)
def get_all():
    """
    Obtiene todos los empleados.

    Returns:
        List[EmpleadoSales]: Lista de empleados con sus ventas e ingresos generados.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_all()

@router.post(
    "/",
    status_code=201,
    response_model=Empleado,
    summary="Crear empleado",
    description="Crea un nuevo empleado."
)
def create(e: EmpleadoBase):
    """
    Crea un nuevo empleado.

    Args:
        e (EmpleadoBase): Datos del empleado a crear.

    Returns:
        Empleado: Empleado creado con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.create(e.nombre)

@router.put(
    "/{id}",
    status_code=200,
    response_model=Empleado,
    summary="Actualizar empleado",
    description="Actualiza la información de un empleado existente."
)
def update(id: int, e: EmpleadoBase):
    """
    Actualiza un empleado existente.

    Args:
        id (int): ID del empleado a actualizar.
        e (EmpleadoBase): Nuevos datos del empleado.

    Returns:
        Empleado: Empleado actualizado con su identificador.

    Raises:
        HTTPException: Si el empleado no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    return service.update(id, e.nombre)

@router.delete(
    "/{id}",
    status_code=204,
    summary="Eliminar empleado",
    description="Elimina un empleado del sistema."
)
def delete(id: int):
    """
    Elimina un empleado por su ID.

    Args:
        id (int): ID del empleado a eliminar.

    Raises:
        HTTPException: Si el empleado no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    service.delete(id)
