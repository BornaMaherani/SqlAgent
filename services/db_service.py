from typing import Type, Any, Dict, Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal

def get_db() -> Session:
    """Get database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database dependency type
db_dependency = Annotated[Session, Depends(get_db)]

class DBService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_to_db(self, db_table: Type[Any], row_dict: Dict[str, Any]) -> None:
        """Add a new row to the specified database table"""
        db_model = db_table(**row_dict)
        self.db.add(db_model)
        self.db.commit()
        self.db.refresh(db_model)
