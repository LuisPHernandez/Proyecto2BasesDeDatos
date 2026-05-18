from sqlalchemy import text # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError # pyrefly: ignore [missing-import]
from models import Categoria

def get_all(db: Session):
    """
    Obtiene todas las categorías.

    Returns:
        list: Lista de categorías.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    try:
        return db.query(Categoria).all()
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_all categoria: {e}")
        raise

def get_income(db: Session):
    """
    Obtiene las categorías con sus ingresos.

    Returns:
        list: Lista de categorías con sus ingresos.

    Raises:
        DatabaseError: Si ocurre un error al consultar la base de datos.
    """
    try:
        sql = text("""
            SELECT 
                c.id_categoria, 
                c.nombre, 
                SUM(dv.precio_unitario * dv.cantidad) AS ingresos
            FROM categoria c
            JOIN producto p ON c.id_categoria = p.id_categoria
            JOIN detalle_venta dv ON p.id_producto = dv.id_producto
            GROUP BY c.id_categoria, c.nombre
            HAVING SUM(dv.precio_unitario * dv.cantidad) > 1
            ORDER BY ingresos DESC;
        """)

        rows = db.execute(sql).mappings().all()

        return [dict(row) for row in rows]
    except SQLAlchemyError as e:
        print(f"Error de base de datos en get_income_categoria: {e}")
        raise

def create(nombre: str, db: Session):
    """
    Crea una nueva categoría.

    Args:
        nombre (str): Nombre de la categoría.

    Returns:
        dict: Categoría creada con su ID asignado.

    Raises:
        DatabaseError: Si ocurre un error al crear la categoría.
    """
    try:
        categoria = Categoria(nombre=nombre)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        return categoria
    except SQLAlchemyError as e:
        print(f"Error de base de datos en create categoria: {e}")
        raise

def update(id: int, nombre: str, db: Session):
    """
    Actualiza una categoría existente.

    Args:
        id (int): ID de la categoría a actualizar.
        nombre (str): Nuevo nombre de la categoría.

    Returns:
        dict: Categoría actualizada.

    Raises:
        DatabaseError: Si ocurre un error al actualizar la categoría.
    """
    try:
        categoria = db.query(Categoria).filter(Categoria.id_categoria == id).first()

        if categoria is None:
            return None

        categoria.nombre = nombre

        db.commit()
        db.refresh(categoria)
        return categoria
    except SQLAlchemyError as e:
        print(f"Error de base de datos en update categoria: {e}")
        raise

def delete(id: int, db: Session):
    """
    Elimina una categoría por su ID.

    Args:
        id (int): ID de la categoría a eliminar.

    Returns:
        dict: Categoría eliminada.

    Raises:
        DatabaseError: Si ocurre un error al eliminar la categoría.
    """
    try:
        categoria = db.query(Categoria).filter(Categoria.id_categoria == id).first()

        if categoria is None:
            return None

        db.delete(categoria)
        db.commit()
        return categoria
    except SQLAlchemyError as e:
        print(f"Error de base de datos en delete categoria: {e}")
        raise  
