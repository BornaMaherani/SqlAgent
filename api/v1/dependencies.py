from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator
from database import SessionLocal
from services.db_service import DBService
from services.message_service import MessageService
from services.session_service import SessionService

def get_db() -> Generator:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_service(db: Session = Depends(get_db)) -> DBService:
    """DBService dependency"""
    return DBService(db)

def get_message_service(db_service: DBService = Depends(get_db_service)) -> MessageService:
    """MessageService dependency"""
    return MessageService(db_service)

def get_session_service(db_service: DBService = Depends(get_db_service)) -> SessionService:
    """SessionService dependency"""
    return SessionService(db_service)
