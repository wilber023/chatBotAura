from fastapi import Depends
from app.db.session import SessionLocal
from typing import Generator

def get_db() -> Generator:
    """
    Inyecta la sesión de la base de datos en los endpoints.
    Asegura que la conexión local se cierre al concluir la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
