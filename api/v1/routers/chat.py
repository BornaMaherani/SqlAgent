from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlalchemy.orm import Session
from api.v1.dependencies import get_db, get_db_service
from api.v1.schemas import ChatRequest, ErrorResponse
from services.chat_service import ChatService
from services.db_service import DBService
from services.message_service import MessageService
from models import Messages
from util.helper import connect_llm, connect_db
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sessions", tags=["chat"])

# Global session chains storage
session_chains = {}

@router.post("/{sess_id}", responses={500: {"model": ErrorResponse}})
async def process_chat_message(
    sess_id: int, 
    chat_request: ChatRequest, 
    db: Session = Depends(get_db),
    db_service: DBService = Depends(get_db_service)
):
    """Process a chat message and return analysis results"""
    try:
        # Create chat service with proper DB service
        chat_service = ChatService(db_service, settings.api_key)
        
        # If session doesn't exist, establish connection to LLM and database
        if sess_id not in session_chains:
            new_llm = connect_llm(settings.api_key)
            new_db = connect_db()
            session_chains[sess_id] = {"llm": new_llm, "db": new_db}

        llm = session_chains[sess_id]["llm"]
        db_conn = session_chains[sess_id]["db"]

        # Create message service for this request
        message_service = MessageService(db_service)

        # Create new message using MessageService
        user_dict = message_service.make_msg_dict(sess_id, "user", chat_request.message)

        # Retrieve previous messages from database and format them properly
        filtered = db.query(Messages).filter(Messages.session_id == sess_id).all()
        mem_from_db = [
            {"role": msg.role, "content": msg.content, "timestamp": str(msg.timestamp)}
            for msg in filtered
        ]

        # Use ChatService for query and analysis
        table_data, mem, column_names, query_string = chat_service.query_chat(
            llm=llm, db=db_conn, mem_from_db=mem_from_db, new_message=chat_request.message
        )
        query_dict = message_service.make_msg_dict(sess_id, "assistant", "The query: " + f"{query_string['result']}")
        
        # Get analysis response as JSON
        analyser_response = chat_service.analyse_chat(llm=llm, table_data=table_data, conversation_history=mem, column_names=column_names)
        
        # Save query and analysis messages to database
        message_service.add_message(sess_id, "user", chat_request.message)
        message_service.add_message(sess_id, "assistant", "The query: " + f"{query_string['result']}")
        message_service.add_message(sess_id, "assistant", "The analyse: " + f"{analyser_response.json()}")
        
        # Return the analysis response as JSON
        return analyser_response

    except Exception as e:
        logger.error("Error processing message for session: ", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
