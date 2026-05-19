from fastapi import HTTPException  # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError  # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session  # pyrefly: ignore [missing-import]
from repositories import auth as repo

def login(username: str, password: str, db: Session):
    """
    Valida credenciales y devuelve los datos de sesion del usuario.
    """
    try:
        usuario = repo.authenticate(username.strip(), password, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al iniciar sesion"
        )

    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario o contrasena incorrectos")

    return {
        "id_usuario": usuario.id_usuario,
        "username": usuario.username,
        "nombre": usuario.nombre,
        "rol": usuario.rol,
    }
