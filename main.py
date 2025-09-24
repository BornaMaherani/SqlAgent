from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine
import models
import logging
from dotenv import load_dotenv
from api.v1.routers import sessions, messages, chat

# Load environment variables first
load_dotenv()

# Import settings after environment variables are loaded
from config import settings

logger = logging.getLogger(__name__)
app = FastAPI(
    title="Langchain Database Chatbot API",
    description="A FastAPI application for database query generation and analysis using Langchain",
    version="1.0.0"
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(sessions.router)
app.include_router(messages.router)
app.include_router(chat.router)

@app.get("/")
async def serve_frontend():
    """Serve the frontend interface"""
    return FileResponse("templates/index.html")
