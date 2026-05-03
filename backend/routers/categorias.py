from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services import categorias as service

router = APIRouter()

class CategoriaBase(BaseModel):
    """
    Modelo base que se recibe en una creación o actualización de categorías.

    Attributes:
        nombre (str): Nombre de la categoría.
    """
    nombre: str

class Categoria(CategoriaBase):
    """
    Modelo con identificador que se devuelve en una creación o actualización de categoría.

    Extiende CategoriaBase agregando el ID de la categoría.

    Attributes:
        id_categoria (int): Identificador único de la categoría.
    """
    id_categoria: int

class CategoriaConIngresos(Categoria):
    """
    Modelo con identificador que se devuelve al obtener las categorías con sus ingresos.

    Extiende Categoria agregando el ID de la categoría.

    Attributes:
        ingresos (float): Ingresos de la categoría.
    """
    ingresos: float

@router.get(
    "/",
    status_code=200,
    response_model=List[Categoria],
    summary="Obtener todas las categorías",
    description="Devuelve una lista de todas las categorías disponibles."
)
def get_all():
    """
    Obtiene todas las categorías.

    Returns:
        List[Categoria]: Lista de categorías.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_all()

@router.get(
    "/ingresos",
    status_code=200,
    response_model=List[CategoriaConIngresos],
    summary="Obtener categorías con sus ingresos",
    description="Devuelve una lista de todas las categorías con sus ingresos."
)
def get_income():
    """
    Obtiene las categorías con sus ingresos.

    Returns:
        List[CategoriaConIngresos]: Lista de categorías con sus ingresos.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.get_income()

@router.post(
    "/",
    status_code=201,
    response_model=Categoria,
    summary="Crear categoría",
    description="Crea una nueva categoría."
)
def create(c: CategoriaBase):
    """
    Crea una nueva categoría.

    Args:
        c (CategoriaBase): Datos de la categoría a crear.

    Returns:
        Categoria: Categoría creada con su ID asignado.

    Raises:
        HTTPException: Si ocurre un error interno (500).
    """
    return service.create(c.nombre)

@router.put(
    "/{id}",
    status_code=200,
    response_model=Categoria,
    summary="Actualizar categoría",
    description="Actualiza la información de una categoría existente."
)
def update(id: int, c: CategoriaBase):
    """
    Actualiza una categoría existente.

    Args:
        id (int): ID de la categoría a actualizar.
        c (CategoriaBase): Nuevos datos de la categoría.

    Returns:
        Categoria: Categoría actualizada con su identificador.

    Raises:
        HTTPException: Si la categoría no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    return service.update(id, c.nombre)

@router.delete(
    "/{id}",
    status_code=204,
    summary="Eliminar categoría",
    description="Elimina una categoría del sistema."
)
def delete(id: int):
    """
    Elimina una categoría por su ID.

    Args:
        id (int): ID de la categoría a eliminar.

    Raises:
        HTTPException: Si la categoría no existe (404).
        HTTPException: Si ocurre un error interno (500).
    """
    service.delete(id)
