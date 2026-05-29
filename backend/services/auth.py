from secrets import token_urlsafe
from fastapi import HTTPException  # pyrefly: ignore [missing-import]
from sqlalchemy.exc import SQLAlchemyError  # pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session  # pyrefly: ignore [missing-import]
from repositories import auth as repo

ACTIVE_SESSIONS: dict[str, dict] = {}

def login(username: str, password: str, db: Session):
    """
    Valida credenciales, crea una sesion en memoria y devuelve los datos
    del usuario autenticado.
    """
    try:
        usuario = repo.authenticate(username.strip(), password, db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al iniciar sesion"
        )

    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    session_token = token_urlsafe(32)

    session_data = {
        "id_usuario": usuario.id_usuario,
        "username": usuario.username,
        "nombre": usuario.nombre,
        "rol": usuario.rol,
    }

    ACTIVE_SESSIONS[session_token] = session_data

    return {
        **session_data,
        "session_token": session_token,
    }

def logout(session_token: str | None):
    """
    Cierra la sesion si existe.
    """
    if session_token:
        ACTIVE_SESSIONS.pop(session_token, None)

    return {"message": "Sesion cerrada"}

def get_session(session_token: str | None):
    """
    Obtiene los datos de sesion asociados a un token.
    """
    if not session_token:
        return None

    return ACTIVE_SESSIONS.get(session_token)

def get_session_role(session_token: str | None):
    """
    Devuelve el rol de aplicacion asociado a la sesion autenticada.
    """
    session = get_session(session_token)

    if session is None:
        return None

    return session["rol"]