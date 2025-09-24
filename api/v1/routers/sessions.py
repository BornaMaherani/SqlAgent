from fastapi import APIRouter, Depends, HTTPException
import logging
from api.v1.dependencies import get_session_service, get_db_service
from api.v1.schemas import SessionCreate, SessionUpdate, SessionResponse, ErrorResponse
from services.session_service import SessionService
from services.db_service import DBService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("", response_model=SessionResponse, responses={500: {"model": ErrorResponse}})
def create_session(
    session_data: SessionCreate, 
    session_service: SessionService = Depends(get_session_service)
):
    """Create a new session"""
    try:
        return session_service.create_session(session_data.dict())
    except Exception as e:
        logger.error(f"Error creating session: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/{sess_id}", response_model=SessionResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
def update_session(
    sess_id: int, 
    session_data: SessionUpdate, 
    session_service: SessionService = Depends(get_session_service)
):
    """Update an existing session"""
    try:
        return session_service.update_session(sess_id, session_data.dict())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating session {sess_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{sess_id}", responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
def delete_session(
    sess_id: int, 
    session_service: SessionService = Depends(get_session_service)
):
    """Delete a session and all associated messages"""
    try:
        return session_service.delete_session(sess_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session {sess_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{sess_id}/info", response_model=SessionResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def show_session_info(
    sess_id: int, 
    db_service: DBService = Depends(get_db_service)
):
    """Get session information"""
    try:
        from models import Sessions
        session_info = db_service.db.query(Sessions).filter(Sessions.session_id == sess_id).all()
        if not session_info:
            raise HTTPException(status_code=404, detail="Session info not found")
        return session_info[0]  # Return first session since session_id should be unique
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session info {sess_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
