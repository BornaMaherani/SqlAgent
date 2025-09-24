from fastapi import APIRouter, Depends, HTTPException
import logging
from api.v1.dependencies import get_message_service
from api.v1.schemas import MessageResponse, ErrorResponse
from services.message_service import MessageService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sessions", tags=["messages"])

@router.get("/{sess_id}/messages", response_model=list[MessageResponse], responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def show_session_messages(
    sess_id: int, 
    message_service: MessageService = Depends(get_message_service)
):
    """Get all messages for a specific session"""
    try:
        messages = message_service.show_session_messages(sess_id)
        return messages
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving messages for session {sess_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
