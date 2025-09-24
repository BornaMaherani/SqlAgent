#!/usr/bin/env python3
"""
Run script for the Langchain Database Chatbot API.
This script starts the FastAPI application using uvicorn.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
