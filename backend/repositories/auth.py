from sqlalchemy.orm import Session  # pyrefly: ignore [missing-import]
from models import UsuarioApp

def authenticate(username: str, password: str, db: Session):
    """
    Busca un usuario de aplicacion por credenciales.

    Returns:
        UsuarioApp | None: Usuario autenticado, si existe.
    """
    return (
        db.query(UsuarioApp)
        .filter(
            UsuarioApp.username == username,
            UsuarioApp.password == password,
        )
        .first()
    )
