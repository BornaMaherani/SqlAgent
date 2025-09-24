from sqlalchemy.orm import Session
from models import Sessions, Messages
from fastapi import HTTPException
from typing import Dict, Any
from services.db_service import DBService


class SessionService:
    def __init__(self, db_service: DBService) -> None:
        self.db_service = db_service

    def create_session(self, new_message: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new session"""
        import datetime
        
        session_dict = {
            "session_id": new_message.get("session_id"),
            "name": new_message.get("name"),
            "date_created": str(datetime.datetime.utcnow())
        }
        self.db_service.add_to_db(Sessions, session_dict)
        
        # Return the created session data in the format expected by SessionResponse
        session = self.db_service.db.query(Sessions).filter(Sessions.session_id == session_dict["session_id"]).first()
        return {
            "session_id": session.session_id,
            "name": session.name,
            "date_created": session.date_created
        }

    def update_session(self, sess_id: int, new_message: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing session"""
        # Find the session to update
        session = self.db_service.db.query(Sessions).filter(Sessions.session_id == sess_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Update the session name
        session.name = new_message.get("name", session.name)
        self.db_service.db.commit()
        self.db_service.db.refresh(session)
        
        # Return the updated session data
        return {
            "session_id": session.session_id,
            "name": session.name,
            "date_created": session.date_created
        }

    def delete_session(self, sess_id: int) -> None:
        """Delete a session and all its messages (manual cascade delete)"""
        # First delete all messages associated with the session
        self.db_service.db.query(Messages).filter(Messages.session_id == sess_id).delete()
        
        # Then delete the session
        session = self.db_service.db.query(Sessions).filter(Sessions.session_id == sess_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
            
        self.db_service.db.delete(session)
        self.db_service.db.commit()
        
        return {"detail": "Session and all associated messages deleted successfully"}
