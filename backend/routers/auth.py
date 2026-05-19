from fastapi import APIRouter, Depends  # pyrefly: ignore [missing-import]
from pydantic import BaseModel
from sqlalchemy.orm import Session  # pyrefly: ignore [missing-import]
from database import get_db
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

@router.post(
    "/login",
    status_code=200,
    response_model=AuthUser,
    summary="Iniciar sesion",
    description="Valida credenciales y devuelve el usuario autenticado con su rol."
)
def login(credentials: LoginInput, db: Session = Depends(get_db)):
    return service.login(credentials.username, credentials.password, db)

@router.post(
    "/logout",
    status_code=200,
    summary="Cerrar sesion",
    description="Endpoint simple para cerrar sesion en el cliente."
)
def logout():
    return {"message": "Sesion cerrada"}
