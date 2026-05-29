import os
from dotenv import load_dotenv  # pyrefly: ignore [missing-import]
from fastapi import Header, HTTPException  # pyrefly: ignore [missing-import]
from sqlalchemy import create_engine, text  # pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker, declarative_base  # pyrefly: ignore [missing-import]

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

VALID_DB_ROLES = {
    "rol_admin",
    "rol_gerente",
    "rol_vendedor",
    "rol_bodeguero",
    "rol_auditor",
}

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_auth_db():
    """
    Sesion de base de datos para login.

    No usa SET ROLE porque todavia no existe una sesion autenticada.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db(x_session_token: str | None = Header(default=None, alias="X-Session-Token")):
    """
    Sesion de base de datos para endpoints protegidos.

    El backend obtiene el rol desde la sesion activa y asume ese rol en
    PostgreSQL. El frontend solo envia el token de sesion.
    """
    from services.auth import get_session_role

    if x_session_token is None:
        raise HTTPException(status_code=401, detail="Sesion requerida")

    db_role = get_session_role(x_session_token)

    if db_role is None:
        raise HTTPException(status_code=401, detail="Sesion invalida o expirada")

    if db_role not in VALID_DB_ROLES:
        raise HTTPException(status_code=403, detail="Rol de base de datos invalido")

    db = SessionLocal()
    role_was_set = False

    try:
        db.execute(text(f"SET ROLE {db_role}"))
        role_was_set = True
        db.info["db_role"] = db_role

        yield db
    finally:
        try:
            if role_was_set:
                db.rollback()
                db.execute(text("RESET ROLE"))
        finally:
            db.close()