from sqlalchemy import text # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError # pyrefly: ignore [missing-import]
from models import Proveedor

def get_all(db: Session):
    """
    Obtiene todos los proveedores.

    Returns:
        list: Lista de proveedores.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    try:
        return db.query(Proveedor).all()
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_all proveedor: {e}")
        raise

def create(nombre: str, email: str, db: Session):
    """
    Crea un nuevo proveedor.

    Args:
        nombre (str): Nombre del proveedor.
        email (str): Correo electrónico del proveedor.

    Returns:
        dict: Proveedor creado con su ID asignado.

    Raises:
        DatabaseError: Si ocurre un error al crear el proveedor.
    """
    try:
        proveedor = Proveedor(nombre=nombre, email=email)
        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)
        return proveedor
    except SQLAlchemyError as e:
        print(f"Error de base de datos en create proveedor: {e}")
        raise

def update(id: int, nombre: str, email: str, db: Session):
    """
    Actualiza un proveedor existente.

    Args:
        id (int): ID del proveedor a actualizar.
        nombre (str): Nuevo nombre del proveedor.
        email (str): Nuevo correo electrónico del proveedor.

    Returns:
        dict: Proveedor actualizado.

    Raises:
        DatabaseError: Si ocurre un error al actualizar el proveedor.
    """
    try:
        proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id).first()

        if proveedor is None:
            return None

        proveedor.nombre = nombre
        proveedor.email = email

        db.commit()
        db.refresh(proveedor)
        return proveedor
    except SQLAlchemyError as e:
        print(f"Error de base de datos en update proveedor: {e}")
        raise

def delete(id: int, db: Session):
    """
    Elimina un proveedor por su ID.

    Args:
        id (int): ID del proveedor a eliminar.

    Returns:
        dict: Proveedor eliminado.

    Raises:
        DatabaseError: Si ocurre un error al eliminar el proveedor.
    """
    try:
        proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id).first()

        if proveedor is None:
            return None

        db.delete(proveedor)
        db.commit()
        return proveedor
    except SQLAlchemyError as e:
        print(f"Error de base de datos en delete proveedor: {e}")
        raise
