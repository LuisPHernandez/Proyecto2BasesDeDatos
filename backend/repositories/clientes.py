from sqlalchemy import text  # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session  # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError  # pyrefly: ignore [missing-import]
from models import Cliente


def get_all(db: Session):
    """
    Obtiene todos los clientes.

    Returns:
        list[Cliente]: Lista de clientes.

    Raises:
        SQLAlchemyError: Si ocurre un error al consultar la base de datos.
    """
    try:
        return db.query(Cliente).order_by(Cliente.id_cliente).all()
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_all cliente: {e}")
        raise


def get_active(db: Session):
    """
    Obtiene los IDs de clientes activos (con compras en el último mes).

    Returns:
        list[int]: Lista de IDs de clientes activos.

    Raises:
        SQLAlchemyError: Si ocurre un error al consultar la base de datos.
    """
    try:
        sql = text("""
            SELECT id_cliente
            FROM cliente
            WHERE id_cliente IN (
                SELECT DISTINCT id_cliente
                FROM venta
                WHERE fecha >= CURRENT_DATE - INTERVAL '1 month'
            )
            ORDER BY id_cliente
        """)

        rows = db.execute(sql).mappings().all()
        return [row["id_cliente"] for row in rows]
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_active cliente: {e}")
        raise


def get_by_id(id: int, db: Session):
    """
    Obtiene un cliente por su ID.

    Args:
        id (int): ID del cliente.

    Returns:
        Cliente | None: Cliente encontrado o None si no existe.

    Raises:
        SQLAlchemyError: Si ocurre un error al consultar la base de datos.
    """
    try:
        return db.query(Cliente).filter(Cliente.id_cliente == id).first()
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_by_id cliente: {e}")
        raise


def create(nombre: str, email: str, db: Session):
    """
    Crea un nuevo cliente.

    Args:
        nombre (str): Nombre del cliente.
        email (str): Correo electrónico del cliente.

    Returns:
        Cliente: Cliente creado con su ID asignado.

    Raises:
        SQLAlchemyError: Si ocurre un error al crear el cliente.
    """
    try:
        cliente = Cliente(nombre=nombre, email=email)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos en create cliente: {e}")
        raise


def update(id: int, nombre: str, email: str, db: Session):
    """
    Actualiza un cliente existente.

    Args:
        id (int): ID del cliente a actualizar.
        nombre (str): Nuevo nombre del cliente.
        email (str): Nuevo correo electrónico del cliente.

    Returns:
        Cliente | None: Cliente actualizado o None si no existe.

    Raises:
        SQLAlchemyError: Si ocurre un error al actualizar el cliente.
    """
    try:
        cliente = db.query(Cliente).filter(Cliente.id_cliente == id).first()

        if cliente is None:
            return None

        cliente.nombre = nombre
        cliente.email = email

        db.commit()
        db.refresh(cliente)
        return cliente
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos en update cliente: {e}")
        raise


def delete(id: int, db: Session):
    """
    Elimina un cliente por su ID.

    Args:
        id (int): ID del cliente a eliminar.

    Returns:
        Cliente | None: Cliente eliminado o None si no existe.

    Raises:
        SQLAlchemyError: Si ocurre un error al eliminar el cliente.
    """
    try:
        cliente = db.query(Cliente).filter(Cliente.id_cliente == id).first()

        if cliente is None:
            return None

        db.delete(cliente)
        db.commit()
        return cliente
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos en delete cliente: {e}")
        raise