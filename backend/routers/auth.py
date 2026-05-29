from fastapi import APIRouter, Depends, Header  # pyrefly: ignore [missing-import]
from pydantic import BaseModel
from sqlalchemy.orm import Session  # pyrefly: ignore [missing-import]
from database import get_auth_db
from services import auth as service

router = APIRouter()

class LoginInput(BaseModel):
    username: str
    password: str

class AuthUser(BaseModel):
    id_usuario: int
    username: str
    nombre: str
    rol: str
    session_token: str

@router.post(
    "/login",
    status_code=200,
    response_model=AuthUser,
    summary="Iniciar sesion",
    description="Valida credenciales y devuelve el usuario autenticado con su rol."
)
def login(credentials: LoginInput, db: Session = Depends(get_auth_db)):
    return service.login(credentials.username, credentials.password, db)

@router.post(
    "/logout",
    status_code=200,
    summary="Cerrar sesion",
    description="Cierra la sesion activa del usuario."
)
def logout(x_session_token: str | None = Header(default=None, alias="X-Session-Token")):
    return service.logout(x_session_token)