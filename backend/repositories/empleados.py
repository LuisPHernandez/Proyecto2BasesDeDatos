from sqlalchemy import text  # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session  # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError  # pyrefly: ignore [missing-import]
from models import Empleado


def get_all(db: Session):
    """
    Obtiene todos los empleados con sus ventas e ingresos.
    Usa SQL explícito por el GROUP BY / HAVING.

    Returns:
        list[dict]: Lista de empleados con conteo de ventas e ingresos.

    Raises:
        SQLAlchemyError: Si ocurre un error al consultar la base de datos.
    """
    try:
        sql = text("""
            SELECT e.id_empleado, e.nombre, COUNT(v.id_venta) AS ventas, SUM(v.total) AS ingresos
            FROM empleado e
            JOIN venta v ON e.id_empleado = v.id_empleado
            GROUP BY e.id_empleado, e.nombre
            HAVING SUM(v.total) > 1
            ORDER BY ingresos DESC
        """)
        rows = db.execute(sql).mappings().all()
        return [dict(row) for row in rows]
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_all empleado: {e}")
        raise


def get_by_id(id: int, db: Session):
    """
    Obtiene un empleado por su ID.

    Args:
        id (int): ID del empleado.

    Returns:
        Empleado | None: Empleado encontrado o None si no existe.

    Raises:
        SQLAlchemyError: Si ocurre un error al consultar la base de datos.
    """
    try:
        return db.query(Empleado).filter(Empleado.id_empleado == id).first()
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_by_id empleado: {e}")
        raise


def create(nombre: str, db: Session):
    """
    Crea un nuevo empleado.

    Args:
        nombre (str): Nombre del empleado.

    Returns:
        Empleado: Empleado creado con su ID asignado.

    Raises:
        SQLAlchemyError: Si ocurre un error al crear el empleado.
    """
    try:
        empleado = Empleado(nombre=nombre)
        db.add(empleado)
        db.commit()
        db.refresh(empleado)
        return empleado
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos en create empleado: {e}")
        raise


def update(id: int, nombre: str, db: Session):
    """
    Actualiza un empleado existente.

    Args:
        id (int): ID del empleado a actualizar.
        nombre (str): Nuevo nombre del empleado.

    Returns:
        Empleado | None: Empleado actualizado o None si no existe.

    Raises:
        SQLAlchemyError: Si ocurre un error al actualizar el empleado.
    """
    try:
        empleado = db.query(Empleado).filter(Empleado.id_empleado == id).first()

        if empleado is None:
            return None

        empleado.nombre = nombre
        db.commit()
        db.refresh(empleado)
        return empleado
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos en update empleado: {e}")
        raise


def delete(id: int, db: Session):
    """
    Elimina un empleado por su ID.

    Args:
        id (int): ID del empleado a eliminar.

    Returns:
        Empleado | None: Empleado eliminado o None si no existe.

    Raises:
        SQLAlchemyError: Si ocurre un error al eliminar el empleado.
    """
    try:
        empleado = db.query(Empleado).filter(Empleado.id_empleado == id).first()

        if empleado is None:
            return None

        db.delete(empleado)
        db.commit()
        return empleado
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos en delete empleado: {e}")
        raise