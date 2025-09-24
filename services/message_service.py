from sqlalchemy.orm import Session
from models import Messages
from fastapi import HTTPException
from typing import Dict, List
from services.db_service import DBService


class MessageService:
    def __init__(self, db_service: DBService) -> None:
        self.db_service = db_service

    def make_msg_dict(self, session_id: int, role: str, content: str) -> Dict[str, any]:
        """Create a message dictionary for database insertion"""
        import datetime
        
        msg_dict = {
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": str(datetime.datetime.utcnow())
        }
        return msg_dict

    def add_message(self, session_id: int, role: str, content: str) -> None:
        """Add a new message to the database"""
        msg_dict = self.make_msg_dict(session_id, role, content)
        self.db_service.add_to_db(Messages, msg_dict)

    def show_session_messages(self, sess_id: int) -> List[Messages]:
        """Retrieve all messages for a specific session"""
        messages = self.db_service.db.query(Messages).filter(Messages.session_id == sess_id).all()
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found for this session")
        return messages
