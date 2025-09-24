# Langchain Database Chatbot + FastAPI

A FastAPI application that provides SQL query generation and analysis capabilities using Langchain and OpenAI models through OpenRouter.

## Features

- **Session Management**: Create, update, and delete chat sessions
- **Message Persistence**: Store and retrieve conversation history
- **SQL Query Generation**: Generate SQL queries from natural language
- **Data Analysis**: Analyze query results with statistical insights
- **RESTful API**: Clean FastAPI endpoints with proper validation
- **Database Integration**: SQLite for session/message storage + external SQL Server for querying

## Architecture

```
├── main.py              # FastAPI application entry point
├── database.py          # SQLAlchemy database configuration
├── models.py           # SQLAlchemy ORM models
├── schemas.py          # Pydantic models for request/response validation
├── config.py           # Application configuration management
├── requirements.txt    # Python dependencies
├── services/          # Service layer
│   ├── db_service.py      # Database operations
│   ├── message_service.py  # Message management
│   ├── session_service.py  # Session management
│   └── chat_service.py     # LLM integration and query processing
└── util/              # Utility functions
    └── helper.py          # Database/LLM connection helpers
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with:
   ```
   deep_api=your_openrouter_api_key_here
   ```

## API Endpoints

### Sessions
- `GET /show_sessions_info/{sess_id}` - Get session information
- `POST /create-session` - Create a new session
- `PUT /update_sessions/{sess_id}` - Update session name
- `DELETE /delete-session/{sess_id}` - Delete a session

### Messages
- `GET /show_sessions_messages/{sess_id}` - Get all messages for a session
- `POST /sessions/{sess_id}` - Process a new message and generate SQL query + analysis

## Usage

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API documentation at: `http://localhost:8000/docs`

3. Create a session:
   ```bash
   curl -X POST "http://localhost:8000/create-session" \
        -H "Content-Type: application/json" \
        -d '{"session_id": 1, "name": "My Session"}'
   ```

4. Send a message:
   ```bash
   curl -X POST "http://localhost:8000/sessions/1" \
        -H "Content-Type: application/json" \
        -d '{"message": "Show me all products"}'
   ```

## Configuration

The application uses Pydantic settings for configuration management. Key settings:

- `database_url`: SQLite database URL (default: `sqlite:///./Messages.db`)
- `api_key`: OpenRouter API key (required)
- `model_name`: LLM model name (default: `deepseek/deepseek-chat-v3.1:free`)
- `openrouter_base_url`: OpenRouter API base URL

## Database Setup

The application uses two databases:

1. **SQLite**: For storing sessions and messages (`Messages.db`)
2. **SQL Server**: For querying (configured in `util/helper.py`)

Ensure you have:
- SQL Server running with the `grocery` database
- ODBC Driver 17 for SQL Server installed

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints throughout
- Include docstrings for all functions and classes

### Testing
Run tests with:
```bash
python -m pytest tests/
```

### Logging
The application uses Python's built-in logging module. Log level can be configured via environment variables.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details
