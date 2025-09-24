from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SessionCreate(BaseModel):
    session_id: int
    name: str

class SessionUpdate(BaseModel):
    name: str

class ChatRequest(BaseModel):
    message: str

class SessionResponse(BaseModel):
    session_id: int
    name: str
    date_created: datetime

class MessageResponse(BaseModel):
    message_id: int
    session_id: int
    role: str
    content: str
    timestamp: datetime

class ErrorResponse(BaseModel):
    detail: str
