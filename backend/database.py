import psycopg2
import os
from dotenv import load_dotenv # pyrefly: ignore [missing-import]
from sqlalchemy import create_engine # pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker, declarative_base # pyrefly: ignore [missing-import]

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    """
    Obtiene una sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()